# ICP Signal Extraction Reference

Used by SKILL.md Step 5 to identify who is posting about these pains -- not just what they say.

---

## The ICP Is In the Metadata

Most ICP research focuses on post content. The higher-signal data is in the metadata:

| Signal | What it tells you |
|---|---|
| Subreddit | Role/function of the person (r/devops = DevOps engineer, r/SaaS = SaaS founder) |
| Post flair | Self-declared role or context within the community |
| GitHub org type | Organization = professional context, individual = personal use |
| HN bio | Often shows company affiliation and seniority |
| Post time | Work hours posts = professional pain, evening posts = side-project or consumer |
| Account age | Older accounts = established practitioners, new = emerging problem awareness |

---

## Subreddit to ICP Role Mapping

| Subreddit | Likely ICP role | Company size signal |
|---|---|---|
| r/devops | DevOps engineer, SRE, platform engineer | Mid to large |
| r/sysadmin | Sysadmin, IT ops, infrastructure | SMB to mid-market |
| r/ExperiencedDevs | Senior+ software engineer | Any |
| r/SaaS | SaaS founder, product manager | Early stage |
| r/startups | Founder, early employee | Pre-seed to Series A |
| r/entrepreneur | Solo founder, small business owner | SMB |
| r/microsaas | Solo founder, indie hacker | Tiny/bootstrapped |
| r/dataengineering | Data engineer, analytics engineer | Mid to large |
| r/datascience | Data scientist, ML engineer | Any |
| r/MachineLearning | ML researcher, ML engineer | Research or large tech |
| r/webdev | Frontend/fullstack dev, indie hacker | Any |
| r/sales | Account exec, SDR, sales leader | Any |
| r/humanresources | HR manager, CHRO | SMB to mid-market |

---

## Pain Concentration = ICP Confidence

The ICP is most reliable when the same pain appears in MULTIPLE subreddits that map to the same role:

- Pain X appears in r/devops (89 posts) AND r/sysadmin (67 posts): ICP = infrastructure/ops practitioners (high confidence)
- Pain X appears in r/startups (12 posts) AND r/SaaS (8 posts): ICP = early-stage founders (medium confidence)
- Pain X appears in r/programming (5 posts): ICP unknown, likely developer but context unclear (low confidence)

---

## Language Patterns to Extract

When reading posts for ICP, look for:

**Job title mentions:**
- "As a DevOps lead at a 200-person company..."
- "We're a small team of 3 engineers..."
- "I manage infrastructure for..."

**Company stage signals:**
- "We just Series A'd..."
- "We're bootstrapped, so..."
- "Our startup..."
- "At my enterprise job..."

**Existing tools mentioned:**
- "We use X but hate..."
- "Switched from X to Y but..."
- "X is too expensive at our scale"

**Decision context:**
- "I'm evaluating..."
- "My manager wants me to..."
- "We're building a business case for..."
- "I own the tooling decision..."

These phrases should appear in the ICP section's "what they say" field as verbatim quotes.

---

## ICP Confidence Levels

| Confidence | Criteria |
|---|---|
| High | 3+ subreddits with 20+ posts each, consistent role signals, multiple verbatim role mentions |
| Medium | 2 subreddits with 10+ posts each, or 1 subreddit with strong signal |
| Low | Single subreddit, < 10 total signals, or mixed/unclear role signals |

Always report the confidence level in the ICP section. Do not present a low-confidence ICP as definitive.
