# Security

Security findings are the clearest "block the merge" cases, so they justify thorough checking — but
hold them to evidence: name the untrusted input and the path it takes to the dangerous sink.
Speculative "could be unsafe" without a reachable source→sink path is a Pass-B casualty. Patterns are
language-agnostic; map them to the stack in front of you.

## Injection (the dominant class)
Untrusted input reaching an interpreter — SQL, shell, OS command, LDAP, NoSQL query, template engine.
- **SQL:** any query built with string concatenation/interpolation of user input. Fix: parameterized
  queries / bound params / ORM, never f-strings or `+`.
- **Command:** user input in `exec`/`system`/`subprocess` with a shell. Fix: pass an argv array, no
  shell; validate against an allowlist.
- **NoSQL / template / LDAP:** same shape — user data changing query/template *structure* rather than
  being passed as a value.

## XSS / output encoding
Untrusted data written into HTML/JS/DOM without escaping: `innerHTML`, `dangerouslySetInnerHTML`,
unescaped template output, building DOM from user strings. Fix: textContent / auto-escaping templates
/ sanitize (e.g. DOMPurify) when HTML is genuinely needed.

## AuthZ / AuthN
- A new endpoint/handler/mutation missing an authentication or ownership check — can user A act on
  user B's resource? This is among the most common *real* bugs in feature PRs and easy to miss.
- Authorization checked on the client but not the server.
- Privilege/role check skipped on a new admin or destructive action.

## Secrets & sensitive data
- Hardcoded API keys, tokens, passwords, private keys in source or committed config. Fix: env/secret
  manager. (If a real secret appears committed, flag Critical and recommend rotation — exposure ≠
  removal.)
- Secrets, tokens, PII, full card/SSN logged or returned in errors/responses.

## Other high-value classes
- **SSRF:** server fetches a user-supplied URL without an allowlist → internal network/metadata access.
- **Unsafe deserialization:** `pickle`/Java native/`yaml.load`/`eval` on untrusted data → RCE.
- **Path traversal:** user input in a file path without normalization+containment (`../`).
- **Missing authz on direct object reference (IDOR):** `/api/doc/{id}` returning any id's data.
- **Weak randomness for security:** `Math.random()`/`rand()` for tokens, IDs, password resets.
- **Crypto misuse:** MD5/SHA1 for passwords (use bcrypt/argon2), hardcoded IV, ECB mode.

## Calibration
Exploitable + reachable from untrusted input → Critical. A defense-in-depth gap with no clear
reachable path → Medium at most, and only if you can articulate the scenario.
