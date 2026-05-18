# Channel Types Reference

Seven channel types discovered by this skill. Each type has a different discovery method, metadata available, and scoring characteristics.

---

## 1. Reddit

**Discovery method:** Signal-trace (primary) -- search Reddit for ICP pain posts, extract which subreddits those posts came from. Subreddits with the most ICP posts = highest-confidence channels.

**Metadata available:**
- `subscribers` -- total member count from `r/{sub}/about.json`
- `active_user_count` -- users online right now (proxy for posts/day activity)
- `public_description` -- subreddit purpose from about.json
- `icp_signal_count` -- posts matching ICP queries found in this subreddit (counted by script)
- `competitor_mentions` -- how many ICP posts also mention a competitor product

**Scoring notes:**
- Highest-confidence channel type because signals are traced from actual ICP posts
- active_user_count / 100 used as activity_score (capped at 30)
- Open entry -- no penalty

**Evidence standard:** Every Reddit channel must have at least 1 evidence_post from the raw data. If icp_signal_count = 0, the channel was found via competitor layer, not signal_trace -- note this distinction.

---

## 2. Slack

**Discovery method:** DuckDuckGo search -- `"{category} slack community"` and `"{icp_role} slack workspace"`

**Metadata available:**
- Member count from search snippets (e.g. "Join 12,000+ DevOps professionals")
- URL from search result (often a landing page or Slack direct link)

**Scoring notes:**
- No icp_signal_count from script (0 unless competitor layer fires)
- Member count drives size component of score
- activity_score defaults to 5 (DDG doesn't expose post frequency)
- Most Slack communities are open-invite (via website form) -- no penalty

**Evidence standard:** Channel name and URL must come from DDG results. Member count from snippet or 0 -- never estimated. Note if invite-required (entry_type = "invite-only", -10 penalty).

---

## 3. Discord

**Discovery method:** DuckDuckGo search -- `"{icp_role} discord server"` and `"{category} discord community"`

**Metadata available:**
- Member count from DDG snippets
- Invite link or website from search result

**Scoring notes:**
- Same scoring structure as Slack
- Many Discord servers are invite-only -- check the URL for discord.gg invite links
- Gaming/consumer ICPs: Discord scores higher than Slack

**Evidence standard:** Same as Slack. If invite link expires, note as "invite may expire -- check current link."

---

## 4. Newsletter

**Discovery method:** DuckDuckGo search -- `"{category} newsletter weekly"` and HN "Ask HN: what newsletters do you read about {category}"

**Metadata available:**
- Subscriber count from DDG snippets (less reliable than Reddit API)
- Frequency (weekly/monthly) from snippet
- Sponsorship availability often mentioned in description

**Scoring notes:**
- Newsletters score well for reach but entry is typically paid sponsorship or content contribution
- entry_type = "paid" (-20 penalty) if snippet mentions "sponsor" or "advertising"
- Subscriber count varies widely -- treat as directional

**Evidence standard:** Newsletter name must appear in DDG results. Subscriber count from snippet or "subscriber count not found."

---

## 5. Podcast

**Discovery method:** DuckDuckGo search -- `"{icp_role} podcast"` and `"best {category} podcast"`

**Metadata available:**
- Episode count from snippet
- Frequency (weekly/biweekly) from snippet
- Guest appearances as entry point

**Scoring notes:**
- Podcasts score lower than Reddit because reach per episode is smaller and entry requires production effort
- Guest appearances are the primary entry tactic -- not "listening"
- activity_score defaults to 5

**Evidence standard:** Podcast name and URL from DDG results. Episode count from snippet or omitted.

---

## 6. Conference

**Discovery method:** DuckDuckGo search -- `"{category} conference summit 2025"` and `"{icp_role} conference annual"`

**Metadata available:**
- Attendee count from snippet
- Date and location from snippet
- Ticket price category (free/paid) from snippet

**Scoring notes:**
- Conferences have the highest ICP density per touchpoint but low accessibility
- entry_type = "paid" (-20 penalty) for paid conferences
- Sponsorship is a separate entry path (expensive) -- not the primary tactic
- Hallway conversations and evening events > sponsored sessions for early-stage founders

**Evidence standard:** Conference name from DDG results. Attendee count from snippet or "attendee count not found." Check for 2025/2026 dates -- exclude past conferences.

---

## 7. YouTube Channel

**Discovery method:** DuckDuckGo search -- `"best {category} youtube channel"` and `"{icp_role} tutorial youtube"`

**Metadata available:**
- Subscriber count from DDG snippets
- Channel name and URL

**Scoring notes:**
- YouTube channels are consumption channels, not community channels
- Entry tactic = guest appearance or collaboration, not commenting
- High subscriber counts inflate scores -- cap with size component (log scale)

**Evidence standard:** Channel name and subscriber count from DDG results.

---

## 8. Forum (catch-all)

**Discovery method:** Competitor layer DuckDuckGo search -- `"{competitor} community forum users"`

**Metadata available:**
- URL from DDG results
- Description from snippet

**Scoring notes:**
- Competitor forums = high intent ICP (actively evaluating alternatives)
- icp_signal_count = 0, but competitor_mentions bumped to 3 as proxy
- Includes HN (scored separately with actual signal count)

**Evidence standard:** URL and name from DDG results or direct knowledge (HN is always valid).
