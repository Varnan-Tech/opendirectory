# Elite Motion Design Patterns: Apple-Style Reference

This guide provides the technical blueprints for achieving "Apple-level" motion quality using GSAP and modern web techniques.

---

## 1. Scroll-Driven Image Sequences (The Flipbook Effect)
Apple uses this for product teardowns and hero reveals. By scrubbing through pre-rendered image frames on a `<canvas>`, we avoid the performance bottlenecks of video or DOM manipulation.

### The Technique
- **Canvas Rendering**: Drawing pre-loaded images to a canvas is GPU-accelerated and avoids layout thrashing.
- **Proxy Object**: Use a simple object to track the current frame index, which GSAP animates.
- **Scrub Smoothing**: A `scrub` value of `0.5` to `1` adds a "physical" weight to the scroll.

```javascript
const canvas = document.querySelector("#hero-canvas");
const context = canvas.getContext("2d");
const frameCount = 120;
const images = [];
const airpods = { frame: 0 };

// Pre-load images into memory
for (let i = 0; i < frameCount; i++) {
  const img = new Image();
  img.src = `./assets/frames/hero_${i.toString().padStart(3, '0')}.jpg`;
  images.push(img);
}

// Scrub through frames
gsap.to(airpods, {
  frame: frameCount - 1,
  snap: "frame",
  ease: "none",
  scrollTrigger: {
    trigger: ".scroll-section",
    start: "top top",
    end: "+=300%",
    scrub: 0.5,
    pin: true
  },
  onUpdate: () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(images[Math.round(airpods.frame)], 0, 0);
  }
});
```

---

## 2. Kinetic Typography & Text Reveals
Text shouldn't just "appear"; it should arrive with intent.

### A. The "Apple Slide Up"
A clean, sophisticated reveal where text slides up from behind an invisible boundary.
- **Implementation**: Wrap text in a container with `overflow: hidden` or use `clip-path: inset(0 0 100% 0)`.
- **Animation**: Animate `yPercent: 100` to `0` with a `power4.out` ease.

```javascript
gsap.from(".reveal-text", {
  yPercent: 100,
  duration: 1.2,
  ease: "power4.out",
  stagger: 0.1,
  scrollTrigger: ".reveal-text"
});
```

### B. The "Shatter/Clash"
Simulates a physical impact where elements collide with text, causing it to scatter.
- **Implementation**: Split text into individual characters (spans).
- **Animation**: On impact, stagger random X/Y/Rotation values with an aggressive `expo.out` or `power4.out`.

```javascript
function triggerShatter() {
  gsap.to(".char", {
    x: () => gsap.utils.random(-500, 500),
    y: () => gsap.utils.random(-500, 500),
    rotation: () => gsap.utils.random(-720, 720),
    opacity: 0,
    duration: 0.8,
    ease: "power4.out",
    stagger: { amount: 0.3, from: "center" }
  });
}
```

---

## 3. The "Eraser" Pass (Masking)
A high-end transition where a moving element (like a logo) appears to "eat" or "erase" the content beneath it.

### The Technique
- **Opposing Staggers**: As the "Eraser" element moves from Left to Right, the text beneath it fades out with a stagger starting from the Right (`from: "end"`).
- **Timing**: The movement and the stagger must be perfectly synchronized.

```javascript
const tl = gsap.timeline();
tl.to(".eraser-logo", { x: "100vw", duration: 2, ease: "power2.inOut" })
  .to(".text-to-erase .char", { 
    opacity: 0, 
    scale: 0.8,
    stagger: {
      each: 0.05,
      from: "end" // Erase from the opposite direction of the logo
    },
    duration: 0.2 
  }, 0); // Start simultaneously
```

---

## 4. Cinematic Camera Moves
Simulate a physical camera lens to create depth and focus.

### A. The "Macro Pull-Out"
Starts extremely close to a detail (abstract/blurred) and pulls back to reveal the full context.
- **Animation**: Start at `scale: 4.5` with a heavy `blur(20px)`. Animate to `scale: 1` and `blur(0px)`.
- **Ease**: Use `expo.inOut` for a smooth, high-acceleration feel.

```javascript
gsap.fromTo(".product-detail", 
  { scale: 4.5, filter: "blur(20px)", opacity: 0 },
  { 
    scale: 1, 
    filter: "blur(0px)", 
    opacity: 1, 
    duration: 2.5, 
    ease: "expo.inOut" 
  }
);
```

### B. The "Emotional Snap Zoom"
Abruptly zooms into a specific UI element or label to simulate a user's sudden focus or a "lightbulb" moment.
- **Ease**: Use `back.out(1.7)` or `power4.out` to create a sharp, intentional "snap."

```javascript
gsap.to(".feature-highlight", {
  scale: 1.2,
  duration: 0.6,
  ease: "back.out(2)",
  boxShadow: "0 20px 50px rgba(0,0,0,0.3)"
});
```

---

## 5. Premium UI Styles

### Glassmorphism
Floating UI elements that feel like physical glass.
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}
```

### Typewriter Physics
Text that physically pushes a cursor, with each character having its own "bounce."
```javascript
gsap.from(".char", {
  opacity: 0,
  y: 10,
  stagger: 0.05,
  ease: "back.out(2)"
});
```
