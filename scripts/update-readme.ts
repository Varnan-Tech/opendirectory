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

function findImageInReadme(skillPath: string): string | null {
  const skillDir = path.join(__dirname, '../', skillPath);
  
  function searchDir(dir: string): string | null {
    if (!fs.existsSync(dir)) return null;
    
    const files = fs.readdirSync(dir);
    
    const readmePath = path.join(dir, 'README.md');
    if (fs.existsSync(readmePath)) {
      const content = fs.readFileSync(readmePath, 'utf-8');
      
      const imgRegex = /<img[^>]+src=["']([^"']+)["']/g;
      const mdImgRegex = /!\[.*?\]\((.*?)\)/g;
      
      const matches: { url: string, index: number }[] = [];
      
      let match;
      while ((match = imgRegex.exec(content)) !== null) {
        const url = match[1];
        if (!url.match(/\.(mp4|mov|webm)$/i)) {
          matches.push({ url, index: match.index });
        }
      }
      
      while ((match = mdImgRegex.exec(content)) !== null) {
        const url = match[1];
        if (!url.match(/\.(mp4|mov|webm)$/i)) {
          matches.push({ url, index: match.index });
        }
      }
      
      if (matches.length > 0) {
        matches.sort((a, b) => a.index - b.index);
        return matches[0].url;
      }
    }
    
    for (const file of files) {
      const fullPath = path.join(dir, file);
      if (fs.statSync(fullPath).isDirectory() && file !== 'node_modules' && file !== '.git') {
        const result = searchDir(fullPath);
        if (result) return result;
      }
    }
    
    return null;
  }
  
  return searchDir(skillDir);
}

function generateMarkdownTable(skills: Skill[]): string {
  let table = '| Skill Name | Description | Version |\n';
  table += '|---|---|---|\n';

  for (const skill of skills) {
    let desc = skill.description;
    
    const imageUrl = findImageInReadme(skill.path);
    
    if (imageUrl) {
      desc = `<img src="${imageUrl}" width="600" />`;
    } else {
      desc = desc
        .replace(/\n/g, ' ')
        .replace(/\|/g, '\\|')
        .trim();
        
      if (!desc) {
        desc = 'No description provided.';
      }
    }
    
    table += `| \`${skill.name}\` | ${desc} | \`${skill.version}\` |\n`;
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
