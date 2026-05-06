# GTM Model Fit Profiler — Default Workload Prompts

When the user does not provide `source_material`, use these default benchmark prompts to evaluate model performance against each workload.

---

## Market Research Prompts

### MR-1: Pain point extraction

```
Here are 5 customer support tickets from a B2B project management tool:

1. "We keep losing track of who approved what. Our compliance team is breathing down our necks because there's no audit trail for task reassignments."
2. "The timeline view is useless for programs with 50+ workstreams. It just becomes a wall of bars. We had to buy a separate tool just for executive reporting."
3. "Integration with Jira keeps breaking after every update. Our engineering team has stopped trusting the sync and maintains a separate board."
4. "We need different permission levels per workspace but your tool forces one global admin role. This is a dealbreaker for our enterprise security review."
5. "Onboarding new PMs takes forever because there's no template library. Every new project starts from scratch."

Task: Extract the top pain points, group them by theme, and rank by frequency and severity.
```

### MR-2: Signal clustering

```
Here are 8 Reddit posts from r/devops about CI/CD frustrations:

1. "Spent 3 days debugging a flaky test in our GitHub Actions pipeline. Turns out the runner was running out of memory."
2. "Our Jenkins setup is a nightmare to maintain. 47 plugins, half of them abandoned."
3. "Anyone else struggling with monorepo build times? 45 minutes for a single PR check."
4. "We moved to GitLab CI and the YAML configs are out of control. 2000+ lines across 12 files."
5. "Self-hosted runners keep dying on weekends. No one notices until Monday standup."
6. "Docker layer caching in CI is unreliable. We rebuild from scratch 60% of the time."
7. "Test parallelization sounds great until you realize half your tests have hidden dependencies."
8. "Our deploy pipeline has 23 manual approval gates. Shipping a hotfix takes 4 hours."

Task: Cluster these signals into GTM-relevant themes and identify which buyer persona each theme maps to.
```

### MR-3: ICP pattern identification

```
Here are 6 companies that recently churned from a developer productivity platform:

1. FinServ Corp (500 eng, Series D) — cited "doesn't scale past 200 concurrent users"
2. HealthTech AI (80 eng, Series B) — cited "missing SOC2 compliance features"
3. RetailStack (300 eng, public) — cited "no on-premise deployment option"
4. CryptoLedger (40 eng, Series A) — cited "too expensive for our stage"
5. GovCloud Systems (1200 eng, government) — cited "FedRAMP certification missing"
6. DataMesh Inc (150 eng, Series C) — cited "API rate limits too restrictive for our data pipeline"

Task: Identify ICP patterns among churned accounts. Which segments should the company deprioritize?
```

### MR-4: Strategic synthesis

```
A B2B email deliverability platform notices:
- 40% of new signups in Q4 came from e-commerce companies (up from 15% in Q2)
- Enterprise deals (>$50K ACV) have a 6-month sales cycle but 95% retention
- SMB accounts (<$5K ACV) have a 2-week sales cycle but 40% churn within 90 days
- Competitor X just raised $80M and is offering free tiers
- 3 of the last 5 lost deals cited "no Shopify integration" as the reason

Task: Summarize the strategic implications. What should the company prioritize and why?
```

---

## Pricing / Competitor Analysis Prompts

### PA-1: Pricing page comparison

```
Compare these two SaaS pricing pages:

Tool A — "CloudMetrics"
- Free: 3 dashboards, 1 user, 7-day retention
- Pro ($29/user/mo): 25 dashboards, 5 users, 30-day retention, Slack alerts
- Business ($79/user/mo): Unlimited dashboards, unlimited users, 1-year retention, SSO, API access
- Enterprise: Custom pricing, dedicated support, SLA, custom retention

Tool B — "InsightHub"
- Starter ($0): 5 dashboards, 3 users, 14-day retention, community support
- Growth ($49/mo flat): 50 dashboards, 10 users, 90-day retention, email support
- Scale ($199/mo flat): Unlimited everything, 2-year retention, priority support, SSO

Task: Compare the pricing structures. What strategy is each tool using?
```

### PA-2: Packaging strategy inference

```
A developer tools company currently prices at:
- Hobby: Free, 1 project, shared compute
- Pro: $20/dev/mo, 5 projects, dedicated compute, team features
- Enterprise: Custom, unlimited everything, SOC2 report, SSO, SLA

They are considering adding a "Team" tier at $49/dev/mo between Pro and Enterprise.
60% of Pro users are on teams of 3-8 developers. Enterprise deals take 4-6 months to close.

Task: Analyze the proposed tier. What problems does it solve? What risks does it create?
```

### PA-3: Competitive response strategy

```
Your company sells a data pipeline tool at $500/mo. Your main competitor just:
1. Cut their price from $600/mo to $299/mo
2. Launched a free tier with 100K events/month
3. Added a startup program offering 1 year free for YC companies
4. Published a migration guide targeting your users

You have 85% gross margins, NPS 62 (competitor: 34), 3x more integrations.

Task: Recommend a response strategy with trade-offs.
```

---

## Outreach Personalization Prompts

### OP-1: Cold email from buying signal

```
Your product: API monitoring tool for engineering teams
Target: StreamData (Series B, 120 engineers, real-time data infrastructure)
Signal: Job post for "Senior SRE" requiring "API observability tools, distributed tracing"
Persona: VP of Engineering

Task: Write a short cold email (under 100 words) using this buying signal with a low-friction CTA.
```

### OP-2: Account-based opener

```
Your product: Sales enablement platform
Target: GrowthForce (Series C, 200 employees, HR software for SMBs)
Intel: Head of Sales promoted to CRO, SDR team grew from 8 to 20, 3 new AE roles posted
Persona: Newly promoted CRO

Task: Write a LinkedIn message opener (under 75 words) referencing their growth signals.
```

### OP-3: Signal-to-outreach conversion

```
Your product: Compliance automation for fintech
Signal: Reddit post — "We just got hit with our first SOC2 audit request from an enterprise prospect. We have zero compliance infrastructure."
Persona: Head of Engineering or CEO

Task: Draft a cold email (under 120 words) that turns this signal into helpful, non-pushy outreach.
```

### OP-4: Multi-signal outreach

```
Your product: Developer documentation platform
Target: CodeShip (Series B, 80 engineers, developer tools)
Signals: Docs site 2.1-star G2 rating, just hired Developer Experience Lead, 45 open GitHub issues tagged "documentation"
Persona: Developer Experience Lead

Task: Write a cold email (under 100 words) weaving multiple signals without overwhelming the reader.
```
