# GTM Translation Reference

How to convert demand clusters from competitor GitHub issues into GTM language. Used by SKILL.md Step 6 to guide the messaging brief generation.

---

## The Translation Problem

Raw demand data from GitHub is in user language, not buyer language. A product manager reads:

> "Add support for multiple workspaces per account" -- 87 reactions, open 2 years

A GTM-trained analyst reads:

> "Enterprise buyers need multi-tenancy. This competitor has not shipped it in 2 years. 87 teams are waiting. If you have this, lead with it."

This reference document is the bridge between those two readings.

---

## Translation by Category

### feature_gap clusters

**What the data shows:** Users want something that does not exist.

**GTM translation:**
- If you have the feature: "We built what [competitor] has not." Name the feature specifically.
- If you are building it: Use the cluster as proof that the market exists. "87 teams on [competitor] asked for X. We built it."
- If you do not have it: This is a roadmap signal, not a positioning signal yet.

**Outreach hook pattern:**
```
"[Number] teams on [competitor] have been asking for [specific feature] for [time].
We shipped [your feature] in [your product] [time ago / as a core feature].
[One-line ask]."
```

**Example:**
```
"Over 200 teams on [competitor] asked for multi-workspace support. It has been open for 3 years with no planned label.
We built workspace isolation as a core feature, not an add-on.
Would a 20-minute call be useful?"
```

---

### bug_pattern clusters

**What the data shows:** Something is reliably broken. High reaction counts on bug issues mean many users hit the same wall.

**GTM translation:**
- Do not say "they are buggy." Say: "Teams in [X workflow] need reliability."
- Position the broken area as a category where you have invested specifically.
- The number of reactions is the credibility anchor. Use it.

**Outreach hook pattern:**
```
"[Number] teams using [competitor] hit [specific bug area].
[Your product] was built [for/around/specifically to handle] this workflow without [the failure mode].
[One-line ask]."
```

**Example:**
```
"Teams using [competitor] have hit login failures with SSO -- 43 reactions on that issue, open for 18 months.
We built our auth layer around SSO-first design and have not had an SSO outage in 18 months of production.
Worth a conversation?"
```

---

### ux_complaint clusters

**What the data shows:** The feature exists but users cannot use it without friction.

**GTM translation:**
- Simplicity is a product decision, not a feature. Position it as intentional design.
- Use "setup time" or "time to value" as the measurable proxy for simplicity.
- Do not say "our UI is better." Say: "Teams get to [outcome] in [time], without [the friction they described]."

**Outreach hook pattern:**
```
"[Number] users of [competitor] said [specific UX friction in quotes].
[Your product] gets [persona] to [outcome] in [time] with [fewer steps / no setup / no configuration].
[One-line ask]."
```

**Example:**
```
"158 users of [competitor] called the project navigation 'confusing' -- that issue is 2 years old.
We redesigned navigation around the workflow, not the feature tree. Teams reach their first result in under 2 minutes.
Would you like to see it?"
```

---

### performance clusters

**What the data shows:** The product hits a scale ceiling. High-reaction performance issues cluster around a specific bottleneck (large files, large teams, high query volume).

**GTM translation:**
- Name the scale ceiling specifically: "repos over 1000 files", "teams over 50 users", "queries over 10k/day".
- If you have benchmarks, use them. If not, use the absence of the complaint as proof.
- Performance positioning works best for technical buyers (engineers, infrastructure teams).

**Outreach hook pattern:**
```
"Teams at [competitor] hit [specific bottleneck] at [scale threshold].
[Your product] handles [scale threshold] in [benchmark or time].
[One-line ask]."
```

**Example:**
```
"Engineering teams using [competitor] report 10+ second load times on repos over 500 files -- 67 reactions, no fix in sight.
We load repos of that size in under 1.5 seconds because we index differently.
I can show you a benchmark on a repo your size."
```

---

### integration_missing clusters

**What the data shows:** Users work in tools this competitor does not connect to. High-reaction integration requests tell you exactly what else is in their users' daily stack.

**GTM translation:**
- If you have the integration: make it the lead, not a footnote.
- The reaction count is the size of the audience that wants this bridge. Name the number.
- Integration positioning works best when the target tool is a category leader (Slack, Notion, GitHub Actions, Salesforce).

**Outreach hook pattern:**
```
"[Number] teams on [competitor] asked for [specific integration]. It has been open [time] with no planned label.
[Your product] connects to [integration] natively -- [brief description of how it works].
[One-line ask]."
```

**Example:**
```
"94 teams on [competitor] asked for Slack integration. The request is 3 years old with no planned label.
We shipped bidirectional Slack sync 6 months ago -- alerts in Slack, actions back to [your product].
Worth showing you?"
```

---

### docs_missing clusters

**What the data shows:** Users cannot figure out how to do something. The product may work, but the path to value is opaque.

**GTM translation:**
- Documentation is a trust signal, not a feature. "We have clear docs" is not a hook.
- Translate to: "Teams are in production in [time]" or "We have a guided setup for [exact use case they documented badly]."
- Onboarding speed is the business outcome. Use it.

**Outreach hook pattern:**
```
"[Number] users on [competitor] asked for documentation on [specific topic].
We have [specific guide / template / interactive tutorial] for [exact use case].
Teams using our [guide/setup] are in production in [time].
[One-line ask]."
```

**Example:**
```
"38 teams on [competitor] asked for documentation on webhook authentication. There is still no official guide.
We have a step-by-step webhook setup guide that gets teams from zero to first event in under 15 minutes.
I can send it -- it works for any webhook destination, not just ours."
```

---

## Using Verbatim Issue Language

The most effective outreach hooks use the user's exact words from the issue title. This works because:

1. It proves you read real feedback, not marketing copy.
2. It speaks in the buyer's language, not product language.
3. It names the pain before pitching the solution.

**Wrong approach (paraphrased):**
> "Many teams find navigation confusing in competitor products."

**Right approach (verbatim quote):**
> "158 users said 'confusing navigation between projects' has been open for 2 years. We redesigned for workflow, not feature hierarchy."

The quote is the credibility anchor. Do not remove it.

---

## Ignored Demand: The Highest-Signal Category

An issue that meets all three criteria:
- 10+ reactions (significant real demand)
- Open 180+ days (competitor has had time to act)
- No planned/in-progress label (they have explicitly not prioritized it)

This is not a feature request. This is a documented unmet need with a timestamp.

**GTM translation:** "Their users asked. Their team did not respond. We built it."

This framing works across all 6 categories. The combination of volume + age + inaction is the signal. The category determines the messaging angle.

**Ignored demand outreach template:**
```
"[Competitor]'s users have been asking for [verbatim issue title] for [age].
[Reaction count] teams upvoted it. There is no planned label.
[Your product] handles this [natively / differently / as a core feature].
[One-line ask]."
```
