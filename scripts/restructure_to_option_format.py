#!/usr/bin/env python3
import os
import re
import urllib.parse

SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'skills')
ROOT_README = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
MANUS_VIDEO_URL = "https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm"
CLAUDE_VIDEO_URL = "https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c"


def skill_name(filepath):
    return os.path.basename(os.path.dirname(filepath))


def manus_link(skill_name):
    url = f"https://github.com/Varnan-Tech/opendirectory/tree/main/skills/{skill_name}"
    encoded = urllib.parse.quote(url, safe='')
    return f"https://manus.im/import-skills?githubUrl={encoded}&utm_source=opendirectory"


def has(content, header):
    return header in content


def extract_content(content, pattern):
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else ""


def restructure_skill_readme(filepath):
    name = skill_name(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    h1 = has(content, '### Step 1: Download the skill')
    h2 = has(content, '### Step 2: Install')
    h3 = has(content, '### Step 3: Install in Manus AI')
    if not h1 and not h2 and not h3:
        return False, ["skipped - no Step sections"]

    step1 = extract_content(content, r'### Step 1: Download the skill from GitHub[^\n]*\n(.*?)(?=\n### |\n## |\Z)')
    step2 = extract_content(content, r'### Step 2:.*?[^\n]*\n(.*?)(?=\n### |\n## |\Z)')
    step3 = extract_content(content, r'### Step 3: Install in Manus AI[^\n]*\n(.*?)(?=\n### |\n## |\Z)')

    v_match = re.search(r'(<video[^>]*></video>)', step2) if step2 else None
    step2_video = v_match.group(1) if v_match else ""
    n_match = re.search(r'(> \*\*Note:\*\*.*?)(?=\n\n|\n$|\Z)', step2, re.DOTALL) if step2 else None
    step2_note = n_match.group(1).strip() if n_match else ""

    rest = step2
    if step2_video:
        rest = rest.replace(step2_video, '', 1).strip()
    if step2_note:
        rest = rest.replace(step2_note, '', 1).strip()
    step2_instructions = rest.strip()

    s3n = re.search(r'(>.*)', step3, re.DOTALL) if step3 else None
    step3_note = s3n.group(1).strip() if s3n else ""
    step3_text = step3.replace(step3_note, '', 1).strip() if step3_note and step3 else (step3.strip() if step3 else "")

    ml = manus_link(name)
    option_d = "\n".join([
        "### Option D: Manus AI\n",
        f'<video src="{MANUS_VIDEO_URL}" controls width="100%"></video>',
        "",
        f"[**Install in Manus AI**]({ml})",
        "",
        step3_text if step3_text else "",
        "",
        step3_note if step3_note else ""
    ])

    option_c = "### Option C: Claude Code Native\n\nRun this command inside Claude Code:\n\n```bash\n/plugin install opendirectory-gtm-skills@opendirectory-marketplace\n```"

    option_b_parts = ["### Option B: Claude Desktop App\n"]
    option_b_parts.append(f'<video src="{CLAUDE_VIDEO_URL}" controls width="100%"></video>')
    option_b_parts.append("")
    if step1:
        option_b_parts.append("**Step 1: Download the skill from GitHub**")
        option_b_parts.append("")
        option_b_parts.append(step1)
        option_b_parts.append("")
    if step2_instructions:
        option_b_parts.append("**Step 2: Install in Claude**")
        option_b_parts.append("")
        option_b_parts.append(step2_instructions)
        option_b_parts.append("")
    if step2_note:
        option_b_parts.append(step2_note)
    option_b = "\n".join(option_b_parts).rstrip()

    npx_m = re.search(r'## Install(?:ation)?\n\n```bash\n(npx[^\n]+)\n```', content)
    npx_cmd = npx_m.group(1) if npx_m else f'npx "@opendirectory.dev/skills" install {name} --target claude'
    option_a = f"### Option A: npx CLI (Recommended)\n\nNo global install. Always runs the latest version.\n\n```bash\n{npx_cmd}\n```"

    im = re.search(r'(## Install(?:ation)?\n)(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not im:
        return False, ["no ## Install section"]

    new_body = "\n\n".join([option_a, option_b, option_c, option_d]) + "\n"
    content = content[:im.start()] + im.group(1) + new_body + content[im.end():]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, ["restructured to Option format"]

    return False, ["no changes"]


def update_root_readme():
    with open(ROOT_README, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    if MANUS_VIDEO_URL in content:
        return False

    p = re.compile(r'(### Option D: Manus AI\n\n)')
    r = r'\1' + f'<video src="{MANUS_VIDEO_URL}" controls width="100%"></video>\n\n'
    if p.search(content):
        content = p.sub(r, content, count=1)
        if content != original:
            with open(ROOT_README, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    return False


def main():
    updated = 0
    skipped = 0
    errors = 0
    log = []

    for d in sorted(os.listdir(SKILLS_DIR)):
        p = os.path.join(SKILLS_DIR, d)
        if not os.path.isdir(p):
            continue
        rp = os.path.join(p, 'README.md')
        if not os.path.exists(rp):
            continue
        try:
            ok, msgs = restructure_skill_readme(rp)
            if ok:
                updated += 1
                log.append(f"  UPDATED: {d}")
            else:
                skipped += 1
                log.append(f"  SKIPPED: {d} - {msgs[0]}")
        except Exception as e:
            errors += 1
            log.append(f"  ERROR: {d} - {e}")

    print(f"Updated: {updated}  Skipped: {skipped}  Errors: {errors}")
    for line in log:
        print(line)

    print("\n--- Root README ---")
    if update_root_readme():
        print("UPDATED: README.md (added Manus video to Option D)")
    else:
        print("No changes needed")


if __name__ == '__main__':
    main()
