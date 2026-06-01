import os
import re
import urllib.parse

CLAUDE_VIDEO_URL = "https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c"
MANUS_VIDEO_URL = "https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm"


def _manus_link(skill_name):
    url = f"https://github.com/Varnan-Tech/opendirectory/tree/main/skills/{skill_name}"
    encoded = urllib.parse.quote(url, safe='')
    return f"https://manus.im/import-skills?githubUrl={encoded}&utm_source=opendirectory"


INSTALL_SNIPPET_TMPL = """## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install {skill_name} --target claude
```

### Option B: Claude Desktop App

<video src="{CLAUDE_VIDEO_URL}" controls style="width: 100%"></video>

**Step 1: Download the skill from GitHub**
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

### Option C: Claude Code Native

Run this command inside Claude Code:

```bash
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="{MANUS_VIDEO_URL}" controls style="width: 100%"></video>

[**Install in Manus AI**]({manus_link})

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
"""

INSTALL_EXISTS_RE = re.compile(
    r"(?:^|\n)##\s*Install(?:ation)?\s*\n\n```bash\s*\nnpx \"@opendirectory\.dev/skills\" install",
    re.MULTILINE,
)


def has_install_section(content: str) -> bool:
    return bool(INSTALL_EXISTS_RE.search(content))


def inject_install_section(content: str, skill_name: str) -> str:
    snippet = INSTALL_SNIPPET_TMPL.format(skill_name=skill_name, manus_link=_manus_link(skill_name))
    match = re.search(r"^## ", content, re.MULTILINE)
    if match:
        return content[:match.start()] + snippet + "\n\n" + content[match.start():]
    return content.rstrip() + "\n\n" + snippet


def update_readmes(base_dir="skills"):
    if os.path.basename(os.getcwd()) == "scripts":
        os.chdir("..")
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found.")
        return
    for skill_dir in sorted(os.listdir(base_dir)):
        if not os.path.isdir(os.path.join(base_dir, skill_dir)):
            continue
        readme_path = os.path.join(base_dir, skill_dir, "README.md")
        if not os.path.exists(readme_path):
            print(f"SKIP (no README.md): {skill_dir}")
            continue
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        if has_install_section(content):
            print(f"SKIP (already has install): {skill_dir}")
            continue
        new_content = inject_install_section(content, skill_dir)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"UPDATED: {skill_dir}")


if __name__ == "__main__":
    update_readmes("skills")
