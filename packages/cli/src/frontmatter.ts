import { parseDocument } from 'yaml';
import { compatibilityStateFromDeclaration, type CompatibilityState } from './compat';

export interface FrontmatterDocument {
  data: Record<string, unknown>;
  content: string;
}

export interface SkillFrontmatterDocument extends FrontmatterDocument {
  compatibility: CompatibilityState;
}

const FRONTMATTER_PATTERN = /^---[^\S\r\n]*\r?\n([\s\S]*?(?:\r?\n))?---[^\S\r\n]*(?:\r?\n|$)/;
const FRONTMATTER_OPENING_PATTERN = /^---[^\S\r\n]*(?:\r?\n|$)/;

export function parseFrontmatter(source: string): FrontmatterDocument {
  const cleaned = source.charCodeAt(0) === 0xfeff ? source.slice(1) : source;
  const match = FRONTMATTER_PATTERN.exec(cleaned);
  if (!match) {
    if (FRONTMATTER_OPENING_PATTERN.test(cleaned)) {
      throw new TypeError('Invalid YAML frontmatter: missing closing --- delimiter.');
    }
    return { data: {}, content: cleaned };
  }

  const document = parseDocument(match[1] ?? '');
  if (document.errors.length > 0) {
    throw new TypeError(`Invalid YAML frontmatter: ${document.errors[0].message}`);
  }

  const parsed = document.toJS();
  if (parsed == null) return { data: {}, content: cleaned.slice(match[0].length) };
  if (typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new TypeError('Frontmatter must be a YAML mapping.');
  }

  return {
    data: parsed as Record<string, unknown>,
    content: cleaned.slice(match[0].length),
  };
}

/**
 * Parses SKILL.md and resolves its compatibility declaration. Only a top-level
 * key is supported; nested metadata.compatibility is intentionally rejected.
 */
export function inspectSkillFrontmatter(source: string): SkillFrontmatterDocument {
  try {
    const parsed = parseFrontmatter(source);
    const metadata = parsed.data.metadata;
    if (isRecord(metadata) && hasOwn(metadata, 'compatibility')) {
      return {
        ...parsed,
        compatibility: {
          kind: 'invalid',
          error: 'metadata.compatibility is not supported; declare compatibility at the top level.',
        },
      };
    }

    return {
      ...parsed,
      compatibility: compatibilityStateFromDeclaration(
        parsed.data.compatibility,
        hasOwn(parsed.data, 'compatibility'),
      ),
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      data: {},
      content: '',
      compatibility: { kind: 'invalid', error: message },
    };
  }
}

function hasOwn(value: Record<string, unknown>, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
