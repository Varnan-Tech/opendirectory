# vid-product-launch

Generate a cinematic product launch video — builds anticipation with narrative storytelling, a dramatic product reveal, and a clear CTA. Designed for announcement posts, email campaigns, landing page heroes, and launch day social content.

Different from a sizzle reel (which is pure energy) — a launch video has **narrative structure** and a specific **product reveal moment** everything else builds toward.

---

## Install

```bash
npx opendirectory add vid-product-launch
```

---

## How It Works

1. Provide product details and launch context
2. Agent generates a narrative script with reveal structure
3. Agent produces a single HTML file using the `renderFrame(t)` architecture
4. Export script captures frames via Playwright → assembles MP4 via FFmpeg

No external AI video APIs. No API costs. Works offline.

---

## Launch Video Structure

| Section | Timing (60s) | Content |
|---------|-------------|---------|
| **Tease** | 0–10s | The problem — without naming the product yet |
| **Build** | 10–30s | Rising tension, hints at the solution |
| **Reveal** | 30–45s | Product name + tagline + first look |
| **Proof** | 45–55s | One key result or feature (not five) |
| **CTA** | 55–60s | Launch offer or "available now" with URL |

Auto-scaled for 30s and 90s durations too.

---

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `product_name` | ✅ | — | Product or feature name |
| `product_description` | ✅ | — | What it does and who it's for (2–3 sentences) |
| `tagline` | — | auto | Key headline — 4–6 words (write this yourself) |
| `launch_date` | — | — | ISO date for countdown timer (e.g. `2026-06-01`) |
| `cta` | — | auto | Final CTA (e.g. `"Join the waitlist at gooseworks.ai"`) |
| `tone` | — | `cinematic` | `cinematic` / `energetic` / `minimal` / `emotional` |
| `duration` | — | `60` | `30` / `60` / `90` seconds |
| `aspect_ratio` | — | `16:9` | `16:9` / `9:16` |
| `letterbox` | — | `false` | 2.35:1 black bars (cinematic tone only) |
| `music` | — | — | Path to audio file (mp3/m4a/wav) |

---

## Tone Reference

| Tone | Reference Feel | Best For |
|------|---------------|----------|
| `cinematic` | Apple product reveal | B2C, premium positioning, Series A+ |
| `energetic` | Product Hunt launch day | Developer tools, SaaS, younger audiences |
| `minimal` | Linear / Vercel announcement | Design-forward tools, developer market |
| `emotional` | Kickstarter campaign | Consumer products, mission-driven brands |

---

## Export

The agent saves the HTML to `launch/[slug]/product-launch.html`. Then run:

```bash
# Standard 16:9, 60 seconds
bash scripts/export-video.sh launch/my-product/product-launch.html --duration 60

# With music
bash scripts/export-video.sh launch/my-product/product-launch.html --duration 60 --music bg.mp3

# Both orientations in one run (16:9 + 9:16)
bash scripts/export-video.sh launch/my-product/product-launch.html --duration 60 --both-orientations

# Cinematic with letterbox bars
bash scripts/export-video.sh launch/my-product/product-launch.html --duration 60 --letterbox --width 1920 --height 1080
```

**Output:** `launch/[slug]/product-launch.mp4` — 1080p H.264, compatible with QuickTime, iOS, Twitter, LinkedIn, Instagram.

---

## Prompt Tips

**Write the tagline yourself.** The tagline is the product's entire promise in 4–6 words. Don't skip it — it's the most important text in the video.

**The reveal moment is everything.** Everything before it builds tension. The reveal must feel earned.

**One benefit in the proof section.** Trying to show 5 features kills launch video pacing.

**Match tone to your market.** Cinematic doesn't work for developer tools; minimal doesn't work for consumer apps.

---

## Prompt Examples

✅ **Good:**
```
Product launch video, 60 seconds. Product: Gooseworks. Description: AI workspace that
automates research, content creation, and outreach for growth teams. Tagline: "Work at
AI speed." Tone: minimal. Proof: "500+ growth teams, 10x output." CTA: "Join the
waitlist at gooseworks.ai." Music: ambient electronic build. Aspect ratio: 16:9.
```

❌ **Bad:**
```
launch video for our new product
```

---

## Output

```
launch/
└── [slug]/
    ├── product-launch.html    (agent-generated source, open in browser to preview)
    └── product-launch.mp4     (H.264, 1080p, yuv420p, faststart)
```

Preview the HTML in any browser before exporting — it runs a live animation loop at full quality.

---

## Requirements

- Node.js 18+
- FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`)
- Playwright installs automatically on first export run
