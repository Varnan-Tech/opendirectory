export interface InstalledSkill {
  name: string;        // skill name
  target: string;      // agent (claude, opencode, etc.)
  version: string;     // version installed (from registry at install time)
  installedAt: string; // ISO timestamp
  path: string;        // absolute path where skill was copied to
}

export interface Manifest {
  version: number;
  skills: InstalledSkill[];
}

import { resolvePath } from './fs-adapters';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

const MANIFEST_PATH_TILDE = '~/.opendirectory/installed.json';

// CRITICAL: Node.js `fs` does NOT expand `~`. Always use resolvePath() before any fs.* call.
function getManifestPath(): string {
  return resolvePath(MANIFEST_PATH_TILDE);
}

export async function readManifest(): Promise<Manifest> {
  const resolved = getManifestPath();
  try {
    const content = await fs.readFile(resolved, 'utf-8');
    return JSON.parse(content);
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

  if (removed > 0) {
    manifest.skills = validSkills;
    await writeManifest(manifest);
  }

  return { removed, added: 0 };
}
