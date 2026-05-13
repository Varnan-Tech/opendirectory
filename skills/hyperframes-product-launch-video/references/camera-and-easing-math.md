# Camera and Easing Math for Premium Motion

This document details the exact mathematical configurations required to achieve elite, Apple-style motion design within Hyperframes.

## Macro Zooms

Macro zooms create a sense of scale and premium quality by starting extremely close to an object and pulling back to reveal the full context.

### The Configuration
- **Start Scale**: 4.5 to 8.0
- **End Scale**: 1.0
- **Easing**: `expo.inOut` or `power4.inOut`
- **Duration**: 1.2s to 2.5s

### Implementation Pattern
```javascript
// Starting from a massive zoom to reveal the product
tl.from(".product-hero", {
  scale: 4.5,
  opacity: 0,
  duration: 1.8,
  ease: "expo.inOut"
}, 0);
```

## Snap Zooms

Snap zooms are used for high-energy transitions or to emphasize a specific feature. They use "overshoot" to create a physical, spring-like feel.

### The Configuration
- **Start Scale**: 0.5 or 1.5 (depending on zoom direction)
- **End Scale**: 1.0
- **Easing**: `back.out(1.5)` to `back.out(3.0)`
- **Duration**: 0.4s to 0.7s

### Implementation Pattern
```javascript
// Snapping into a feature highlight
tl.from(".feature-card", {
  scale: 0.8,
  opacity: 0,
  duration: 0.6,
  ease: "back.out(1.7)"
}, "+=0.2");
```

## Timeline Shifting and the Duration Bug

A common pitfall in Hyperframes is the "Duration Mismatch" where the GSAP timeline duration does not match the `data-duration` attribute of the clip.

### The Math
If your GSAP timeline is 10 seconds long, but your `data-duration` is 8 seconds, the last 2 seconds of your animation will be cut off. Conversely, if `data-duration` is 12 seconds, the video will freeze on the last frame for 2 seconds.

### The Fix: Dynamic Duration Calculation
Always ensure your `data-duration` is calculated based on the final tween's end time.

```javascript
// In your main script
const totalDuration = tl.duration();
document.querySelector('[data-composition-id="main"]').setAttribute('data-duration', totalDuration);
```

### Relative Offsets
Use relative offsets (`"+=0.2"`, `"-=0.1"`) or labels to maintain rhythm even when durations change.

```javascript
tl.addLabel("start")
  .from(".el1", { opacity: 0 }, "start")
  .from(".el2", { opacity: 0 }, "start+=0.2");
```

## Easing Signature Table

| Effect | Easing Function | Feel |
| :--- | :--- | :--- |
| Cinematic Reveal | `expo.inOut` | Smooth, premium, expensive |
| UI Interaction | `power2.out` | Responsive, snappy |
| Physical Impact | `bounce.out` | Playful, heavy |
| Feature Pop | `back.out(1.7)` | Energetic, modern |
| Constant Motion | `none` (linear) | Technical, precise |
