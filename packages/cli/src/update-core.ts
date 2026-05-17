import { loadRegistry } from './registry';
import * as manifest from './manifest';
import { uninstallSkill } from './uninstall-core';
import { installSkill, InstallResult } from './install-core';

export async function updateSkill(name: string, target: string): Promise<InstallResult> {
  try {
    const skills = await loadRegistry();
    const registrySkill = skills.find(s => s.name === name);
    if (!registrySkill) {
      return { skillName: name, target, path: '', success: false, error: new Error(`Skill '${name}' is not in the registry — cannot update.`) };
    }

    const m = await manifest.readManifest();
    const installedSkill = m.skills.find(s => s.name === name && s.target === target);
    if (!installedSkill) {
      return { skillName: name, target, path: '', success: false, error: new Error(`Skill '${name}' is not installed for target '${target}' — use install instead.`) };
    }

    const uninstallResult = await uninstallSkill(name, target);
    if (!uninstallResult.removed) {
      return { skillName: name, target, path: '', success: false, error: new Error(`Failed to uninstall old version: ${uninstallResult.error?.message}`) };
    }

    const installResult = await installSkill(name, target);
    if (!installResult.success) {
      return { skillName: name, target, path: '', success: false, error: new Error(`Failed to update '${name}' (old version was removed but new install failed): ${installResult.error?.message}`) };
    }

    return installResult;
  } catch (error: any) {
    return { skillName: name, target, path: '', success: false, error };
  }
}
