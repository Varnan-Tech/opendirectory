export interface InstalledSkill {
  name: string;
  target: string;
  version: string;
  installedAt: string;
  path: string;
}

export interface Manifest {
  version: number;
  skills: InstalledSkill[];
}

import { resolvePath } from './fs-adapters';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { AGENT_PATHS, ValidAgent, getAgentSkillsDir } from './detect';

const MANIFEST_PATH_TILDE = '~/.opendirectory/installed.json';

function getManifestPath(): string {
  return resolvePath(MANIFEST_PATH_TILDE);
}

export async function readManifest(): Promise<Manifest> {
  const resolved = getManifestPath();
  try {
    const content = await fs.readFile(resolved, 'utf-8');
    const parsed = JSON.parse(content);
    // Structural validation: guard against corrupt/partial manifest files
    if (parsed && typeof parsed === 'object' && Array.isArray(parsed.skills)) {
      return parsed as Manifest;
    }
    return { version: 1, skills: [] };
  } catch (e) {
    return { version: 1, skills: [] };
  }
}

export async function writeManifest(m: Manifest): Promise<void> {
  const resolved = getManifestPath();
  await fs.mkdir(path.dirname(resolved), { recursive: true });
  const tmpPath = resolved + '.tmp.' + process.pid;
  await fs.writeFile(tmpPath, JSON.stringify(m, null, 2), 'utf-8');
  await fs.rename(tmpPath, resolved);
}

export async function addInstalled(skill: InstalledSkill): Promise<void> {
  const manifest = await readManifest();
  const existingIndex = manifest.skills.findIndex(s => s.name === skill.name && s.target === skill.target);
  if (existingIndex >= 0) {
    manifest.skills[existingIndex] = skill;
  } else {
    manifest.skills.push(skill);
  }
  await writeManifest(manifest);
}

export async function removeInstalled(name: string, target: string): Promise<void> {
  const manifest = await readManifest();
  manifest.skills = manifest.skills.filter(s => !(s.name === name && s.target === target));
  await writeManifest(manifest);
}

export async function reconcile(): Promise<{ removed: number; added: number }> {
  const manifest = await readManifest();
  const validSkills: InstalledSkill[] = [];
  let removed = 0;

  for (const skill of manifest.skills) {
    try {
      const stat = await fs.stat(skill.path);
      if (stat.isDirectory() || stat.isFile()) {
        validSkills.push(skill);
      } else {
        removed++;
      }
    } catch {
      removed++;
    }
  }

  let added = 0;
  const knownPaths = new Set(validSkills.map(s => path.resolve(s.path)));

  for (const agentName of Object.keys(AGENT_PATHS) as ValidAgent[]) {
    const skillsDir = getAgentSkillsDir(agentName);
    let entries: import('node:fs').Dirent[];
    try {
      entries = await fs.readdir(skillsDir, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const fullPath = path.resolve(skillsDir, entry.name);
      if (knownPaths.has(fullPath)) continue;

      try {
        await fs.access(path.join(fullPath, 'SKILL.md'));
      } catch {
        continue;
      }

      validSkills.push({
        name: entry.name,
        target: agentName,
        version: 'unknown',
        installedAt: new Date(0).toISOString(),
        path: fullPath,
      });
      knownPaths.add(fullPath);
      added++;
    }
  }

  if (removed > 0 || added > 0) {
    manifest.skills = validSkills;
    await writeManifest(manifest);
  }

  return { removed, added };
}
