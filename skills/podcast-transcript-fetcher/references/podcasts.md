# Podcast Transcript Sources

Detailed reference for each podcast's transcript availability and how to access them.

---

## Lenny's Podcast

| Detail | Value |
|--------|-------|
| **Host** | Lenny Rachitsky |
| **Website** | https://www.lennyspodcast.com |
| **RSS Feed** | `https://api.substack.com/feed/podcast/10845.rss` |
| **Substack** | https://lennyspodcast.substack.com |
| **Episode archive** | Full back-catalog on Substack |

### Transcript Sources (in priority order)

**Tier 1 — GitHub Archive (free, 269+ transcripts)**
- Repo: `ChatPRD/lennys-podcast-transcripts`
- 269 pre-transcribed episodes in Markdown format
- Clone: `git clone https://github.com/ChatPRD/lennys-podcast-transcripts.git`
- Episodes are named by title, searchable via grep
- Best source for older/medium episodes

**Tier 2 — Dropbox Official Archive**
- Linked from Substack episode pages
- Contains official transcripts uploaded by Lenny's team
- Accessible via shared Dropbox links (no login required for reading)

**Tier 3 — RSS Transcript Tag**
- Some episodes include `<podcast:transcript>` in RSS XML
- Usually links to Substack page with inline transcript
- Format: `text/html` or `text/plain`

**Existing Tools**
- `akshayvkt/lenny-mcp`: MCP server searching 284 transcripts via FlexSearch
- `mpnikhil/lenny-rag-mcp`: Hierarchical RAG over 299 transcripts in ChromaDB

---

## Dwarkesh Podcast

| Detail | Value |
|--------|-------|
| **Host** | Dwarkesh Patel |
| **Website** | https://www.dwarkesh.com |
| **RSS Feed** | `https://api.substack.com/feed/podcast/69345.rss` |
| **Substack** | https://dwarkesh.substack.com |

### Transcript Sources

**Tier 1 — Website Scrape (free)**
- Individual episode pages on dwarkesh.com contain full transcripts
- Layout: Episode page → scroll down for transcript section
- URL pattern: `https://www.dwarkesh.com/p/{episode-slug}`

**Tier 2 — PodScripts**
- Indexed on PodScripts.co
- URL: https://podscripts.co/podcasts/dwarkesh-podcast

**Tier 3 — GitHub Gists**
- Some transcripts posted as gists
- Search: `git.io/dwarkesh-transcript` or GitHub search

---

## The Cheeky Pint

| Detail | Value |
|--------|-------|
| **Website** | https://thecheekypint.com |
| **RSS Feed** | `https://feeds.transistor.fm/cheeky-pint-with-john-collison` |
| **Hosting** | Transistor.fm |

### Transcript Sources

**Tier 1 — RSS + Whisper (default)**
- Download MP3 from RSS feed
- Transcribe with local Whisper or Groq API
- See `get_transcript.py --method whisper`

**Note:** The RSS feed was renamed from `the-cheeky-pint` to `cheeky-pint-with-john-collison` (Transistor.fm migration). The old feed URL returns 404.

---

## 20 Minutes VC (20VC)

| Detail | Value |
|--------|-------|
| **Host** | Harry Stebbings |
| **Website** | https://20vc.com |
| **RSS Feed** | `https://feeds.libsyn.com/61840/rss` |
| **Hosting** | Libsyn (migrated from Simplecast) |

### Transcript Sources

**Tier 1 — RSS + Whisper (default)**
- Hosted on Libsyn (12 MB feed, 1476+ episodes)
- Download MP3 from RSS feed, transcribe with Whisper
- See `get_transcript.py --method whisper`

**Tier 2 — YouTube Transcripts (free, 199+ episodes)**
- Existing skill: `sboghossian/20vc-claude-skill` — 199 YouTube transcripts
- GitHub: https://github.com/sboghossian/20vc-claude-skill

- Covers many recent episodes

**Tier 3 — Substack PDFs**
- Some episodes published on Substack with PDF transcripts
- URL: https://20vc.substack.com

**Note:** 20VC migrated from Simplecast to Libsyn. The old Simplecast RSS (`feeds.simplecast.com/3GxrMqOd`) returns 404 (`NoSuchKey`).

---

## A16z Podcast

| Detail | Value |
|--------|-------|
| **Website** | https://a16z.com/podcasts |
| **RSS Feed** | `https://feeds.simplecast.com/JGE3yC0V` |
| **Hosting** | Simplecast (relocated feed) |

### Transcript Sources

**Tier 1 — RSS + Whisper (default)**
- Download MP3 from Simplecast RSS (8.9 MB feed, 1000 episodes)
- Transcribe with Whisper (local or Groq)

**Tier 2 — PodScripts (free)**
- URL: https://podscripts.co/podcasts/a16z-podcast
- Indexed and searchable

**Tier 3 — Website Scrape**
- a16z.com/podcasts has per-episode pages
- Some episodes include transcript sections
- Format varies by episode

**Note:** The a16z Podcast (now "The a16z Show") RSS feed UUID changed. Old feed at `feeds.simplecast.com/0cJfpoz2` returns 404 (`NoSuchKey`). Current live feed at `feeds.simplecast.com/JGE3yC0V`.

---

## Taddy API (Commercial, Tier 2)

For any podcast not covered by free sources above:

| Detail | Value |
|--------|-------|
| **Endpoint** | `https://api.taddy.org` |
| **Auth** | `X-API-Key` header with `TADDY_API_KEY` env var |
| **Coverage** | 4M+ podcasts, 200M episodes |
| **Transcripts** | Auto-transcribes top 5,000 podcasts (includes all 5 targets) |
| **On-demand** | ~10s per 1hr audio for rest |
| **Pricing** | Free: 500 req/mo. Pro: $75/mo (100k req + 100 transcripts) |

### GraphQL Query Example
```graphql
query {
  getEpisode(uuid: "...") {
    name
    transcript
    audioUrl
  }
}
```

---

## Whisper Transcription (Tier 3 Fallback)

### Local (faster-whisper)
```bash
pip install faster-whisper
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('large-v3', device='cpu', compute_type='int8')
segments, _ = model.transcribe('episode.mp3')
for seg in segments:
    print(f'[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text}')
"
```

### Cloud (Groq API — generous free tier)
```bash
pip install groq
# Set GROQ_API_KEY
python -c "
from groq import Groq
client = Groq()
with open('episode.mp3', 'rb') as f:
    transcription = client.audio.transcriptions.create(
        file=f, model='whisper-large-v3'
    )
    print(transcription.text)
"
```
