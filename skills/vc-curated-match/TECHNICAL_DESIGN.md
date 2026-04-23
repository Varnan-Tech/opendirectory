# Technical Design: vc-curated-match

## Data Architecture
- **Source of Truth**: Uses a strictly curated static dataset (`data/vc_funds.json`) containing verified fund data.
- **Data Integrity**: Every firm, thesis, and check size is hardcoded to prevent hallucinations.
- **Expansion**: Adding new funds requires updating the JSON file, ensuring human-in-the-loop validation of investor data.

## Deterministic Pipeline
The skill uses a 100% rule-based matching engine implemented in Python (zero LLM dependency for core matching):

1. **Context Extraction**: The `fetch_product_context.py` script uses regular expressions with word-boundary detection (`\b`) to map product descriptions to a hardened taxonomy.
2. **Geography Inference**: Inferred via URL Top-Level Domain (TLD) parsing to determine primary regional focus (e.g., India, Europe, US).
3. **Scoring Engine**: `match_vcs.py` calculates a weighted score (0-100) based on:
   - **Tag Overlap (60%)**: Exact matches between product tags and fund industry focus.
   - **Stage Fit (20%)**: Proximity matching between target stage and fund focus.
   - **Geography (20%)**: Regional alignment or Global presence boosts.
4. **Ranking & Filtering**: Funds are ranked by score and stabilized by alphabetical order. Only the top 10 matches are returned.
5. **Report Generation**: `generate_report.py` synthesizes the final Markdown using deterministic templates grounded strictly in the matched fund data.

## Hallucination Guards
- **No LLM in Match Loop**: By using Python heuristics instead of LLM reasoning, the tool guarantees that no "fake" funds are invented and theses are never distorted.
- **Regex Boundaries**: Prevents false positive tag matches (e.g., preventing "infrastructure" from matching "structure").
- **Confidence Tiers**: Scores are mapped to High/Medium/Low tiers to communicate the strength of the algorithmic match.

## Output Consistency
All reports follow a standardized Markdown structure with mandatory metadata blocks, ensuring programmatic readability and consistent user experience.
