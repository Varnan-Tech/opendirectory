import re
from typing import Dict, List, Optional

TAXONOMY = {
    "AI": ["artificial intelligence", "machine learning", "ml", "llm", "large language model", "generative ai", "gen ai", "ai-powered", "ai powered", "neural network", "nlp", "natural language processing", "deep learning"],
    "DevTools": ["developer tools", "devtools", "coding", "programming", "software development", "sdk", "developer", "developers", "engineering team", "software engineer", "for engineers", "cli", "terminal", "command line", "command-line", "command line tool"],
    "B2B SaaS": ["saas", "b2b", "enterprise software", "business software", "subscription software", "automation", "workflow", "productivity", "b2b software", "automate"],
    "Open Source": ["open source", "open-source", "coss", "github", "public repo"],
    "FinTech": ["fintech", "financial", "payment", "banking", "crypto", "blockchain", "wallet"],
    "HealthTech": ["healthtech", "healthcare", "medical", "biotech", "wellness"],
    "Consumer": ["consumer", "b2c", "app", "social media", "social platform", "gaming", "lifestyle"],
    "DeepTech": ["deeptech", "robotics", "quantum", "hard tech", "science"],
    "Infrastructure": ["infrastructure", "infra", "cloud", "backend", "hosting", "database"],
    "Cybersecurity": ["security", "cybersecurity", "privacy", "protection", "firewall"],
    "Marketplaces": ["marketplace", "multi-sided", "brokerage", "two-sided market", "buyer and seller"],
    "E-commerce": ["e-commerce", "ecommerce", "shopping", "retail", "online store"],
    "Enterprise": ["enterprise", "corporate", "large scale"],
    "Data": ["data", "api", "rest", "graphql", "interface"]
}

from urllib.parse import urlparse

def get_geography_from_url(url: str) -> str:
    """Infer geography from URL TLD."""
    if not url:
        return "Global"
    
    try:
        # Prepend scheme if missing for proper parsing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        hostname = urlparse(url).hostname or ""
        if hostname.endswith(".in"):
            return "India"
        if hostname.endswith(".uk") or hostname.endswith(".co.uk"):
            return "Europe"
        if hostname.endswith(".eu"):
            return "Europe"
        if hostname.endswith(".de") or hostname.endswith(".fr") or hostname.endswith(".nl"):
            return "Europe"
    except Exception:
        pass
    
    return "Global"

def extract_tags(description: str, url: str) -> List[str]:
    """Match keywords in description and URL against taxonomy."""
    text = f"{description} {url}".lower()
    extracted = []
    
    for tag, keywords in TAXONOMY.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                extracted.append(tag)
                break
                
    if not extracted:
        return ["Generalist"]
    
    return sorted(list(set(extracted)))

def get_product_context(description: str, url: str, stage: Optional[str] = None, geography: Optional[str] = None) -> Dict:
    """Entry point for parsing product context."""
    return {
        "description": description,
        "url": url,
        "extracted_tags": extract_tags(description, url),
        "stage_hint": stage,
        "geography_hint": geography if geography else get_geography_from_url(url)
    }

if __name__ == "__main__":
    # Quick CLI test
    import sys
    if len(sys.argv) > 1:
        desc = sys.argv[1]
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        print(get_product_context(desc, url))
