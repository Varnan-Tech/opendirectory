![noise-to-linkedin-carousel](./cover.png)

# noise-to-linkedin-carousel

**noise-to-linkedin-carousel** turns rough notes, transcripts, and idea dumps into a LinkedIn-ready carousel content pack with a strong hook, clear slide-by-slide structure, and a CTA — built for founders, GTM teams, and technical marketers who think faster than they write.

## Install

```bash
npx "@opendirectory.dev/skills" install noise-to-linkedin-carousel --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!


## Why This Skill?

Founders and technical operators often think in fragments: voice notes, bullet dumps, rambling transcripts, or Slack thoughts. They have valuable insights but lack a repeatable workflow to convert those noisy inputs into highly readable, LinkedIn-native carousel content.

LinkedIn carousels routinely outperform single-image or text-only posts because they encourage swipe-through engagement and let you teach in a structured, visual way. While `linkedin-post-generator` focuses on crafting a single post, **noise-to-linkedin-carousel** is designed specifically to turn messy raw thinking into a multi-slide narrative that a founder, GTM engineer, or designer can immediately turn into a carousel asset.

This agent skill helps by taking that unstructured "noise" and transforming it into a structured asset pack containing:
- 3 strong cover hook options
- 5-9 correctly sized insight slides (one idea per slide)
- A clear narrative progression
- A custom CTA slide
- A supporting LinkedIn caption

## Prerequisites

- [OpenDirectory CLI](https://github.com/Varnan-Tech/opendirectory)
- An OpenDirectory-compatible agent (e.g., **Anti-Gravity** or **OpenCode**)

## Installation

Install directly into your agent via OpenDirectory:
```bash
npx "@opendirectory.dev/skills" install noise-to-linkedin-carousel --target anti-gravity
```
*(Replace `anti-gravity` with your preferred agent target.)*

## Usage Examples

Once installed, you can simply message your agent with noisy source material. 

**Example Prompt:**
> I recorded this rough voice note about why most devtools marketing fails. It’s a rant, not a clean outline. Here’s the transcript — turn this into a LinkedIn carousel I can hand to my designer:  
>  
> “okay so basically what i realized is that most devtools fail because they market features not use cases like everyone lists api endpoints and configs but nobody explains when you’d actually use this thing in production you know what i mean and founders think more features will solve it but the buyer just wants to know what problem disappears after they install you and how fast they get there”

**Sample Output Shape:**

- **Thesis:**  
  Most devtools fail because they market features instead of clear, real-world use cases.

- **Hooks (3 options):**  
  1. “90% of devtools die because they market features, not outcomes.”  
  2. “Your devtool doesn’t have a feature problem. It has a use-case problem.”  
  3. “If your devtool landing page looks like an API manual, this is for you.”

- **Slide Breakdown (example):**  
  - **Slide 1 – Cover (Hook):** One of the hooks above.  
  - **Slide 2 – Problem:** What most devtools marketing looks like today.  
  - **Slide 3 – Insight:** Buyers buy outcomes and solved problems, not endpoints.  
  - **Slide 4 – Insight:** Why “more features” doesn’t fix the positioning gap.  
  - **Slide 5 – Example:** Before/after example of reframing features as use cases.  
  - **Slide 6 – Framework:** Simple checklist to rewrite your own devtool pitch.  
  - **Slide 7 – CTA:** Ask readers to audit their landing page or share with a founder.

- **Caption:**  
  A LinkedIn-ready caption that tees up the carousel, adds 1–2 sentences of context, and ends with a natural CTA (e.g., “Reply ‘DEVS’ if you want a teardown of your current page”), plus 2–4 relevant hashtags.

## Under the Hood

Unlike simple text generators, this skill operates as a structured workflow:
1. **Thesis Extraction** - It strips away the noise to find the actual point.
2. **Hook Selection** - It maps the thesis to known high-performing LinkedIn hook patterns.
3. **Slide Constraint Enforcement** – It forces one main idea per slide and short, punchy copy so the deck feels like a high-signal LinkedIn carousel, not a pasted blog post.

## File Architecture

- `SKILL.md` - Core workflow instructions and formatting constraints.
- `references/output-format.md` - The deterministic output schema.
- `references/hook-patterns.md` - High-performing hook structures.
- `references/slide-types.md` - Rules for cover, context, insight, and CTA slides.
- `references/quality-checklist.md` - GTM-aligned checks run before returning output.

## Contributing

Pull requests to refine hook patterns, add new slide structures, or include helper scripts that refine raw transcripts are welcome.
