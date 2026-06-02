# domain-expired-opportunity-finder

Evaluate expired domain candidates against your niche. Get a conservative,
explainable shortlist with risk flags — not another noisy domain list.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install domain-expired-opportunity-finder --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fdomain-expired-opportunity-finder&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Accepts a target niche and a set of expired domain candidates
- Collects signals from free public sources (Wayback Machine, WHOIS, domain analysis)
- Scores each candidate across 6 transparent dimensions: topical relevance, historical activity level, historical content quality, history cleanliness, redirect suitability, and signal completeness.
- This skill acts as a **Level 1 Triage** filter. It automatically pulls historical data, runs a strict 6-dimension scoring model (penalizing topic mismatches and spammy histories), and outputs a highly readable shortlist for your team.
- *Note: This tool uses public historical data (Wayback/RDAP) to infer domain legitimacy. It is designed to filter out junk before you spend paid Ahrefs/Majestic API credits on the remaining candidates.*
- Flags risks explicitly (spam content risk, topic mismatch, unclear history, possible deindex)
- Outputs a ranked shortlist where every domain has a `why_selected` AND `why_risky` explanation
- Saves structured JSON output to `docs/expired-domain-intel/YYYY-MM-DD.json`

## What It Does NOT Do

- Does not automate domain buying, bidding, or registration
- Does not promise rankings or guarantee SEO outcomes
- Does not encourage PBN construction or deceptive redirects
- Does not replace commercial tools like Ahrefs or DomCop for bulk discovery
- Does not produce black-box scores — every recommendation is auditable

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| Python 3.10+ | Signal collection and scoring | python.org |
| curl | API calls to Wayback Machine | Pre-installed on most systems |
| whois CLI | Domain registration checks | `apt install whois` or `brew install whois` |
| LLM API key (optional) | Enhanced niche-relevance scoring | See .env.example |

The skill works without an LLM API key. Rule-based scoring uses domain string
analysis and Wayback CDX data. Adding an LLM key enables deeper contextual
niche-relevance assessment.

## Setup

```bash
cp .env.example .env
```

Fill in `LLM_API_KEY` if you want LLM-enhanced scoring (optional).

## How to Use

Basic usage:
```
"Find expired domain opportunities in the developer tools niche"
"Evaluate these expired domains for my cybersecurity blog"
"Triage this list of expired domains for AI SaaS redirect potential"
```

With specific candidates:
```
"Evaluate these expired domains for the fintech niche: paymentsdaily.com, fintechweekly.io, cheaploans247.net"
```

With options:
```
"Find expired domain opportunities in developer tools. Minimum 20 referring domains. Only show low-risk candidates. Focus on rebuild potential."
```

Run with the built-in demo set:
```
"Run the expired domain finder with the example set"
```

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target_niche` | string | Yes | Core niche to evaluate against (e.g., "developer tools") |
| `seed_keywords` | array | No | Keywords for refined matching (e.g., ["devops", "CI/CD"]) |
| `candidate_domains` | array | No | Domains to evaluate (prompted if not provided) |
| `discovery_source` | string | No | Where candidates came from |
| `min_ref_domains` | integer | No | Minimum referring-domain threshold (default: 10) |
| `max_risk_level` | string | No | `low`, `medium`, `high` — controls filtering aggressiveness |
| `intended_use` | string | No | `rebuild`, `redirect`, or `either` (default: `either`) |

## Output Example

```json
{
  "skill": "domain-expired-opportunity-finder",
  "target_niche": "developer tools",
  "shortlist": [
    {
      "domain": "devtoolsweekly.com",
      "opportunity_score": 86,
      "confidence": "high",
      "recommended_action": "high-priority-review",
      "redirect_suitability": "high",
      "topical_fit_summary": "Domain name contains 'devtools'. Wayback snapshots confirm it was a weekly newsletter covering developer tools and IDE plugins from 2019 to 2024.",
      "activity_level_summary": "High snapshot frequency across 6 consecutive years, indicating sustained active use.",
      "content_quality_summary": "Historical page titles are predominantly branded ('DevTools Weekly') and natural. No keyword stuffing detected.",
      "history_summary": "6 years of consistent Wayback snapshots (2019–2024). All snapshots show real content. No parking pages or sudden drop-offs.",
      "risk_flags": [],
      "why_selected": "Strong topical match with healthy activity level and clean 6-year history.",
      "why_risky": "No significant risk signals. Standard due diligence recommended."
    }
  ]
}
```

## Scoring Overview

The skill uses a transparent weighted model (no black-box ranking):

| Dimension | Weight | Signals Analyzed |
| :--- | :--- | :--- |
| **Topical Relevance** | 30% | Keyword match, Wayback titles, LLM classification |
| **Historical Activity Level** | 25% | Snapshot frequency and long-term continuity |
| **Historical Content Quality** | 15% | Title keyword stuffing, natural phrasing |
| **History Cleanliness** | 15% | Years active, parking pages, 200 vs 404 ratio |
| **Redirect Suitability** | 10% | Niche overlap, content format consistency |
| **Signal Completeness** | 5% | Availability of Wayback and RDAP data |

Full scoring details: `references/scoring-model.md`

## Risk Flags

| Flag | Severity | Effect |
| :--- | :--- | :--- |
| `topic_mismatch` | High | Caps score. Domain is in a completely unrelated niche. |
| `spam_content_risk` | High | Caps score. Heavy exact-match money keywords in titles. |
| `possible_deindex` | High | Caps score. Sudden drop-off in Wayback captures. |
| `redirect_mismatch` | High | Caps redirect suitability. Not safe for 301. |
| `unclear_history` | Medium | Reduces score. <3 Wayback captures or mostly parking pages. |
| `short_history` | Medium | Reduces score. Domain active < 1 year before expiry. |
| `weak_historical_activity` | Medium | Reduces score. Snapshots below threshold. |
| `suspicious_registrar` | Medium | Known spam-associated registrar |

Full flag definitions: `references/risk-flags.md`

## Recommendation Labels

| Label | Meaning |
|---|---|
| `high-priority-review` | Strong match, low risk — review first |
| `review` | Worth investigating, mixed or incomplete evidence |
| `rebuild-only-review` | Good for rebuild, not suitable for redirect |
| `reject` | Does not meet quality or relevance threshold |

## Guardrails

This skill is a research and triage tool. It:
- Frames all results as recommendations, not guarantees
- Requires topic continuity for redirect recommendations
- Flags manipulative patterns instead of optimizing for them
- Includes a disclaimer on every output

Full guardrails policy: `references/guardrails.md`

## Project Structure

```
domain-expired-opportunity-finder/
├── SKILL.md               # Agent workflow instructions
├── README.md              # This file
├── .env.example           # API key template (optional)
├── evals/
│   └── evals.json         # 5 test scenarios
└── references/
    ├── scoring-model.md   # Transparent scoring dimensions
    ├── output-format.md   # JSON output schema
    ├── risk-flags.md      # Risk flag definitions
    └── guardrails.md      # Anti-abuse policy
```

## License

MIT
