# vid-sizzle-reel

Generate a high-energy sizzle reel or hype video from brand assets and key messages. Fast-paced montage format with dynamic cuts, bold text overlays, and optional beat-synced music.

Use it for launch days, investor pitches, conference openers, event promos, and social media campaign kickoffs. The goal is to create excitement, not to explain.

This is different from a product launch video. A sizzle reel has no single story arc. It has energy, rhythm, and one punchy message per cut.

---

## Install

```bash
npx "@opendirectory.dev/skills" install vid-sizzle-reel --target claude
```
### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you are uploading the folder that contains the `SKILL.md` file!

---

## How It Works

1. Provide your key messages and brand assets.
2. The agent builds a HyperFrames HTML composition with GSAP animation timelines.
3. The HyperFrames CLI captures frames via headless Chromium and assembles an MP4 via FFmpeg.

No Runway. No Pika. No AI video APIs. Works offline.

---

## Sizzle Reel Structure

| Section | Timing (60s) | Content |
|---------|-------------|---------|
| Cold Open | 0-5s | One stat or impact phrase. No brand name. |
| Build | 5-40s | Key messages flash one at a time, rising energy |
| Peak | 40-55s | Maximum intensity; strongest message at full scale |
| Land | 55-60s | Logo, tagline, CTA URL |

Timing scales automatically for 30s and 90s durations.

---

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `key_messages` | Yes | | 3-5 phrases that flash on screen (you write these) |
| `brand_assets` | | | Logo URL or path, brand colors (hex), key screenshots |
| `tone` | | `energetic` | `energetic` / `cinematic` / `emotional` / `professional` |
| `music` | | | File path or BPM/genre string (e.g. `"128bpm electronic"`) |
| `duration` | | `60` | `30` / `60` / `90` seconds |
| `aspect_ratio` | | `16:9` | `16:9` / `9:16` |
| `cut_style` | | auto | `fast` (1-2s) / `cinematic` (3-5s); auto derives from tone |
| `end_card` | | auto | Logo + tagline + CTA URL for the Land section |

---

## Tone Reference

| Tone | Reference Feel | Cut Style | Best For |
|------|---------------|-----------|----------|
| `energetic` | Product Hunt launch day | fast (1-2s) | Social media, launch days, developer tools |
| `cinematic` | Apple product reveal | cinematic (3-5s) | Investor decks, B2C premium, Series A+ |
| `emotional` | Kickstarter campaign | mixed (2-4s) | Consumer products, mission-driven brands |
| `professional` | B2B conference opener | 2s cuts | Enterprise SaaS, internal events, sales decks |

---

## Output

```
sizzle/
└── [slug]/
    ├── index.html           (HyperFrames composition source)
    └── sizzle-reel.mp4      (H.264, 1080p, yuv420p)
```

Open `index.html` in any browser to preview the animation before exporting.

---

## Prompt Tips

Write the key messages yourself. These are the exact phrases that appear on screen. The agent cannot invent good copy for your brand. 3 sharp lines beats 10 vague ones.

Choose music before visuals. The BPM drives the cut style. The cut style drives every timing decision in the video.

Cold open: one number. Not a sentence, not a tagline. One specific, surprising number. It earns 5 seconds of attention before the audience knows who you are.

Land section: logo plus one line plus one URL. Anything more dilutes the CTA.

Match tone to channel. Energetic for social and Product Hunt. Cinematic for investor decks. Professional for conference openers.

---

## Prompt Examples

Good:
```
Sizzle reel, 60 seconds. Tone: energetic. Key messages: ['AI skills, ready to install' /
'52+ skills across GTM, content, and research' / 'Works with Claude, Codex, and Gemini' /
'Zero setup. Instant value.']. Music: 128bpm electronic. Cut style: fast.
End card: OpenDirectory + 'AI skills, ready to install' + 'opendirectory.dev'. Aspect: 16:9.
```

Bad:
```
hype video for our company
```

---

## Requirements

- Node.js 22+
- FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`)
- HyperFrames (installed automatically via `npx skills add heygen-com/hyperframes`)
