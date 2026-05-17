import * as fs from 'node:fs/promises';
import * as manifest from './manifest';

export interface UninstallResult {
  skillName: string;
  target: string;
  removed: boolean;
  error?: Error;
}

export async function uninstallSkill(name: string, target: string): Promise<UninstallResult> {
  try {
    const m = await manifest.readManifest();
    const skill = m.skills.find(s => s.name === name && s.target === target);
    
    if (!skill) {
      return { skillName: name, target, removed: false, error: new Error('Skill not found in manifest.') };
    }

    await fs.rm(skill.path, { recursive: true, force: true });
    await manifest.removeInstalled(name, target);

    return { skillName: name, target, removed: true };
  } catch (error: any) {
    return { skillName: name, target, removed: false, error };
  }
}
