# Evals — `app-store-review-arbitrage`

This directory contains eval scenarios for verifying skill behavior. Evals check **structural expectations** — output shape, gate behavior, and content rules. They do not pin exact content, since live review data changes daily.

## Running Evals

### Eval 1 — Notion iOS (high signal)

```bash
python3 scripts/fetch_reviews.py "https://apps.apple.com/us/app/notion-notes-tasks-ai/id1232780281" \
  --output /tmp/asr-raw.json

# Then run the skill on the collected data
```

Expected: `low_star_count >= 10`, ≥ 3 clusters, Section 2 populated, 3 H1s, 3 ad copy directions.

### Eval 2 — Robinhood Google Play (moderate signal)

```bash
python3 scripts/fetch_reviews.py "https://play.google.com/store/apps/details?id=com.robinhood.android" \
  --output /tmp/asr-raw.json
```

Expected: `platform = google_play`, `low_star_count >= 10`, ≥ 2 clusters, Section 2 present (any state).

### Eval 3 — Gate 1 behavior (low signal, fixture)

Eval 3 tests that the skill correctly stops before LLM analysis when fewer than 10 low-star reviews are found. It uses a mock fixture to avoid dependence on a specific live URL.

```bash
# To simulate Gate 1 being triggered, pass the fixture directly to the SKILL.md agent:
# "Use /tmp/asr-raw.json with this content instead of running the script"
# Then load: evals/fixtures/eval3-mock.json as the raw collection data

# Or verify the gate message programmatically:
python3 - <<'EOF'
import json
data = json.load(open("evals/fixtures/eval3-mock.json"))
count = data["collection_stats"]["low_star_count"]
assert count < 10, f"Fixture should have < 10 low-star reviews, got {count}"
print(f"Fixture OK: {count} low-star reviews — Gate 1 should trigger")
EOF
```

Expected: gate message contains the actual count (5) and the minimum required (10). No output file written.

## Adding Evals

New evals should follow the schema in `evals.json`. Use real app URLs where possible. Document the app name and expected behavior. For gate-behavior tests, use the fixture approach documented above.
