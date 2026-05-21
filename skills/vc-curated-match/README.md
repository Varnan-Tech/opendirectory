# vc-curated-match

> Identify targeted VC funds based on a product's description and URL. This skill matches project inputs to a curated dataset of top global venture capital firms based on industry tags, stage, and geography.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)

## Overview

The `vc-curated-match` is an OpenDirectory skill that connects founders and open-source creators with highly relevant Venture Capital firms. It relies on a static, curated list of real VC funds to prevent LLM hallucinations, ensuring all recommendations and rationales are grounded in actual fund thesis data.

**Positioning Note**: This skill is intentionally different from live-research investor discovery workflows. It provides deterministic, curated VC matching from a verified static dataset. It is best for fast, low-cost, repeatable first-pass investor targeting.

## Install

```bash
npx "@opendirectory.dev/skills" install vc-curated-match --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

---

## Requirements
- Python 3.10+ (Standard Library only used internally by the agent)

## Implementation Specs
- Pulls from a static `data/vc_funds.json` dataset to guarantee data validity.
- Ranks funds using tag-matching algorithms across industry focus, stage, and geography fit.
- Outputs confidence tiers (High, Medium, Low) to transparently surface the precision of the fit.

## Usage

```bash
python scripts/run.py \
  --description "A Next.js template for enterprise B2B SaaS" \
  --url "https://trymylandingpage.com" \
  --stage "Pre-seed"
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
