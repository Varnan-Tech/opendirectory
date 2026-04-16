import fs from 'node:fs';
import path from 'node:path';

const REGISTRY_PATH = path.join(__dirname, '../packages/cli/registry.json');
const README_PATH = path.join(__dirname, '../README.md');

interface Skill {
  name: string;
  description: string;
  version: string;
  path: string;
}

function generateMarkdownTable(skills: Skill[]): string {
  let table = '| Skill Name | Description | Version |\n';
  table += '|---|---|---|\n';

  for (const skill of skills) {
    let desc = skill.description.replace(/<img[^>]*>/g, '').replace(/!\[.*?\]\(.*?\)/g, '').trim();
    
    desc = desc
      .replace(/\n/g, ' ')
      .replace(/\|/g, '\\|')
      .trim();
      
    if (!desc) {
      desc = 'No description provided.';
    }
    
    table += `| [\`${skill.name}\`](${skill.path}) | ${desc} | \`${skill.version}\` |\n`;
  }

  return table;
}

function updateReadme() {
  try {
    const registryData = fs.readFileSync(REGISTRY_PATH, 'utf-8');
    const skills: Skill[] = JSON.parse(registryData);

    const table = generateMarkdownTable(skills);

    const readmeContent = fs.readFileSync(README_PATH, 'utf-8');
    
    const startMarker = '<!-- SKILLS_LIST_START -->';
    const endMarker = '<!-- SKILLS_LIST_END -->';
    
    const regex = new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`);
    
    if (!regex.test(readmeContent)) {
      console.error('Could not find SKILLS_LIST markers in README.md');
      process.exit(1);
    }

    const updatedContent = readmeContent.replace(
      regex,
      `${startMarker}\n\n${table}\n${endMarker}`
    );

    fs.writeFileSync(README_PATH, updatedContent, 'utf-8');
    console.log('Successfully updated README.md with skills list.');
  } catch (error) {
    console.error('Error updating README:', error);
    process.exit(1);
  }
}

updateReadme();
