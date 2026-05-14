import { describe, it, expect } from 'vitest';
import { z } from 'zod';
import * as fs from 'fs';
import * as path from 'path';

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
}).strict(); // strict() rejects unknown keys — matches Anthropic's strict Zod validator

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

describe('Claude Code plugin manifest (regression test for issue #24)', () => {
  it('plugin.json validates against the official Anthropic schema', () => {
    const pluginJsonPath = path.join(process.cwd(), '.claude-plugin', 'plugin.json');
    const raw = JSON.parse(fs.readFileSync(pluginJsonPath, 'utf-8'));
    const result = PluginManifestSchema.safeParse(raw);
    if (!result.success) {
      throw new Error(`plugin.json failed validation:\n${JSON.stringify(result.error.format(), null, 2)}`);
    }
  });

  it('plugin.json author is an object, not a string (issue #24 regression guard)', () => {
    const raw = JSON.parse(fs.readFileSync(path.join(process.cwd(), '.claude-plugin', 'plugin.json'), 'utf-8'));
    expect(typeof raw.author).toBe('object');
    expect(raw.author).not.toBeNull();
    expect(Array.isArray(raw.author)).toBe(false);
    expect(raw.author.name).toBeTruthy();
  });

  it('plugin.json does NOT contain a skills metadata array (issue #24 regression guard)', () => {
    const raw = JSON.parse(fs.readFileSync(path.join(process.cwd(), '.claude-plugin', 'plugin.json'), 'utf-8'));
    // The bug was: skills was an array of {name, description, path} objects.
    // The fix is: skills is omitted entirely OR is a string/string[] of paths.
    if (raw.skills !== undefined) {
      const ok = typeof raw.skills === 'string' || (Array.isArray(raw.skills) && raw.skills.every((s: unknown) => typeof s === 'string'));
      expect(ok, 'skills must be string or string[] per Anthropic schema').toBe(true);
    }
  });

  it('marketplace.json validates against the official Anthropic marketplace schema', () => {
    const marketplacePath = path.join(process.cwd(), '.claude-plugin', 'marketplace.json');
    const raw = JSON.parse(fs.readFileSync(marketplacePath, 'utf-8'));
    const result = MarketplaceManifestSchema.safeParse(raw);
    if (!result.success) {
      throw new Error(`marketplace.json failed validation:\n${JSON.stringify(result.error.format(), null, 2)}`);
    }
  });

  it('plugin name is kebab-case (matches what README documents users typing)', () => {
    const raw = JSON.parse(fs.readFileSync(path.join(process.cwd(), '.claude-plugin', 'plugin.json'), 'utf-8'));
    expect(raw.name).toMatch(/^[a-z0-9][a-z0-9-]*$/);
    expect(raw.name).toBe('opendirectory-gtm-skills');
  });
});
