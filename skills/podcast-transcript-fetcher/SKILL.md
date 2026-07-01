---
name: podcast-transcript-fetcher
description: Use when fetching, searching, or analyzing transcripts from Lenny's Podcast, Dwarkesh Podcast, Cheeky Pint, 20VC, or A16z Podcast. Tier 2 (RSS+Groq Whisper) is the recommended approach -- fast, free, and most reliable. Also use when asked to "get transcript", "find episode", "summarize podcast", or "search podcast content". Do not use for general web scraping or non-podcast audio transcription.
author: farizanjum
version: 1.1.0
---

# Podcast Transcript Fetcher

Fetch transcripts from 5 supported podcasts. **Tier 2 (RSS+Groq Whisper) is the recommended approach** -- fast, free, and the most reliable across all podcasts. Tier 1 free sources are best-effort (limited availability). Tier 3 Taddy API is the premium/commercial option.

## Quick Reference

```bash
# Get latest episode transcript (auto-detects best method)
python scripts/get_transcript.py "Lenny's Podcast" --latest

# Search by episode title or number
python scripts/get_transcript.py 20vc --episode "Marc Andreessen"
python scripts/get_transcript.py dwarkesh --episode 15

# Force specific method
python scripts/get_transcript.py "cheeky pint" --latest --method whisper
python scripts/get_transcript.py a16z --latest --method taddy

# Save to file
python scripts/get_transcript.py lennys --latest --output transcript.md

# List all supported podcasts
python scripts/get_transcript.py --list-podcasts
```

## Supported Podcasts

| Podcast | Tier 1 (best-effort) | Tier 2 RSS+Whisper [RECOMMENDED] | Tier 3 Taddy (premium) |
|---------|---------------------|-----------------------------------|------------------------|
| Lenny's Podcast | GitHub archive (269 transcripts) | ✅ Substack RSS | ✅ Covered |
| Dwarkesh Podcast | Website scrape + Substack PDF | ✅ Substack RSS | ✅ Covered |
| Cheeky Pint | (none) | ✅ Transistor.fm RSS | ✅ Covered |
| 20VC | Substack PDF | ✅ Libsyn RSS | ✅ Covered |
| A16z Podcast | Website scrape | ✅ Simplecast RSS | ✅ Covered |

## Implementation

### 1. Install Dependencies

```bash
# Core (always required)
pip install requests

# Cloud transcription (recommended — fast, free tier)
pip install groq
export GROQ_API_KEY="your-key"  # Get at https://console.groq.com

# Local transcription (free, needs ~5GB RAM)
pip install faster-whisper

# Audio compression (for Groq's 25 MB limit — Windows: winget/scoop)
#   winget install ffmpeg  or  scoop install ffmpeg

# Taddy API (commercial, optional)
export TADDY_API_KEY="your-key"  # Get at https://taddy.org
```

### 2. Get a Transcript

The script auto-selects the best method. **Tier 2 is the default recommendation:**

```
Tier 1 → Tier 2 (RECOMMENDED) → Tier 3
(best-effort)  (Whisper)  (Taddy API premium)
```

**Tier 1: Free direct sources (best-effort, limited availability)**
- Lenny's: Clones `ChatPRD/lennys-podcast-transcripts` and searches by title
- Dwarkesh: Substack PDF scrape
- 20VC: Substack PDF scrape
- A16z: Website scrape
- Cheeky Pint: No Tier 1 sources available
- Note: Most free APIs (youtubetranscript.com, Spoken.md) are broken or paid. Tier 1 is unreliable -- prefer Tier 2.

**Tier 2: RSS + Whisper transcription [RECOMMENDED]**
- Downloads MP3 from podcast RSS feed
- Compresses if >25 MB (ffmpeg)
- Transcribes via Groq Whisper API (free tier, ~10s per hour of audio)
- Fast, free, and works for every podcast in the registry
- Default recommendation for all use cases

**Tier 3: Taddy API (commercial/premium)**
- Requires `TADDY_API_KEY` ($75/mo+)
- Use for large-scale or production transcript needs
- Covers all 5 podcasts with auto-transcription

### 3. Analyze with AI

Once you have a transcript, pipe it to the agent for analysis:

```markdown
I have this transcript from [podcast]. Can you:
1. Summarize the key arguments
2. Extract 3 actionable insights
3. Identify any controversial claims
4. Compare with [other podcast] on the same topic
```

## Supported Workflows

### Single Episode

| Scenario | Command |
|----------|---------|
| Latest episode | `get_transcript.py "Lenny's Podcast" --latest` |
| Specific episode by title | `get_transcript.py 20vc --episode "Sam Altman"` |
| Episode by number | `get_transcript.py dwarkesh --episode 42` |
| Force Whisper transcription (Tier 2, recommended) | `get_transcript.py a16z --latest --method whisper` |
| Force Taddy API (premium) | `get_transcript.py lennys --latest --method taddy` |
| Save to Markdown | `get_transcript.py cheeky-pint --latest --output episode.md` |
| JSON output | `get_transcript.py dwarkesh --latest --json` |

### Cross-Podcast Search & Batch

| Scenario | Command |
|----------|---------|
| Search all podcasts by keyword | `get_transcript.py --search "Marc Andreessen"` |
| Search by guest name | `get_transcript.py --guest "Sam Altman"` |
| Search within one podcast | `get_transcript.py "Lenny's Podcast" --search "vibe coding"` |
| Batch-transcribe last N episodes | `get_transcript.py "Dwarkesh Podcast" --last 5` |
| Search + transcribe top matches | `get_transcript.py --search "AI safety" --transcribe` |
| Pipeline with custom count | `get_transcript.py --search "scaling laws" --transcribe --transcribe-count 5` |
| Filtered search pipeline | `get_transcript.py "A16z Podcast" --search "crypto" --transcribe` |

### Output Structure

Batch transcription saves to `output/` with per-podcast subdirectories:

```
output/dwarkesh-podcast/Dwarkesh Podcast_2024-01-15_agi-is-still-30-years-away.md
output/20vc/20 Minutes VC (20VC)_2024-03-10_funding-round-analysis.md
```

Each file includes a YAML frontmatter header:
```yaml
---
podcast: Dwarkesh Podcast
episode: AGI is still 30 years away
date: 2024-01-15
url: https://...
source: whisper
---
```

## Podcast Registry

The registry at `scripts/podcasts.json` maps each podcast to its RSS feeds, transcript sources, and API endpoints. To add new podcasts:

```json
{
  "id": "new-podcast",
  "name": "New Podcast",
  "rss": "https://example.com/feed.xml",
  "transcript_sources": {
    "primary": {"type": "website_scrape", "url": "https://example.com"}
  }
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No transcript found" | Tier 2 (RSS+Whisper) is the recommended approach. If auto mode fails, try `--method whisper` to force it. |
| RSS fetch fails | RSS feeds may change; check `scripts/podcasts.json` for current URLs |
| Audio download slow | Large MP3s can take minutes on slow connections |
| Groq rate limited | Wait or switch to local faster-whisper |
| Taddy not returning transcripts | Some episodes lack transcripts; try `--method whisper` |
| Podcast not in registry | Add it to `scripts/podcasts.json` |
| Unicode error on Windows | Fixed: script auto-reconfigures stdout to UTF-8; saved files use UTF-8 encoding |
| Audio > 25 MB for Groq | Install ffmpeg: `winget install ffmpeg` (Windows) or `brew install ffmpeg` (macOS) |

## RSS Feed Status (as of 2026-06)

| Podcast | Old Feed (broken) | Current Feed |
|---------|------------------|--------------|
| Cheeky Pint | `feeds.transistor.fm/the-cheeky-pint` (404) | `feeds.transistor.fm/cheeky-pint-with-john-collison` |
| 20VC | `feeds.simplecast.com/3GxrMqOd` (404) | `feeds.libsyn.com/61840/rss` |
| A16z | `feeds.simplecast.com/0cJfpoz2` (404) | `feeds.simplecast.com/JGE3yC0V` |

## Common Mistakes

- **Forgetting API keys**: Set `GROQ_API_KEY` in your env or `.env` file
- **Relying on Tier 1 free sources**: Most free APIs (youtubetranscript.com, Spoken.md) are broken or paid. Always fall back to Tier 2 (RSS+Whisper) which is the recommended method.
- **Not cloning the Lenny's repo first**: The GitHub archive must be cloned locally for Tier 1 to work
- **Using --method taddy without TADDY_API_KEY**: Falls through silently; set the key or use auto mode
