# PRD: vc-curated-match

## Overview
The `vc-curated-match` is an OpenDirectory skill that connects founders and open-source creators with highly relevant Venture Capital firms. It accepts a product description and a homepage URL to algorithmically identify investors targeting that exact stage, industry, and niche.

## Who it is for
Startup founders, open-source maintainers considering commercialization, and indie hackers seeking early-stage (Pre-seed, Seed, Series A) or niche-specific funding.

## Inputs
- `--description`: A brief summary of the product and problem it solves.
- `--url`: The product's main homepage or GitHub repository URL.
- `--stage`: (Optional) Desired funding stage (e.g., Pre-Seed, Seed, Series A).
- `--output`: (Optional) Format destination (default: `vc-matches.md`).

## Outputs
A Markdown document ranking the highest-confidence VC funds, outlining their thesis, standard check sizes, their recent portfolio investments in that sector, and a personalized "Match Rationale."

## What "Good" Output Looks Like
A highly specific, noise-free list. If the user submits a Kubernetes DevTool, the output should exclusively feature infrastructure/DevTool-focused funds (like boldstart, Heavybit, Amplify) rather than generic consumer SaaS funds. It should explain exactly why the match is included based on the fund's data. Note that it will also include generalist funds if they match the desired stage, but they will be labeled with lower confidence compared to vertical-specific matches.

## Honest Limitations
- **Data Currency:** Relies on a static snapshot dataset; funds rapidly shift theses or stop deploying capital.
- **No warm intros:** Identifying targets provides no competitive networking advantage.
- **No financial advice:** Strictly matches semantic descriptions to public theses.
