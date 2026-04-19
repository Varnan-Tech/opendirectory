# Troubleshooting FAQ: `openai/openai-python`
> Auto-generated from 100 open issues.

> **Note:** This is an illustrative mock output. Issue numbers and titles are simulated here to demonstrate the markdown structure outputted by the generation script.

## Why am I getting 429 errors on `/v1/chat/completions`?

**Common symptoms**
- Consistent errors matching cluster signature: `endpoint:/v1/chat/completions|status:429`
- API typically responds with HTTP `429`

**Likely cause**
- This is often caused by exceeding the allowable burst or sustained request volume for the targeted API key or IP address.

**Suggested workaround**
- Likely resolved by implementing exponential backoff, reducing active concurrency, or checking workspace usage limits.

**Cluster Confidence Score:** 0.8/1.0

**Related issues (3)**
- [#899](https://github.com/openai/openai-python/issues/899) - Async RateLimitError not matching docs (Mock)
- [#812](https://github.com/openai/openai-python/issues/812) - Retries failing on 429 Too Many Requests (Mock)
- [#744](https://github.com/openai/openai-python/issues/744) - Need help with batch /v1/chat/completions (Mock)

---

## Why am I seeing the error: `invalid_request_error`?

**Common symptoms**
- Consistent errors matching cluster signature: `error:invalid_request_error`

**Likely cause**
- This typically indicates missing required fields, improper data types, or an invalid JSON payload schema.

**Suggested workaround**
- Review the request payload carefully and ensure all required parameters securely match the official documentation.

**Cluster Confidence Score:** 0.6/1.0

**Related issues (2)**
- [#955](https://github.com/openai/openai-python/issues/955) - Sending image URL returns invalid_request_error (Mock)
- [#901](https://github.com/openai/openai-python/issues/901) - Pydantic validation failing serialization (Mock)
