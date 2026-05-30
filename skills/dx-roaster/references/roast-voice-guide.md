# Roast Voice Guide

The roast is a 3–5 paragraph review of the repo's DX. Tone is controlled by user input. Always reference specific findings from the scan — never generic platitudes.

---

## Tone: `brutal`

Voice: a battle-scarred CTO who has seen every kind of bad README. Cutting, specific, dryly funny. Punches the work, not the person.

**Do:**
- Quote bad lines verbatim and explain why they fail
- Compare to known good examples ("This is where stripe/stripe-node would have a gif")
- Use vivid imagery: "This README opens like a tax filing"
- Score is harsh — a 6 here is a 4 elsewhere

**Don't:**
- Never name the maintainer or contributors
- No personal attacks
- No "you're stupid" — say "the README is unclear", not "you wrote unclear stuff"

**Opening line example:**
> "Three minutes after landing on this repo, I have learned that it uses TypeScript, has 12 GitHub Actions checks, and is licensed under MIT. I have learned nothing about what it actually does."

---

## Tone: `honest` (default)

Voice: an experienced engineer giving a code review to a friend. Direct, kind, specific. Calls out problems but offers paths.

**Do:**
- Lead with what works (1–2 sentences) before what doesn't
- Be precise about line numbers, sections, and what's missing
- Suggest specific fixes alongside the critique
- Acknowledge effort where present

**Don't:**
- No sugar-coating that obscures the issue
- No vague "could be better" — always say what specifically

**Opening line example:**
> "The install instructions are clean — one command, two lines, no fluff. The README around them is the problem: a new user has to scroll past 47 lines of badges and a logo to understand what this thing does."

---

## Tone: `kind`

Voice: an encouraging mentor. Specific about issues but framed as opportunities. Never harsh. Best for solo maintainers and first-time OSS authors.

**Do:**
- Use "could", "consider", "an opportunity"
- Lead with strengths, position fixes as next-level moves
- Acknowledge that DX work is invisible labor

**Don't:**
- Don't be vague — kind still means specific
- Don't praise things that don't deserve praise

**Opening line example:**
> "There's clearly a thoughtful project here. The quick-start example is unusually clear and runs as written. The next leap forward — moving from 'good for engineers who already get it' to 'instantly understood by anyone' — comes down to a few specific moves at the top of the README."

---

## Structural rules (all tones)

1. **First paragraph:** the verdict. What the repo does well + the big DX gap.
2. **Body paragraphs:** specific examples tied to scoring dimensions. Reference lines, files, missing assets.
3. **Closing paragraph:** the path forward. Reference the action plan file.

Length: 250–500 words.

Every roast must reference at least 3 specific findings from the scan. Never write "documentation could be better" — say "the docs/ folder has 4 files, all empty stubs except api-reference.md".
