import { describe, expect, test } from 'vitest';
import { inspectSkillFrontmatter, parseFrontmatter } from './frontmatter';

describe('parseFrontmatter delimiters', () => {
  test.each([
    ['LF', '---\n\n---\n# Body'],
    ['CRLF', '---\r\n\r\n---\r\n# Body'],
  ])('accepts zero-content frontmatter with %s line endings', (_label, source) => {
    expect(parseFrontmatter(source)).toEqual({ data: {}, content: '# Body' });
  });

  test.each([
    ['LF', '---\ncompatibility: [codex]\n---\n# Body'],
    ['CRLF', '---\r\ncompatibility: [codex]\r\n---\r\n# Body'],
  ])('accepts well-formed compatibility frontmatter with %s line endings', (_label, source) => {
    expect(parseFrontmatter(source)).toEqual({
      data: { compatibility: ['codex'] },
      content: '# Body',
    });
  });

  test.each([
    ['LF', '---\n---\n# Body'],
    ['CRLF', '---\r\n---\r\n# Body'],
  ])('accepts immediately adjacent empty frontmatter delimiters with %s line endings', (_label, source) => {
    expect(parseFrontmatter(source)).toEqual({ data: {}, content: '# Body' });
  });

  test.each([
    ['LF', '---\n---\n# Body'],
    ['CRLF', '---\r\n---\r\n# Body'],
  ])('treats adjacent empty frontmatter as universal compatibility with %s line endings', (_label, source) => {
    expect(inspectSkillFrontmatter(source).compatibility).toEqual({ kind: 'missing' });
  });

  test('rejects an inline closing delimiter as unterminated frontmatter', () => {
    expect(() => parseFrontmatter('---\ncompatibility: [codex]---\n# Body')).toThrow(
      'Invalid YAML frontmatter: missing closing --- delimiter.',
    );
  });

  test('rejects an inline closing delimiter with CRLF line endings', () => {
    expect(() => parseFrontmatter('---\r\ncompatibility: [codex]---\r\n# Body')).toThrow(
      'Invalid YAML frontmatter: missing closing --- delimiter.',
    );
  });

  test('distinguishes an unterminated frontmatter block', () => {
    expect(() => parseFrontmatter('---\nname: fixture\n# Body')).toThrow(
      'Invalid YAML frontmatter: missing closing --- delimiter.',
    );
  });
});
