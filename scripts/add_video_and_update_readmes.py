import os
import re

VIDEO_URL = "https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c"
VIDEO_TAG = f'<video src="{VIDEO_URL}" controls width="100%"></video>'

MANUS_SECTION = """### Step 3: Install in Manus AI

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.

"""


def has_video_in_step2(content):
    step2_match = re.search(r'### Step 2:.*?Install.*?\n', content, re.DOTALL)
    if not step2_match:
        return False
    start = step2_match.end()
    next_heading = re.search(r'\n###?\s', content[start:])
    if next_heading:
        step2_content = content[start:start + next_heading.start()]
    else:
        step2_content = content[start:]
    return '<video' in step2_content


def add_video_to_step2(content):
    pattern = r'(### Step 2:.*?Install.*?in Claude[^\n]*\n)'
    replacement = r'\1' + VIDEO_TAG + '\n'
    return re.sub(pattern, replacement, content, count=1)


def has_manus_section(content):
    return '### Step 3: Install in Manus AI' in content


def has_video_tutorial_section(content):
    return '### Video Tutorial' in content


def remove_video_tutorial(content):
    pattern = r'### Video Tutorial\nWatch this quick video to see how it\'s done:\n\nhttps://github.com/user-attachments/assets/\S+\n\n?'
    return re.sub(pattern, '', content)


def add_manus_section(content):
    note_pattern = r'(> \*\*Note:\*\*.*?folder that contains the `SKILL\.md` file!\n\n)'
    match = re.search(note_pattern, content)
    if match:
        return content[:match.end()] + MANUS_SECTION + content[match.end():]
    step2_end = re.search(r'(### Step 2:.*?(?=\n### |\n## |\Z))', content, re.DOTALL)
    if step2_end:
        return content[:step2_end.end()] + '\n' + MANUS_SECTION + content[step2_end.end():]
    return content


def update_skill_readme(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    if has_video_tutorial_section(content):
        content = remove_video_tutorial(content)
        changes.append('removed Video Tutorial')

        if not has_video_in_step2(content):
            content = add_video_to_step2(content)
            changes.append('added <video> to Step 2')

        if not has_manus_section(content):
            content = add_manus_section(content)
            changes.append('added Manus Step 3')

    elif has_manus_section(content) and not has_video_in_step2(content):
        content = add_video_to_step2(content)
        changes.append('added <video> to Step 2')

    elif not has_manus_section(content) and not has_video_in_step2(content):
        if not has_video_in_step2(content):
            content = add_video_to_step2(content)
            changes.append('added <video> to Step 2')
        if not has_manus_section(content):
            content = add_manus_section(content)
            changes.append('added Manus Step 3')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes

    return False, []


def update_template_script():
    filepath = os.path.join(os.path.dirname(__file__), 'update_skill_readmes.py')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_snippet = """### Video Tutorial
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

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!"""

    new_snippet = f"""### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude

<video src="{VIDEO_URL}" controls width="100%"></video>

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

### Step 3: Install in Manus AI

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus."""

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    base_dir = 'skills'
    updated_count = 0
    skipped_count = 0
    detail_log = []

    for skill_dir in sorted(os.listdir(base_dir)):
        if not os.path.isdir(os.path.join(base_dir, skill_dir)):
            continue
        readme_path = os.path.join(base_dir, skill_dir, 'README.md')
        if not os.path.exists(readme_path):
            continue

        updated, changes = update_skill_readme(readme_path)
        if updated:
            updated_count += 1
            detail_log.append(f"  UPDATED: {skill_dir} - {', '.join(changes)}")
        else:
            skipped_count += 1

    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print()
    for line in detail_log:
        print(line)

    print()
    print("=== Template Script ===")
    if update_template_script():
        print("UPDATED: scripts/update_skill_readmes.py")
    else:
        print("No changes needed")


if __name__ == '__main__':
    main()
