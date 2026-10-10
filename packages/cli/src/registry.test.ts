import { describe, expect, test } from 'vitest';
import { parseSkillFrontmatter } from './registry';

function parse(frontmatter: string) {
  return parseSkillFrontmatter(`---\nname: fixture\ndescription: fixture\n${frontmatter}\n---\n`);
}

describe('parseSkillFrontmatter compatibility state', () => {
  test('normalizes a valid top-level declaration', () => {
    expect(parse('compatibility: [ OPENCODE, CODEX ]')).toMatchObject({
      hasCompatibility: true,
      compatibility: ['codex', 'opencode'],
      compatibilityState: { kind: 'valid', targets: ['codex', 'opencode'] },
    });
  });

  test('treats an omitted top-level declaration as universal', () => {
    expect(parse('')).toMatchObject({ compatibilityState: { kind: 'missing' } });
  });

  test.each([
    ['scalar', 'compatibility: codex', 'must be a non-empty YAML list'],
    ['empty list', 'compatibility: []', 'must not be empty'],
    ['alias', 'compatibility: [claude-code]', 'unknown target "claude-code"'],
  ])('preserves explicit invalid %s as a fail-closed state', (_label, source, error) => {
    expect(parse(source)).toMatchObject({
      compatibilityState: { kind: 'invalid', error: expect.stringContaining(error) },
      frontmatterError: expect.stringContaining(error),
    });
  });

  test('preserves YAML syntax errors as a fail-closed state', () => {
    const parsed = parseSkillFrontmatter('---\nname: fixture\ncompatibility: [codex\n---\n');
    expect(parsed).toMatchObject({
      compatibilityState: { kind: 'invalid', error: expect.stringContaining('Invalid YAML frontmatter:') },
    });
  });

  test('rejects metadata.compatibility instead of promoting it', () => {
    expect(parse('metadata:\n  compatibility: [codex]')).toMatchObject({
      compatibilityState: {
        kind: 'invalid',
        error: expect.stringContaining('metadata.compatibility is not supported'),
      },
    });
  });
});
