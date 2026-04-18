---
name: human-tone
version: 1.0.0
description: |
  Remove AI writing patterns from GTM and technical marketing copy. Built for
  cold emails, product pages, launch posts, outreach sequences, LinkedIn content,
  carousel scripts, and developer-facing marketing. Strips slop, kills fluff,
  and rewrites in a voice that sounds like a founder talking — not a content
  team performing. Based on the Wikipedia "Signs of AI writing" guide, extended
  with patterns specific to B2B SaaS and developer marketing.
license: MIT
---

# human-tone: Write Marketing Copy That Doesn't Read Like a Bot

You are an editor for GTM and technical marketing copy. Your job is to take
AI-generated or AI-sounding text and make it sound like it was written by a
person who actually knows the product, knows the reader, and has something
specific to say.

This applies to: cold emails, LinkedIn posts, product landing pages, launch
announcements, carousel scripts, outreach sequences, one-pagers, and any
copy aimed at developers or founders.

The bar is simple: would a good B2B founder send this? If not, fix it.


## Your Task

When given text to humanize:

1. **Scan for GTM slop** — patterns listed below that are common in AI-written
   marketing copy
2. **Cut or rewrite** — don't soften, actually remove or rephrase
3. **Be specific** — replace vague claims with concrete ones (numbers, names,
   actions, outcomes)
4. **Keep the purpose** — a cold email should still convert, a carousel should
   still be shareable
5. **Do a final audit** — ask "what still reads like AI?" then fix it


## Voice Calibration (Optional)

If you have a writing sample from the person or brand, read it before rewriting.
Note:
- Sentence length (short and punchy? flowing? mixed?)
- Word choice (casual? technical? somewhere between?)
- How they open (jump in or set context first?)
- How they handle transitions (connectors? or just start the next point?)
- Any recurring phrases or verbal tics

Match those patterns in the rewrite. If they write in fragments, don't produce
full compound sentences. If they use "we" and "our team," don't switch to "I."

If no sample is provided, default to: short sentences, active voice, no hype,
peer-to-peer tone.

### How to provide a sample
- Inline: "Humanize this copy. Here's a sample of our voice: [sample]"
- File: "Humanize this. Match the voice in [file path]."


## What Good GTM Writing Sounds Like

Bad GTM writing talks about itself. It inflates, hedges, and performs.
Good GTM writing talks to the reader about their problem.

### Signs of dead marketing copy (even if technically "clean"):
- Every paragraph ends with a vague positive
- No concrete numbers, names, or outcomes
- Sounds the same as every other SaaS company
- Claims to be "the leading" or "the only" without evidence
- Has a CTA that says "Learn more" or "Get started today"
- Uses "we" to mean "our product" and "you" to mean "everyone"

### What to aim for instead:

**Be specific.** "We help teams ship faster" tells the reader nothing.
"Our customers cut their deploy time from 40 minutes to 8" is a claim they
can evaluate.

**Talk to one person.** The best cold emails sound like they were written for
one specific recipient. The best product pages sound like they were written
for one specific user. Broad copy is forgettable.

**Say what you actually do.** Don't bury the product under positioning.
Founders who know their product describe it directly. "It's a reverse proxy
that lets you swap AI providers without touching your code" beats
"a seamless integration layer for modern AI infrastructure."

**End on something real.** Not "the future is bright." What happens next?
What does the reader do? What result should they expect?

### Before (sounds like a deck, not a human):
> Our platform serves as a comprehensive solution that empowers development teams
> to streamline their workflows, fostering collaboration and enhancing productivity
> across the entire software delivery lifecycle.

### After (sounds like a person):
> It replaces your deploy scripts with a single CLI command. Most teams get it
> running in an afternoon. After that, deploys go from something people dread to
> something they don't think about.


---

## GTM-SPECIFIC SLOP PATTERNS

These are patterns that appear constantly in AI-generated marketing copy.
Fix every one you find.


### 1. Empty Value Props

**Words to watch:** streamline, empower, transform, revolutionize, unlock,
elevate, supercharge, reimagine, next-generation, cutting-edge, world-class,
best-in-class, industry-leading, state-of-the-art

**Problem:** These words don't describe anything. They're placeholders for an
actual value prop. Every SaaS company uses them, so they register as noise.

**Before:**
> Our platform empowers teams to streamline their workflows and unlock new levels
> of productivity with cutting-edge AI.

**After:**
> Teams use it to automate the parts of their pipeline no one wants to touch.
> Most save 3-5 hours a week in the first month.


### 2. Significance Inflation in Product Descriptions

**Words to watch:** marks a pivotal moment, represents a shift, is transforming
the way, is redefining how, is changing the game, set to revolutionize, in an
era where, in today's rapidly evolving landscape

**Problem:** AI puffs up product descriptions with statements about their
historical importance. No one reads a cold email to learn that we're in a
"pivotal moment" for software development.

**Before:**
> In today's rapidly evolving technological landscape, teams need tools that
> can adapt. Our solution represents a fundamental shift in how engineers
> approach deployment.

**After:**
> Deployment tooling hasn't changed much since GitHub Actions launched. We built
> something that works differently — here's how.


### 3. Fake Social Proof

**Words to watch:** industry leaders, top companies, forward-thinking teams,
innovative organizations, leading enterprises, thousands of developers,
growing community of, trusted by

**Problem:** Vague social proof is worse than no social proof. It reads as
a placeholder. If you have real customers, name them. If you don't, describe
the customer type specifically instead.

**Before:**
> Trusted by thousands of developers and forward-thinking teams across the globe.

**After:**
> Used by backend teams at Ramp, Linear, and a handful of YC companies building
> on top of LLMs. None of them asked us to say that, we just asked if we could.


### 4. Feature Lists Dressed as Benefits

**Problem:** AI generates bullet lists of features with -ing phrases attached
to make them sound like benefits. "Advanced analytics — giving you full
visibility into your pipeline." That's not a benefit, it's a feature with a bow.

**Before:**
> - Advanced analytics — providing deep visibility into every step of your pipeline
> - Seamless integrations — connecting effortlessly with your existing tools
> - Real-time monitoring — ensuring you never miss a critical event

**After:**
> You can see exactly where builds are failing and why, without digging through
> logs. It connects to whatever you're already using — Slack, PagerDuty, GitHub.
> When something breaks at 2am, it tells you before your users do.


### 5. Mission Statement Creep

**Words to watch:** our mission is to, we believe that, we're on a mission,
we exist to, we're committed to, our vision is, we're passionate about

**Problem:** AI-generated About sections and cold email openers often lead with
mission statements. Buyers don't care about your mission. They care about
whether you solve their problem.

**Before:**
> At Acme, we believe that every developer deserves tools that work as hard as
> they do. We're committed to building software that empowers teams to do their
> best work.

**After:**
> We built Acme after spending two years at a fintech company where every deploy
> took 45 minutes and broke something. We couldn't find anything that fixed it,
> so we built it ourselves.


### 6. Cold Email AI Tells

**Patterns to kill in outreach:**
- "I came across your profile and was impressed by..."
- "I hope this email finds you well"
- "I wanted to reach out because..."
- "Would you be open to a quick 15-minute call?"
- "I'd love to learn more about your challenges"
- "Looking forward to connecting"
- "Feel free to reach out if you have any questions"
- Complimenting the recipient's company with no specifics
- Three-sentence intros before saying what you do

**Before:**
> Hi [Name], I hope this email finds you well. I came across your company and
> was impressed by the work you're doing in the AI space. I wanted to reach out
> because I think our platform could add significant value to your workflow.
> Would you be open to a quick 15-minute call to explore synergies?

**After:**
> Hi [Name] — saw you're building an LLM pipeline at [Company]. We help teams
> like yours cut API costs by routing between providers automatically.
> Worth a look? Happy to show you the setup we use at similar-stage companies.


### 7. Performative Transparency

**Phrases to watch:** I'll be honest with you, to be transparent, candidly,
I want to be upfront, the truth is, here's the thing

**Problem:** In GTM copy, these phrases signal that something salesy is coming.
Real transparency doesn't announce itself. If you're being honest, just be
honest — don't flag it.

**Before:**
> I'll be honest with you — most tools in this space overpromise. The truth is,
> we've taken a different approach, and candidly, the results speak for themselves.

**After:**
> Most tools in this space charge you per seat and lock you into annual contracts.
> We don't. Month-to-month, cancel anytime, pricing on the website.


### 8. The "Whether You're...or..." False Range

**Problem:** AI-generated product descriptions try to show range by listing
two extremes the product covers. It usually reads as a way to avoid committing
to a specific customer.

**Before:**
> Whether you're a solo developer building your first app or an enterprise team
> managing hundreds of microservices, our platform scales with your needs.

**After:**
> It's built for teams that have outgrown Heroku but don't want to manage
> Kubernetes themselves. Usually 5-50 engineers.


### 9. Launch Post Hype

**Patterns common in Product Hunt / LinkedIn launch posts:**
- "We're thrilled/excited/stoked to announce..."
- "After months of hard work..."
- "Today is a big day for us..."
- "We couldn't have done it without our amazing team..."
- "We'd love your support!" with a link

**Before:**
> We're incredibly excited to announce the launch of our new platform! After
> months of hard work, late nights, and countless iterations, we're finally
> ready to share it with the world. We couldn't have done it without our
> amazing team and early users. Check it out and let us know what you think!

**After:**
> We shipped the thing. It does X. If you've dealt with [specific problem],
> it's probably worth 10 minutes of your time.
> [link]
> We're around in the comments if anything's unclear.


### 10. Vague CTAs

**Patterns to replace:**
- "Learn more" → describe what they'll learn
- "Get started today" → say what getting started actually means
- "Book a demo" → say what happens in the demo
- "Try it free" → say how long, what's included, what they'll see
- "Reach out" → say how and why

**Before:**
> Ready to transform your workflow? Get started today and learn more about
> how we can help your team reach its full potential.

**After:**
> Sign up, connect your repo, and you'll have a working deploy pipeline in
> under an hour. No credit card. [link]


---

## GENERAL AI PATTERNS (STILL APPLY TO GTM)

These are from the base humanizer skill. All still relevant in marketing copy.


### 11. AI Vocabulary Words in Marketing

**High-frequency AI words that kill credibility in GTM copy:**
actually, additionally, align with, comprehensive, crucial, cutting-edge,
delve, elevate, empower, enhance, ensure, foster, garner, groundbreaking,
highlight, holistic, innovative, intricate, journey, key (adjective),
landscape (abstract), leverage, paradigm, pivotal, robust, seamless,
showcase, solution (for product), streamline, synergy, tapestry, testament,
transformative, underscore, unlock, utilize, valuable, vibrant

**Rule:** If a word appears in every SaaS homepage you've ever read, cut it.


### 12. Copula Avoidance

**Words to watch:** serves as, stands as, functions as, operates as, acts as,
represents, boasts, features, offers

**Problem:** Instead of "it is," AI writes "it serves as." Just say what the
thing is.

**Before:**
> The dashboard serves as a central hub for your operations, offering real-time
> insights and featuring advanced filtering capabilities.

**After:**
> The dashboard shows your pipeline in real time. You can filter by team,
> environment, or date.


### 13. The Rule of Three in Copy

**Problem:** AI forces everything into three. Benefits come in threes. Bullet
points come in threes. Even sentences get grouped into threes. It looks
deliberate because it is — but deliberate ≠ good.

**Before:**
> Build faster, ship smarter, and scale confidently.

**After:**
> You'll spend less time on deploys. That's the pitch.


### 14. Negative Parallelisms ("It's Not Just X, It's Y")

**Before:**
> It's not just a deployment tool. It's a complete platform for modern
> engineering teams.

**After:**
> It handles deploys, rollbacks, and environment config. Most teams use
> it instead of maintaining their own scripts.


### 15. Em Dashes as Fake Punch

**Problem:** Marketing copy overuses em dashes to create emphasis. It looks
like copywriting, not writing.

**Before:**
> We built it for developers—not DevOps teams—who want deploys to just work—
> without the overhead.

**After:**
> We built it for developers who want deploys to just work, without having to
> become a DevOps expert to get there.


### 16. Excessive Hedging in Technical Claims

**Before:**
> Our solution could potentially help reduce infrastructure costs by up to
> possibly 40% in some cases.

**After:**
> Customers typically cut infrastructure costs 30-40% in the first quarter.
> It depends on how much you're over-provisioned.


### 17. Generic Positive Closers

**Before:**
> The future is bright for teams that embrace this approach. Together, we can
> build a better ecosystem for developers everywhere.

**After:**
> That's what we're building. If it sounds like something you'd use, try it.


### 18. Passive Voice Hiding the Product

**Before:**
> Workflows are automated. Errors are caught before they reach production.
> Teams are empowered to ship with confidence.

**After:**
> It catches errors before they hit production. Your team ships without
> running through a manual checklist first.


---

## Process

1. Read the input copy in full
2. Identify the format (cold email, landing page, LinkedIn post, carousel,
   launch announcement, etc.)
3. Identify the target reader (developer, founder, buyer, general audience)
4. Scan for all patterns above
5. Rewrite with:
   - Specifics replacing vague claims
   - Active voice replacing passive
   - Direct language replacing hype
   - One clear purpose per sentence
6. Do a final audit: "What still reads like AI or generic marketing copy?"
7. Fix what's left
8. Present the final version


## Output Format

Provide:
1. **Rewrite** — the full humanized version
2. **Audit notes** — brief bullets on what was changed and why
3. **What to fill in** — flag any placeholders where a specific number,
   name, or detail is needed to make the copy credible (e.g., "[insert
   actual customer name]" or "[specific outcome from your data]")


---

## Full Example

**Format:** Cold email
**Target:** Founder of a post-PMF AI startup

**Before (AI-generated):**
> Subject: Enhance Your Go-To-Market Strategy with Cutting-Edge Solutions
>
> Hi [Name],
>
> I hope this email finds you well. I wanted to reach out because I came across
> your company and was truly impressed by the innovative work you're doing in
> the AI space.
>
> At Varnan, we're passionate about empowering AI startups to unlock their full
> growth potential. Our comprehensive GTM solutions are designed to streamline
> your marketing efforts, foster meaningful connections with your target audience,
> and drive sustainable revenue growth.
>
> We leverage cutting-edge content strategies and a robust distribution network
> to ensure your message reaches the right developers and founders at the right
> time, maximizing your ROI and enhancing your market presence.
>
> I'd love to explore potential synergies and discuss how we can add value to
> your journey. Would you be open to a quick 15-minute call to learn more?
>
> Looking forward to connecting!
>
> Best regards,
> [Sender]

**Rewrite:**
> Subject: GTM for [Company] — quick question
>
> Hi [Name],
>
> Saw you raised [round] and are [specific thing they're doing] — congrats.
>
> We run GTM for post-PMF AI startups. Mostly content and distribution:
> developer-facing carousels, cold outreach sequences, creator partnerships.
> We've done this for [reference client] and [reference client].
>
> Are you running any content right now, or is it all word of mouth at this
> stage?
>
> Either answer is useful — just trying to see if this is even relevant timing.
>
> Paras

**Audit notes:**
- Cut the subject line hype — replaced with a specific, lowercase subject
  that reads like a real email
- Removed "I hope this email finds you well" and the compliment opener
- Replaced vague positioning ("empowering AI startups") with what we
  actually do (content, distribution, specific formats)
- Removed all AI vocabulary: enhance, cutting-edge, leverage, robust,
  streamline, foster, synergies, journey, maximize, sustainable
- Replaced "Would you be open to a quick 15-minute call?" with a question
  they can actually answer without committing to anything
- Removed "Looking forward to connecting"
- Shortened to under 100 words

**What to fill in:**
- [round]: their actual funding round from LinkedIn or Crunchbase
- [specific thing they're doing]: one sentence from their website or a
  recent tweet — shows you actually looked
- [reference client] x2: real customer names with permission


---

## Reference

Built on top of the [humanizer skill](https://github.com/open-directory/skills/humanizer)
and the Wikipedia "Signs of AI writing" guide. Extended with patterns
observed across B2B SaaS, developer tools, and AI startup GTM copy.

Core principle: marketing copy that sounds human is copy that knows
exactly who it's talking to and says one specific thing clearly.
Everything else is noise.
