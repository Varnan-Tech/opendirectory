# geo-gap-fixer

**Audit how often LLMs recommend your brand vs. competitors — then get a concrete action plan to fix the gaps.**

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install geo-gap-fixer --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill geo-gap-fixer
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

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

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

<video src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgeo-gap-fixer&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Why this skill exists
In 2026, buyers discover tools by asking ChatGPT, Claude, Gemini, and Perplexity *"what's the best X for Y?"* — not by Googling. If LLMs consistently recommend a competitor instead of you, your traditional SEO rank is irrelevant.

**geo-gap-fixer** is a free, open-source agent skill for GTM Intelligence that audits your Generative Engine Optimization (GEO) share-of-voice. It probes the LLMs, analyzes who gets recommended, and outputs a prioritized content backlog to fix the gaps.

> One skill run replaces a $200/month AI-monitoring SaaS subscription.

---

## Sample Report Output

```markdown
### 1. Share of Voice (LLM Mention Rate)
| Brand | Mention Rate | Avg Rank | Win Rate | Assessment |
|-------|-------------|----------|----------|------------|
| **Linear** | **18.4%** | **4.2** | **5.3%** | 🔴 Critical: Brand is rarely recommended |
| Jira | 94.7% | 1.4 | 82.1% | 🟢 Dominant: Default recommendation |

### 5. GEO Action Plan
🔴 **Critical Priority: Fix Mention Rate (<30%)**
- Create dedicated "Best <Category> Tools in 2026" comparison content.
- Ensure your homepage explicitly answers: "Why use Linear for <Category>?"
```

---

## What You Get

| # | Output Section | Description |
|---|---------------|-------------|
| 1 | **Share-of-Voice Table** | Brand mention rate per LLM (% of prompts where you're mentioned), ranked |
| 2 | **Prompt-Level Loss Log** | Which exact prompts your brand lost and to whom |
| 3 | **Competitor Language Patterns** | What framing/keywords LLMs use for competitors that they don't use for you |
| 4 | **Citation Gap List** | Which domains get cited by LLMs instead of your site |
| 5 | **GEO Action Plan** | Prioritized fixes: FAQ pages, comparison pages, alternative pages, schema improvements, authority targets |

---

## Prerequisites

- **Python 3.10+**
- **At least 2 of 4 API keys** (missing providers are skipped gracefully)
- Dependencies: `pip install openai anthropic google-genai`

| Provider | Package | Model | Env Variable |
|----------|---------|-------|-------------|
| OpenAI | `openai` | gpt-4o | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | claude-sonnet-4-6 | `ANTHROPIC_API_KEY` |
| Google | `google-genai` | gemini-2.5-flash | `GOOGLE_API_KEY` |
| Perplexity | `openai` (reused) | sonar-pro | `PERPLEXITY_API_KEY` |

> **Note**: Perplexity uses the OpenAI SDK with a different base URL, so only 3 packages are needed.

---

## Configuration (`config.json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brand_name` | string | ✅ | Your brand name (e.g., "Linear") |
| `competitors` | list | ✅ | 1–10 competitor brand names |
| `category` | string | ✅ | Product category (e.g., "project management tool for developers") |
| `buyer_intent_prompts` | list | ❌ | Custom prompts. Empty = auto-generate from templates |
| `target_llms` | list | ❌ | Which LLMs to probe. Default: all 4 |
| `website_url` | string | ❌ | Your website for citation gap analysis |

---

## Limitations (What this skill does NOT do)

- **Not a continuous monitor**: This is a point-in-time audit. Run it monthly to track progress.
- **Not for traditional SEO**: It does not track Google Blue Link rankings, domain authority, or keyword search volume.
- **Not deep NLP sentiment analysis**: Sentiment uses keyword proximity, not complex NLP models.
- **Not free to run**: While the tool is free, you pay the LLM API providers directly (typically ~$0.50–$2.00 per audit).

---

## Error Handling

All scripts are designed to fail clearly, not silently:

| Scenario | Behavior |
|----------|----------|
| Invalid JSON config | Exits with parse error and line number |
| Missing required fields | Exits listing exactly which fields are missing |
| No API keys set | Exits listing all 4 env variable names |
| Transient API failure | Retries with exponential backoff (2 attempts, 2s → 4s) |
| Persistent API failure | Skips that provider, continues with others |
| Zero responses collected | Exits non-zero after saving empty results |
| Missing upstream data file | Exits with instructions to run the previous script |

---

## File Structure

```
geo-gap-fixer/
├── README.md              ← You are here
├── SKILL.md               ← Agent instruction flow
├── .env.example           ← API key template
├── .gitignore             ← Excludes data/, report/, config.json
├── package.json           ← OpenDirectory metadata
├── config.example.json    ← Sample configuration
├── scripts/
│   ├── probe_llms.py      ← Send prompts to LLM APIs
│   ├── analyze_results.py ← Extract mentions, rank, sentiment, citations
│   └── build_report.py    ← Assemble the 5-section report
├── references/
│   ├── prompt_templates.md  ← 20 default buyer-intent prompts
│   ├── scoring_rubric.md    ← How metrics are calculated
│   └── output_format.md    ← Sample report with realistic data
├── data/                  ← Generated at runtime (gitignored)
│   ├── raw_responses.json
│   └── analysis.json
└── report/                ← Generated at runtime (gitignored)
    ├── geo_audit_report.md
    └── geo_audit_report.json
```
