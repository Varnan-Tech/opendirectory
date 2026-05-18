import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { loadRegistry } from './registry';
import * as manifest from './manifest';
import { installSkill, InstallResult } from './install-core';
import { ValidAgent, isValidAgent, getAgentSkillsDir } from './detect';

export async function updateSkill(name: string, target: string): Promise<InstallResult> {
  const normalizedTarget = target.toLowerCase();
  if (!isValidAgent(normalizedTarget)) {
    return { skillName: name, target, path: '', success: false, error: new Error(`Unsupported target '${target}'.`) };
  }

  let backupPath: string | null = null;
  let originalPath: string | null = null;

  try {
    const skills = await loadRegistry();
    const registrySkill = skills.find(s => s.name === name);
    if (!registrySkill) {
      return { skillName: name, target: normalizedTarget, path: '', success: false, error: new Error(`Skill '${name}' is not in the registry — cannot update.`) };
    }

    const m = await manifest.readManifest();
    const installedSkill = m.skills.find(s => s.name === name && s.target === normalizedTarget);
    if (!installedSkill) {
      return { skillName: name, target: normalizedTarget, path: '', success: false, error: new Error(`Skill '${name}' is not installed for target '${normalizedTarget}' — use install instead.`) };
    }

    const expectedRoot = path.resolve(getAgentSkillsDir(normalizedTarget as ValidAgent));
    const resolved = path.resolve(installedSkill.path);
    const rel = path.relative(expectedRoot, resolved);
    if (rel.startsWith('..') || path.isAbsolute(rel) || rel.length === 0) {
      return { skillName: name, target: normalizedTarget, path: '', success: false, error: new Error(`Refusing to update '${resolved}': path is outside the agent's skills directory.`) };
    }

    originalPath = resolved;
    backupPath = `${resolved}.bak.${process.pid}.${Date.now()}`;

    try {
      await fs.rename(originalPath, backupPath);
    } catch (renameErr: any) {
      return { skillName: name, target: normalizedTarget, path: '', success: false, error: new Error(`Failed to stage backup for update: ${renameErr.message}`) };
    }

    await manifest.removeInstalled(name, normalizedTarget);

    const installResult = await installSkill(name, normalizedTarget);
    if (!installResult.success) {
      try {
        await fs.rm(originalPath, { recursive: true, force: true });
        await fs.rename(backupPath, originalPath);
        await manifest.addInstalled(installedSkill);
        backupPath = null;
      } catch (rollbackErr: any) {
        return {
          skillName: name,
          target: normalizedTarget,
          path: '',
          success: false,
          error: new Error(`Update failed AND rollback failed. Manual recovery needed: backup at '${backupPath}'. Install error: ${installResult.error?.message}. Rollback error: ${rollbackErr.message}`)
        };
      }
      return { skillName: name, target: normalizedTarget, path: '', success: false, error: new Error(`Update failed; original version restored: ${installResult.error?.message}`) };
    }

    if (backupPath) {
      try {
        await fs.rm(backupPath, { recursive: true, force: true });
      } catch (cleanupErr) {
      }
    }

    return installResult;
  } catch (error: any) {
    if (backupPath && originalPath) {
      try {
        await fs.rm(originalPath, { recursive: true, force: true });
        await fs.rename(backupPath, originalPath);
      } catch {}
    }
    return { skillName: name, target: normalizedTarget, path: '', success: false, error };
  }
}
