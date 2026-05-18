# Pricing Models

## The Six Models

### Per-Seat / Per-User
Price scales with the number of users on the account.

**How to identify from a pricing page:**
- "per user/month", "per seat/month", "per member"
- Tier descriptions include a user count or say "unlimited users" as a feature
- Price shown as "$X per user" or "$X × [N] users"

**Common in:** Project management (Jira, Linear, Asana), CRM (Salesforce, HubSpot), collaboration tools (Notion, Confluence), communication tools (Slack, Zoom)

**Why spaces adopt it:** Revenue scales naturally with team size. Easy to understand. Aligns cost with value (bigger team = more value extracted).

**Risk for new entrants:** Per-seat pricing raises the cost of adoption at the team level. Enterprises resist it because seats are hard to forecast. Often results in "seat-sharing" workarounds.

---

### Flat-Rate
One fixed price for all users, regardless of team size.

**How to identify:**
- Single price shown prominently, no mention of per-user scaling
- "Unlimited users" or "your whole team" as a feature, not a tier limit
- Simple 1-2 plan structure

**Common in:** Single-operator tools, small business software, simple utilities

**Why spaces adopt it:** Removes friction for SMB buyers who hate per-seat math. Good for tools where most value comes from the tool itself, not from network effects within a team.

**Risk:** Revenue doesn't scale with usage or team size. Hard to grow ARPU without tier upgrades.

---

### Usage-Based / Consumption
Price scales with how much the product is used (API calls, messages, rows, compute minutes, etc.).

**How to identify:**
- Pricing page shows units: "per 1,000 API calls", "per GB", "per message sent", "per transaction"
- Overage fees listed
- "Pay as you go" or "credits" system
- Calculator on the pricing page

**Common in:** APIs (Stripe, Twilio, OpenAI), data tools (Snowflake, BigQuery), infrastructure (AWS, Vercel), AI/ML tools

**Why spaces adopt it:** Revenue scales with customer success. Low barrier to entry (start free, pay as you grow). Natural fit when value is directly proportional to consumption.

**Risk:** Hard to forecast revenue. Customers may optimize usage aggressively to cut costs. Requires strong unit economics.

---

### Freemium
Permanent free tier with paid upgrades for more features, users, or limits.

**How to identify:**
- "Free forever" plan (not a trial -- permanent)
- Feature gating: key features locked behind paid tiers
- Clear upgrade prompts within the product
- "Upgrade to unlock" language

**Common in:** PLG (product-led growth) companies, developer tools, consumer apps, productivity tools

**Why spaces adopt it:** Drives viral adoption and self-serve discovery. Users qualify themselves -- heavy free users convert to paid. Removes sales friction.

**Risk:** Free tier creates support costs without revenue. Can anchor willingness-to-pay too low. Hard to convert free users if free tier is too generous.

---

### Tiered Flat (Most Common SaaS Pattern)
Fixed tiers (Starter / Pro / Business / Enterprise) with a flat price per tier. Upgrading a tier unlocks more features or higher limits -- not more users.

**How to identify:**
- 3-4 named tiers (Starter, Pro, Business, Enterprise)
- Each tier has a fixed monthly price
- Feature comparison table showing what's included at each tier
- No per-user multiplier within a tier (or per-user pricing is one of several factors)

**Common in:** Most B2B SaaS: email tools, analytics, HR software, marketing platforms

**Why spaces adopt it:** Predictable revenue. Easy to understand. Allows packaging features strategically to drive upgrades.

**Risk:** Customers may downgrade to cheaper tier when budget is tight. Feature selection per tier requires deep knowledge of what customers value.

---

### Hybrid
Combination of two or more models -- most commonly per-seat within tiers, or usage caps within flat tiers.

**How to identify:**
- Tiers have both a flat base price AND per-user scaling: "$50/mo base + $10/user"
- Or: tiers have a flat price but also include usage caps (e.g., "up to 10,000 API calls/mo included")
- Or: flat tiers + usage-based overages

**Common in:** CRM, marketing automation, enterprise platforms

**Why spaces adopt it:** Captures revenue from both team growth and product usage. More complex but reflects true value delivery.

**Risk:** Customer confusion. Hard to predict billing. Often requires a calculator on the pricing page.

---

## Quick Reference Table

| Model | Scales with | Entry barrier | Revenue predictability | Best for |
|---|---|---|---|---|
| Per-seat | Team size | Medium | High | Collaboration, CRM |
| Flat-rate | Nothing | Low | High | SMB, single-operator tools |
| Usage-based | Consumption | Very low | Low | APIs, infrastructure |
| Freemium | Feature needs | None | Medium | PLG, developer tools |
| Tiered flat | Feature needs | Low | High | Most B2B SaaS |
| Hybrid | Multiple factors | Medium | Medium | Enterprise platforms |
