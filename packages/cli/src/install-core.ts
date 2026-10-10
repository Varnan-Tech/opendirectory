import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { loadRegistry } from './registry';
import { ValidAgent, isValidAgent, getAgentSkillsDir } from './detect';
import * as manifest from './manifest';
import { normalizeTarget, validateCompatibilityState } from './compat';
import { loadSkillSource } from './skill-discovery';

export interface InstallResult {
  skillName: string;
  target: string;
  path: string;
  success: boolean;
  error?: Error;
}

export interface PreparedInstall {
  skillName: string;
  target: string;
  skillDir: string;
  manifestName: string;
  destPath: string;
  version: string;
}

export interface InstallPreparationResult {
  skillName: string;
  target: string;
  success: boolean;
  preparation?: PreparedInstall;
  error?: Error;
}

export async function prepareInstallSkill(skillName: string, target: string): Promise<InstallPreparationResult> {
  try {
    const normalizedTarget = normalizeTarget(target);
    if (!isValidAgent(normalizedTarget)) {
      return { skillName, target, success: false, error: new Error(`Unsupported target '${target}'.`) };
    }

    const root = path.resolve(__dirname, '..');
    const repoDir = path.join(root, 'skills', skillName);
    try {
      await fs.access(repoDir);
    } catch {
      return { skillName, target: normalizedTarget, success: false, error: new Error(`Repository '${skillName}' not found.`) };
    }

    const source = await loadSkillSource(repoDir);
    if (!source) {
      return { skillName, target: normalizedTarget, success: false, error: new Error(`Skill '${skillName}' missing SKILL.md in registry.`) };
    }

    const skillDir = source.skillDir;

    // Path-boundary guard: verify resolved skillDir stays inside skills/
    const skillsRoot = path.resolve(root, 'skills');
    const resolvedSkillDir = path.resolve(skillDir);
    const rel = path.relative(skillsRoot, resolvedSkillDir);
    if (rel.startsWith('..') || path.isAbsolute(rel) || rel.length === 0) {
      return {
        skillName,
        target: normalizedTarget,
        success: false,
        error: new Error(`Refusing to install '${resolvedSkillDir}': resolved path is outside the skills directory.`)
      };
    }

    const compatibility = validateCompatibilityState(
      skillName,
      source.frontmatter.compatibility,
      normalizedTarget,
    );
    if (!compatibility.ok) {
      return { skillName, target: normalizedTarget, success: false, error: new Error(compatibility.error) };
    }

    const registrySkills = await loadRegistry();
    const registryEntry = registrySkills.find(s => s.name === skillName);
    const manifestName = registryEntry ? skillName : path.basename(skillDir);
    const destFolderName = path.basename(skillDir);

    return {
      skillName,
      target: normalizedTarget,
      success: true,
      preparation: {
        skillName,
        target: normalizedTarget,
        skillDir,
        manifestName,
        destPath: path.join(getAgentSkillsDir(normalizedTarget as ValidAgent), destFolderName),
        version: registryEntry?.version || 'unknown',
      },
    };
  } catch (error: any) {
    return { skillName, target, success: false, error };
  }
}

export async function installPreparedSkill(prepared: PreparedInstall): Promise<InstallResult> {
  try {
    await fs.mkdir(prepared.destPath, { recursive: true });
    await fs.cp(prepared.skillDir, prepared.destPath, { recursive: true });

    await manifest.addInstalled({
      name: prepared.manifestName,
      target: prepared.target,
      version: prepared.version,
      installedAt: new Date().toISOString(),
      path: prepared.destPath
    });

    return { skillName: prepared.manifestName, target: prepared.target, path: prepared.destPath, success: true };
  } catch (error: any) {
    return { skillName: prepared.skillName, target: prepared.target, path: '', success: false, error };
  }
}

export async function installSkill(skillName: string, target: string): Promise<InstallResult> {
  const preparation = await prepareInstallSkill(skillName, target);
  if (!preparation.success) {
    return {
      skillName,
      target: preparation.target,
      path: '',
      success: false,
      error: preparation.error,
    };
  }

  return installPreparedSkill(preparation.preparation!);
}
