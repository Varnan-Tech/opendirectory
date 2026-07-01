# Podcast Transcript Fetcher

> Fetch, search, and batch-transcribe transcripts from 5 top podcasts using a 3-tier approach: free sources, RSS+Whisper, and commercial API.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)
[![version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/Varnan-Tech/opendirectory)
[![license](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)

**Supported podcasts:** Lenny's Podcast, Dwarkesh Podcast, Cheeky Pint, 20VC (20 Minutes VC), A16z Podcast

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install podcast-transcript-fetcher --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill podcast-transcript-fetcher
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

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

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

<video src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fpodcast-transcript-fetcher&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Quick Start

```bash
# Set up Python dependencies
pip install requests python-dotenv

# Copy and fill in your API key
cp .env.example .env
# Then edit .env with your GROQ_API_KEY

# Get the latest Lenny's Podcast transcript
python scripts/get_transcript.py "Lenny's Podcast" --latest

# Search across ALL podcasts by keyword
python scripts/get_transcript.py --search "Marc Andreessen"

# Batch-transcribe last 3 episodes
python scripts/get_transcript.py "Dwarkesh Podcast" --last 3
```

## Transcription Methods

| Method | Cost | Speed | Quality | Setup |
|--------|------|-------|---------|-------|
| Free sources | $0 | Instant | Varies | None |
| Groq Whisper | Free tier | ~10s/hr audio | 2.7% WER | `pip install groq` + API key |
| Local faster-whisper | $0 (compute) | ~1.5x realtime | 2.7% WER | `pip install faster-whisper` |
| Taddy API | $75/mo+ | Instant | High | `TADDY_API_KEY` |

## Prerequisites

- **Python 3.10+**
- **ffmpeg** — for audio compression (Groq's 25 MB limit)
  - Windows: `winget install ffmpeg` or `scoop install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `apt install ffmpeg`
- **Groq API key** — free at [console.groq.com](https://console.groq.com)
- Works with: **Claude Code · OpenCode · Codex CLI · Gemini CLI · Cursor**

## Usage

### Single Episode

```bash
# Get latest episode (auto-detects best method)
python scripts/get_transcript.py "Lenny's Podcast" --latest

# Specific episode by title
python scripts/get_transcript.py 20vc --episode "Sam Altman"

# Force a specific method
python scripts/get_transcript.py a16z --latest --method whisper

# Save to file
python scripts/get_transcript.py lennys --latest --output episode.md
```

### Cross-Podcast Search

```bash
# Find episodes by keyword across all 5 podcasts
python scripts/get_transcript.py --search "regulation"

# Search by guest name
python scripts/get_transcript.py --guest "Marc Andreessen"

# Filter to one podcast
python scripts/get_transcript.py "Lenny's Podcast" --search "vibe coding"
```

### Batch Transcription

```bash
# Transcribe last 5 episodes
python scripts/get_transcript.py "20vc" --last 5

# Search + auto-transcribe top matches
python scripts/get_transcript.py --search "AI safety" --transcribe --transcribe-count 5
```

## How It Works

```
User provides podcast + episode
      ↓
Tier 1: Free sources (GitHub archive, PodScripts, YouTube)
  → Found? Return transcript instantly
  → Not found? Fall through
      ↓
Tier 2: RSS + Whisper transcription
  → Download MP3 from podcast RSS feed
  → Compress if >25 MB (ffmpeg)
  → Transcribe via Groq Whisper API
      ↓
Tier 3: Taddy API (commercial fallback)
  → Requires TADDY_API_KEY
```

Search and batch features build on Tier 2:
- **Search** scans RSS metadata (titles + descriptions) across all podcasts — instant, no API key needed
- **Batch** downloads and transcribes the last N episodes in sequence
- **Pipeline** chains search results into batch transcription

## Project Structure

```
podcast-transcript-fetcher/
├── SKILL.md                ← AI instructions (the brain)
├── README.md               ← This file
├── package.json            ← Skill metadata
├── .env.example            ← Template for API keys
├── scripts/
│   ├── get_transcript.py   ← Core CLI (3-tier transcript fetcher)
│   └── podcasts.json       ← Podcast registry (RSS feeds, sources)
└── references/
    └── podcasts.md         ← Detailed source documentation
```

## Use with AI Agents

Once you have a transcript, ask your AI agent to analyze it:

> "Summarize this transcript from Lenny's Podcast"
> "Extract 3 actionable insights from this 20VC episode"
> "Compare the Dwarkesh and A16z takes on AI safety"
> "Find all episodes where they discuss [topic]"

---

## Contributing

Want to add more podcasts? Open a PR or issue at the [OpenDirectory repo](https://github.com/Varnan-Tech/opendirectory).

To add a podcast, just add an entry to `scripts/podcasts.json` with the podcast name, RSS feed URL, available transcript sources, and a slug. See the existing entries for the format.
