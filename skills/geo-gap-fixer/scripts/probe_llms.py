#!/usr/bin/env python3
"""
probe_llms.py — Send buyer-intent prompts to LLM APIs and capture raw responses.

Sends each prompt to every configured LLM provider, captures the full text
response, and saves all results to data/raw_responses.json.

Graceful degradation: if an API key is missing or a provider errors out,
that provider is skipped with a warning — the script never crashes.

Usage:
    python scripts/probe_llms.py [--config path/to/config.json]
"""

import json
import os
import re
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

# ── Constants ───────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = SKILL_ROOT / "config.json"
DATA_DIR = SKILL_ROOT / "data"
RAW_RESPONSES_PATH = DATA_DIR / "raw_responses.json"
PROMPT_TEMPLATES_PATH = SKILL_ROOT / "references" / "prompt_templates.md"

MAX_RESPONSE_CHARS = 4000  # Cap response length to avoid memory issues
SLEEP_BETWEEN_CALLS = 1.0  # seconds between API calls
MAX_RETRIES = 2  # Retry transient API failures
RETRY_BACKOFF = 2.0  # Exponential backoff base (seconds)

# System prompt that normalizes LLM output for easier parsing
SYSTEM_PROMPT = (
    "You are a helpful assistant. When recommending tools or products, "
    "list them clearly by name. If you cite sources, include full URLs."
)

PROVIDER_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "perplexity": "PERPLEXITY_API_KEY",
}

# ── Config Loading ──────────────────────────────────────────────────────────


def load_config(config_path: Path) -> dict:
    """Load and validate the user config file."""
    if not config_path.exists():
        print(f"[ERROR] Config file not found: {config_path}")
        print("  Copy config.example.json to config.json and fill in your details.")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {config_path}: {e}")
        sys.exit(1)

    # Validate required fields
    required = ["brand_name", "competitors", "category"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        print(f"[ERROR] Missing required config fields: {', '.join(missing)}")
        sys.exit(1)

    if not isinstance(config["competitors"], list) or len(config["competitors"]) < 1:
        print("[ERROR] 'competitors' must be a list with at least 1 entry.")
        sys.exit(1)

    if len(config["competitors"]) > 10:
        print("[WARN] More than 10 competitors will produce many API calls. Trimming to 10.")
        config["competitors"] = config["competitors"][:10]

    # Validate target_llms if provided
    config.setdefault("buyer_intent_prompts", [])
    config.setdefault("target_llms", ["openai", "anthropic", "google", "perplexity"])
    config.setdefault("website_url", "")

    valid_llms = set(PROVIDER_ENV_KEYS.keys())
    invalid = [llm for llm in config["target_llms"] if llm not in valid_llms]
    if invalid:
        print(f"[WARN] Unknown LLM providers ignored: {', '.join(invalid)}")
        config["target_llms"] = [llm for llm in config["target_llms"] if llm in valid_llms]

    return config


# ── Prompt Generation ───────────────────────────────────────────────────────


def load_prompt_templates() -> list[str]:
    """Load prompt templates from references/prompt_templates.md."""
    if not PROMPT_TEMPLATES_PATH.exists():
        return get_fallback_templates()

    templates = []
    with open(PROMPT_TEMPLATES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            # Extract templates from markdown table rows: | # | Category | "template" |
            match = re.search(r'"([^"]+\{[^"]+)"', line)
            if match:
                templates.append(match.group(1))

    return templates if templates else get_fallback_templates()


def get_fallback_templates() -> list[str]:
    """Hardcoded fallback templates if the reference file is missing."""
    return [
        "What is the best {category}?",
        "What {category} do you recommend?",
        "Top {category} in 2026",
        "Best {category} for startups",
        "Best {category} for teams",
        "{brand} vs {competitor}: which is better?",
        "Compare {brand} and {competitor} for {category}",
        "Should I use {brand} or {competitor}?",
        "{brand} vs {competitor} pros and cons",
        "Differences between {brand} and {competitor}",
        "I need a {category} that is fast and simple",
        "Best {category} for developer teams",
        "What {category} has the best API?",
        "Most affordable {category} for small teams",
        "{category} with best integrations",
        "Best alternatives to {competitor}",
        "Cheaper alternatives to {competitor}",
        "What to use instead of {competitor}",
        "Moving away from {competitor}, what should I try?",
        "{competitor} competitors worth trying",
    ]


def generate_prompts(config: dict) -> list[dict]:
    """Generate the full list of prompts from config or templates."""
    # If user supplied custom prompts, use them directly
    if config["buyer_intent_prompts"]:
        return [
            {"text": p, "category": "custom", "variables": {}}
            for p in config["buyer_intent_prompts"]
        ]

    templates = load_prompt_templates()
    prompts = []
    brand = config["brand_name"]
    category = config["category"]
    competitors = config["competitors"]

    for template in templates:
        try:
            if "{competitor}" in template:
                # Generate one prompt per competitor
                for comp in competitors:
                    text = template.format(
                        brand=brand, competitor=comp, category=category
                    )
                    prompts.append({
                        "text": text,
                        "category": _classify_template(template),
                        "variables": {"brand": brand, "competitor": comp, "category": category},
                    })
            else:
                text = template.format(brand=brand, category=category)
                prompts.append({
                    "text": text,
                    "category": _classify_template(template),
                    "variables": {"brand": brand, "category": category},
                })
        except KeyError as e:
            print(f"  [WARN] Skipping template with unknown variable {e}: {template}")

    return prompts


def _classify_template(template: str) -> str:
    """Classify a template into a category based on its pattern."""
    t = template.lower()
    if "vs" in t or "compare" in t or "should i use" in t or "differences" in t:
        return "comparison"
    if "alternative" in t or "instead of" in t or "moving away" in t or "competitors" in t:
        return "alternative"
    if "i need" in t or "best api" in t or "affordable" in t or "integration" in t or "developer" in t:
        return "problem"
    return "direct"


# ── Provider Adapters ───────────────────────────────────────────────────────


def _retry(fn: Callable, provider_name: str) -> dict | None:
    """Retry a provider call with exponential backoff on transient errors."""
    for attempt in range(MAX_RETRIES + 1):
        result = fn()
        if result is not None:
            return result
        if attempt < MAX_RETRIES:
            wait = RETRY_BACKOFF ** (attempt + 1)
            print(f"    → retrying {provider_name} in {wait:.0f}s (attempt {attempt + 2}/{MAX_RETRIES + 1})")
            time.sleep(wait)
    return None


def probe_openai(prompt_text: str) -> dict | None:
    """Send prompt to OpenAI gpt-4o. Returns None if key missing or error."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        print("  [WARN] openai package not installed. pip install openai")
        return None

    def _call() -> dict | None:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_text},
                ],
                max_tokens=2048,
                temperature=0.0,  # Deterministic output
            )
            text = response.choices[0].message.content or ""
            return {
                "provider": "openai",
                "model": "gpt-4o",
                "response": text[:MAX_RESPONSE_CHARS],
            }
        except Exception as e:
            print(f"  [WARN] OpenAI error: {e}")
            return None

    return _retry(_call, "openai")


def probe_anthropic(prompt_text: str) -> dict | None:
    """Send prompt to Anthropic claude-sonnet-4-6."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic
    except ImportError:
        print("  [WARN] anthropic package not installed. pip install anthropic")
        return None

    def _call() -> dict | None:
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt_text}],
            )
            text = response.content[0].text if response.content else ""
            return {
                "provider": "anthropic",
                "model": "claude-sonnet-4-6",
                "response": text[:MAX_RESPONSE_CHARS],
            }
        except Exception as e:
            print(f"  [WARN] Anthropic error: {e}")
            return None

    return _retry(_call, "anthropic")


def probe_google(prompt_text: str) -> dict | None:
    """Send prompt to Google gemini-2.5-flash."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
    except ImportError:
        print("  [WARN] google-genai package not installed. pip install google-genai")
        return None

    def _call() -> dict | None:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{SYSTEM_PROMPT}\n\n{prompt_text}",
            )
            text = response.text or ""
            return {
                "provider": "google",
                "model": "gemini-2.5-flash",
                "response": text[:MAX_RESPONSE_CHARS],
            }
        except Exception as e:
            print(f"  [WARN] Google error: {e}")
            return None

    return _retry(_call, "google")


def probe_perplexity(prompt_text: str) -> dict | None:
    """Send prompt to Perplexity sonar-pro via OpenAI-compatible API."""
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        print("  [WARN] openai package not installed. pip install openai")
        return None

    def _call() -> dict | None:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai",
            )
            response = client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_text},
                ],
            )
            text = response.choices[0].message.content or ""
            return {
                "provider": "perplexity",
                "model": "sonar-pro",
                "response": text[:MAX_RESPONSE_CHARS],
            }
        except Exception as e:
            print(f"  [WARN] Perplexity error: {e}")
            return None

    return _retry(_call, "perplexity")


# Provider dispatch map
PROVIDERS = {
    "openai": probe_openai,
    "anthropic": probe_anthropic,
    "google": probe_google,
    "perplexity": probe_perplexity,
}


# ── Main Orchestrator ───────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Probe LLMs with buyer-intent prompts")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to config.json (default: config.json in skill root)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and show prompts without making API calls",
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  GEO Gap Fixer — LLM Probe")
    print("=" * 60)

    # 1. Load config
    config = load_config(args.config)
    print(f"  Brand:       {config['brand_name']}")
    print(f"  Competitors: {', '.join(config['competitors'])}")
    print(f"  Category:    {config['category']}")

    # 2. Determine available providers
    target_llms = config["target_llms"]
    available = []
    skipped = []
    for llm in target_llms:
        env_key = PROVIDER_ENV_KEYS.get(llm)
        if env_key and os.environ.get(env_key):
            available.append(llm)
        else:
            skipped.append(llm)

    if len(available) < 1 and not args.dry_run:
        print("\n[ERROR] No API keys found. Set at least 2 of:")
        for llm, key in PROVIDER_ENV_KEYS.items():
            print(f"  export {key}=...")
        sys.exit(1)

    print(f"\n  Providers:   {', '.join(available)}")
    if skipped:
        print(f"  Skipped:     {', '.join(skipped)} (no API key)")

    # 3. Generate prompts
    prompts = generate_prompts(config)
    print(f"  Prompts:     {len(prompts)}")

    if args.dry_run:
        print("\n  [DRY RUN] Showing first 5 prompts:")
        for i, p in enumerate(prompts[:5], 1):
            print(f"    {i}. [{p['category']}] {p['text']}")
        print(f"\n  Total: {len(prompts)} prompts × {len(available)} providers = {len(prompts) * len(available)} API calls")
        print("  No API calls made. Remove --dry-run to execute.")
        sys.exit(0)

    print("-" * 60)

    # 4. Probe each prompt against each provider
    results = []
    total = len(prompts) * len(available)
    count = 0

    for prompt_obj in prompts:
        for llm in available:
            count += 1
            prompt_text = prompt_obj["text"]
            short = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
            print(f"  [{count}/{total}] {llm}: {short}")

            probe_fn = PROVIDERS[llm]
            result = probe_fn(prompt_text)

            if result:
                result["prompt"] = prompt_text
                result["prompt_category"] = prompt_obj["category"]
                result["prompt_variables"] = prompt_obj["variables"]
                results.append(result)
            else:
                print(f"    → skipped (error or missing key)")

            time.sleep(SLEEP_BETWEEN_CALLS)

    # 5. Save results
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "meta": {
            "brand_name": config["brand_name"],
            "competitors": config["competitors"],
            "category": config["category"],
            "website_url": config.get("website_url", ""),
            "target_llms": target_llms,
            "providers_used": available,
            "providers_skipped": skipped,
            "total_prompts": len(prompts),
            "total_responses": len(results),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "responses": results,
    }

    with open(RAW_RESPONSES_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"  ✅ Saved {len(results)} responses to {RAW_RESPONSES_PATH}")
    print(f"     {len(prompts)} prompts × {len(available)} providers")
    if skipped:
        print(f"     ⚠️  Skipped providers: {', '.join(skipped)}")
    print("=" * 60 + "\n")

    if len(results) == 0:
        print("[ERROR] No responses collected. Check your API keys and network.")
        sys.exit(1)


if __name__ == "__main__":
    main()
