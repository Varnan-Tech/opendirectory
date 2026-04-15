const fs = require('fs');
const content = fs.readFileSync('CONTRIBUTING.md', 'utf-8');
const startMarker = '## Looking for Inspiration? Build One of These!';
const newIdeas = \## Looking for Inspiration? Build One of These!

If you want to contribute but aren't sure what to build, pick one of these high-demand, advanced Go-To-Market (GTM) ideas. Our automation script tracks these, so once your PR is merged, the box will be checked automatically!

- [ ] \\\gh-issue-to-demand-signal\\\ - Scans the open GitHub issues of a competitor's public repo, clusters them by theme (missing features, bugs, UX complaints), and outputs a ranked demand gap report. Tells you exactly what their users are begging for.
- [ ] \\\who-viewed-my-talk\\\ - Given a conference talk URL (YouTube/Luma/Sessionize), scrapes the comments, likes, and attendee list, cross-references speakers from the event's speaker page, and outputs a warm lead list.
- [ ] \\\linkedin-hiring-intent-scanner\\\ - Searches LinkedIn job posts for roles that signal buying intent at companies in a given funding stage, and outputs a prioritized list with context.
- [ ] \\\
pm-downloads-to-leads\\\ - Takes a list of npm package names, pulls weekly download trends via the npm API, identifies packages with breakout velocity, and maps the maintainers to Twitter/GitHub profiles. Useful for finding evangelists.
- [ ] \\\pi-error-to-faq-builder\\\ - Pulls open issues from your GitHub repo tagged as bug or question, clusters them by the error message or API endpoint mentioned, and auto-drafts a troubleshooting FAQ in Markdown.
- [ ] \\\sdk-adoption-tracker\\\ - Given your SDK name, searches GitHub code search for public repos that import/require it, categorizes them by company/project type, and tracks week-over-week adoption velocity.
- [ ] \\\
oise-to-linkedin-carousel\\\ - Takes a raw voice note transcript or messy thread of thoughts, and restructures it into a polished LinkedIn carousel script — slide-by-slide, with a hook slide, 5-7 insight slides, and a CTA slide.
- [ ] \\\oss-launch-kit\\\ - Given a GitHub repo URL, generates the full launch kit: a Show HN post, a Product Hunt description, 5 Reddit posts tailored to relevant subreddits, a Twitter thread, and a first week community plan.
- [ ] \\\competitor-churner-finder\\\ - Monitors Twitter and Reddit for posts from people expressing frustration with a specific competitor tool, extracts their profiles, and drafts a timely, empathetic DM offering your product as the alternative.
- [ ] \\\ph-daily-radar\\\ - Hits the Product Hunt API every morning, filters launches by category, extracts the makers' Twitter/LinkedIn, and sends you a digest of who launched in your category today — with drafted outreach for each maker.
- [ ] \\\domain-expired-opportunity-finder\\\ - Monitors daily expired domain lists, filters for domains that still have backlinks pointing to them, and flags ones in your niche that you could buy cheaply and redirect.
- [ ] \\\pricing-page-psychology-audit\\\ - Takes a SaaS pricing page URL and audits it against 12 known pricing psychology principles. Outputs specific suggestions on how to reframe each tier.
- [ ] \\\content-repurpose-queue\\\ - Looks at your last 30 pieces of content, flags every one that got above-average engagement but was never repurposed, and generates a queue of 5 repurposing formats for each one.
- [ ] \\\github-discussion-to-devrel-content\\\ - Monitors GitHub Discussions on your or a competitor's repo, surfaces threads with 10+ replies or unresolved questions, and auto-drafts a short blog post or Twitter thread that answers each one.
- [ ] \\\product-hunt-launch-hijacker\\\ - Monitors the Product Hunt GraphQL API for trending launches, extracts upvoter profiles, enriches data via Apollo, and drafts tailored sales outreach.
- [ ] \\\hacker-news-intent-listener\\\ - Polls the Hacker News API for buying intent keywords, extracts commenter profiles, cross-references GitHub/Twitter for emails, and logs leads to a local SQLite database.
- [ ] \\\eddit-pain-point-clusterer\\\ - Scrapes niche subreddits using PRAW, clusters posts by user pain points using local sentence-transformer embeddings, and generates data-backed Meta ad copy.
- [ ] \\\	witter-follower-overlap-mapper\\\ - Uses the Twitter/X API to analyze follower overlap between multiple competitors, identifies high-influence accounts, and builds a targeted DM outreach list.
- [ ] \\\youtube-tutorial-comment-scraper\\\ - Scrapes comments on popular tutorial videos for competitor products, identifies frustrated users, extracts channel metadata, and finds business emails for outreach.
- [ ] \\\dark-funnel-slack-monitor\\\ - Connects to Slack workspaces via user tokens, monitors specific channels for keyword triggers indicating software evaluation, and alerts the sales team with context.
- [ ] \\\seo-content-gap-orchestrator\\\ - Scrapes the top 10 Google results via Serper API, extracts H2/H3 tags, runs TF-IDF analysis to find missing subtopics, and generates a comprehensive SEO content brief.
- [ ] \\\pricing-page-ab-test-detector\\\ - Takes DOM snapshots of competitor pricing pages using Playwright, uses visual diffing to detect silent changes in pricing tiers, and alerts the product marketing team.
- [ ] \\\domain-registration-intent-tracker\\\ - Monitors newly registered domains via daily WHOIS database dumps for industry keywords, cross-references registrants with LinkedIn, and triggers day-zero outreach for tooling sales.
\
const idx = content.indexOf(startMarker);
if (idx !== -1) {
  const newContent = content.substring(0, idx) + newIdeas + '\n';
  fs.writeFileSync('CONTRIBUTING.md', newContent, 'utf-8');
  console.log('Updated CONTRIBUTING.md successfully.');
} else {
  console.log('Marker not found.');
}
