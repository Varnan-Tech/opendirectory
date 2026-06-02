import os
import re
from urllib.parse import quote


START_MARKER = "<!-- OPENDIRECTORY_INSTALL_START -->"
END_MARKER = "<!-- OPENDIRECTORY_INSTALL_END -->"
DECORATIVE_HTML_TAG_RE = re.compile(r"</?(?:div|br|p|span|center)(?:\s+[^>]*)?>", re.IGNORECASE)

MANAGED_INSTALL_RE = re.compile(
    rf"^{re.escape(START_MARKER)}.*?^{re.escape(END_MARKER)}\s*",
    re.MULTILINE | re.DOTALL,
)
FIRST_MAJOR_SECTION_RE = re.compile(r"^## ", re.MULTILINE)
GENERIC_INSTALL_SIGNALS = (
    "@opendirectory.dev/skills",
    "npx opendirectory add",
    "download-directory.github.io",
    "Upload a skill",
    "Install the Skill in Claude",
    "Video Tutorial",
)


def has_meaningful_intro(content: str) -> bool:
    for line in content.splitlines():
        stripped = line.strip().lstrip("\ufeff")
        if not stripped:
            continue
        if stripped.startswith("<img") or DECORATIVE_HTML_TAG_RE.fullmatch(stripped):
            continue
        if stripped.startswith("![") or stripped.startswith("[!["):
            continue
        if re.fullmatch(r"[-*_]{3,}", stripped):
            continue
        if stripped.startswith("#"):
            continue
        return True
    return False


def top_level_sections(content: str) -> list[tuple[int, int, str, str]]:
    matches = list(FIRST_MAJOR_SECTION_RE.finditer(content))
    sections: list[tuple[int, int, str, str]] = []
    for index, match in enumerate(matches):
        heading_end = content.find("\n", match.start())
        if heading_end == -1:
            heading_end = len(content)
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        heading = content[match.start() : heading_end].strip()
        body = content[heading_end:section_end]
        sections.append((match.start(), section_end, heading, body))
    return sections


def is_install_heading(heading: str) -> bool:
    return heading.lower().startswith("## install")


def is_generic_install_section(heading: str, body: str) -> bool:
    return is_install_heading(heading) and any(signal in body for signal in GENERIC_INSTALL_SIGNALS)


def remove_generic_install_sections(content: str) -> str:
    result = content
    for start, end, heading, body in reversed(top_level_sections(content)):
        if is_generic_install_section(heading, body):
            result = result[:start].rstrip() + "\n\n" + result[end:].lstrip()
    return result


def remove_managed_install_section(content: str) -> str:
    if MANAGED_INSTALL_RE.search(content):
        return MANAGED_INSTALL_RE.sub("", content, count=1)

    marker_index = content.find(START_MARKER)
    if marker_index == -1:
        return content

    for start, _end, heading, _body in top_level_sections(content):
        if start > marker_index and not is_install_heading(heading):
            return content[:marker_index].rstrip() + "\n\n" + content[start:].lstrip()

    return content[:marker_index].rstrip() + "\n"


def normalize_remaining_installation_headings(content: str) -> str:
    lines: list[str] = []
    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("## installation") or stripped == "## install":
            lines.append("## Setup")
        elif stripped.startswith("#") and "install" in stripped:
            leading_space_count = len(line) - len(line.lstrip())
            leading_space = line[:leading_space_count]
            updated = line.lstrip()
            updated = re.sub(r"\bInstallation\b", "Setup", updated)
            updated = re.sub(r"\binstallation\b", "setup", updated)
            updated = re.sub(r"\bInstall\b", "Set up", updated)
            updated = re.sub(r"\binstall\b", "set up", updated)
            lines.append(leading_space + updated)
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def find_install_insert_index(content: str) -> int | None:
    match = FIRST_MAJOR_SECTION_RE.search(content)
    if not match:
        return None

    intro = content[: match.start()]
    if has_meaningful_intro(intro):
        return match.start()

    first_section = top_level_sections(content)[0]
    return first_section[1]


def manus_import_url(skill_name: str) -> str:
    github_url = f"https://github.com/Varnan-Tech/opendirectory/tree/main/skills/{skill_name}"
    encoded_github_url = quote(github_url, safe="")
    return f"https://manus.im/import-skills?githubUrl={encoded_github_url}&utm_source=opendirectory"


def build_install_block(skill_name: str) -> str:
    manus_url = manus_import_url(skill_name)
    return f"""{START_MARKER}
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install {skill_name} --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**]({manus_url})

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
{END_MARKER}
"""


def inject_install_section(content: str, skill_name: str) -> str:
    block = build_install_block(skill_name)
    content = remove_managed_install_section(content)

    content = remove_generic_install_sections(content)
    content = normalize_remaining_installation_headings(content)

    insert_index = find_install_insert_index(content)
    if insert_index is not None:
        return content[:insert_index].rstrip() + "\n\n" + block + "\n\n" + content[insert_index:].lstrip()

    return content.rstrip() + "\n\n" + block + "\n"


def update_readmes(base_dir: str = "skills") -> None:
    if os.path.basename(os.getcwd()) == "scripts":
        _ = os.chdir("..")

    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found.")
        return

    for skill_dir in sorted(os.listdir(base_dir)):
        skill_path = os.path.join(base_dir, skill_dir)
        if not os.path.isdir(skill_path):
            continue

        readme_path = os.path.join(skill_path, "README.md")
        if not os.path.exists(readme_path):
            print(f"SKIP (no README.md): {skill_dir}")
            continue

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = inject_install_section(content, skill_dir)
        if new_content == content:
            print(f"UNCHANGED: {skill_dir}")
            continue

        with open(readme_path, "w", encoding="utf-8") as f:
            _ = f.write(new_content)
        print(f"UPDATED: {skill_dir}")


if __name__ == "__main__":
    update_readmes("skills")
