import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const SKILLS_DIR = path.join(process.cwd(), 'skills');
const PLUGIN_DIR = path.join(process.cwd(), '.claude-plugin');
const PLUGIN_JSON_PATH = path.join(PLUGIN_DIR, 'plugin.json');
const MARKETPLACE_JSON_PATH = path.join(process.cwd(), 'marketplace.json');

function buildPlugin() {
  if (!fs.existsSync(PLUGIN_DIR)) {
    fs.mkdirSync(PLUGIN_DIR, { recursive: true });
  }

  const skills: any[] = [];

  if (fs.existsSync(SKILLS_DIR)) {
    const skillDirs = fs.readdirSync(SKILLS_DIR).filter(file => {
      return fs.statSync(path.join(SKILLS_DIR, file)).isDirectory();
    });

    for (const dir of skillDirs) {
      const skillMdPath = path.join(SKILLS_DIR, dir, 'SKILL.md');
      if (fs.existsSync(skillMdPath)) {
        const content = fs.readFileSync(skillMdPath, 'utf-8');
        const parsed = matter(content);
        
        skills.push({
          name: parsed.data.name || dir,
          description: parsed.data.description || `Skill for ${dir}`,
          path: `./skills/${dir}`
        });
      }
    }
  }

  const pluginData = {
    name: "OpenDirectory GTM Skills",
    author: "Varnan",
    description: "A collection of GTM skills for Claude Code",
    version: "1.0.0",
    skills: skills
  };

  fs.writeFileSync(PLUGIN_JSON_PATH, JSON.stringify(pluginData, null, 2));
  console.log(`Generated ${PLUGIN_JSON_PATH} with ${skills.length} skills.`);

  const marketplaceData = {
    name: "OpenDirectory Marketplace",
    description: "Official marketplace for OpenDirectory skills",
    plugins: [
      {
        name: "OpenDirectory GTM Skills",
        path: "./.claude-plugin"
      }
    ]
  };

  fs.writeFileSync(MARKETPLACE_JSON_PATH, JSON.stringify(marketplaceData, null, 2));
  console.log(`Generated ${MARKETPLACE_JSON_PATH}.`);
}

buildPlugin();
