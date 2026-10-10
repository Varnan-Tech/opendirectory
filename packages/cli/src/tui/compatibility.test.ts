import { describe, expect, test, vi } from 'vitest';
import { getSkillAvailability } from './compatibility';
import { resolveBrowseTarget } from './browse';
import { shouldPersistDefault } from './target-picker';
import type { Skill } from '../registry';

const skill = (name: string, compatibility?: unknown, hasCompatibility = false): Skill => ({
  name,
  description: name,
  tags: [],
  author: 'test',
  version: '1.0.0',
  path: `skills/${name}`,
  compatibilityState: !hasCompatibility
    ? { kind: 'missing' }
    : name === 'invalid-alias'
      ? { kind: 'invalid', error: 'unknown target "claude-code"' }
      : { kind: 'valid', targets: compatibility as string[] },
});

describe('getSkillAvailability', () => {
  test('filters incompatible and invalid explicit declarations before selection', () => {
    const result = getSkillAvailability([
      skill('universal'),
      skill('codex-only', ['codex'], true),
      skill('claude-only', ['claude'], true),
      skill('invalid-alias', ['claude-code'], true),
    ], ' CODEX ');

    expect(result.available.map(item => item.name)).toEqual(['universal', 'codex-only']);
    expect(result.unavailable.map(item => item.name)).toEqual(['claude-only', 'invalid-alias']);
  });
});

test('preserves an explicitly requested target without invoking the picker', async () => {
  const pick = vi.fn(async () => 'codex');
  expect(await resolveBrowseTarget('claude', pick)).toBe('claude');
  expect(pick).not.toHaveBeenCalled();
  expect(await resolveBrowseTarget(undefined, pick)).toBe('codex');
  expect(pick).toHaveBeenCalledTimes(1);
});

test('does not persist a default target during an explicit-target session', () => {
  expect(shouldPersistDefault('claude', true)).toBe(false);
  expect(shouldPersistDefault(undefined, true)).toBe(true);
  expect(shouldPersistDefault(undefined, false)).toBe(false);
});
