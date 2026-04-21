# YC Intent Radar

<img width="1280" height="640" alt="yc-intent-radar-cover" src="https://github.com/user-attachments/assets/2328ae2b-1b5d-45ad-8604-b90721b8d398" />

An automated scraper that pulls job listings and company data from YCombinator's Workatastartup platform. It bypasses login bottlenecks by utilizing authenticated sessions and ensures no duplicates are recorded by saving everything directly to a local SQLite database (`jobs.db`).

## Install

```bash
npx "@opendirectory.dev/skills" install yc-intent-radar-skill --target claude
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
