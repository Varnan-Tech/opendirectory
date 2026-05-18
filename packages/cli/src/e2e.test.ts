import { test, expect, beforeAll, beforeEach, afterEach } from 'vitest';
import { execSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { randomUUID } from 'node:crypto';

let tmpHome: string;
let originalHome: string | undefined;
let originalUserprofile: string | undefined;

beforeAll(() => {
  if (!fs.existsSync(path.join(process.cwd(), 'dist', 'index.js'))) {
    execSync('pnpm run build', { stdio: 'inherit' });
  }
});

beforeEach(() => {
  originalHome = process.env.HOME;
  originalUserprofile = process.env.USERPROFILE;
  tmpHome = path.join(os.tmpdir(), `od-test-${randomUUID()}`);
  fs.mkdirSync(tmpHome, { recursive: true });
  process.env.HOME = tmpHome;
  process.env.USERPROFILE = tmpHome;
});

afterEach(() => {
  fs.rmSync(tmpHome, { recursive: true, force: true });
  if (originalHome === undefined) delete process.env.HOME;
  else process.env.HOME = originalHome;
  if (originalUserprofile === undefined) delete process.env.USERPROFILE;
  else process.env.USERPROFILE = originalUserprofile;
});

test('installs skill via CLI args', async () => {
  const expectedPath = path.join(tmpHome, '.config/opencode/skills/claude-md-generator/SKILL.md');
  execSync('node dist/index.js install claude-md-generator --target opencode', { stdio: 'pipe' });
  expect(fs.existsSync(expectedPath)).toBe(true);
});

test('list --plain prints table identical to old format', async () => {
  const output = execSync('node dist/index.js list --plain', { stdio: 'pipe' }).toString();
  expect(output).toContain('Skill Name');
  expect(output).toContain('Description');
  expect(output).toContain('claude-md-generator');
});

test('list with piped stdout falls back to plain', async () => {
  const output = execSync('node dist/index.js list', { stdio: 'pipe' }).toString();
  expect(output).toContain('Skill Name');
  expect(output).toContain('Description');
});

test('NO_COLOR=1 strips all ANSI from output', async () => {
  const output = execSync('node dist/index.js list --plain', { stdio: 'pipe', env: { ...process.env, NO_COLOR: '1' } }).toString();
  expect(output).not.toMatch(/\x1b\[[0-9;]*m/);
});

test('install + uninstall round-trips manifest', async () => {
  execSync('node dist/index.js install claude-md-generator --target opencode', { stdio: 'pipe' });
  const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
  expect(fs.existsSync(manifestPath)).toBe(true);

  execSync('node dist/index.js uninstall claude-md-generator --target opencode', { stdio: 'pipe' });
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  expect(manifest.skills.length).toBe(0);
});

test('reconcile removes stale manifest entries', async () => {
  execSync('node dist/index.js install claude-md-generator --target opencode', { stdio: 'pipe' });
  const skillPath = path.join(tmpHome, '.config/opencode/skills/claude-md-generator');
  fs.rmSync(skillPath, { recursive: true, force: true });

  execSync('node dist/index.js installed --plain', { stdio: 'pipe', env: { ...process.env, CI: '1' } });

  const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  expect(manifest.skills.length).toBe(0);
});

test('--target flag overrides config default', async () => {
  const configPath = path.join(tmpHome, '.opendirectory/config.json');
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify({ defaultTarget: 'claude', version: 1 }));

  execSync('node dist/index.js install claude-md-generator --target opencode', { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, '.config/opencode/skills/claude-md-generator/SKILL.md'))).toBe(true);
  expect(fs.existsSync(path.join(tmpHome, '.claude/skills/claude-md-generator/SKILL.md'))).toBe(false);
});

test('install command accepts uppercase target (case-insensitive)', async () => {
  execSync('node dist/index.js install claude-md-generator --target OPENCODE', { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, '.config/opencode/skills/claude-md-generator/SKILL.md'))).toBe(true);
});

test('install command uses saved default target when --target omitted', async () => {
  const configPath = path.join(tmpHome, '.opendirectory/config.json');
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify({ defaultTarget: 'opencode', version: 1 }));

  execSync('node dist/index.js install claude-md-generator', { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, '.config/opencode/skills/claude-md-generator/SKILL.md'))).toBe(true);
});

test('non-existent skill errors with exact message', async () => {
  expect.assertions(2);
  try {
    execSync('node dist/index.js install non-existent-skill --target claude', { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.stderr.toString()).toContain("Error: Repository 'non-existent-skill' not found.");
    expect(error.status).toBe(1);
  }
});

test('uninstall not-installed skill errors clearly', async () => {
  expect.assertions(2);
  try {
    execSync('node dist/index.js uninstall some-skill --target claude', { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.stderr.toString()).toContain('Failed to uninstall:');
    expect(error.status).toBe(1);
  }
});

test('update of un-installed skill errors with "use install instead"', async () => {
  expect.assertions(2);
  try {
    execSync('node dist/index.js update claude-md-generator --target claude', { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.stderr.toString()).toContain('use install instead');
    expect(error.status).toBe(1);
  }
});

test('update is idempotent (replaces installed skill in place)', async () => {
  execSync('node dist/index.js install claude-md-generator --target opencode', { stdio: 'pipe' });
  const skillPath = path.join(tmpHome, '.config/opencode/skills/claude-md-generator/SKILL.md');
  expect(fs.existsSync(skillPath)).toBe(true);

  execSync('node dist/index.js update claude-md-generator --target opencode', { stdio: 'pipe' });
  expect(fs.existsSync(skillPath)).toBe(true);

  const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  expect(manifest.skills.length).toBe(1);
  expect(manifest.skills[0].name).toBe('claude-md-generator');
});
