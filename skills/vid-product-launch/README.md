# vid-product-launch

Generate a cinematic product launch video from a product description and launch context. The video follows a 5-section narrative arc: build anticipation, reveal the product, prove the value, and close with a CTA.

This is different from a sizzle reel. A launch video has a specific reveal moment. Every section before it builds toward that moment.

Use it for announcement posts, email campaigns, landing page heroes, and launch day social content.

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install vid-product-launch --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fvid-product-launch&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## How It Works

1. Provide your product name, description, and launch context.
2. The agent generates a narrative script with timed sections.
3. The agent produces a single HTML file using the `renderFrame(t)` architecture.
4. The export script captures frames via Playwright and assembles an MP4 via FFmpeg.

No external AI video APIs. No API costs. Works offline.

---

## Launch Video Structure

| Section | Timing (60s) | Content |
|---------|-------------|---------|
| Tease | 0-10s | The problem, without naming your product |
| Build | 10-30s | Rising tension, hints at the solution |
| Reveal | 30-45s | Product name, tagline, and first look |
| Proof | 45-55s | One key result or feature |
| CTA | 55-60s | Your URL or launch offer |

Timing scales automatically for 30s and 90s durations.

---

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `product_name` | Yes | | Product or feature name |
| `product_description` | Yes | | What it does and who it is for (2-3 sentences) |
| `tagline` | | auto | Key headline, 4-6 words (write this yourself) |
| `launch_date` | | | ISO date for countdown timer (e.g. `2026-06-01`) |
| `cta` | | auto | Final CTA (e.g. `"Browse skills at opendirectory.dev"`) |
| `tone` | | `cinematic` | `cinematic` / `energetic` / `minimal` / `emotional` |
| `duration` | | `60` | `30` / `60` / `90` seconds |
| `aspect_ratio` | | `16:9` | `16:9` / `9:16` |
| `letterbox` | | `false` | 2.35:1 black bars (cinematic tone only) |
| `music` | | | Path to audio file (mp3/m4a/wav) |

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

Output: `launch/[slug]/product-launch.mp4`. 1080p H.264, compatible with QuickTime, iOS, Twitter, LinkedIn, and Instagram.

---

## Prompt Tips

Write the tagline yourself. It is the product's entire promise in 4-6 words. The agent uses it as the centerpiece of the reveal moment.

The reveal is everything. Everything before it creates tension. If the reveal does not feel earned, the video does not work.

Put one stat in the proof section. Five stats kill the pacing. One oversized number creates the punch.

Match tone to your market. Cinematic does not work for developer tools. Minimal does not work for consumer apps.

---

## Prompt Examples

Good:
```
Product launch video, 60 seconds. Product: OpenDirectory. Description: A library
of pre-built AI agent skills for Claude, Codex, and Gemini. Covers GTM, content,
research, and developer tools. Tagline: "AI skills, ready to install." Tone: minimal.
Proof: "52+ skills, zero setup." CTA: "Browse skills at opendirectory.dev." Aspect: 16:9.
```

Bad:
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

Preview the HTML in any browser before exporting. It runs a live animation loop at full quality.

---

## Requirements

- Node.js 18+
- FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`)
- Playwright installs automatically on first export run
