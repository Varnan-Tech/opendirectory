import { parse as parseYaml } from 'yaml';

export interface FrontmatterDocument {
  data: Record<string, unknown>;
  content: string;
}

const FRONTMATTER_PATTERN = /^---[^\S\r\n]*\r?\n([\s\S]*?)\r?\n---[^\S\r\n]*(?:\r?\n|$)/;

export function parseFrontmatter(source: string): FrontmatterDocument {
  const match = FRONTMATTER_PATTERN.exec(source);
  if (!match) {
    return { data: {}, content: source };
  }

  const parsed = parseYaml(match[1]);
  if (parsed == null) {
    return { data: {}, content: source.slice(match[0].length) };
  }
  if (typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new TypeError('Frontmatter must be a YAML mapping.');
  }

  return {
    data: parsed as Record<string, unknown>,
    content: source.slice(match[0].length),
  };
}
