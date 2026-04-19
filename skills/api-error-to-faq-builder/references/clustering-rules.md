# Clustering Heuristics

This document details the signal priority used by `build_faq.py` when generating the Markdown artifact.

## 1. Signal Extraction
Text is merged from `title` + `body` + `comments` (if enabled) and checked for:
- Endpoints (e.g. `/v1/chat/completions`)
- Status Codes (e.g. `401`, `429`)
- Categorical hints (e.g. `rate limit`, `timeout`, `api token`, `auth token`)
- Exact Quoted Errors (from ` ```...``` ` blocks)

## 2. Deterministic Key
Issues are chunked first by a strict deterministic identifier based on signal strength:
1. `endpoint + status_code`
2. `endpoint + category`
3. `endpoint_only`
4. `quoted_error_only`
5. `category_only`

## 3. Fuzzy Merge (Threshold ≥ 80)
If an issue lacks strong signals, it is run against the generated representative titles and top issue titles of existing clusters using `thefuzz.token_set_ratio`. 
- **Rule:** A minimum threshold ratio of `80` must be met.

## 4. Confidence Score Formula
```python
Confidence = Size_Score (max 0.5) + Signal_Score (max 0.5)
```
- `Size_Score`: Each grouped issue grants `+0.1` (caps at `0.5`).
- `Signal_Score`: Presence of deterministic factors (endpoint + status `0.5`, endpoint only `0.3`, etc.).
