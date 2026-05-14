import { describe, it, expect, beforeAll } from 'vitest';
import { z } from 'zod';
import * as fs from 'fs';
import * as path from 'path';
import { execFileSync } from 'child_process';

// Mirrors Anthropic's Claude Code plugin.json schema.
// Spec: https://code.claude.com/docs/en/plugins-reference
// Regression test for: https://github.com/Varnan-Tech/opendirectory/issues/24
const AuthorSchema = z.object({
  name: z.string().min(1),
  email: z.string().email().optional(),
  url: z.string().url().optional(),
});

const PathOverride = z.union([z.string(), z.array(z.string())]);

const PluginManifestSchema = z.object({
  name: z.string().regex(/^[a-z0-9][a-z0-9-]*$/, 'must be kebab-case'),
  version: z.string().regex(/^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$/, 'must be valid semver'),
  description: z.string().optional(),
  author: AuthorSchema.optional(),
  homepage: z.string().url().optional(),
  repository: z.union([z.string().url(), z.object({ type: z.string(), url: z.string().url() })]).optional(),
  license: z.string().optional(),
  keywords: z.array(z.string()).optional(),
  commands: PathOverride.optional(),
  agents: PathOverride.optional(),
  skills: PathOverride.optional(),
  hooks: z.union([z.string(), z.record(z.unknown())]).optional(),
  mcpServers: z.union([z.string(), z.record(z.unknown())]).optional(),
  lspServers: z.union([z.string(), z.record(z.unknown())]).optional(),
}).strict();

const MarketplacePluginSchema = z.object({
  name: z.string(),
  source: z.string(),
  description: z.string().optional(),
}).strict();

const MarketplaceManifestSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  owner: z.object({ name: z.string() }).strict(),
  plugins: z.array(MarketplacePluginSchema),
}).strict();

const REPO_ROOT = path.resolve(__dirname, '..');
const PLUGIN_JSON_PATH = path.join(REPO_ROOT, '.claude-plugin', 'plugin.json');
const MARKETPLACE_JSON_PATH = path.join(REPO_ROOT, '.claude-plugin', 'marketplace.json');
const SKILLS_DIR = path.join(REPO_ROOT, 'skills');
const BUILD_SCRIPT = path.join(__dirname, 'build-claude-plugin.ts');

function countSkillsOnDisk(): number {
  if (!fs.existsSync(SKILLS_DIR)) return 0;
  return fs.readdirSync(SKILLS_DIR).filter(file => {
    if (file.startsWith('.')) return false;
    return fs.statSync(path.join(SKILLS_DIR, file)).isDirectory();
  }).length;
}

describe('Claude Code plugin manifest (regression test for issue #24)', () => {
  beforeAll(() => {
    execFileSync('npx', ['tsx', BUILD_SCRIPT], { cwd: REPO_ROOT, stdio: 'pipe', shell: process.platform === 'win32' });
  });

  it('plugin.json validates against the official Anthropic schema', () => {
    const raw = JSON.parse(fs.readFileSync(PLUGIN_JSON_PATH, 'utf-8'));
    const result = PluginManifestSchema.safeParse(raw);
    if (!result.success) {
      throw new Error(`plugin.json failed validation:\n${JSON.stringify(result.error.format(), null, 2)}`);
    }
  });

  it('plugin.json author is an object, not a string (issue #24 regression guard)', () => {
    const raw = JSON.parse(fs.readFileSync(PLUGIN_JSON_PATH, 'utf-8'));
    expect(typeof raw.author).toBe('object');
    expect(raw.author).not.toBeNull();
    expect(Array.isArray(raw.author)).toBe(false);
    expect(raw.author.name).toBeTruthy();
  });

  it('plugin.json does NOT contain a skills metadata array (issue #24 regression guard)', () => {
    const raw = JSON.parse(fs.readFileSync(PLUGIN_JSON_PATH, 'utf-8'));
    if (raw.skills !== undefined) {
      const ok = typeof raw.skills === 'string' || (Array.isArray(raw.skills) && raw.skills.every((s: unknown) => typeof s === 'string'));
      expect(ok, 'skills must be string or string[] per Anthropic schema').toBe(true);
    }
  });

  it('marketplace.json validates against the official Anthropic marketplace schema', () => {
    const raw = JSON.parse(fs.readFileSync(MARKETPLACE_JSON_PATH, 'utf-8'));
    const result = MarketplaceManifestSchema.safeParse(raw);
    if (!result.success) {
      throw new Error(`marketplace.json failed validation:\n${JSON.stringify(result.error.format(), null, 2)}`);
    }
  });

  it('plugin name is kebab-case (matches what README documents users typing)', () => {
    const raw = JSON.parse(fs.readFileSync(PLUGIN_JSON_PATH, 'utf-8'));
    expect(raw.name).toMatch(/^[a-z0-9][a-z0-9-]*$/);
    expect(raw.name).toBe('opendirectory-gtm-skills');
  });

  it('marketplace description reflects the actual on-disk skill count (catches stale committed JSON)', () => {
    const raw = JSON.parse(fs.readFileSync(MARKETPLACE_JSON_PATH, 'utf-8'));
    const expectedCount = countSkillsOnDisk();
    const description: string = raw.plugins?.[0]?.description ?? '';
    expect(description).toMatch(new RegExp(`\\b${expectedCount}\\b`));
  });

  it('plugin.json description reflects the actual on-disk skill count', () => {
    const raw = JSON.parse(fs.readFileSync(PLUGIN_JSON_PATH, 'utf-8'));
    const expectedCount = countSkillsOnDisk();
    expect(raw.description).toMatch(new RegExp(`\\b${expectedCount}\\b`));
  });
});
