import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { loadRegistry } from './registry';
import { ValidAgent, isValidAgent, getAgentSkillsDir } from './detect';
import * as manifest from './manifest';

export interface InstallResult {
  skillName: string;
  target: string;
  path: string;
  success: boolean;
  error?: Error;
}

export async function installSkill(skillName: string, target: string): Promise<InstallResult> {
  try {
    const normalizedTarget = target.toLowerCase();
    if (!isValidAgent(normalizedTarget)) {
      return { skillName, target, path: '', success: false, error: new Error(`Unsupported target '${target}'.`) };
    }

    const root = path.resolve(__dirname, '..');
    const repoDir = path.join(root, 'skills', skillName);
    let skillDir = repoDir;
    let skillMdPath = path.join(skillDir, 'SKILL.md');

    try {
      await fs.access(skillMdPath);
    } catch (e) {
      let foundAtDepth1 = false;
      try {
        const entries = await fs.readdir(repoDir, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.isDirectory()) {
            const possiblePath = path.join(repoDir, entry.name, 'SKILL.md');
            try {
              await fs.access(possiblePath);
              skillDir = path.join(repoDir, entry.name);
              skillMdPath = possiblePath;
              foundAtDepth1 = true;
              break;
            } catch (err) {}
          }
        }
        if (!foundAtDepth1) {
          outer: for (const entry of entries) {
            if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git') {
              const subDir = path.join(repoDir, entry.name);
              const subEntries = await fs.readdir(subDir, { withFileTypes: true });
              for (const subEntry of subEntries) {
                if (subEntry.isDirectory()) {
                  const possiblePath = path.join(subDir, subEntry.name, 'SKILL.md');
                  try {
                    await fs.access(possiblePath);
                    skillDir = path.join(subDir, subEntry.name);
                    skillMdPath = possiblePath;
                    break outer;
                  } catch (err) {}
                }
              }
            }
          }
        }
      } catch (dirErr) {
        return { skillName, target: normalizedTarget, path: '', success: false, error: new Error(`Repository '${skillName}' not found.`) };
      }
    }

    try {
      await fs.access(skillMdPath);
    } catch (e) {
      return { skillName, target: normalizedTarget, path: '', success: false, error: new Error(`Skill '${skillName}' missing SKILL.md in registry.`) };
    }

    // Path-boundary guard: verify resolved skillDir stays inside skills/
    const skillsRoot = path.resolve(root, 'skills');
    const resolvedSkillDir = path.resolve(skillDir);
    const rel = path.relative(skillsRoot, resolvedSkillDir);
    if (rel.startsWith('..') || path.isAbsolute(rel) || rel.length === 0) {
      return {
        skillName,
        target: normalizedTarget,
        path: '',
        success: false,
        error: new Error(`Refusing to install '${resolvedSkillDir}': resolved path is outside the skills directory.`)
      };
    }

    const registrySkills = await loadRegistry();
    const registryEntry = registrySkills.find(s => s.name === skillName);

    const manifestName = registryEntry ? skillName : path.basename(skillDir);
    const destFolderName = path.basename(skillDir);

    const destPath = path.join(getAgentSkillsDir(normalizedTarget as ValidAgent), destFolderName);

    await fs.mkdir(destPath, { recursive: true });

    await fs.cp(skillDir, destPath, { recursive: true });

    const version = registryEntry?.version || 'unknown';

    await manifest.addInstalled({
      name: manifestName,
      target: normalizedTarget,
      version,
      installedAt: new Date().toISOString(),
      path: destPath
    });

    return { skillName: manifestName, target: normalizedTarget, path: destPath, success: true };
  } catch (error: any) {
    return { skillName, target, path: '', success: false, error };
  }
}
