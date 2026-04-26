---
name: linkedin-job-post-to-buyer-pain-map
description: Takes pasted LinkedIn job posts or hiring descriptions and converts them into a structured buyer pain map with inferred pains, capability gaps, buy-vs-build signal, account priority scores, and suggested outreach angles. Use when asked to analyze hiring posts, decode job descriptions for buyer intent, build a pain map from job listings, extract GTM signals from hiring activity, or prioritize accounts based on hiring data. Trigger when a user says "analyze these job posts", "what pain does this hiring signal", "build a pain map from these listings", "decode this job description", or "score these accounts from their hiring".
author: ajaycodesitbetter
version: 1.0.0
---

# LinkedIn Job Post to Buyer Pain Map

Take LinkedIn job posts. Decode them into a structured buyer pain map with scores, pains, and outreach angles.

---

**Critical rule:** Every inferred pain must cite specific language from the job description that supports it. Never hallucinate pains that are not grounded in the text. If a post is too generic to infer pain, say so explicitly and assign a low signal strength score.

**Ethical rule:** Do not infer personal attributes or protected characteristics about candidates. Focus strictly on company-level operational pain and organizational needs.

---

## Step 1: Setup Check

Confirm required env vars:

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
```

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

---

## Step 2: Collect Inputs

The skill needs 3 required inputs. Collect them before proceeding.

### 2a: Product Brief

Ask: "Describe your product in 2-5 sentences. What do you do, what is your core value prop, and who do you target?"

**If the user already included this in their prompt:** Extract it. Confirm: "Product brief captured: [summary]."

### 2b: ICP Description

Ask: "Describe your ideal customer profile in 2-6 bullets: industries, company sizes, roles you sell to, tech stack hints."

**If the user already included this in their prompt:** Extract it. Confirm: "ICP captured: [summary]."

### 2c: Hiring Posts

Ask: "Paste the job descriptions you want analyzed. For each post, include the company name, job title, and the full description text. You can paste 1-15 posts."

**Accepted formats:**
- Raw pasted text with company name and job title clearly labeled
- Structured JSON objects with fields: `company_name`, `job_title`, `location` (optional), `seniority` (optional), `team_or_function` (optional), `job_description_text`, `job_url` (optional)
- Multiple posts separated by clear delimiters (--- or numbered)

**If any field is missing:** Infer what you can from the description text. If company_name or job_description_text is missing, ask for it before proceeding.

### 2d: Optional Inputs

If the user provides any of these, capture them:
- `account_notes`: additional context per company (funding, tech stack, known tools, contacts)
- `focus_dimension`: "pipeline" (bias toward scoring and prioritization), "positioning" (bias toward messaging angles), or "both" (default)

---

## Step 3: Extract Signals

For each job post, parse and extract:

1. **Team / function:** Which team is this role on? (GTM, Product, Infra, Data, RevOps, CS, Engineering, etc.)
2. **Seniority:** IC, Senior IC, Manager, Director, VP, C-level
3. **Responsibilities emphasis:** Classify the dominant mode:
   - Fire-fighting: "stabilize", "fix", "reduce downtime", "unblock"
   - Building new: "build from scratch", "0→1", "greenfield", "design and implement"
   - Optimizing: "scale", "optimize", "improve efficiency", "automate"
   - Replacing: "replace legacy", "migrate from", "modernize"
4. **Requirement language:** Note keywords that signal intent: "first X hire", "critical role", "immediate", "must have"
5. **Tool / stack hints:** Any references to specific tools, platforms, or technology categories that overlap with the user's product area

**Group by company.** If multiple posts come from the same company, group their signals together.

State: "Extracted signals from X posts across Y companies."

---

## Step 4: Score with Gemini

Read `references/scoring-rubric.md` for the full scoring model.

Build the Gemini request:

```bash
cat > /tmp/pain-map-score-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a GTM analyst who specializes in decoding hiring signals into buyer intent. For each account provided, you will score three dimensions and infer company context. Rules: (1) Every score must include a one-sentence plain-text explanation. (2) signal_strength measures how many and how specific the hiring signals are relative to the user's product area. (3) urgency measures how time-sensitive the hiring need appears. (4) icp_fit measures how closely the company matches the user's ICP description. (5) Each score is 1-10. (6) overall_score = round((0.4 * signal_strength + 0.3 * urgency + 0.3 * icp_fit) * 10). (7) Infer buy_vs_build from job language. Use EXACTLY one of these labels: 'Leaning build', 'Leaning buy', 'Hybrid (buy-and-build)', 'Unknown'. (8) Infer stage_guess from company clues: funding stage, employee count, company type. (9) Output valid JSON only."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "SCORING_CONTEXT_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 4096
  }
}
ENDJSON
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/pain-map-score-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `SCORING_CONTEXT_HERE` with:
- The product brief and ICP description from Step 2
- The extracted signals per company from Step 3
- The scoring rubric rules from `references/scoring-rubric.md`
- Instructions to output JSON with: `company_name`, `headline`, `overall_score`, `score_breakdown` (signal_strength, urgency, icp_fit — each with score and explanation), `stage_guess`, `buy_vs_build_guess`

---

## Step 5: Build Pain Map

For each account, use the extracted signals and Gemini scoring context to build the buyer pain map.

```bash
cat > /tmp/pain-map-analysis-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a B2B pain analyst who reads job descriptions and identifies the operational pains a company is experiencing. Rules: (1) Every pain must have a short label, a 1-3 sentence description, and specific phrases quoted from the job post as supporting evidence. (2) Classify pains as primary (directly relevant to the user's product) or secondary (real pain but tangential to the product). (3) If a post is too generic to infer specific pain, state that explicitly — do not hallucinate. (4) For each account, also generate 1-3 recommended outreach angles. Each angle has: angle_name (short), narrative (1-2 sentences on how to lead), and talk_track_bullets (2-4 concrete talking points). (5) Outreach angles must reference specific pains and evidence, not generic value props. No banned words: synergy, leverage, innovative, cutting-edge, best-in-class, world-class, game-changing, disruptive, seamless, robust, comprehensive, revolutionize, transform, streamline. (6) Output valid JSON only."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "ANALYSIS_CONTEXT_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.4,
    "maxOutputTokens": 8192
  }
}
ENDJSON
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/pain-map-analysis-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `ANALYSIS_CONTEXT_HERE` with:
- The product brief and ICP description
- Each company's job posts (full text)
- The scores and context from Step 4
- Account notes if provided
- The focus_dimension preference (pipeline / positioning / both)
- Instructions to output per-account: `buyer_pain_map` (primary_pains, secondary_pains) and `recommended_outreach_angles`

Read `references/examples.md` to calibrate the expected output quality and depth.

---

## Step 6: Build Handoff Object

For each account, generate a structured handoff block that `outreach-sequence-builder` can consume directly:

```
handoff:
  for_outreach_sequence_builder:
    account_summary: 2-3 sentence recap of the company's situation and hiring context
    key_pain: The single most actionable pain in one sentence
    suggested_personas: 2-4 job titles of the people most likely to own this pain
    tone: One sentence describing the recommended outreach tone
```

The handoff must be concrete enough that someone could paste it into outreach-sequence-builder's prompt and get a usable sequence without re-researching the account.

---

## Step 7: Self-QA

Run every check and fix violations before presenting:

- [ ] Every inferred pain cites at least one specific phrase from the job description
- [ ] No pains hallucinated for generic/low-signal posts (check posts with signal_strength ≤ 3)
- [ ] All three scores (signal_strength, urgency, icp_fit) have a one-sentence explanation
- [ ] Overall score matches the formula: `round((0.4 × signal + 0.3 × urgency + 0.3 × icp_fit) × 10)`
- [ ] Buy-vs-build label is one of: "Leaning build", "Leaning buy", "Hybrid (buy-and-build)", "Unknown"
- [ ] No banned words in outreach angles: synergy, leverage, innovative, cutting-edge, best-in-class, world-class, game-changing, disruptive, seamless, robust, comprehensive, revolutionize, transform, streamline
- [ ] Each outreach angle has 2-4 talk track bullets, not generic value statements
- [ ] Out-of-ICP accounts are flagged with a clear recommendation to deprioritize
- [ ] Handoff objects are complete with all 4 fields (account_summary, key_pain, suggested_personas, tone)
- [ ] No personal attributes or protected characteristics inferred about candidates
- [ ] Posts grouped by company when multiple posts are from the same company

Fix any violation before presenting.

---

## Step 8: Output and Save

### Human-readable output

Present the full analysis in this format:

```
## Buyer Pain Map — [YYYY-MM-DD]

**Product:** [product name from brief]
**Posts analyzed:** X posts across Y companies
**Focus:** [pipeline / positioning / both]

---

### [Company Name] — Score: [N]/100

**Headline:** [one-line summary of what the hiring reveals]

| Dimension | Score | Explanation |
|-----------|-------|-------------|
| Signal Strength | N/10 | [one sentence] |
| Urgency | N/10 | [one sentence] |
| ICP Fit | N/10 | [one sentence] |

**Stage:** [stage guess] | **Buy-vs-Build:** [posture label]

#### Primary Pains
- **[Pain label]:** [1-3 sentence description]
  - Evidence: "[quoted phrase from job post]"

#### Secondary Pains
- **[Pain label]:** [1-3 sentence description]
  - Evidence: "[quoted phrase from job post]"

#### Recommended Outreach Angles
1. **[Angle name]:** [narrative]
   - [bullet 1]
   - [bullet 2]
   - [bullet 3]

#### Handoff → outreach-sequence-builder
> **Summary:** [2-3 sentences]
> **Key pain:** [one sentence]
> **Suggested personas:** [list]
> **Tone:** [one sentence]

---

[repeat for each company, ordered by overall_score descending]
```

### Save to file

```bash
mkdir -p docs/pain-maps
OUTFILE="docs/pain-maps/$(date +%Y-%m-%d).md"
cat > "$OUTFILE" << 'EOF'
REPORT_CONTENT_HERE
EOF
echo "Pain map saved to $OUTFILE"
```

If multiple companies are analyzed, also save individual files using slugified company names (lowercase, replace spaces and special characters with hyphens, strip trailing hyphens):

e.g., "ACME, Inc." → `acme-inc.md`, "CoolStartup Inc" → `coolstartup-inc.md`

```bash
SLUG=$(echo "COMPANY_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/-$//')
cat > "docs/pain-maps/${SLUG}.md" << 'EOF'
INDIVIDUAL_ACCOUNT_CONTENT_HERE
EOF
```

---

## When to Use

- You have 1-15 pasted job descriptions and want to know what pain each company is feeling
- You are planning account-based outreach and need structured pain analysis before writing sequences
- You want to prioritize which hiring-signal accounts to pursue first
- A PMM wants real-world pain language from job posts to refine positioning

## When NOT to Use

- You need to **find** companies that are hiring (use `linkedin-hiring-intent-scanner` or `yc-intent-radar-skill` instead)
- You need to **write outreach messages** (use `outreach-sequence-builder` instead — feed it the handoff from this skill)
- You want to **monitor** a platform for signals over time (use `reddit-icp-monitor` or `twitter-GTM-find-skill` instead)
- You need contact information or email enrichment (this skill does not provide that)

## Plays Well With

- **outreach-sequence-builder**: Pass the `handoff.for_outreach_sequence_builder` block directly as context when building a sequence.
- **noise-to-linkedin-carousel**: Use the primary pains and evidence quotes as source material for a carousel about buyer problems.
- **reddit-icp-monitor**: Cross-reference pain themes from job posts with pain themes showing up in Reddit discussions.
