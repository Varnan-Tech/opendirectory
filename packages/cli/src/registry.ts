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

async function parseSkillMd(skillDir: string, skillName: string): Promise<Partial<Skill> | null> {
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  try {
    const content = await fs.readFile(skillMdPath, 'utf-8');
    if (!content.startsWith('---')) return null;
    const end = content.indexOf('\n---', 4);
    if (end === -1) return null;
    const frontmatter = content.slice(4, end);
    const result: Partial<Skill> = {};
    let inDescription = false;
    let descriptionParts: string[] = [];
    let descQuote = '';
    for (let rawLine of frontmatter.split(/\r?\n/)) {
      if (rawLine.endsWith('\r')) rawLine = rawLine.slice(0, -1);
      if (inDescription) {
        if (/^[a-z_]+:/i.test(rawLine.trimStart()) && rawLine.startsWith(rawLine.trimStart())) {
          inDescription = false;
        } else {
          descriptionParts.push(rawLine);
          continue;
        }
      }
      const match = rawLine.match(/^([a-z_]+):\s*(.*)$/i);
      if (!match) continue;
      const [, key, rest] = match;
      const value = rest.trim();
      if (key === 'description') {
        if (value.startsWith("'") || value.startsWith('"')) {
          descQuote = value[0];
          const stripped = value.slice(1);
          if (stripped.endsWith(descQuote)) {
            result.description = stripped.slice(0, -1);
          } else {
            descriptionParts = [stripped];
            inDescription = true;
          }
        } else if (value === '|' || value === '>') {
          inDescription = true;
        } else {
          result.description = value;
        }
      } else if (key === 'author') {
        result.author = value.replace(/^['"]|['"]$/g, '');
      } else if (key === 'version') {
        result.version = value.replace(/^['"]|['"]$/g, '');
      } else if (key === 'tags') {
        const tagMatch = value.match(/^\[(.*)\]$/);
        if (tagMatch) {
          result.tags = tagMatch[1].split(',').map(t => t.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean);
        }
      }
    }
    if (descriptionParts.length > 0 && !result.description) {
      let joined = descriptionParts.join(' ').trim();
      if (descQuote && joined.endsWith(descQuote)) joined = joined.slice(0, -1);
      result.description = joined.replace(/\s+/g, ' ');
    }
    return result;
  } catch {
    return null;
  }
}

export async function loadRegistry(): Promise<Skill[]> {
  const root = getProjectRoot();
  const registryPath = path.join(root, 'registry.json');
  const skillsDir = path.join(root, 'skills');

  const registryMap = new Map<string, any>();
  try {
    const registryContent = await fs.readFile(registryPath, 'utf-8');
    const registryArray = JSON.parse(registryContent);
    for (const entry of registryArray) {
      if (entry?.name) registryMap.set(entry.name, entry);
    }
  } catch {}

  let diskEntries: { name: string; dir: string }[] = [];
  try {
    const entries = await fs.readdir(skillsDir, { withFileTypes: true });
    diskEntries = entries
      .filter(e => e.isDirectory() && !e.name.startsWith('.') && !e.name.startsWith('_'))
      .map(e => ({ name: e.name, dir: path.join(skillsDir, e.name) }));
  } catch {}

  const skills: Skill[] = [];
  const seen = new Set<string>();

  for (const { name, dir } of diskEntries) {
    seen.add(name);
    const fromRegistry = registryMap.get(name);
    const fromFrontmatter = await parseSkillMd(dir, name);
    skills.push({
      name,
      description: cleanDescription(fromRegistry?.description || fromFrontmatter?.description || `Skill: ${name}`),
      tags: Array.isArray(fromRegistry?.tags) ? fromRegistry.tags : (fromFrontmatter?.tags ?? []),
      author: fromRegistry?.author || fromFrontmatter?.author || 'OpenDirectory',
      version: fromRegistry?.version || fromFrontmatter?.version || 'unknown',
      path: fromRegistry?.path || `skills/${name}`
    });
  }

  skills.sort((a, b) => a.name.localeCompare(b.name));
  return skills;
}

function cleanDescription(desc: string): string {
  return desc
    .replace(/<img[^>]*>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
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
