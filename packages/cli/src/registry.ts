import * as fs from 'node:fs/promises';
import * as path from 'node:path';

export interface Skill {
  name: string;
  description: string;
  tags: string[];
  author: string;
  version: string;
  path: string;
}

const getProjectRoot = () => path.resolve(__dirname, '..');

export async function loadRegistry(): Promise<Skill[]> {
  const root = getProjectRoot();
  const registryPath = path.join(root, 'registry.json');
  
  let skills: any[] = [];
  try {
    const registryContent = await fs.readFile(registryPath, 'utf-8');
    skills = JSON.parse(registryContent);
  } catch (e) {
    const skillsDir = path.join(root, 'skills');
    try {
      const entries = await fs.readdir(skillsDir, { withFileTypes: true });
      skills = entries
        .filter(entry => entry.isDirectory())
        .map(entry => ({ 
          name: entry.name, 
          description: `Skill: ${entry.name}`,
          tags: [],
          author: 'unknown',
          version: 'unknown',
          path: `skills/${entry.name}`
        }));
    } catch (err) {
      // If skills dir also missing, return empty
    }
  }

  return skills.map(s => {
    let desc = s.description || '';
    desc = desc.replace(/<img[^>]*>/g, '').trim();
    return {
      name: s.name,
      description: desc,
      tags: Array.isArray(s.tags) ? s.tags : [],
      author: s.author || 'unknown',
      version: s.version || 'unknown',
      path: s.path || `skills/${s.name}`
    };
  });
}

export function getAllTags(skills: Skill[]): string[] {
  const tags = new Set<string>();
  for (const skill of skills) {
    for (const tag of skill.tags) {
      tags.add(tag);
    }
  }
  return Array.from(tags).sort();
}

export function filterByTags(skills: Skill[], tags: string[]): Skill[] {
  if (!tags || tags.length === 0) return skills;
  return skills.filter(skill => 
    skill.tags.some(tag => tags.includes(tag))
  );
}
