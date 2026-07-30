import { parse as parseYaml } from 'yaml';

export interface FrontmatterDocument {
  data: Record<string, unknown>;
  content: string;
}

const FRONTMATTER_PATTERN = /^---[^\S\r\n]*\r?\n([\s\S]*?)\r?\n---[^\S\r\n]*(?:\r?\n|$)/;

export function parseFrontmatter(source: string): FrontmatterDocument {
  // Strip UTF-8 BOM so the opening --- anchor matches (parity with gray-matter).
  const cleaned = source.charCodeAt(0) === 0xfe_ff ? source.slice(1) : source;
  const match = FRONTMATTER_PATTERN.exec(cleaned);
  if (!match) {
    return { data: {}, content: cleaned };
  }

  const parsed = parseYaml(match[1]);
  if (parsed == null) {
    return { data: {}, content: cleaned.slice(match[0].length) };
  }
  if (typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new TypeError('Frontmatter must be a YAML mapping.');
  }

  return {
    data: parsed as Record<string, unknown>,
    content: cleaned.slice(match[0].length),
  };
}
