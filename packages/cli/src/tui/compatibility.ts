import { validateCompatibilityState } from '../compat';
import type { Skill } from '../registry';

export interface SkillAvailability {
  available: Skill[];
  unavailable: Skill[];
}

export function getSkillAvailability(skills: Skill[], target: string): SkillAvailability {
  const available: Skill[] = [];
  const unavailable: Skill[] = [];

  for (const skill of skills) {
    const result = validateCompatibilityState(
      skill.name,
      skill.compatibilityState ?? { kind: 'invalid', error: 'Compatibility state is unavailable.' },
      target,
    );
    (result.ok ? available : unavailable).push(skill);
  }

  return { available, unavailable };
}
