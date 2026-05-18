---
name: vid-sizzle-reel
description: 'Generates a high-energy sizzle reel or hype video (MP4) from brand assets and key messages. Fast-paced montage format with dynamic cuts, bold text overlays, and optional music. 4-section structure: Cold Open, Build, Peak, Land. 4 tone presets. Beat-sync cuts when music is provided. Built on HyperFrames (GSAP + headless Chromium + FFmpeg). Trigger when user says "sizzle reel", "hype video", "highlight reel", "launch hype", "conference opener", "event promo video", "investor pitch video", or "brand video montage".'
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# vid-sizzle-reel

Generates a high-energy sizzle reel or hype video from brand assets and key messages.
Pipeline: HyperFrames HTML composition (GSAP timelines) → headless Chromium → FFmpeg H.264 MP4.
No Runway. No Pika. No AI video APIs. Zero runtime cost beyond Node.js + FFmpeg.

**Differentiation from `vid-product-launch`:**
- `vid-product-launch` tells a narrative story — one earned reveal, five sections, tension arc
- `vid-sizzle-reel` creates energy and excitement — fast cuts, music-first, no single story beat

---

## Critical Rules (read before every generation)

1. **Write the key messages yourself — or ask the user to write them.** These are the exact phrases that appear on screen. "AI will figure it out" produces filler. 3-5 sharp lines is the entire content of a sizzle reel.

2. **Brand name appears ONLY in the Land section.** Cold Open and Build create tension without naming the brand. The Land section is the payoff.

3. **Declare the rhythm pattern in a comment at the top of the script before writing any HTML.** Format: `// RHYTHM: flash-sequence | Cold[0-5s]: stat | Build[5-40s]: msg(1.5s)|flash|... | Peak[40-55s]: ... | Land[55-60s]: logo+CTA`. Every timing decision checks against this.

4. **Build end-state layout in CSS first — no GSAP yet.** Position every element at its most-visible moment in static CSS. Then add GSAP entrances with `gsap.from()` and exits with `gsap.to()`. Never position at animated start state.

5. **`class="clip"` on every timed element.** Required by HyperFrames. Without it, the element is invisible to the player.

6. **`data-start`, `data-duration`, `data-track-index` on every clip.** No exceptions. Same-track clips cannot overlap — use different track indices.

7. **No `Math.random()`.** HyperFrames requires deterministic compositions. Use seeded PRNG (mulberry32) for any pseudo-random values.

8. **All GSAP timelines start `{ paused: true }` and register to `window.__timelines["comp-id"]`.** The HyperFrames player controls playback — never call `tl.play()`.

9. **Never `position: absolute` on `.scene-content` containers.** Use `width:100%; height:100%; padding:Npx; display:flex`. Reserve `position:absolute` for decorative elements only.

10. **Music: separate `<audio>` element with `data-track-index`.** Video must be `muted playsinline`. Never put audio in a `<video>` element.

11. **Read `references/cut-patterns.md` AND `references/tone-presets.md` before generating any HTML.**

12. **Never dump HTML in chat.** Save to file. Show summary only.

---

## Step 1: Intake

**Required:**
- `key_messages` — 3-5 punchy lines to flash on screen (user must write these)

**Optional parameters and defaults:**

| Parameter | Default | Description |
|---|---|---|
| brand_assets | none | Logo URL/path, brand colors (hex), key screenshots |
| tone | energetic | energetic / cinematic / emotional / professional |
| music | none | File path, or BPM/genre string (e.g. "128bpm electronic") |
| duration | 60 | 30 / 60 / 90 seconds |
| aspect_ratio | 9:16 | 9:16 (1080x1920) / 16:9 (1920x1080) |
| cut_style | auto | fast (1-2s) / cinematic (3-5s) — auto derives from tone |
| end_card | auto | Logo + tagline + CTA URL for Land section |

`cut_style` auto-defaults: energetic → `fast`; professional → `fast` (2s); cinematic → `cinematic`; emotional → `mixed`

**If `key_messages` is missing, ask exactly:**

> "To generate the sizzle reel, I need your key messages — the exact phrases that will flash on screen. Give me 3-5 punchy lines. These are the most important thing you're writing for this video.
>
> Examples: 'Used by 500+ growth teams' / 'From days to minutes' / 'Works with Claude, Codex, Gemini'
>
> Also useful: tone (energetic/cinematic/emotional/professional), duration (30/60/90s), any brand colors or logo URL."

If key_messages are present → proceed to Step 2 immediately.

---

## Step 2: Install HyperFrames

Install HyperFrames skills (first time only — skip if already installed):

```bash
npx skills add heygen-com/hyperframes
```

Verify environment:
```bash
node --version   # must be >= 22
ffmpeg -version  # must be present
```

Scaffold the project:
```bash
npx hyperframes init sizzle-[slug] --example kinetic-type --non-interactive
cd sizzle-[slug]
```

Slug: kebab-case from end_card brand name or first key_message, max 25 chars.

---

## Step 3: Internal Architecture (never shown to user)

**1. Derive cut-point timing from `duration` + `cut_style`:**

| Section | 30s | 60s | 90s |
|---|---|---|---|
| Cold Open | 0-5s | 0-5s | 0-8s |
| Build | 5-25s | 5-40s | 8-65s |
| Peak | 25-28s | 40-55s | 65-80s |
| Land | 28-30s | 55-60s | 80-90s |

Convert every boundary to milliseconds. Calculate per-scene duration from `cut_style`:
- `fast`: 1.2s-1.8s per message (use 1.5s default)
- `cinematic`: 3.5s-5.0s per message (use 4.0s default)
- `mixed`: 2.0s-4.0s varying by section energy

**2. Map key_messages to scenes:**
- Cold Open (1 scene): one impact stat or question — NO brand name, builds intrigue
- Build: one scene per key_message
- Peak: repeat the strongest message at double scale, or combine 2 messages in rapid flash
- Land: brand name + tagline + CTA URL

**3. Detect beat sync if music provided:**
```bash
npx hyperframes tts --analyze-beats [music-file]
```
If unavailable, calculate from BPM: `beat_ms = 60000 / BPM`. Align cuts to every 2nd beat.

**4. Select tone preset** — read `references/tone-presets.md` for CSS tokens.

**5. Declare rhythm pattern** — write comment at top of script:
```js
// RHYTHM: flash-sequence
// Cold Open [0-5000ms]: stat
// Build [5000-40000ms]: msg-1(1500ms)|flash|msg-2(1500ms)|flash|msg-3(1500ms)|flash|msg-4(1500ms)|flash|build-accum(10000ms)
// Peak [40000-55000ms]: msg-strongest(1200ms)|flash|msg-2nd(1200ms)|flash|HOLD(5600ms)
// Land [55000-60000ms]: logo+tagline+cta
```

**6. Determine pixel dimensions:**
- `9:16` → W=1080, H=1920 (default — Instagram Reels, TikTok, YouTube Shorts)
- `16:9` → W=1920, H=1080

---

## Step 4: HyperFrames HTML Composition

Read `references/cut-patterns.md` and the HyperFrames skill (`/hyperframes`) before writing any code.

**Required HTML skeleton:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
[font CDN link from tone preset]
<style>
:root {
  [all CSS tokens from tone preset]
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
</style>
</head>
<body>
<div
  data-composition-id="sizzle-[slug]"
  data-width="[W]"
  data-height="[H]"
  style="position:relative;width:[W]px;height:[H]px;overflow:hidden;background:var(--bg)"
>

  [if cut-flash: true]
  <div id="cut-flash"
    style="position:absolute;inset:0;background:var(--cut-flash-bg);opacity:0;pointer-events:none;z-index:200"></div>
  [end if]

  [if film-grain: true]
  <canvas id="grain-overlay"
    width="240" height="135"
    style="position:absolute;inset:0;width:[W]px;height:[H]px;pointer-events:none;opacity:0.022;mix-blend-mode:overlay;z-index:50"></canvas>
  [end if]

  [if vignette: true]
  <div id="vignette-overlay"
    style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 35%,rgba(0,0,0,0.65) 100%);pointer-events:none;z-index:51"></div>
  [end if]

  <!-- Scenes — one div per scene -->
  <div id="scene-cold"
    class="clip"
    data-start="0"
    data-duration="5"
    data-track-index="0"
    style="position:absolute;inset:0;opacity:0"
  >
    <div class="scene-content" style="width:100%;height:100%;padding:120px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-sizing:border-box">
      [cold open content — one stat or impact phrase, no brand name]
    </div>
  </div>

  [one div per Build scene, data-start increments by cut duration]
  [Peak scene(s)]
  [Land scene — brand name + tagline + CTA]

  [if music provided]
  <audio id="music"
    class="clip"
    data-start="0"
    data-duration="[total_duration]"
    data-track-index="10"
    data-volume="0.85"
    src="[music_path]"
  ></audio>
  [end if]

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
  // ── RHYTHM DECLARATION ──────────────────────────────────────────────────────
  // RHYTHM: [flash-sequence | cinematic-hold | beat-sync | mixed]
  // Cold Open [0-Nms]: ...
  // Build [N-Nms]: ...
  // Peak [N-Nms]: ...
  // Land [N-Nms]: ...

  // ── SEEDED PRNG (for grain only — no other random values) ───────────────────
  function mulberry32(seed) {
    return function() {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  [if film-grain: true]
  // ── FILM GRAIN (cinematic/emotional only) ───────────────────────────────────
  const grainCanvas = document.getElementById('grain-overlay');
  const grainCtx = grainCanvas ? grainCanvas.getContext('2d') : null;
  // Grain updated by GSAP ticker (not per-frame capture — HyperFrames handles this)
  [end if]

  // ── GSAP TIMELINE ───────────────────────────────────────────────────────────
  const tl = gsap.timeline({ paused: true });

  // ── COLD OPEN ───────────────────────────────────────────────────────────────
  [cold open entrance and exit tweens — see cut-patterns.md for exact pattern]

  // ── BUILD SECTION ───────────────────────────────────────────────────────────
  [per-message tweens — flash-sequence or cinematic-hold from cut-patterns.md]

  // ── PEAK SECTION ─────────────────────────────────────────────────────────────
  [peak tweens — same pattern as build but tighter timing]

  // ── LAND SECTION ─────────────────────────────────────────────────────────────
  [land entrances — logo, tagline, CTA. No exit — holds to end]

  // ── TIMELINE REGISTRATION ────────────────────────────────────────────────────
  window.__timelines = window.__timelines || {};
  window.__timelines["sizzle-[slug]"] = tl;
  </script>
</div>
</body>
</html>
```

**Design quality rules:**
- Cold open stat: ≥160px font size for 16:9, ≥100px for 9:16
- Key messages: ≥80px font size — readable at a glance
- Land section brand name: ≥120px for 16:9
- All colors from preset token variables — no free hex except `var(--accent)` literal hex inside canvas `fillStyle`
- `scene-content` always uses `padding + flex` — never `position:absolute` on content container
- `class="clip"` on every element with `data-start`

---

## Step 5: Self-QA (fix every failure before Step 6)

**Content:**
- [ ] `key_messages` — each phrase appears exactly once, no duplicates
- [ ] Brand name appears ONLY in Land section (not cold open, not build, not peak)
- [ ] Cold open contains NO brand name and NO product name — only stat or impact phrase
- [ ] Land section has: brand name + tagline + CTA URL (three elements minimum)
- [ ] end_card CTA URL present on final frame

**HyperFrames contract:**
- [ ] `class="clip"` on every element with `data-start`
- [ ] `data-start`, `data-duration`, `data-track-index` on every clip
- [ ] `data-composition-id` on the root composition div
- [ ] `window.__timelines["sizzle-[slug]"] = tl` registered
- [ ] All timelines start `{ paused: true }`
- [ ] No `Math.random()` — seeded PRNG only
- [ ] No `tl.play()` or `tl.resume()` calls

**GSAP / Layout:**
- [ ] `gsap.from()` for all entrances (FROM offscreen TO CSS position)
- [ ] `gsap.to()` for all exits (FROM CSS position TO offscreen)
- [ ] No `position:absolute` on `.scene-content` containers
- [ ] Rhythm pattern declared in comment at top of script

**Cut timing:**
- [ ] `fast` tone: average cut duration ≤ 2.0s
- [ ] `cinematic` tone: average cut duration ≥ 3.0s
- [ ] Cut flash fires at every cut boundary for `energetic` tone (60ms, opacity 0→1→0)
- [ ] Same-track clips do NOT overlap (check all `data-track-index` groupings)

**SFX:**
- [ ] `window.__sfxTimeline` present and placed before timeline registration
- [ ] `word-hit` event per key message
- [ ] `whoosh` at Build → Peak transition boundary
- [ ] `cta-chime` at Land start
- [ ] No SFX fires before 500ms

---

## Step 6: Lint, Render, Output

```bash
npx hyperframes lint
npx hyperframes inspect --json
```

Fix all lint errors. Fix all inspect errors (text overflow, clip escaping containers). Then render:

```bash
npx hyperframes render --output sizzle/[slug]/sizzle-reel.mp4
```

Output:
```
## Sizzle Reel: [brand name from end_card]
Tone: [tone] | Duration: [N]s | Cut style: [cut_style] | Aspect: [ratio]
Rhythm: [declared pattern]

Sections
  Cold Open [0-Ns]:  [impact stat or phrase]
  Build     [N-Ns]:  [N key messages listed]
  Peak      [N-Ns]:  [strongest message at max scale]
  Land      [N-Ns]:  [brand name] + "[tagline]" + [CTA URL]

Files
  Source: sizzle/[slug]/index.html
  Output: sizzle/[slug]/sizzle-reel.mp4
```

---

## SFX Timeline (embed in every composition)

The same FFmpeg-synthesized SFX system as `vid-product-launch`. Place `window.__sfxTimeline` immediately before the GSAP timeline registration.

SFX type reference for sizzle reel:

| Type | Sound | Duration | Placement |
|---|---|---|---|
| `word-hit` | Sub punch (50Hz) + transient click (2.2kHz) + noise burst | 180ms | One per key_message scene start |
| `whoosh` | Two-band noise sweep (1.1kHz body + 4-8kHz air) | 700ms | At Build → Peak boundary |
| `cta-chime` | A major chord (440+554+659+880Hz) + aecho bell shimmer | 1.2s | Exactly at Land start |

```js
window.__sfxTimeline = [
  // one word-hit per key_message (computed from scene start times)
  { ms: MSG_1_START_MS,           sfx: 'word-hit',   vol: 0.50 },
  { ms: MSG_2_START_MS,           sfx: 'word-hit',   vol: 0.50 },
  { ms: MSG_3_START_MS,           sfx: 'word-hit',   vol: 0.50 },
  // ... repeat for each message
  { ms: PEAK_START_MS - 700,      sfx: 'whoosh',     vol: 0.55 },
  { ms: LAND_START_MS,            sfx: 'cta-chime',  vol: 0.65 },
];
```

Compute all `ms` values from declared section timing constants. Never hardcode.

---

## Prompt Tips (show when user asks for guidance)

> "Write the key messages yourself. They are the entire content of this video. 3 sharp lines beats 10 vague ones every time."
>
> "Choose music before choosing visuals. The BPM determines the cut style. The cut style determines every timing decision."
>
> "Cold open: one number. Not a sentence, not a tagline — one specific, surprising number. It earns 5 seconds of attention."
>
> "The Land section is not a credits page. Logo + one line + one URL. Anything more dilutes the CTA."
>
> "Match tone to channel. Energetic for social and Product Hunt. Cinematic for B2C premium and investor decks. Professional for enterprise conferences. Emotional for crowdfunding."

Good:
```
Sizzle reel, 60 seconds. Tone: energetic. Key messages: ['AI skills, ready to install' /
'52+ skills across GTM, content, research' / 'Works with Claude, Codex, Gemini' /
'Zero setup. Instant value.']. Music: 128bpm electronic. Cut style: fast.
End card: OpenDirectory + 'AI skills, ready to install' + 'opendirectory.dev'. Aspect: 9:16.
```

Bad:
```
hype video for our company
```
