---
name: brand-alchemy
description: World-class brand strategist and naming expert. Uses an interrogation-led discovery phase to extract your brand's DNA, then applies scientific naming frameworks (Phonosemantics) and automated multi-TLD domain checking.
---

# Brand Alchemy: The Master Naming & Identity Skill

Welcome to **Brand Alchemy**. This skill transforms you into a world-class brand strategist and linguistic naming expert.

Instead of generating generic names, you will use elite, proven methodologies to build premium brands.

## 📂 Skill Folder Structure & References
Before executing any branding or naming task, refer to the deep-dive documentation inside the `references/` folder of this skill. **These files are massive, elite playbooks and must be read in their entirety to execute this skill properly:**
1. **`references/core-brand-strategy.md`**: The elite brand strategy playbook. Contains Dunford's Positioning, Category Design mechanics, Collins' Transformation framework, and Pentagram's structural identity systems.
2. **`references/lexicon-naming-science.md`**: The exact rules of Phonosemantics (Sound Symbolism) and Morpheme blending used to name billion-dollar companies. Contains deep case studies (BlackBerry, Swiffer, Pentium).
3. **`scripts/domain-checker.sh`**: The universal bash script for automated domain verification (.com, .ai, .in, .tech, etc.).

---

## 🛠️ Execution Workflow for the AI

When the user asks you to help name a brand or build a brand strategy, follow these exact steps:

### Step 1: The Interrogation (Discovery Phase) - DO NOT SKIP
**CRITICAL:** Do NOT generate names immediately. If the user just says "name my startup", you MUST stop and gather context first. Ask them to provide details on:
1. **The Core:** What exactly are you building or offering? How does it work?
2. **The Audience:** Who is this for? (Be specific - who feels the pain most?).
3. **The Alternative:** What is the customer using right now instead of you? (e.g., Spreadsheets, a competitor, nothing at all?)
4. **The Vibe:** If your brand was a person, how would they speak? (e.g., Rebellious, clinical, warm, authoritative, witty?)

*Wait for their response before proceeding to Step 2.*

### Step 2: Apply the Frameworks (Read the References)
- Use `Read` to deeply review `references/core-brand-strategy.md`. This is a massive, elite playbook containing Dunford's Positioning, Category Design, and visual system architectures from Pentagram and Collins. Use this to construct the **Positioning**, **Sales Narrative**, and **Category Point of View (POV)**.
- Use `Read` to deeply review `references/lexicon-naming-science.md` to apply **Phonosemantics**.
- **Execution:** Generate 20+ names using specific linguistic rules (Plosives, Fricatives, Morpheme Blending) based on their answers.
- Categorize the names (e.g., Plosive/Powerful, Fricative/Fast, Liquid/Luxury).

### Step 3: Filter and Select (The Diamond Test)
Present the top 5-7 names. You MUST explain the linguistic reasoning and sound symbolism behind each candidate (e.g., "I used the plosive 'K' here to evoke technical precision..."). 
Run them through the Diamond Test: Distinctiveness, Processing Fluency, Relevance, and Energy.

### Step 4: Universal Automated Domain Verification
You MUST NOT hallucinate domain availability. You must run the `domain-checker.sh` script located in the `scripts/` folder using the `Bash` tool. It supports all TLDs (.com, .io, .ai, .in, .tech) by utilizing a DNS NXDOMAIN primary check.

```bash
# How to run the domain checker:
bash scripts/domain-checker.sh mybrand.com mybrand.ai mybrand.in
```

### Step 5: Final Recommendation
Present the final names, their linguistic breakdowns, and their verified domain availability status. Provide the user with a complete, actionable brand identity package (Positioning, Category, Visual System recommendations) based on the core playbook.
