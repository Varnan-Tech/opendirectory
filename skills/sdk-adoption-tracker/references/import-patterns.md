# Import Patterns Reference

Used by SKILL.md Step 3 to build GitHub code search queries per ecosystem.

---

## Ecosystem Detection

Auto-detect from the SDK name before falling back to user input:

| Signal | Ecosystem |
|---|---|
| Starts with `@` (e.g. `@clerk/nextjs`) | npm |
| Contains `-` and no `github.com/` (e.g. `react-query`) | npm |
| snake_case only, no `-` or `/` (e.g. `requests`, `boto3`) | python |
| Contains `github.com/` (e.g. `github.com/stripe/stripe-go`) | go |
| Contains `.` with no other signals (e.g. `org.springframework.boot`) | java |
| Ambiguous | ask the user |

---

## npm / Node.js

**Search patterns (run each as a separate code search query):**

```
require("sdk-name")
require('sdk-name')
from "sdk-name"
from 'sdk-name'
```

**Notes:**
- `from "sdk-name"` catches ES module default and named imports: `import foo from "sdk-name"` and `import { bar } from "sdk-name"`
- `require("sdk-name")` catches CommonJS usage
- Use the full package name including `@org/` prefix for scoped packages
- Do NOT search `"sdk-name"` as a bare string -- too many false positives in package.json files

**Example for `@clerk/nextjs`:**
```
require("@clerk/nextjs")
from "@clerk/nextjs"
from '@clerk/nextjs'
```

---

## Python

**Search patterns:**

```
import sdk_name
from sdk_name import
from sdk_name.
```

**Notes:**
- `from sdk_name.` catches submodule imports: `from requests.exceptions import`
- Use the PyPI package name (snake_case), not the import name if they differ
- Example: `Pillow` installs as `pillow` but imports as `PIL` -- search `from PIL import` not `import pillow`

**Example for `requests`:**
```
import requests
from requests import
from requests.
```

---

## Go

**Search patterns:**

```
"github.com/org/sdk-name"
```

**Notes:**
- Go imports use the full module path, not just the package name
- Include the full `github.com/org/sdk-name` path in quotes
- For major version suffixes, add the version: `"github.com/org/sdk-name/v2"`

**Example for `github.com/stripe/stripe-go`:**
```
"github.com/stripe/stripe-go"
```

---

## Ruby / RubyGems

**Search patterns:**

```
require 'sdk-name'
require "sdk-name"
gem 'sdk-name'
```

**Notes:**
- `gem 'sdk-name'` catches Gemfile declarations (projects listing the dependency)
- `require 'sdk-name'` catches runtime usage

---

## Rust / Cargo

**Search patterns:**

```
sdk-name = 
sdk_name = 
```

**Notes:**
- Search `Cargo.toml` files for the dependency declaration
- Add `filename:Cargo.toml` to the query to narrow results
- Cargo uses hyphens in package names but underscores in crate names -- search both

**Example for `tokio`:**
```
tokio =
```

---

## PHP / Composer

**Search patterns:**

```
require 'vendor/sdk-name'
use VendorName\SdkName
```

---

## Java / Maven

**Search patterns:**

```
import com.vendor.sdkname
<artifactId>sdk-name</artifactId>
```

**Notes:**
- Maven/Gradle projects declare dependencies in `pom.xml` or `build.gradle`
- `<artifactId>sdk-name</artifactId>` catches Maven declarations
- Add `filename:pom.xml` to the query to narrow to Maven projects

---

## Generic Fallback

If the ecosystem is unclear, use the bare SDK name as the search query. This catches any file that mentions the name but produces more false positives. Always filter by file extension or language qualifier when possible:

```
sdk-name language:javascript
sdk-name language:python
sdk-name language:typescript
```

---

## Query Limit Budget

GitHub code search rate limit: 10 requests/minute (authenticated).

- npm: 4 queries
- Python: 3 queries
- Go: 1 query
- Ruby: 3 queries
- Generic: 1-3 queries

Sleep 6 seconds between queries to stay within 10 req/min.

Total scan time per ecosystem:
- npm: ~24 seconds (4 queries x 6s)
- Python: ~18 seconds (3 queries x 6s)
- Go: ~6 seconds (1 query)
