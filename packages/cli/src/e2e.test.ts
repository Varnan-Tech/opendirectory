import { test, expect, beforeAll, beforeEach, afterAll, afterEach } from 'vitest';
import { execSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { randomUUID } from 'node:crypto';

let tmpHome: string;
let originalHome: string | undefined;
let originalUserprofile: string | undefined;
const UNIVERSAL_SKILL = 'brand-alchemy';
const CLI_ROOT = path.resolve(__dirname, '..');
let originalCwd: string;

beforeAll(() => {
  originalCwd = process.cwd();
  process.chdir(CLI_ROOT);
  if (!fs.existsSync(path.join(CLI_ROOT, 'dist', 'index.js'))) {
    execSync('pnpm run build', { stdio: 'inherit', cwd: CLI_ROOT });
  }
});

afterAll(() => {
  process.chdir(originalCwd);
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
  const expectedPath = path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}/SKILL.md`);
  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  expect(fs.existsSync(expectedPath)).toBe(true);
});

test('list --plain prints table identical to old format', async () => {
  const output = execSync('node dist/index.js list --plain', { stdio: 'pipe' }).toString();
  expect(output).toContain('Skill Name');
  expect(output).toContain('Description');
  expect(output).toContain(UNIVERSAL_SKILL);
});

test('list with piped stdout falls back to plain', async () => {
  const output = execSync('node dist/index.js list', { stdio: 'pipe' }).toString();
  expect(output).toContain('Skill Name');
  expect(output).toContain('Description');
});

test('interactive browser exposes an explicit target option', () => {
  const output = execSync('node dist/index.js --help', { stdio: 'pipe' }).toString();
  expect(output).toContain('--target <tool>');
});

test('NO_COLOR=1 strips all ANSI from output', async () => {
  const output = execSync('node dist/index.js list --plain', { stdio: 'pipe', env: { ...process.env, NO_COLOR: '1' } }).toString();
  expect(output).not.toMatch(/\x1b\[[0-9;]*m/);
});

test('install + uninstall round-trips manifest', async () => {
  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
  expect(fs.existsSync(manifestPath)).toBe(true);

  execSync(`node dist/index.js uninstall ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  expect(manifest.skills.length).toBe(0);
});

test('reconcile removes stale manifest entries', async () => {
  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  const skillPath = path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}`);
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

  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}/SKILL.md`))).toBe(true);
  expect(fs.existsSync(path.join(tmpHome, `.claude/skills/${UNIVERSAL_SKILL}/SKILL.md`))).toBe(false);
});

test('install command accepts uppercase target (case-insensitive)', async () => {
  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target OPENCODE`, { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}/SKILL.md`))).toBe(true);
});

test('install command uses saved default target when --target omitted', async () => {
  const configPath = path.join(tmpHome, '.opendirectory/config.json');
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify({ defaultTarget: 'opencode', version: 1 }));

  execSync(`node dist/index.js install ${UNIVERSAL_SKILL}`, { stdio: 'pipe' });
  expect(fs.existsSync(path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}/SKILL.md`))).toBe(true);
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
    execSync(`node dist/index.js update ${UNIVERSAL_SKILL} --target claude`, { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.stderr.toString()).toContain('use install instead');
    expect(error.status).toBe(1);
  }
});

test('update is idempotent (replaces installed skill in place)', async () => {
  execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  const skillPath = path.join(tmpHome, `.config/opencode/skills/${UNIVERSAL_SKILL}/SKILL.md`);
  expect(fs.existsSync(skillPath)).toBe(true);

  execSync(`node dist/index.js update ${UNIVERSAL_SKILL} --target opencode`, { stdio: 'pipe' });
  expect(fs.existsSync(skillPath)).toBe(true);

  const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  expect(manifest.skills.length).toBe(1);
  expect(manifest.skills[0].name).toBe(UNIVERSAL_SKILL);
});

// --- Compatibility enforcement e2e tests ---

const COMPAT_FIXTURE_DIR = path.join(__dirname, '..', 'skills', 'test-compat-fixture');
const REGISTRY_PATH = path.join(__dirname, '..', 'registry.json');
const PROJECT_ROOT = path.resolve(__dirname, '..', '..', '..');
const ROOT_SKILLS_DIR = path.join(PROJECT_ROOT, 'skills');

function createCompatFixture(frontmatter: string, closeFrontmatter = true, nested = false) {
  const sourceDir = nested ? path.join(COMPAT_FIXTURE_DIR, 'nested', 'source') : COMPAT_FIXTURE_DIR;
  fs.mkdirSync(sourceDir, { recursive: true });
  const closing = closeFrontmatter ? '\n---\n\n# Test Skill\nThis is a test fixture.\n' : '\n';
  fs.writeFileSync(
    path.join(sourceDir, 'SKILL.md'),
    `---\nname: test-compat-fixture\ndescription: Test fixture for compatibility\n${frontmatter}${closing}`,
  );
}

function removeCompatFixture() {
  fs.rmSync(COMPAT_FIXTURE_DIR, { recursive: true, force: true });
}

function writeSkillFixture(skillDir: string, frontmatter: string, meta?: Record<string, unknown>) {
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(
    path.join(skillDir, 'SKILL.md'),
    `---\nname: ${path.basename(skillDir)}\ndescription: Compatibility fixture\n${frontmatter}\n---\n`,
  );
  if (meta) fs.writeFileSync(path.join(skillDir, 'skill.meta.json'), JSON.stringify(meta));
}

function addStaleRegistryFixture(): () => void {
  const original = fs.readFileSync(REGISTRY_PATH, 'utf-8');
  const registry = JSON.parse(original);
  registry.push({
    name: 'test-compat-fixture',
    description: 'Stale test registry entry',
    tags: [],
    author: 'test',
    version: '1.0.0',
    path: 'skills/test-compat-fixture',
    compatibility: ['codex'],
  });
  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2));
  return () => fs.writeFileSync(REGISTRY_PATH, original);
}

test('compatibility: [codex] + --target codex → succeeds', () => {
  try {
    createCompatFixture('compatibility: [codex]');
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    const skillPath = path.join(tmpHome, '.codex/skills/test-compat-fixture/SKILL.md');
    expect(fs.existsSync(skillPath)).toBe(true);
  } finally {
    removeCompatFixture();
  }
});

test('compatibility: [codex] + --target claude → exit 1, no dest dir, no manifest entry', () => {
  try {
    createCompatFixture('compatibility: [codex]');
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target claude', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports:');
    }
    // No destination directory created
    const destDir = path.join(tmpHome, '.claude/skills/test-compat-fixture');
    expect(fs.existsSync(destDir)).toBe(false);
    // No manifest entry
    const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
    if (fs.existsSync(manifestPath)) {
      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
      expect(manifest.skills.length).toBe(0);
    } else {
      expect(true).toBe(true); // no manifest file at all is also correct
    }
  } finally {
    removeCompatFixture();
  }
});

test('compatibility: [CODEX, " opencode "] normalizes and succeeds', () => {
  try {
    createCompatFixture('compatibility: [CODEX, " opencode "]');
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture/SKILL.md'))).toBe(true);
  } finally {
    removeCompatFixture();
  }
});

test('update of unknown skill with missing skills root returns an actionable error', async () => {
  const skillsRoot = path.join(CLI_ROOT, 'skills');
  const hiddenRoot = path.join(CLI_ROOT, `skills-missing-${randomUUID()}`);
  fs.renameSync(skillsRoot, hiddenRoot);
  try {
    expect.assertions(2);
    try {
      execSync('node dist/index.js update unknown-skill --target claude', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.stderr.toString()).toContain("missing SKILL.md in registry");
      expect(error.status).toBe(1);
    }
  } finally {
    fs.renameSync(hiddenRoot, skillsRoot);
  }
});

test('update of unknown skill with an existing skills root returns an actionable error', async () => {
  expect.assertions(2);
  try {
    execSync('node dist/index.js update unknown-skill --target claude', { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.stderr.toString()).toContain("missing SKILL.md in registry");
    expect(error.status).toBe(1);
  }
});

test('underscore-prefixed skills can be installed directly', () => {
  const skillName = '_underscore-compat-fixture';
  const sourceDir = path.join(__dirname, '..', 'skills', skillName);
  try {
    writeSkillFixture(sourceDir, '');
    execSync(`node dist/index.js install ${skillName} --target claude`, { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.claude/skills', skillName, 'SKILL.md'))).toBe(true);
  } finally {
    fs.rmSync(sourceDir, { recursive: true, force: true });
  }
});

test('--target " CODEX " is normalized before validation and installation', () => {
  try {
    createCompatFixture('compatibility: [codex]');
    execSync('node dist/index.js install test-compat-fixture --target " CODEX "', { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture/SKILL.md'))).toBe(true);
  } finally {
    removeCompatFixture();
  }
});

test('compatibility: [codex, opencode] + --target gemini → rejected', () => {
  try {
    createCompatFixture('compatibility: [codex, opencode]');
    expect.assertions(2);
    try {
      execSync('node dist/index.js install test-compat-fixture --target gemini', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports:');
    }
  } finally {
    removeCompatFixture();
  }
});

test('no compatibility field → installs to any target', () => {
  try {
    createCompatFixture('');
    execSync('node dist/index.js install test-compat-fixture --target gemini', { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.gemini/skills/test-compat-fixture/SKILL.md'))).toBe(true);
  } finally {
    removeCompatFixture();
  }
});

test('--target omitted, saved default incompatible → rejected', () => {
  try {
    createCompatFixture('compatibility: [codex]');
    const configPath = path.join(tmpHome, '.opendirectory/config.json');
    fs.mkdirSync(path.dirname(configPath), { recursive: true });
    fs.writeFileSync(configPath, JSON.stringify({ defaultTarget: 'claude', version: 1 }));

    expect.assertions(2);
    try {
      execSync('node dist/index.js install test-compat-fixture', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports:');
    }
  } finally {
    removeCompatFixture();
  }
});

test('update incompatible → rejected, existing files + manifest unchanged', () => {
  try {
    // First install with a universal fixture
    createCompatFixture('');
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    const skillPath = path.join(tmpHome, '.codex/skills/test-compat-fixture/SKILL.md');
    expect(fs.existsSync(skillPath)).toBe(true);

    const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
    const manifestBefore = fs.readFileSync(manifestPath, 'utf-8');
    const skillContentBefore = fs.readFileSync(skillPath, 'utf-8');

    // Change fixture to be incompatible with codex
    createCompatFixture('compatibility: [claude]');

    expect.assertions(5);
    try {
      execSync('node dist/index.js update test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports:');
    }

    // Verify files and manifest are byte-identical
    expect(fs.readFileSync(skillPath, 'utf-8')).toBe(skillContentBefore);
    expect(fs.readFileSync(manifestPath, 'utf-8')).toBe(manifestBefore);
  } finally {
    removeCompatFixture();
  }
});

test('list --plain shows Compatibility column with all and canonical ordering', () => {
  try {
    createCompatFixture('compatibility: [ OPENCODE, CODEX ]');
    const output = execSync('node dist/index.js list --plain', { stdio: 'pipe' }).toString();
    expect(output).toContain('Compatibility');
    expect(output).toContain('codex, opencode');
    expect(output).toContain('all');
  } finally {
    removeCompatFixture();
  }
});

test('uppercase --target CODEX preserves existing behavior', () => {
  try {
    createCompatFixture('compatibility: [codex]');
    execSync('node dist/index.js install test-compat-fixture --target CODEX', { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture/SKILL.md'))).toBe(true);
  } finally {
    removeCompatFixture();
  }
});

test.each([
  ['number member', 'compatibility: [codex, 1]', 'item 2 must be a string'],
  ['null member', 'compatibility: [codex, null]', 'item 2 must be a string'],
  ['alias', 'compatibility: [claude-code]', 'unknown target "claude-code"'],
  ['unknown target', 'compatibility: [codex, unknown-target]', 'unknown target "unknown-target"'],
])('invalid explicit compatibility (%s) is never universal', (_label, frontmatter, expectedError) => {
  try {
    createCompatFixture(frontmatter);
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain(expectedError);
    }
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('malformed compatibility YAML rejects install before destination or manifest mutation', () => {
  try {
    createCompatFixture('compatibility: [codex');
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('Invalid YAML frontmatter');
    }
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('malformed compatibility YAML rejects update before backup or mutation', () => {
  try {
    createCompatFixture('');
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    const skillPath = path.join(tmpHome, '.codex/skills/test-compat-fixture');
    const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
    const skillContentBefore = fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8');
    const manifestBefore = fs.readFileSync(manifestPath, 'utf-8');

    createCompatFixture('compatibility: [codex');
    expect.assertions(6);
    try {
      execSync('node dist/index.js update test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('Invalid YAML frontmatter');
    }
    expect(fs.existsSync(skillPath)).toBe(true);
    expect(fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8')).toBe(skillContentBefore);
    expect(fs.readFileSync(manifestPath, 'utf-8')).toBe(manifestBefore);
    expect(fs.readdirSync(path.dirname(skillPath)).some(entry => entry.includes('.bak.'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('unterminated compatibility frontmatter rejects install before mutation', () => {
  try {
    createCompatFixture('compatibility: [codex', false);
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('missing closing --- delimiter');
    }
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('unterminated compatibility frontmatter rejects update before mutation', () => {
  try {
    createCompatFixture('');
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    const skillPath = path.join(tmpHome, '.codex/skills/test-compat-fixture');
    const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
    const skillContentBefore = fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8');
    const manifestBefore = fs.readFileSync(manifestPath, 'utf-8');

    createCompatFixture('compatibility: [codex', false);
    expect.assertions(6);
    try {
      execSync('node dist/index.js update test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('missing closing --- delimiter');
    }
    expect(fs.existsSync(skillPath)).toBe(true);
    expect(fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8')).toBe(skillContentBefore);
    expect(fs.readFileSync(manifestPath, 'utf-8')).toBe(manifestBefore);
    expect(fs.readdirSync(path.dirname(skillPath)).some(entry => entry.includes('.bak.'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test.each(['constructor', 'toString'])('unsupported inherited target %s returns an actionable error', target => {
  expect.assertions(2);
  try {
    execSync(`node dist/index.js install ${UNIVERSAL_SKILL} --target ${target}`, { stdio: 'pipe' });
  } catch (error: any) {
    expect(error.status).toBe(1);
    expect(error.stderr.toString()).toContain(`Unsupported target '${target}'.`);
  }
});

test('local omission is universal despite stale registry compatibility', () => {
  const restoreRegistry = addStaleRegistryFixture();
  try {
    createCompatFixture('');
    execSync('node dist/index.js install test-compat-fixture --target claude', { stdio: 'pipe' });
    expect(fs.existsSync(path.join(tmpHome, '.claude/skills/test-compat-fixture/SKILL.md'))).toBe(true);
  } finally {
    restoreRegistry();
    removeCompatFixture();
  }
});

test('local compatibility controls over stale registry compatibility', () => {
  const restoreRegistry = addStaleRegistryFixture();
  try {
    createCompatFixture('compatibility: [claude]');
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports: claude');
    }
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    restoreRegistry();
    removeCompatFixture();
  }
});

test('nested local compatibility rejects an incompatible target before side effects', () => {
  try {
    createCompatFixture('compatibility: [codex]', true, true);
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target claude', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports: codex');
    }
    expect(fs.existsSync(path.join(tmpHome, '.claude/skills/source'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('nested malformed source rejects update before backup or mutation', () => {
  try {
    createCompatFixture('', true, true);
    execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    const skillPath = path.join(tmpHome, '.codex/skills/source');
    const manifestPath = path.join(tmpHome, '.opendirectory/installed.json');
    const skillContentBefore = fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8');
    const manifestBefore = fs.readFileSync(manifestPath, 'utf-8');

    removeCompatFixture();
    createCompatFixture('compatibility: [codex', false, true);
    expect.assertions(6);
    try {
      execSync('node dist/index.js update test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('missing closing --- delimiter');
    }
    expect(fs.existsSync(skillPath)).toBe(true);
    expect(fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf-8')).toBe(skillContentBefore);
    expect(fs.readFileSync(manifestPath, 'utf-8')).toBe(manifestBefore);
    expect(fs.readdirSync(path.dirname(skillPath)).some(entry => entry.includes('.bak.'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('hidden source compatibility rejects before installation side effects', () => {
  const skillName = '.hidden-compat-fixture';
  const sourceDir = path.join(__dirname, '..', 'skills', skillName);
  try {
    writeSkillFixture(sourceDir, 'compatibility: [codex]');
    expect.assertions(4);
    try {
      execSync(`node dist/index.js install ${skillName} --target claude`, { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports: codex');
    }
    expect(fs.existsSync(path.join(tmpHome, '.claude/skills', skillName))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    fs.rmSync(sourceDir, { recursive: true, force: true });
  }
});

test('metadata.compatibility is rejected before installation side effects', () => {
  try {
    createCompatFixture('metadata:\n  compatibility: [codex]');
    expect.assertions(4);
    try {
      execSync('node dist/index.js install test-compat-fixture --target codex', { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('metadata.compatibility is not supported');
    }
    expect(fs.existsSync(path.join(tmpHome, '.codex/skills/test-compat-fixture'))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    removeCompatFixture();
  }
});

test('registry generation and PR validation reject metadata.compatibility', () => {
  const skillName = 'test-nested-metadata-fixture';
  const sourceSkillDir = path.join(ROOT_SKILLS_DIR, skillName);
  try {
    writeSkillFixture(sourceSkillDir, 'metadata:\n  compatibility: [codex]');
    expect.assertions(4);
    try {
      execSync('pnpm exec tsx scripts/build-registry.ts', { cwd: PROJECT_ROOT, stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(`${error.stdout}${error.stderr}`).toContain('metadata.compatibility is not supported');
    }
    try {
      execSync('pnpm exec tsx scripts/validate-pr.ts', { cwd: PROJECT_ROOT, stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(`${error.stdout}${error.stderr}`).toContain('metadata.compatibility is not supported');
    }
  } finally {
    fs.rmSync(sourceSkillDir, { recursive: true, force: true });
  }
});

test('SKILL.md compatibility controls generated registry and ignores skill.meta.json compatibility', () => {
  const skillName = 'test-meta-source-fixture';
  const runtimeSkillDir = path.join(__dirname, '..', 'skills', skillName);
  const sourceSkillDir = path.join(ROOT_SKILLS_DIR, skillName);
  const registryBefore = fs.readFileSync(REGISTRY_PATH, 'utf-8');
  try {
    writeSkillFixture(runtimeSkillDir, 'compatibility: [codex]', { compatibility: ['claude'] });
    writeSkillFixture(sourceSkillDir, 'compatibility: [codex]', { compatibility: ['claude'] });
    execSync('pnpm exec tsx scripts/build-registry.ts', { cwd: PROJECT_ROOT, stdio: 'pipe' });

    const entry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'))
      .find((skill: { name: string }) => skill.name === skillName);
    expect(entry.compatibility).toEqual(['codex']);

    expect.assertions(5);
    try {
      execSync(`node dist/index.js install ${skillName} --target claude`, { stdio: 'pipe' });
    } catch (error: any) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('supports: codex');
    }
    expect(fs.existsSync(path.join(tmpHome, '.claude/skills', skillName))).toBe(false);
    expect(fs.existsSync(path.join(tmpHome, '.opendirectory/installed.json'))).toBe(false);
  } finally {
    fs.writeFileSync(REGISTRY_PATH, registryBefore);
    fs.rmSync(runtimeSkillDir, { recursive: true, force: true });
    fs.rmSync(sourceSkillDir, { recursive: true, force: true });
  }
});
