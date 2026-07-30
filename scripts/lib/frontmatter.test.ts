import { describe, expect, it } from 'vitest';
import { parseFrontmatter } from './frontmatter';

describe('parseFrontmatter', () => {
  it('parses YAML values and returns the remaining content', () => {
    const source = [
      '---',
      'name: example-skill',
      'description: "Research: public sources only"',
      'compatibility: [claude-code, gemini-cli]',
      '---',
      '',
      '# Example',
    ].join('\n');

    expect(parseFrontmatter(source)).toEqual({
      data: {
        name: 'example-skill',
        description: 'Research: public sources only',
        compatibility: ['claude-code', 'gemini-cli'],
      },
      content: '\n# Example',
    });
  });

  it('returns an empty metadata object when frontmatter is absent', () => {
    expect(parseFrontmatter('# Example')).toEqual({
      data: {},
      content: '# Example',
    });
  });

  it('rejects a non-mapping YAML document', () => {
    expect(() => parseFrontmatter('---\n- invalid\n---\nBody')).toThrow(
      'Frontmatter must be a YAML mapping.',
    );
  });

  it('strips a UTF-8 BOM before matching frontmatter', () => {
    const bom = '\uFEFF';
    const source = `${bom}---\nname: bom-skill\n---\n# Body`;
    expect(parseFrontmatter(source)).toEqual({
      data: { name: 'bom-skill' },
      content: '# Body',
    });
  });

  it('handles empty frontmatter delimiters', () => {
    expect(parseFrontmatter('---\n\n---\n# Body')).toEqual({
      data: {},
      content: '# Body',
    });
  });

  it('handles CRLF line endings', () => {
    const source = '---\r\nname: crlf-skill\r\ndescription: "crlf test"\r\n---\r\n# Body';
    expect(parseFrontmatter(source)).toEqual({
      data: { name: 'crlf-skill', description: 'crlf test' },
      content: '# Body',
    });
  });
});
