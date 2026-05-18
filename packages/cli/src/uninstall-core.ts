import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as manifest from './manifest';
import { ValidAgent, isValidAgent, getAgentSkillsDir } from './detect';

export interface UninstallResult {
  skillName: string;
  target: string;
  removed: boolean;
  error?: Error;
}

export async function uninstallSkill(name: string, target: string): Promise<UninstallResult> {
  try {
    const normalizedTarget = target.toLowerCase();
    if (!isValidAgent(normalizedTarget)) {
      return { skillName: name, target, removed: false, error: new Error(`Unsupported target '${target}'.`) };
    }

    const m = await manifest.readManifest();
    const skill = m.skills.find(s => s.name === name && s.target === normalizedTarget);

    if (!skill) {
      return { skillName: name, target: normalizedTarget, removed: false, error: new Error('Skill not found in manifest.') };
    }

    const expectedRoot = path.resolve(getAgentSkillsDir(normalizedTarget as ValidAgent));
    const resolvedPath = path.resolve(skill.path);
    const rel = path.relative(expectedRoot, resolvedPath);
    const isInsideAgentDir = rel.length > 0 && !rel.startsWith('..') && !path.isAbsolute(rel);
    if (!isInsideAgentDir) {
      return {
        skillName: name,
        target: normalizedTarget,
        removed: false,
        error: new Error(`Refusing to remove '${resolvedPath}': path is outside the agent's skills directory.`)
      };
    }

    await fs.rm(resolvedPath, { recursive: true, force: true });
    await manifest.removeInstalled(name, normalizedTarget);

    return { skillName: name, target: normalizedTarget, removed: true };
  } catch (error: any) {
    return { skillName: name, target, removed: false, error };
  }
}
