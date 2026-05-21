# Cut Patterns — vid-sizzle-reel

Four named rhythm patterns with GSAP timing examples.
Read before declaring rhythm in Step 3. Declare the rhythm pattern explicitly before writing any HTML.

---

## flash-sequence

**Use for:** `energetic` tone. Fast 1-2s cuts with white flash at every transition.

**Rhythm notation:** `flash-flash-flash-HOLD-flash-flash-PEAK-land`

**Flash element (place in every scene, hidden by default):**
```html
<div id="cut-flash"
  style="position:fixed;inset:0;background:var(--cut-flash-bg);opacity:0;pointer-events:none;z-index:200"></div>
```

**GSAP cut flash (fire at every scene end time `T`):**
```js
// Fire at T = scene end, duration = 0.06s
tl.to("#cut-flash", { opacity: 1, duration: 0.03, ease: "none" }, T);
tl.to("#cut-flash", { opacity: 0, duration: 0.03, ease: "none" }, T + 0.03);
```

**Full scene GSAP pattern (1.5s scene starting at T):**
```js
// Build end-state in CSS first. Then:
// Entrance: slam-in
tl.fromTo(".msg-1", { scale: 1.08, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.12, ease: "power3.out" }, T + 0.06);
// Hold for 1.2s
// Exit: flash handles visual cut — no explicit exit tween needed for flash-sequence
// Cut flash at T + 1.5
tl.to("#cut-flash", { opacity: 1, duration: 0.03, ease: "none" }, T + 1.47);
tl.to("#cut-flash", { opacity: 0, duration: 0.03, ease: "none" }, T + 1.50);
```

**Scene count per duration:**
- 30s: 12-18 cuts (avg 1.7s each)
- 60s: 25-35 cuts (avg 1.8s each)
- 90s: 35-50 cuts (avg 1.9s each)

---

## cinematic-hold

**Use for:** `cinematic` and `emotional` tones. 3-5s scenes with slow cross-dissolve transitions.

**Rhythm notation:** `slow-SLOW-hold-BREATHE-slow-PEAK-land`

**Dissolve pattern (no flash element — opacity handled by GSAP):**
```js
const SCENE_DUR = 4.0;   // agent adjusts per section
const FADE_IN   = 0.7;   // entrance duration
const FADE_OUT  = 0.5;   // exit overlap before next scene

// Entrance at T
tl.from(".msg-1", { opacity: 0, filter: "blur(8px)", duration: FADE_IN, ease: "power2.out" }, T);
// Exit at T + SCENE_DUR - FADE_OUT
tl.to(".msg-1",   { opacity: 0, y: -15, duration: FADE_OUT, ease: "power2.in" }, T + SCENE_DUR - FADE_OUT);
```

**Overlap:** next scene entrance starts `FADE_OUT` before current scene exits — creates cross-dissolve feel.

**Scene count per duration:**
- 30s: 6-8 scenes (avg 4s each)
- 60s: 12-16 scenes (avg 4s each)
- 90s: 18-24 scenes (avg 4s each)

---

## beat-sync

**Use for:** Any tone when `music` is provided as a file. Cut points derived from audio analysis.

**How to get cut points:**
```bash
npx hyperframes tts --analyze-beats [music-file]
# Outputs JSON: { beats: [0.48, 0.96, 1.44, ...], bpm: 128 }
```

If `npx hyperframes tts` beat analysis is unavailable, calculate from BPM:
```
beat_interval_ms = 60000 / BPM
# 128 BPM → 468.75ms per beat
# Align cuts to every 2nd or 4th beat for readability
# 128 BPM → cut every 937.5ms (2 beats) or every 1875ms (4 beats)
```

**GSAP pattern (cut on beat offset `B`):**
```js
const BEATS = [0.94, 1.88, 2.81, 3.75, 5.63, 7.50]; // agent fills from analysis
BEATS.forEach((b, i) => {
  // Exit current element
  tl.to(`.msg-${i}`, { opacity: 0, scale: 0.95, duration: 0.08, ease: "power2.in" }, b - 0.08);
  // Cut flash (energetic) or instant cut
  if (tone === 'energetic') {
    tl.to("#cut-flash", { opacity: 1, duration: 0.03 }, b - 0.03);
    tl.to("#cut-flash", { opacity: 0, duration: 0.03 }, b);
  }
  // Entrance next element
  tl.from(`.msg-${i + 1}`, { opacity: 0, y: 20, duration: 0.15, ease: "power3.out" }, b + 0.02);
});
```

---

## build-sequence

**Use for:** Build section of all tones. Staggered sequential reveals — no hard cuts, elements accumulate.

**Use case:** Multiple data points, feature lists, or stats that build up within a single scene.

**Pattern: elements appear and stay (no exit until scene ends)**
```js
const ITEMS = [".item-1", ".item-2", ".item-3"]; // max 4 items
const SCENE_START = 10.0;
const ITEM_STAGGER = 1.4;  // seconds between each item entrance

ITEMS.forEach((sel, i) => {
  tl.from(sel, {
    opacity: 0,
    y: 30,
    duration: 0.5,
    ease: "power3.out"
  }, SCENE_START + i * ITEM_STAGGER);
});

// Exit all together at scene end
tl.to(ITEMS, {
  opacity: 0,
  y: -20,
  stagger: 0.05,
  duration: 0.4,
  ease: "power2.in"
}, SCENE_START + ITEMS.length * ITEM_STAGGER + 1.0);
```

**Use when:** Build section has 3+ key messages that benefit from accumulation. Switch to `flash-sequence` or `cinematic-hold` for single-message-per-scene pacing.

---

## Rhythm Declaration Format

Before writing HTML, write this comment at the top of the composition script:

```js
// RHYTHM: flash-sequence
// Cold Open [0-5s]:   one-stat | flash
// Build     [5-40s]:  msg-1(1.5s) | flash | msg-2(1.5s) | flash | msg-3(1.5s) | flash | msg-4(2s) | flash | build-accum(8s)
// Peak      [40-55s]: full-speed-flash | msg-5(1s) | flash | msg-6(1s) | flash | msg-7(1s) | HOLD(4s)
// Land      [55-60s]: logo-fade | tagline | cta
```

This is the reference all subsequent timing decisions check against. If a scene doesn't fit the declared rhythm, adjust the scene — not the rhythm.
