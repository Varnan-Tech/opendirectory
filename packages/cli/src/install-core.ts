import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { loadRegistry } from './registry';
import { ValidAgent, isValidAgent, getAgentSkillsDir } from './detect';
import * as manifest from './manifest';

export interface InstallResult {
  skillName: string;     // resolved (may differ from input if nested)
  target: string;
  path: string;          // resolved target path
  success: boolean;
  error?: Error;
}

export async function installSkill(skillName: string, target: string): Promise<InstallResult> {
  try {
    // 1. Target validation
    if (!isValidAgent(target)) {
      return { skillName, target, path: '', success: false, error: new Error(`Unsupported target '${target}'.`) };
    }

    // 2. Locate the skill folder on disk
    const root = path.resolve(__dirname, '..');
    const repoDir = path.join(root, 'skills', skillName);
    let skillDir = repoDir;
    let skillMdPath = path.join(skillDir, 'SKILL.md');

    try {
      await fs.access(skillMdPath);
    } catch (e) {
      try {
        const entries = await fs.readdir(repoDir, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.isDirectory()) {
            const possiblePath = path.join(repoDir, entry.name, 'SKILL.md');
            try {
              await fs.access(possiblePath);
              skillDir = path.join(repoDir, entry.name);
              skillMdPath = possiblePath;
              break;
            } catch (err) {}
          }
        }
        if (skillDir === repoDir) {
          for (const entry of entries) {
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
                    break;
                  } catch (err) {}
                }
              }
            }
          }
        }
      } catch (dirErr) {
        return { skillName, target, path: '', success: false, error: new Error(`Repository '${skillName}' not found.`) };
      }
    }

    try {
      await fs.access(skillMdPath);
    } catch (e) {
      return { skillName, target, path: '', success: false, error: new Error(`Skill '${skillName}' missing SKILL.md in registry.`) };
    }

    const actualSkillFolderName = path.basename(skillDir);
    const finalSkillName = actualSkillFolderName === skillName ? skillName : actualSkillFolderName;

    // 3. Compute destination path
    const destPath = path.join(getAgentSkillsDir(target as ValidAgent), finalSkillName);

    // 4. Create destination dir
    await fs.mkdir(destPath, { recursive: true });

    // 5. Copy recursively
    await fs.cp(skillDir, destPath, { recursive: true });

    // 6. Look up version from registry
    const skills = await loadRegistry();
    const skill = skills.find(s => s.name === finalSkillName);
    const version = skill?.version || 'unknown';

    // 7. Update manifest
    await manifest.addInstalled({
      name: finalSkillName,
      target,
      version,
      installedAt: new Date().toISOString(),
      path: destPath
    });

    // 8. Return
    return { skillName: finalSkillName, target, path: destPath, success: true };
  } catch (error: any) {
    return { skillName, target, path: '', success: false, error };
  }
}
