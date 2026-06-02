# YC Intent Radar

<img width="1280" height="640" alt="yc-intent-radar-cover" src="https://github.com/user-attachments/assets/2328ae2b-1b5d-45ad-8604-b90721b8d398" />

An automated scraper that pulls job listings and company data from YCombinator's Workatastartup platform. It bypasses login bottlenecks by utilizing authenticated sessions and ensures no duplicates are recorded by saving everything directly to a local SQLite database (`jobs.db`).

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install yc-intent-radar-skill --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fyc-intent-radar-skill&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Features
- **Deduplication:** Utilizes `better-sqlite3` to store state, ensuring you never scrape the same job twice.
- **Robust Extraction:** Identifies hidden JSON payloads on YC pages to grab accurate backend `job_id` values.
- **Filtered Exports:** Includes an export script (`export_radar_candidates.js`) that queries the SQLite database for intent-based hiring (e.g., GTM, DevRel, Growth, Content) and outputs it as a JSON payload for secondary research tools.

## Setup
1. Clone the repository.
2. Navigate to the `scripts/` directory:
   ```bash
   cd scripts
   npm install
   npx playwright install
   ```

3. **Authenticate (First Time Only):**
   Run the following script and log in to YC via the browser that opens. This creates a `state.json` file.
   ```bash
   node auth.js
   ```

4. **Run the Scraper:**
   ```bash
   node scraper.js
   ```

5. **Export Targeted Jobs:**
   ```bash
   node export_radar_candidates.js
   ```
   This will query the DB and produce `radar_candidates.json` containing the targeted companies and matching roles.

## Note on Sensitive Files
The `.gitignore` strictly protects your `state.json` (authentication cookies) and `jobs.db` (local history). Do not commit these files to a public repository.
