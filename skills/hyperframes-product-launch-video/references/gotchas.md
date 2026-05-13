# Critical Hyperframes Gotchas

Avoid these common pitfalls to ensure your video renders perfectly.

## 1. The "Blank Scene" Bug (Duration Mismatch)
**Problem**: GSAP timelines MUST NOT exceed the `data-duration` on the HTML `.clip` container.
**Solution**: If you add 2 seconds to a scene's animation, you MUST manually shift every subsequent `data-start`, `data-duration`, and GSAP time parameter forward by +2 seconds. Otherwise, Hyperframes destroys the DOM element while GSAP is still animating it, resulting in a blank screen.

## 2. GSAP Target Missing
**Problem**: GSAP cannot animate elements that don't exist yet.
**Solution**: Always ensure dynamic elements are fully created and appended to the DOM *before* creating the GSAP timeline. Use `window.addEventListener('DOMContentLoaded', ...)` or ensure your script runs after the HTML is parsed.

## 3. TextPlugin HTML Breakage
**Problem**: `TextPlugin` often breaks when typing out complex HTML with nested spans or images.
**Solution**: DO NOT use `TextPlugin` for complex HTML. Instead, hardcode the HTML, start it invisible (`autoAlpha: 0`), and use CSS clip-path masks or `autoAlpha` staggers to reveal it.

## 4. Transform Scale vs. Physical Gap
**Problem**: `transform: scale()` visually enlarges elements but does not change their flexbox/grid hitbox.
**Solution**: If you need a logo to be bigger without overlapping its neighbors in a row, change its actual `height`/`width` properties so the browser calculates the layout gap correctly. Use transforms only for animation flair.

## 5. Visibility Hard Kills
**Problem**: Overlapping scenes can cause rendering artifacts or performance drops.
**Solution**: Use `autoAlpha` (which toggles `opacity` and `visibility`) to strictly manage scene transitions. Ensure previous scenes are fully hidden before the next one starts.

## 6. FFmpeg Installation
**Problem**: Rendering fails because FFmpeg is missing from the environment.
**Solution**: Provide OS-agnostic instructions for installing FFmpeg. The renderer typically looks for `ffmpeg` in your system `PATH`.
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`
- **Windows:** `choco install ffmpeg`
If you cannot install it system-wide, use the local binary wrapper:
```bash
npm install @ffmpeg-installer/ffmpeg
```
Ensure your render script is configured to use the path provided by `require('@ffmpeg-installer/ffmpeg').path`.
