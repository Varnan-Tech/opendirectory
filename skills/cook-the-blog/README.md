# cook-the-blog

<img width="1280" height="640" alt="cook-the-blog-cover" src="https://github.com/user-attachments/assets/01fc87a2-78a8-433d-8531-a06a6a6df617" />

This guide explains how to set up, configure, and run the `cook-the-blog` skill. This AI agent pipeline autonomously researches companies, extracts SEO keywords, generates custom cover images, writes high-converting MDX case studies without AI fluff, uploads assets to cloud storage, and pushes the final code to your designated GitHub repository.

## Install

```bash
npx "@opendirectory.dev/skills" install cook-the-blog --target claude
```

## Prerequisites & Dependencies

Before running the skill, the AI agent needs access to several external tools, APIs, and environment details.

**Agent Instruction:** Before executing the pipeline for the first time, you (the AI Agent) must explicitly ask the user for any missing configuration details listed below (Target Repo, GCS Bucket, Email, etc.). **Do not hardcode these values into the skill.md file automatically without asking.**

### 1. Tavily Search (Deep Research)
Used for deep, high-quality web research to extract hard metrics, founder details, and GTM strategies.
- **Setup:** You need a Tavily API key from [Tavily](https://tavily.com/).
- **Installation:** Install the Tavily MCP server so the agent can use it natively.
  ```bash
  npx -y @modelcontextprotocol/server-tavily
  ```
- **Environment Variable:** Set `TAVILY_API_KEY` in your agent's environment or MCP config.

### 2. SerpApi (SEO Keyword Research)
Used to pull Google Trends data to find breakout search queries.
- **Setup:** Get a SerpApi key from [SerpApi](https://serpapi.com/).
- **Installation:** Ensure Python 3 and the `requests` / `google-search-results` libraries are installed. The user must provide a custom Python script (e.g., `blog_seo_research.py`) that queries the Google Trends API. The agent must be told the exact file path to this script.
- **Environment Variable:** `SERPAPI_KEY`

### 3. Blog Cover Image CLI
A custom Node.js CLI tool used to generate 16:9 minimalist cover images with company logos.
- **Installation:** Install the tool globally via npm.
  ```bash
  npm i -g blog-cover-image-cli
  ```
- **Usage:** The agent calls it via `blog-cover-cli generate -t "Title" -l "Logo URL" -o "./cover.png"`.

### 4. Cloud Storage (e.g., Google Cloud Storage, AWS S3)
Used to host the generated cover images. The user must specify which cloud provider they want to use.
- **Setup (Example for GCP):** The user needs a Google Cloud Service Account with storage write permissions.
- **Installation:** Install the Google Cloud SDK (`gcloud` and `gsutil`).
- **Authentication:** The user must provide a `service-account.json` file to authenticate.
  ```bash
  gcloud auth activate-service-account --key-file=service-account.json
  ```
- **Target Bucket:** The user must provide the target bucket URL (e.g., `gs://your-bucket-name/covers/`).

### 5. GitHub CLI & Git
Used for pushing the final MDX file to the target repository.
- **Setup:** Ensure `git` and `gh` (GitHub CLI) are installed on the host.
- **Authentication:** Log in to the GitHub CLI using a personal access token.
  ```bash
  gh auth login --with-token < token.txt
  ```
- **Configuration:** The agent will need the user's `git config user.name` and `git config user.email` to ensure proper commit attribution.

### 6. Email Notifications (SMTP)
Used to send a final success summary to the admin.
- **Setup:** The agent creates a Python script (`send_summary.py`) using the built-in `smtplib`.
- **Credentials:** The user must provide a dedicated sender Gmail account and an **App Password** (not their real password), as well as the destination admin email.

### 7. Stop Slop (AI Output Quality)
Used to ensure the generated case studies avoid typical AI fluff and maintain a high-quality, human-like tone.
- **Setup:** Add the [Stop Slop](https://github.com/hardikpandya/stop-slop) skill to your agent's loaded skills before running the generation pipeline.

---

## Configuration Variables to Ask For

When initializing this skill, the agent must ask the user to provide or confirm the following placeholders before running the pipeline:

1. **`[TARGET_REPO_URL]`**: The exact GitHub repository URL or slug (e.g., `username/my-blog-repo`).
2. **`[TARGET_BUCKET]`**: The cloud storage bucket path (e.g., `gs://my-images-bucket/blogs/`).
3. **`[PUBLIC_IMAGE_BASE_URL]`**: The public base URL where the uploaded images will be accessible (e.g., `https://storage.googleapis.com/my-images-bucket/blogs/`).
4. **`[GIT_USER_NAME]` & `[GIT_USER_EMAIL]`**: The exact name and email to use for Git commit authorship.
5. **`[ADMIN_EMAIL]`**: Where to send the final summary report.
6. **`[SENDER_EMAIL]` & `[SENDER_APP_PASSWORD]`**: The credentials for the SMTP Python script.
7. **`[PATH_TO_SEO_SCRIPT]`**: The exact path to the Python script that handles the SerpApi Google Trends queries.
8. **Brand Promotion Link**: The URL and pitch text to inject into the final FAQ of the MDX template (e.g., "If you want to build this, check out [MyBrand](https://mybrand.com)").

---

## How to Run

1. Once the user has provided the environment variables and configuration details, place the `skill.md` file in your agent's workspace.
2. The agent will read `skill.md` to understand the 8-step execution loop.
3. Trigger the agent by saying: *"Run the case study generator for [Company Name]."*
4. The agent will autonomously execute the entire pipeline from research to deployment.

## Installation in Claude Desktop App

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
