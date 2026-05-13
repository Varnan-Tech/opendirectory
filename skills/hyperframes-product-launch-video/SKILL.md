---
name: hyperframes-product-launch-video
description: Elite agent skill for creating premium "Product Launch Videos" using Hyperframes. Supports brand DNA extraction, scene-by-scene art direction, premium motion design (Apple-style camera, glassmorphism, typewriter physics), and perfect sound design sync. Use when asked to create a product launch video, promo video, or high-end feature announcement.
---

# Product Launch Video Skill

This skill guides you through the creation of high-end, premium product launch videos using Hyperframes. It emphasizes a structured workflow from brand discovery to final verification.

## Leveraging Official Hyperframes Skills

This skill acts as the Director and Architect for your video project. To ensure technical accuracy and access to the latest framework patterns, you must use it in conjunction with the official Hyperframes skills.

**Before writing any code, you should:**
1. Invoke the **official /hyperframes skill** to review composition rules, data-attribute semantics, and framework constraints.
2. Invoke the **official /gsap skill** for detailed timeline references, easing functions, and complex animation patterns.

By combining the strategic guidance of this skill with the technical documentation of the official skills, you will produce production-grade video compositions.

## Stateless Project Generation (CRITICAL)

This directory (`hyperframes-product-launch-video`) is a **read-only template and skill folder**. You must never write project-specific files here.

Whenever you create a new video project:
1. **Target Directory**: All project files must be created in the user's target video project folder (e.g., `my-new-video/` or `my-new-video/assets/`).
2. **Project DNA**: Generate the `brand_dna.json` inside the target project's `assets/` or root folder.
3. **Art Direction**: Save the final `ART_DIRECTION.md` inside the target project folder.
4. **No Side Effects**: Do not modify any files within this skill folder during a project run.

## Workflow

### 1. The Interrogation Phase (Brand DNA)
Before starting, you must understand the brand.
- **Website Analysis**: Use Playwright to visit the user's website. Extract brand colors, typography (fonts), and core value propositions.
- **Asset Request**: Ask the user for logos and icons. Specify the need for clean, transparent, tightly-cropped PNGs or SVGs.
- **Video Type Selection**: Ask if this is a 100% motion graphics video or a hybrid (e.g., Founder talking head + Hyperframes motion graphics).

### 2. The Planning Phase (Art Direction)
NEVER write HTML before planning.
- **Generate Art Direction**: Create an `ART_DIRECTION.md` document based on the Art Direction Template.
- **Scene Breakdown**: Define every second of the video, specifying visual action, camera movements, easing functions, and sound effects.

### 3. Implementation (Premium Motion Design)
Apply elite motion design principles. See Motion Design Patterns for code snippets.
- **Apple-Style Camera**: Use massive macro zooms and snap-zooms (`back.out`).
- **Eraser Reveal**: Staggered text opacity "eaten" by a sliding logo.
- **Clash/Shatter**: Physical impact effects using GSAP scatter.
- **Glassmorphism**: Premium UI elements with `backdrop-filter: blur(40px)`.
- **Typewriter Physics**: Bouncing spans that push the cursor.

### 4. Sound Design (SFX)
- **Shopping List**: Provide the user with a "Sound Design Shopping List" based on the storyboard.
- **Syncing**: Use `<audio data-start="...">` tags to match GSAP hits perfectly.

### 5. Verification & Troubleshooting
- **Gotchas**: Review Critical Gotchas to avoid common Hyperframes bugs (duration mismatches, target missing, etc.).
- **FFmpeg**: If rendering fails, guide the user to install FFmpeg locally.

## Best Practices
- **Atomic Scenes**: Keep scenes modular and strictly managed by `data-start` and `data-duration`.
- **Visibility Management**: Use `autoAlpha` for scene transitions to ensure clean seeking.
- **Layout vs. Transform**: Use physical dimensions for flexbox gaps, and transforms for visual flair.
