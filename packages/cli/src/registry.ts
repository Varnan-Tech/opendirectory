import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { inspectSkillFrontmatter } from './frontmatter';
import { type CompatibilityState } from './compat';
import { loadSkillSource } from './skill-discovery';

export interface Skill {
  name: string;
  description: string;
  tags: string[];
  author: string;
  version: string;
  path: string;
  compatibility?: unknown;
  /** Distinguishes an omitted key from an explicit null, scalar, or empty list. */
  hasCompatibility?: boolean;
  /** Preserves frontmatter parse failures so malformed skills cannot become universal. */
  frontmatterError?: string;
  compatibilityState?: CompatibilityState;
}

const getProjectRoot = () => path.resolve(__dirname, '..');

async function parseSkillMd(skillDir: string): Promise<Partial<Skill> | null> {
  try {
    const source = await loadSkillSource(skillDir);
    if (!source) return null;
    return parseSkillFrontmatterDocument(source.frontmatter, true);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const readError = `Unable to load discovered SKILL.md: ${message}`;
    return { compatibilityState: { kind: 'invalid', error: readError }, frontmatterError: readError };
  }
}

export function parseSkillFrontmatter(content: string): Partial<Skill> | null {
  return parseSkillFrontmatterDocument(inspectSkillFrontmatter(content), content.startsWith('---'));
}

function parseSkillFrontmatterDocument(
  frontmatter: ReturnType<typeof inspectSkillFrontmatter>,
  hasSourceFile: boolean,
): Partial<Skill> | null {
  const source = frontmatter.data;
  if (Object.keys(source).length === 0 && !hasSourceFile && frontmatter.compatibility.kind === 'missing') return null;
  const result: Partial<Skill> = { compatibilityState: frontmatter.compatibility };
  if (typeof source.description === 'string') result.description = source.description;
  if (typeof source.author === 'string') result.author = source.author;
  if (typeof source.version === 'string') result.version = source.version;
  if (Array.isArray(source.tags)) result.tags = source.tags.filter((tag): tag is string => typeof tag === 'string');
  if (frontmatter.compatibility.kind === 'valid') {
    result.hasCompatibility = true;
    result.compatibility = frontmatter.compatibility.targets;
  }
  if (frontmatter.compatibility.kind === 'invalid') {
    result.frontmatterError = frontmatter.compatibility.error;
  }
  return result;
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
    const fromFrontmatter = await parseSkillMd(dir);
    const compatibilityState = fromFrontmatter?.compatibilityState ?? { kind: 'missing' };
    skills.push({
      name,
      description: cleanDescription(fromRegistry?.description || fromFrontmatter?.description || `Skill: ${name}`),
      tags: Array.isArray(fromRegistry?.tags) ? fromRegistry.tags : (fromFrontmatter?.tags ?? []),
      author: fromRegistry?.author || fromFrontmatter?.author || 'OpenDirectory',
      version: fromRegistry?.version || fromFrontmatter?.version || 'unknown',
      path: fromRegistry?.path || `skills/${name}`,
      compatibilityState,
      ...(compatibilityState.kind === 'valid' && {
        compatibility: compatibilityState.targets,
        hasCompatibility: true,
      }),
      ...(compatibilityState.kind === 'invalid' && { frontmatterError: compatibilityState.error }),
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
