# oss-launch-kit Technical Design

## Architecture Summary
`oss-launch-kit` should follow the same advanced-skill pattern used elsewhere in this repo:
- `README.md` for public overview and usage
- `SKILL.md` for operational instructions
- `.env.example` for required environment variables
- `scripts/` for executable orchestration
- `references/` for design guides, templates, and frameworks (note: these are for design-time reference, the current scripts use hardcoded templates for maximum performance and stability).
- `evals/` for validation cases

The implementation should be a two-stage pipeline:

1. repo context -> structured product brief
2. product brief -> channel-specific launch assets

This mirrors the repo’s stronger launch skills and keeps the generation grounded.

## Stage A: Repo Context -> Product Brief
### Responsibility
Convert raw GitHub repo data into a normalized brief that captures only what can be supported by evidence.

### Inputs
- repo metadata JSON
- README text
- optional release metadata

### Output schema
```json
{
  "repo_name": "string",
  "one_line_summary": "string",
  "project_type": "string",
  "launch_readiness": {
    "score": "low | medium | high",
    "signals": "object",
    "fix_plan": "list"
  },
  "audience": "string",
  "problem_solved": "string",
  "value_proposition": "string",
  "key_proof_points": "list",
  "key_features": "list",
  "links": "object",
  "confidence": "low | medium | high",
  "assumptions": "list",
  "channel_fitness": "object"
}
```

### Failure cases
- README is sparse or missing.
- Repo description conflicts with README.
- Audience is implied, not explicit.

### Hallucination controls
- Treat README and repo metadata as the only factual source.
- Allow `unknown` or empty values when evidence is missing.
- Store evidence alongside every major inference.

## Stage B: Product Brief -> Launch Assets
### Responsibility
Use the brief to generate channel-specific drafts with channel rules applied.

### Inputs
- product brief JSON
- channel rules from `references/channel_rules.md`
- output template from `references/output_template.md`

### Output
- final Markdown launch kit

### Failure cases
- assets become generic
- channel tone drifts away from platform norms
- unsupported claims leak into drafts

### Hallucination controls
- no new facts beyond the brief
- confidence notes carry through to final output
- use explicit `[!TIP]` handoffs to specialized skills
- suppress aggressive channels for unready repos

## Channel Rules
### Show HN
- direct and technical
- no hype language
- no fake performance claims
- plain title alternative only if useful

### Product Hunt
- include tagline and description
- maker comment should sound human and specific
- avoid invented social proof
- do not exceed practical PH length constraints

### Reddit
- generate niche suggestions based on repo tags and description
- include a warning to verify subreddit rules before posting
- prioritize feedback-first communities for early-stage repos

### Twitter/X
- concise thread
- each tweet should carry one idea
- use evidence-based language only
- no spammy hashtags

## File Structure
```text
skills/oss-launch-kit/
├── README.md
├── SKILL.md
├── .env.example
├── PRD.md
├── TECHNICAL_DESIGN.md
├── evals/
│   └── evals.json
├── references/
│   ├── launch_framework.md
│   ├── channel_rules.md
│   └── output_template.md
└── scripts/
    ├── run.py
    ├── fetch_repo_context.py
    ├── build_product_brief.py
    └── generate_assets.py
```

## Implementation Phases
### Phase 1: Skeleton and docs
- Create folder structure and planning docs.
- Acceptance: skill folder exists with PRD, technical design, and reference stubs.
- Risk: too much upfront design before validation.

### Phase 2: GitHub fetcher
- Implement repo URL parsing and GitHub API fetches.
- Acceptance: metadata and README resolve for public repos.
- Risk: API rate limits and README format variance.

### Phase 3: Brief builder
- Turn repo context into structured brief JSON.
- Acceptance: evidence-backed fields and explicit confidence notes.
- Risk: over-inference from weak READMEs.

### Phase 4: Asset generation
- Produce final channel drafts from the brief.
- Acceptance: all outputs obey channel rules and remain grounded.
- Risk: repetitive or generic copy.

### Phase 5: Testing on 3 public repos
- Test on a dev tool repo, a library/package repo, and a weak README repo.
- Acceptance: all three produce usable outputs with honest low-confidence handling.
- Risk: one-size-fits-all messaging.

### Phase 6: README polish and PR prep
- Align README with final behavior and usage.
- Acceptance: maintainer can review quickly and see the merge value.

## Testing Strategy
### Test set
- one dev-tool repo with strong README
- one library/package repo with clear positioning
- one repo with a weak README

### Good output means
- factual repo summary
- specific audience and problem framing
- channel-appropriate tone
- no fabricated proof points
- explicit assumptions where evidence is thin

## Risks and Mitigations
- Weak README: keep output short, honest, and confidence-tagged.
- Misleading repo description: prefer README over description.
- Unclear audience: provide one primary hypothesis and note ambiguity.
- Generic launch copy: require evidence fields before drafting assets.
- Wrong subreddit suggestions: mark them as suggestions, not endorsements.
- Hallucinated claims: final validation pass checks every claim against brief evidence.

## PR Plan
- Branch: `skill/oss-launch-kit`
- PR title: `feat(skill): add oss-launch-kit`
- Commit sequence:
  - `docs(skill): add oss-launch-kit prd and technical design`
  - `docs(skill): add oss-launch-kit reference docs and scaffold`
  - `feat(skill): implement repo context fetcher`
  - `feat(skill): implement brief builder and launch asset generation`
