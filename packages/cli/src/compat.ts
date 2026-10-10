import { CANONICAL_TARGETS } from './detect';

export interface CompatResult {
  ok: boolean;
  error?: string;
  targets?: string[];
}

export type CompatibilityState =
  | { kind: 'missing' }
  | { kind: 'valid'; targets: string[] }
  | { kind: 'invalid'; error: string };

const CANONICAL_TARGET_SET = new Set<string>(CANONICAL_TARGETS);

export function normalizeTarget(target: string): string {
  return target.trim().toLowerCase();
}

/**
 * Strictly parses an optional compatibility declaration. An omitted field is
 * universal; every declared target is normalized and returned in canonical order.
 */
export function parseCompatibility(
  compatibility: unknown,
  hasCompatibility: boolean,
): CompatResult {
  if (!hasCompatibility) return { ok: true };

  if (!Array.isArray(compatibility)) {
    return { ok: false, error: 'must be a non-empty YAML list of canonical targets, for example [codex, claude].' };
  }
  if (compatibility.length === 0) {
    return { ok: false, error: 'must not be empty. Omit the field to allow all targets, or list canonical targets.' };
  }

  const targets = new Set<string>();
  for (const [index, value] of compatibility.entries()) {
    if (typeof value !== 'string') {
      return { ok: false, error: `item ${index + 1} must be a string.` };
    }

    const normalized = normalizeTarget(value);
    if (!normalized) {
      return { ok: false, error: `item ${index + 1} must be a non-empty canonical target.` };
    }
    if (!CANONICAL_TARGET_SET.has(normalized)) {
      return {
        ok: false,
        error: `item ${index + 1} uses unknown target "${normalized}". Allowed targets: ${CANONICAL_TARGETS.join(', ')}.`,
      };
    }
    targets.add(normalized);
  }

  return {
    ok: true,
    targets: CANONICAL_TARGETS.filter(target => targets.has(target)),
  };
}

export function compatibilityStateFromDeclaration(
  compatibility: unknown,
  hasCompatibility: boolean,
): CompatibilityState {
  if (!hasCompatibility) return { kind: 'missing' };
  const result = parseCompatibility(compatibility, true);
  return result.ok
    ? { kind: 'valid', targets: result.targets! }
    : { kind: 'invalid', error: result.error! };
}

export function validateCompatibilityState(
  skillName: string,
  state: CompatibilityState,
  target: string,
): CompatResult {
  if (state.kind === 'invalid') return invalid(skillName, state.error);
  if (state.kind === 'missing') return { ok: true };
  return validateCompatibility(skillName, state.targets, true, target);
}

export function formatCompatibilityState(state: CompatibilityState): string {
  if (state.kind === 'missing') return 'all';
  if (state.kind === 'invalid') return 'invalid declaration';
  return state.targets.join(', ');
}

/**
 * Compatibility is universal only when the key is absent. Every explicit
 * declaration is validated before target membership is considered.
 */
export function validateCompatibility(
  skillName: string,
  compatibility: unknown,
  hasCompatibility: boolean,
  target: string,
): CompatResult {
  const declaration = parseCompatibility(compatibility, hasCompatibility);
  if (!declaration.ok) return invalid(skillName, declaration.error!);
  if (!hasCompatibility) return { ok: true };

  const normalizedTargets = declaration.targets!;

  const normalizedTarget = normalizeTarget(target);
  if (normalizedTargets.includes(normalizedTarget)) {
    return { ok: true, targets: normalizedTargets };
  }

  const titleTarget = normalizedTarget.charAt(0).toUpperCase() + normalizedTarget.slice(1);
  return {
    ok: false,
    targets: normalizedTargets,
    error:
      `Skill "${skillName}" supports: ${normalizedTargets.join(', ')}. ` +
      `It cannot be installed for ${normalizedTarget}. ` +
      `To add ${titleTarget} support, implement and test support, update the compatibility declaration, and open a PR.`,
  };
}

export function formatCompatibility(compatibility: unknown, hasCompatibility: boolean): string {
  if (!hasCompatibility) return 'all';
  const result = parseCompatibility(compatibility, true);
  return result.ok ? result.targets!.join(', ') : 'invalid declaration';
}

function invalid(skillName: string, detail: string): CompatResult {
  return {
    ok: false,
    error: `Skill "${skillName}" has an invalid compatibility declaration: ${detail}`,
  };
}
