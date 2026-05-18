import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';

const repos = [
  "https://github.com/Varnan-Tech/schema-markup-generator",
  "https://github.com/Varnan-Tech/linkedin-post-generator",
  "https://github.com/Varnan-Tech/kill-the-standup",
  "https://github.com/Varnan-Tech/tweet-thread-from-blog",
  "https://github.com/Varnan-Tech/show-hn-writer",
  "https://github.com/Varnan-Tech/reddit-post-engine",
  "https://github.com/Varnan-Tech/reddit-icp-monitor",
  "https://github.com/Varnan-Tech/producthunt-launch-kit",
  "https://github.com/Varnan-Tech/pr-description-writer",
  "https://github.com/Varnan-Tech/outreach-sequence-builder",
  "https://github.com/Varnan-Tech/noise2blog",
  "https://github.com/Varnan-Tech/newsletter-digest",
  "https://github.com/Varnan-Tech/meeting-brief-generator",
  "https://github.com/Varnan-Tech/hackernews-intel",
  "https://github.com/Varnan-Tech/explain-this-pr",
  "https://github.com/Varnan-Tech/dependency-update-bot",
  "https://github.com/Varnan-Tech/claude-md-generator",
  "https://github.com/Varnan-Tech/docs-from-code",
  "https://github.com/Varnan-Tech/meta-ads-skill",
  "https://github.com/Varnan-Tech/llms-txt-generator",
  "https://github.com/Varnan-Tech/position-me",
  "https://github.com/Varnan-Tech/cook-the-blog",
  "https://github.com/Varnan-Tech/google-trends-api-skills",
  "https://github.com/Varnan-Tech/yc-intent-radar-skill",
  "https://github.com/Varnan-Tech/blog-cover-image-cli",
  "https://github.com/Varnan-Tech/twitter-GTM-find-skill",
  "https://github.com/Varnan-Tech/luma-attendees-scraper"
];

const SKILLS_DIR = path.join(process.cwd(), 'skills');

async function migrate() {
  if (!fs.existsSync(SKILLS_DIR)) {
    fs.mkdirSync(SKILLS_DIR, { recursive: true });
  }

  const testMode = process.env.TEST_MODE === 'true';
  const reposToProcess = testMode ? repos.slice(0, 2) : repos;

  console.log(`Starting migration for ${reposToProcess.length} repos...`);

  for (const repoUrl of reposToProcess) {
    const repoName = repoUrl.split('/').pop()?.replace('.git', '');
    if (!repoName) continue;

    const targetDir = path.join(SKILLS_DIR, repoName);
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), `skill-clone-${repoName}-`));

    console.log(`\nProcessing ${repoName}...`);

    try {
      console.log(`  Cloning ${repoUrl} into ${tempDir}...`);
      execSync(`git clone --depth 1 ${repoUrl} "${tempDir}"`, { stdio: 'ignore' });

      const skillMdPath = path.join(tempDir, 'SKILL.md');
      if (!fs.existsSync(skillMdPath)) {
        console.warn(`  Warning: SKILL.md not found in ${repoName}.`);
      }

      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }

      fs.cpSync(tempDir, targetDir, {
        recursive: true,
        filter: (src) => {
          const basename = path.basename(src);
          return basename !== '.git';
        }
      });

      console.log(`  Successfully copied ${repoName} to skills/${repoName}`);
    } catch (error) {
      console.error(`  Error processing ${repoName}:`, error instanceof Error ? error.message : error);
    } finally {
      try {
        fs.rmSync(tempDir, { recursive: true, force: true });
      } catch (cleanupError) {
        console.error(`  Failed to clean up temp dir ${tempDir}:`, cleanupError);
      }
    }
  }
  
  console.log('\nMigration complete!');
}

migrate().catch(console.error);
