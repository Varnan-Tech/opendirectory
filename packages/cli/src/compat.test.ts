import { describe, expect, test } from 'vitest';
import { formatCompatibility, normalizeTarget, parseCompatibility, validateCompatibility } from './compat';

describe('validateCompatibility', () => {
  test('missing compatibility field is universal', () => {
    expect(validateCompatibility('my-skill', undefined, false, 'codex')).toMatchObject({ ok: true });
  });

  test.each([
    ['scalar', 'codex', 'must be a non-empty YAML list'],
    ['empty list', [], 'must not be empty'],
    ['number member', ['codex', 1], 'item 2 must be a string'],
    ['null member', ['codex', null], 'item 2 must be a string'],
    ['alias', ['claude-code'], 'unknown target "claude-code"'],
    ['unknown target', ['codex', 'unknown-target'], 'unknown target "unknown-target"'],
  ])('explicit %s declaration is invalid and never universal', (_label, declaration, message) => {
    const result = validateCompatibility('my-skill', declaration, true, 'codex');
    expect(result.ok).toBe(false);
    expect(result.error).toContain(message);
  });

  test('normalizes declarations and requested target before comparing', () => {
    expect(validateCompatibility('my-skill', [' CODEX ', ' opencode '], true, ' CODEX ')).toMatchObject({
      ok: true,
      targets: ['codex', 'opencode'],
    });
  });

  test('rejects canonical mismatch with a stable actionable message', () => {
    expect(validateCompatibility('my-skill', ['codex'], true, 'gemini').error).toBe(
      'Skill "my-skill" supports: codex. It cannot be installed for gemini. To add Gemini support, implement and test support, update the compatibility declaration, and open a PR.',
    );
  });
});

describe('compatibility presentation helpers', () => {
  test('formats declared canonical targets in canonical order after normalization', () => {
    expect(formatCompatibility([' OPENCODE ', 'CODEX'], true)).toBe('codex, opencode');
  });

  test('formats an absent field as universal and invalid explicit values distinctly', () => {
    expect(formatCompatibility(undefined, false)).toBe('all');
    expect(formatCompatibility(['claude-code'], true)).toBe('invalid declaration');
  });

  test('normalizes requested target input', () => {
    expect(normalizeTarget(' CODEX ')).toBe('codex');
  });

  test('deduplicates declarations in canonical order', () => {
    expect(parseCompatibility(['hermes', 'codex', 'CODEX', 'claude'], true)).toMatchObject({
      ok: true,
      targets: ['claude', 'codex', 'hermes'],
    });
  });
});
