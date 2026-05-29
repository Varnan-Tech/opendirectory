# Company Profile Format

Standardized company profile object used across all radar phases. Every profile must conform to this structure.

---

## Profile Data Model

```yaml
company:
  name: string                    # Required. Official company name
  domain: string | null           # Website domain (e.g., vercel.com)
  description: string | null      # 2-3 sentence description from web research
  logo_url: string | null         # URL to company logo if found

  # Social handles
  twitter_handle: string | null   # Without @ (e.g., "vercel")
  github_org: string | null       # GitHub org or user name (e.g., "vercel")
  linkedin_url: string | null     # Full LinkedIn URL
  youtube_channel: string | null  # YouTube channel handle
  reddit_community: string | null # Subreddit name (e.g., "reactjs")
  blog_url: string | null         # Company blog URL
  docs_url: string | null         # Documentation URL
  careers_url: string | null      # Careers / jobs page URL

  # YC info
  yc_batch: string | null         # e.g., "W21", "S20"
  yc_url: string | null           # Y Combinator company page URL

  # Product Hunt
  producthunt_slug: string | null # PH slug (e.g., "vercel")
  producthunt_url: string | null  # Full PH URL

  # Founders
  founders:
    - name: string                # Founder full name
      title: string | null        # e.g., "CEO", "CTO"
      twitter_handle: string | null

  # Metadata
  is_open_source: boolean         # Whether the company has OSS repos
  is_yc_company: boolean          # Whether it's a YC-backed company
  profile_completeness: integer   # 0-100, how complete the profile is
  source_urls: string[]           # URLs used to build this profile
```

---

## Profile Rules

1. **Every field must come from evidence.** No default values, no guesses.
2. If a handle/URL is not found, set to `null` -- do not invent it.
3. `profile_completeness` = percentage of discoverable fields filled. A company with domain + description + at least one social handle is ~40% complete. Full social handles + YC + founders = ~90%+.
4. `source_urls` must include the actual URLs where each piece of info was found.
5. Founders should only include confirmed founders (not employees, advisors, or investors).

---

## Profile Discovery Flow

When building a company profile from scratch:

```
1. Start with company name and/or domain from user input
2. Run Tavily search: "[name] official website twitter github linkedin producthunt yc"
3. Parse search results for social handles and URLs
4. Visit the company website (if found) for description and positioning
5. Search YC: "site:ycombinator.com/companies [name]" for YC batch info
6. Search founders: "[name] founder ceo twitter" for each likely founder
7. Fill profile fields from discovered data
8. Compute profile_completeness
```

---

## Profile Examples

### High-Completeness Profile

```yaml
company:
  name: Vercel
  domain: vercel.com
  description: "Vercel is the platform for frontend developers, providing the speed and reliability innovators need to create at the moment of inspiration."
  logo_url: "https://vercel.com/api/logo"

  twitter_handle: "vercel"
  github_org: "vercel"
  linkedin_url: "https://linkedin.com/company/vercel"
  youtube_channel: "vercel"
  reddit_community: null
  blog_url: "https://vercel.com/blog"
  docs_url: "https://vercel.com/docs"
  careers_url: "https://vercel.com/careers"

  yc_batch: null
  yc_url: null

  producthunt_slug: "vercel"
  producthunt_url: "https://www.producthunt.com/@vercel"

  founders:
    - name: "Guillermo Rauch"
      title: "CEO"
      twitter_handle: "rauchg"
    - name: "Tim Neutkens"
      title: "CTO"
      twitter_handle: "timneutkens"

  is_open_source: true
  is_yc_company: false
  profile_completeness: 95
  source_urls:
    - "https://vercel.com"
    - "https://github.com/vercel"
    - "https://twitter.com/vercel"
```

### Low-Completeness Profile

```yaml
company:
  name: "ACME Software"
  domain: "acmesoftware.io"
  description: null  # not found in search
  logo_url: null

  twitter_handle: "acmesoftware"
  github_org: null
  linkedin_url: null
  youtube_channel: null
  reddit_community: null
  blog_url: null
  docs_url: null
  careers_url: null

  yc_batch: null
  yc_url: null

  producthunt_slug: null
  producthunt_url: null

  founders: []

  is_open_source: false
  is_yc_company: false
  profile_completeness: 15
  source_urls:
    - "https://acmesoftware.io"
    - "https://twitter.com/acmesoftware"
```
