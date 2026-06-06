---
name: geo-gap-fixer
description: "Audit how often LLMs recommend your brand vs competitors and generate a GEO action plan."
category: "GTM Intelligence"
version: "1.0.0"
---

# GEO Gap Fixer

> Agent skill that audits LLM brand visibility and converts gaps into a
> concrete GEO content action plan.

---

## When to Use

Use this skill when a user wants to audit their Generative Engine Optimization (GEO) share-of-voice to know which LLM prompts their brand is losing, understand why competitors are recommended instead, and get a specific content fix plan.

**Do NOT use this skill for**: general SEO audits, paid ad optimization, or continuous social media monitoring. This is a point-in-time LLM visibility audit.

---

## Step 1: Inputs

To run the audit, the user must provide API keys and a configuration file. Ensure the following are set up:

1. **API Keys**: At least 2 of 4 keys must be set in the environment or `.env` file (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `PERPLEXITY_API_KEY`).
2. **Dependencies**: `pip install openai anthropic google-genai`
3. **Config File**: `config.json` (copied from `config.example.json`) must contain:
   - `brand_name` (string, required)
   - `competitors` (list of strings, required, 1-10 entries)
   - `category` (string, required)
   - `buyer_intent_prompts` (list of strings, optional. If empty, 20 prompts are auto-generated)
   - `target_llms` (list of strings, optional)
   - `website_url` (string, optional)

---

## Step 2: Execution Pipeline

Run the following scripts in order. Stop and ask for clarification if any script fails.

1. **`python scripts/probe_llms.py`** (Optional: append `--dry-run` to test config without API calls)
   - Sends buyer-intent prompts to the configured LLM APIs.
   - Saves responses to `data/raw_responses.json`.

2. **`python scripts/analyze_results.py`**
   - Analyzes raw responses for brand mentions, ranking, sentiment, and cited domains.
   - Saves structured analysis to `data/analysis.json`.

3. **`python scripts/build_report.py`**
   - Assembles the final 5-section GEO audit report.
   - Saves to `report/geo_audit_report.md` and `report/geo_audit_report.json`.

---

## Step 3: Outputs & Interpretation

The primary output is `report/geo_audit_report.md`. Present its findings to the user.

**Key Sections to Interpret:**
1. **Share-of-Voice Table**: A mention rate below 30% is critical. Mention rate is the % of prompts where the brand is recommended.
2. **Prompt-Level Loss Log**: Which exact prompts the brand lost and to whom.
3. **Competitor Language Patterns**: The specific adjectives LLMs use for competitors.
4. **Citation Gap List**: Domains LLMs cite that the brand is missing from.
5. **GEO Action Plan**: Prioritized fixes (🔴 Critical, 🟡 High Priority, 🟢 Growth Plays). 

Direct the user to the **GEO Action Plan** first, as it contains the concrete steps to fix the gaps identified in the audit.

---

## Step 4: Error Handling

If you encounter issues while executing the pipeline, follow these rules:

| Condition | Agent Action |
|-----------|--------------|
| Missing `config.json` | Tell the user to copy `config.example.json` and fill it out. |
| Invalid JSON in config | Notify the user of the parse error location and ask them to fix it. |
| Missing required fields | List the exact missing fields (`brand_name`, `competitors`, `category`). |
| No API keys set | Ask the user to export at least 2 of the 4 supported API keys. |
| 1 API key only | Warn the user that results are less reliable, but proceed with the run. |
| Transient API failure | The script auto-retries. If it fails completely, it skips the provider. |
| Persistent API failure | The script skips the provider gracefully. Continue the pipeline. |
| Zero responses | The script exits non-zero. Notify the user to check API keys or config. |
| Missing upstream data file | Re-run the preceding script in the pipeline (e.g., probe before analyze). |

**Limitations to keep in mind**:
- This is a point-in-time audit, not a background monitor.
- Sentiment analysis uses keyword proximity, not deep NLP.
- API costs apply for each run (typically ~$0.50–$2.00).
