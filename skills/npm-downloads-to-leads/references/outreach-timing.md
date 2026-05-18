# Outreach Timing Reference

Used by SKILL.md Step 6 to guide AI generation of lead briefs and outreach messages. The right timing and angle depends on where the maintainer is in their growth arc.

---

## Why Timing Is Everything

A developer who just crossed 1,000 weekly downloads on their package is experiencing something new: real, sustained organic adoption. They are probably:
- Watching the download counter more closely than usual
- Starting to get GitHub issues from people they have never met
- Wondering if they should write docs or a blog post
- Not yet thinking about monetization, partnerships, or DevRel relationships

This is the window. A relevant, specific message from a company that actually understands what they built lands completely differently than it would 6 months later when they have speaking requests, Twitter DMs from recruiters, and three other companies already in their inbox.

---

## Outreach by Growth Stage

### Stage 1: First Traction (500 to 3,000/week)

The maintainer is in "is this real?" territory. Downloads are clearly growing but they may still be wondering if it is a fluke.

**What works:**
- Acknowledge the specific thing they built, not just "your project"
- Ask for feedback or perspective -- they are not famous enough yet to expect sponsorships or partnerships
- Peer-to-peer framing: "We're building X and we noticed your package solves Y for the same developers"
- Low-commitment ask: feedback, a question, or just an introduction

**What does not work:**
- "We'd love to partner with you" (too big for where they are)
- "We noticed your package is growing fast" without specifics (sounds like a bot)
- Pitching them immediately before establishing relevance

**Template:**
```
Subject: [package-name] -- quick question from a builder in your space

We use [package-name] for [specific use case] and noticed it's been growing fast.
We build [brief description] for the same developers.
[Specific observation about their package or a genuine question about their design decision]
No ask yet -- just wanted to say it's a well-built tool.
[Name]
```

---

### Stage 2: Clear Breakout (3,000 to 20,000/week)

The maintainer now knows the growth is real. They are getting more issues, maybe some contributions, possibly a few people asking about commercial support.

**What works:**
- Naming the inflection: "You've gone from X to Y downloads in 8 weeks -- that puts you in rare company"
- Connecting their growth to a specific audience you both serve
- A concrete proposal: integration, co-marketing, or early access to something relevant to their users
- Flattery that is specific: quote something from their README or a design decision that shows you read it

**What does not work:**
- Vague partnership offers without a specific benefit
- Asking them to promote your product in their README cold
- Not mentioning their package by name

**Template:**
```
Subject: [package-name] -- [specific angle in 6 words]

[Package-name] went from [X] to [Y] downloads over the last 8 weeks.
We build [product] for [same developer segment] and have been using it for [specific use case].
[One sentence connecting their package's growth to why you're reaching out now]
[Specific ask: integration conversation, early access, 20-minute call, or feedback request]
[Name]
```

---

### Stage 3: Established Breakout (20,000 to 100,000/week)

The maintainer is now a recognized figure in their sub-community. They have probably been featured somewhere, have hundreds of GitHub stars, and are starting to think about sustainability.

**What works:**
- Direct business value: sponsorship, paid integration, commercial use case
- "We have [N] customers using your package" -- this legitimizes you and signals commercial interest
- Conference, podcast, or content collaboration (they are now building a reputation)
- Concrete numbers: "We could get you in front of 5,000 of your target users"

**What does not work:**
- Pure outreach without a business angle (they are getting enough of that)
- Asking for free consulting or feedback without offering something in return
- Generic partnership language

**Template:**
```
Subject: [package-name] -- [N] of our customers use it

We have [N] teams using [package-name] through [your product].
We build [product] for [developer segment] and your package is a core dependency for [specific workflow].
[Specific proposal: integration, sponsorship, co-marketing, conference slot, or collaboration]
[One-line ask: call, intro, or yes/no question]
[Name]
```

---

## The Verbatim Quote Technique

The single highest-signal move in any outreach message is quoting something specific from their project -- README language, a design decision they wrote about, a specific feature name.

**Without quote:**
> "We noticed you built a validation library and we think there's a fit."

**With quote:**
> "Your README says 'Zod's goal is to eliminate duplicative type declarations' -- that's exactly the problem our users have when they adopt TypeScript on a legacy codebase. We built something adjacent for the API layer."

The quote proves you read it. It also filters you out of the 95% of outreach that clearly does not. A developer who has been sending bug fixes to a project at midnight will respond to someone who clearly understood what they were building.

---

## Finding the Right Angle Based on Package Category

Use the keywords and description from the npm registry to match the outreach angle to the package type.

| Package Category | Best Angle |
|---|---|
| Build tools / bundlers | Performance, DX, CI integration time, large codebase support |
| Validation / schema | Type safety, form handling, API contract enforcement |
| HTTP / API clients | Multi-environment support, retry logic, error handling |
| Testing utilities | Coverage, speed, snapshot behavior |
| State management | Scale, debugging, SSR support |
| CLI tools | Scripting workflows, automation, team adoption |
| Database / ORM | Migration pain, type inference, query complexity |
| Auth / security | Compliance, session management, multi-provider support |

The suggested first message should reference the specific category and connect it to what the person reaching out actually builds.

---

## What to Never Write

Regardless of growth stage or package category, these phrases signal a template and get ignored:

- "I came across your project" -- too generic
- "I'm a huge fan of your work" -- unverifiable and sounds like a bot
- "We'd love to explore synergies" -- says nothing
- "Your package is powerful" -- the word "powerful" is on every cold email
- "I know you're busy" -- everyone is busy; mentioning it wastes a line
- "Just wanted to reach out" -- there is always a reason; state it
- "Feel free to ignore this" -- they will
- Any subject line over 8 words

The outreach hook that works is: specific thing they built + specific reason you noticed it now (the growth inflection) + specific reason you are the right person to reach out. Three sentences. Under 100 words total.

---

## Following Up

If there is no response after 7 days, one follow-up is acceptable. The follow-up should not repeat the pitch -- it should add new information:

- A new data point: "Your downloads crossed [milestone] since I last wrote"
- A new connection: "I saw you mentioned [topic] in [place] -- that's exactly what we're solving"
- A direct question instead of a pitch: "Are you thinking about [specific pain point] yet?"

Two messages with no response means the timing is wrong. Do not send a third. Revisit in 90 days if the package keeps growing.
