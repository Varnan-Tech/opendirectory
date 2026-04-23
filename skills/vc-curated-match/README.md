# vc-curated-match

> Identify targeted VC funds based on a product's description and URL. This skill matches project inputs to a curated dataset of top global venture capital firms based on industry tags, stage, and geography.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)

## Overview

The `vc-curated-match` is an OpenDirectory skill that connects founders and open-source creators with highly relevant Venture Capital firms. It relies on a static, curated list of real VC funds to prevent LLM hallucinations, ensuring all recommendations and rationales are grounded in actual fund thesis data.

**Positioning Note**: This skill is intentionally different from live-research investor discovery workflows. It provides deterministic, curated VC matching from a verified static dataset. It is best for fast, low-cost, repeatable first-pass investor targeting.

## Prerequisites
- Python 3.10+ (Standard Library only)

## Implementation Specs
- Pulls from a static `data/vc_funds.json` dataset to guarantee data validity.
- Ranks funds using tag-matching algorithms across industry focus, stage, and check size.
- Outputs confidence tiers (High, Medium, Low) to transparently surface the precision of the fit.

## Usage

```bash
python scripts/run.py \
  --description "A Next.js template for enterprise B2B SaaS" \
  --url "https://trymylandingpage.com" \
  --stage "Pre-Seed"
```

## Methodology

- **Tag Matching**: Deterministic keyword matching using whole-word regex boundaries to ensure precision.
- **Geography Inference**: Inferred primarily from the URL Top-Level Domain (TLD). For example, `.in` triggers India and `.eu` triggers Europe.
- **Default Baseline**: Domains like `.com`, `.io`, and `.ai` default to a `Global` geography hint unless a specific `--geography` flag is provided.

## Limitations

- **No Live Research**: This skill does not perform live web discovery and may miss niche or newly launched funds not present in the dataset.
- **Static Dataset**: The VC fund list is a curated static dataset. It reflects fund theses as of the last update and may not capture real-time changes in fund availability or personnel.
- **Taxonomy Constraints**: The scoring engine relies on a fixed taxonomy. Extremely niche or highly unusual product descriptions may not trigger specific industry tags and will default to a "Generalist" view.
- **Human Review Required**: These outputs are best-effort algorithmic matches. They serve as a research starting point and **must be reviewed by a human** before starting outreach.
- **No Financial Advice**: This tool does not provide financial or investment advice.
