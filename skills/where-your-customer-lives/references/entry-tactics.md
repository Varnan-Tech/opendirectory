# Entry Tactic Templates by Channel Type

These are starting templates. The AI must customize each tactic for the specific community, using evidence posts and the subreddit description to identify actual thread types, posting norms, and community rules.

---

## Reddit

**Template structure:** Thread type + content format + community norm + what to avoid.

**Thread types to look for:**
- Weekly/monthly megathreads: "What are you working on?", "Tools & Projects", "Self-Promotion Saturday", "Feedback Friday", "Show HN" equivalent threads
- Recurring "Help" or "Question" flairs
- Monthly community surveys or AMAs

**Content formats that get upvotes:**
- Technical post-mortems: "We did X, it failed, here is why, here is what we changed"
- Comparison breakdowns: "We evaluated 5 tools for {pain} -- here is our matrix"
- Problem-framing posts: "Anyone else dealing with {pain}? We found three approaches..."
- Open questions with context: "We are building {thing}. Ran into {problem}. What would you do?"

**Universal anti-patterns for Reddit:**
- Posting product links in non-promotional threads (auto-removed in most subreddits)
- Asking "what tools do you use?" without a specific problem context (flagged as market research farming)
- First post is a product announcement (zero karma = instant distrust)
- Responding to competitor complaints with "you should try our product"

**Example (r/devops):** "Find the weekly 'What are you working on?' thread (pinned every Monday by automoderator). Reply with a 3-sentence technical challenge: what you were trying to do, what broke, and what you tried. No product mention. Build 3-4 posts of karma before posting standalone content."

---

## Slack

**Template structure:** Specific channel within the workspace + conversation format + timing.

**Entry sequence:**
1. Join via website form or invite link
2. Introduce yourself in #introductions with: role, company, one technical problem you are currently solving
3. Spend 1-2 weeks answering questions in relevant channels before posting about your product
4. Post in #show-and-tell or #tools channels after establishing presence

**Content formats that get engagement:**
- Asking a specific technical question (signals you are a practitioner, not a vendor)
- Sharing a non-promotional resource (article, script, guide)
- Answering someone else's question in detail

**Anti-patterns:**
- DM-ing members directly to pitch (almost always a ban)
- Cross-posting the same message in multiple channels
- Posting product links without being asked

---

## Discord

**Template structure:** Server channel + role assignment + gradual contribution.

**Entry sequence:**
1. Join via invite link
2. Complete any onboarding (many servers require role selection or intro post)
3. Post in #introductions: role + what you build + one specific problem
4. Contribute in technical channels for 1-2 weeks before mentioning your product

**Content formats:**
- Voice channels / stage events: joining community calls builds trust faster than text
- Sharing tools, scripts, or resources in #resources or #tools channels
- Participating in community challenges or hackathons

**Anti-patterns:**
- Posting in #general with a promotional message on day 1
- Spamming invite links in other servers
- Pinging @everyone or using excessive notifications

---

## Newsletter

**Template structure:** Contribution type + relationship path + timeline.

**Entry approaches (ranked by accessibility):**
1. **Sponsor:** Most newsletters have a sponsor slot. Relevant for products with budget.
2. **Guest article:** Pitch a technical deep-dive or case study. Must be non-promotional and provide genuine value.
3. **Mention-worthy news:** Share something newsworthy (open-source release, research finding, benchmark) that the editor would want to share organically.

**Content formats that get accepted:**
- Data-backed insights ("We analyzed 500 incidents -- here is what caused the most downtime")
- Practical guides with code/config examples
- Contrarian takes with evidence

**Anti-patterns:**
- Pitching a sponsored post that reads like a product description
- Sending a cold pitch with no context about why your content fits the audience
- Sending the same pitch to 10 newsletters at once (editors talk to each other)

---

## Podcast

**Template structure:** Guest pitch angle + pre-qualification + follow-up.

**Entry approach:**
1. Listen to 3-5 episodes to identify the host's specific framing and guest style
2. Pitch as a practitioner, not a founder: "I am a DevOps engineer who spent 2 years solving X. I have specific opinions about Y that your audience would disagree with."
3. Lead with controversy or counter-intuition, not company credentials

**Pitch elements that work:**
- A specific claim the audience will want to debate
- A technical story with a surprising outcome
- A data-backed finding that contradicts conventional wisdom

**Anti-patterns:**
- "I am the founder of X and would love to share our story" (generic, rejected)
- Pitching via mass email tools (gets filtered as spam)
- Offering to pay to be a guest (podcast integrity signal to hosts)

---

## Conference

**Template structure:** Specific engagement context + entry level + timeline.

**Entry approaches (ranked by cost/effort):**
1. **Attend + hallway conversations:** Cheapest. Identify 3-5 specific sessions where your ICP will concentrate. Prepare a 30-second context-setting intro. Bring nothing promotional.
2. **Submit a talk:** Submit 6+ months before the conference. Frame as a practitioner talk, not a product demo. "How we cut alert fatigue by 70% (and what didn't work)" beats "Introducing X."
3. **Sponsor a workshop or unconference slot:** Moderate cost. Gives you a captive audience for 45 minutes without a hard pitch.
4. **Conference sponsorship:** Expensive. Only viable if the conference matches your ICP exactly.

**Hallway conversation format:**
- Ask what they are currently working on (not their job title)
- Listen for the specific problem before mentioning your product
- Exchange contact with context: "I am working on something related to what you just described -- can I follow up?"

**Anti-patterns:**
- Setting up a booth and waiting for people to come to you
- Handing out branded swag with no conversation
- Pitching during the speaker's Q&A

---

## YouTube

**Template structure:** Collaboration angle + format match + audience overlap.

**Entry approaches:**
1. **Guest appearance / collaboration:** Reach out to mid-size channels (10K-100K subscribers). Offer to demo your product in the context of a problem the channel covers.
2. **Comment contribution:** Leave specific, detailed technical comments on relevant videos. Builds name recognition if comment is genuinely useful.
3. **Response video:** Create a video that directly responds to or extends content from a popular channel in your space.

**Content formats:**
- Tutorials showing how to solve a specific problem (not "intro to our product")
- Behind-the-scenes engineering decisions ("why we chose X over Y")
- Live coding / live debugging sessions

**Anti-patterns:**
- Posting promotional comments with product links (removed by YouTube spam filters)
- Asking channels to "check out our product" in collaboration outreach
- Creating a channel with only product demos and expecting organic growth

---

## Hacker News

**Template structure:** Post type + framing + timing.

**Entry approaches:**
1. **Show HN:** "Show HN: [product name] -- [what it does in one clause]" Posts that include a working demo, clear problem statement, and invite criticism score highest.
2. **Ask HN:** "Ask HN: How do you handle [specific technical problem]?" -- Join the conversation, answer questions, mention your product only if directly relevant and asked.
3. **Comment on relevant stories:** Find stories about competitor products or your problem space. Leave detailed, opinionated technical comments.

**Timing:**
- Post Show HN between 7am-10am US Eastern on weekdays
- Avoid Friday afternoons and weekends
- Flag posts by 8am to catch morning traffic

**Anti-patterns:**
- "I am the founder of X -- check out our product" (downvoted as marketing)
- Posting without a working demo or detailed technical explanation
- Flagging/reporting competitor posts to reduce their visibility
- Posting the same content twice
