# PR Channel Types

## The Three Tracks

### Track A: Editorial / News
A journalist or staff writer published a piece about the company. The piece has a byline and appeared on a publication's website.

**How to identify from a Tavily result:**
- URL contains a known publication domain: `techcrunch.com`, `forbes.com`, `wired.com`, `theverge.com`, `venturebeat.com`, `infoq.com`, `thenewstack.io`, `businessinsider.com`, `fastcompany.com`, `inc.com`
- Title format: "Company X Raises $Y", "How Company X is Changing Z", "Company X Launches...", "[Name] Profile: ..."
- Content includes phrases like "reported", "according to", "the company said", "in an interview"

**Why it matters for outreach:**
Editorial coverage is the hardest to get but the most credible. Journalists have a beat -- they cover a specific domain -- so a pitch that fits their beat history gets read. The goal is not to pitch the publication; it's to pitch the specific journalist who already covers your category.

**Approach method:** Cold email with a subject line tailored to their beat. Keep it under 150 words. Reference a specific piece they wrote.

---

### Track B: Podcasts
A founder or executive appeared as a guest on a podcast episode to discuss their product, vision, or category.

**How to identify from a Tavily result:**
- URL contains: `podcasts.apple.com`, `open.spotify.com/episode`, `overcast.fm`, `pca.st`, `pod.link`, `buzzsprout.com`, `anchor.fm`, `transistor.fm`
- Title format: "Ep 123: [Name] on building X", "[Name] interviews founder of Y", "How [Company] bootstrapped to $1M ARR"
- A specific podcast name appears consistently: "Indie Hackers", "How I Built This", "The SaaS Podcast", "My First Million", "Acquired", "Lenny's Podcast"
- Content describes a long-form conversation, not a news article

**Why it matters for outreach:**
Podcast hosts are warmer than journalists -- they talk to founders for 30-60 minutes per episode and often have a loyal audience in a specific niche. A show that has featured 3 of your competitors has already built audience trust in your category. The pitch is shorter and more conversational than an editorial pitch.

**Approach method:** Short, casual pitch. Reference a specific episode they did in your space. Propose a concrete angle or talking point, not just "interview me about my startup."

---

### Track C: Communities
The company was discussed, featured, or launched on a community platform -- discussion threads, upvotes, launch pages.

**How to identify from a Tavily result:**
- URL domain: `reddit.com/r/`, `news.ycombinator.com`, `producthunt.com`, `indiehackers.com`, `dev.to`, `hashnode.com`, `discord.gg` (less common in search results)
- HN titles: "Show HN: [Company]" or "Ask HN: ..." with Company mentioned
- Reddit titles: discuss, review, recommendation thread mentioning competitor
- ProductHunt: `/posts/[company-name]` URL, "The best tool for X"

**Why it matters for outreach:**
Communities are earned, not pitched. You cannot pay or email your way in -- but you can post authentically. Subreddits and HN threads about your category are places where the audience already congregates. A ProductHunt launch in the right community can drive more trial signups than a Forbes article.

**Approach method:** Not an email pitch. Launch on ProductHunt. Post genuinely on relevant subreddits (follow community rules, no spam). For HN: "Show HN" post when you have something real to show.

---

## Normalizing URLs to Domains

When building the channel frequency map (Step 7), normalize all result URLs to their root domain so variants of the same publication are grouped:

| Raw URL | Root domain |
|---|---|
| `techcrunch.com/2024/01/company-raises-x` | `techcrunch.com` |
| `www.techcrunch.com/startups/...` | `techcrunch.com` |
| `open.spotify.com/episode/abc123` | `spotify.com (podcast)` |
| `podcasts.apple.com/us/podcast/...` | `apple podcasts` |
| `news.ycombinator.com/item?id=123` | `news.ycombinator.com` |
| `reddit.com/r/devops/comments/...` | `reddit.com/r/devops` |
| `producthunt.com/posts/company-name` | `producthunt.com` |

Reddit: preserve the subreddit level (`reddit.com/r/devops` not just `reddit.com`) because different subreddits serve different audiences.

Podcasts hosted on Spotify or Apple: use the show name, not the platform domain, as the channel identifier. The platform is just the delivery mechanism.

---

## Channel Type to Approach Method

| Channel Type | Approach Method | Notes |
|---|---|---|
| Editorial | Cold email to journalist | Find journalist name via Step 8 lookup |
| Podcast | Pitch email to host or show booking email | Often listed on show website |
| Community (ProductHunt) | Launch on ProductHunt | Schedule for Tuesday AM PT |
| Community (Reddit) | Authentic post or comment in thread | No overt pitching; add value |
| Community (HN) | Show HN post | Must have working product |
| Newsletter | Reply to the author's last issue | Most newsletters have personal reply addresses |
