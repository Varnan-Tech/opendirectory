import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { randomUUID } from 'node:crypto';
import * as prompts from '@clack/prompts';
import { runBrowseTUI, browseByCategory, searchAllSkills } from './browse';
import type { Skill } from '../registry';
import { prepareInstallSkill, installPreparedSkill } from '../install-core';

vi.mock('@clack/prompts', () => ({
  autocompleteMultiselect: vi.fn(),
  groupMultiselect: vi.fn(),
  select: vi.fn(),
  confirm: vi.fn(),
  spinner: vi.fn(() => ({ start: vi.fn(), stop: vi.fn() })),
  note: vi.fn(),
  cancel: vi.fn(),
  outro: vi.fn(),
  isCancel: vi.fn(() => false),
  log: { warn: vi.fn(), error: vi.fn() },
}));

vi.mock('../banner', () => ({ printAnimatedBanner: vi.fn() }));
vi.mock('../registry', () => ({ loadRegistry: vi.fn() }));
vi.mock('../tips', () => ({ printRandomTip: vi.fn() }));
vi.mock('../tty', () => ({ terminalWidth: vi.fn(() => 80), isInteractive: vi.fn(() => false), noColor: vi.fn(() => true) }));
vi.mock('../animations', () => ({ BRAILLE_SPINNER_FRAMES: [], renderProgressBar: vi.fn(() => '[progress]') }));
vi.mock('./target-picker', () => ({
  pickTarget: vi.fn(async () => 'codex'),
  CancelledError: class CancelledError extends Error {},
}));
vi.mock('../install-core', () => ({
  prepareInstallSkill: vi.fn(),
  installPreparedSkill: vi.fn(),
}));

const universal = (name: string): Skill => ({
  name,
  description: name,
  tags: [],
  author: 'test',
  version: '1.0.0',
  path: `skills/${name}`,
  compatibilityState: { kind: 'missing' },
});

const declared = (name: string, targets: string[]): Skill => ({
  ...universal(name),
  compatibilityState: { kind: 'valid', targets },
  compatibility: targets,
  hasCompatibility: true,
});

const optionValues = (options: Record<string, Array<{ value: string; hint?: string; disabled?: boolean }>>) =>
  Object.values(options).flat();

beforeEach(() => {
  vi.clearAllMocks();
  vi.spyOn(process, 'exit').mockImplementation((() => undefined) as never);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('compatibility-aware skill pickers', () => {
  test('search mode shows support hints and disables incompatible skills for an explicit target', async () => {
    vi.mocked(prompts.autocompleteMultiselect).mockResolvedValue([]);

    await searchAllSkills([
      universal('all-skill'),
      declared('codex-skill', ['codex']),
      declared('claude-skill', ['claude']),
    ], 'codex');

    const options = vi.mocked(prompts.autocompleteMultiselect).mock.calls[0][0].options;
    expect(options).toEqual([
      expect.objectContaining({ value: 'all-skill', hint: expect.stringContaining('supports: all'), disabled: false }),
      expect.objectContaining({ value: 'codex-skill', hint: expect.stringContaining('supports: codex'), disabled: false }),
      expect.objectContaining({ value: 'claude-skill', hint: expect.stringContaining('supports: claude'), disabled: true }),
    ]);
  });

  test('category mode shows support hints and disables incompatible skills for an explicit target', async () => {
    vi.mocked(prompts.groupMultiselect).mockResolvedValue([]);

    await browseByCategory([
      universal('all-skill'),
      declared('codex-skill', ['codex']),
      declared('claude-skill', ['claude']),
    ], 'codex');

    const options = vi.mocked(prompts.groupMultiselect).mock.calls[0][0].options;
    expect(optionValues(options)).toEqual(expect.arrayContaining([
      expect.objectContaining({ value: 'all-skill', hint: expect.stringContaining('supports: all'), disabled: false }),
      expect.objectContaining({ value: 'codex-skill', hint: expect.stringContaining('supports: codex'), disabled: false }),
      expect.objectContaining({ value: 'claude-skill', hint: expect.stringContaining('supports: claude'), disabled: true }),
    ]));
  });

  test.each([
    ['search', 'all'],
    ['category', 'category'],
  ])('%s mode retains prior selections and names conflicting declarations on retry', async (mode, modeValue) => {
    const selectedBeforeRetry = ['codex-skill', 'claude-skill'];
    const selectedAfterRetry = ['codex-skill'];
    const skills = [declared('codex-skill', ['codex']), declared('claude-skill', ['claude'])];
    const { loadRegistry } = await import('../registry');
    vi.mocked(loadRegistry).mockResolvedValue(skills);
    vi.mocked(prompts.select)
      .mockResolvedValueOnce(modeValue)
      .mockResolvedValueOnce(modeValue);
    if (mode === 'search') {
      vi.mocked(prompts.autocompleteMultiselect)
        .mockResolvedValueOnce(selectedBeforeRetry)
        .mockResolvedValueOnce(selectedAfterRetry);
    } else {
      vi.mocked(prompts.groupMultiselect)
        .mockResolvedValueOnce(selectedBeforeRetry)
        .mockResolvedValueOnce(selectedAfterRetry);
    }
    vi.mocked(prompts.confirm).mockResolvedValue(true);
    vi.mocked(prepareInstallSkill).mockResolvedValue({
      skillName: 'codex-skill',
      target: 'codex',
      success: true,
      preparation: {
        skillName: 'codex-skill',
        target: 'codex',
        skillDir: path.join(os.tmpdir(), 'codex-skill'),
        manifestName: 'codex-skill',
        destPath: path.join(os.tmpdir(), 'codex-skill-dest'),
        version: '1.0.0',
      },
    });
    vi.mocked(installPreparedSkill).mockResolvedValue({
      skillName: 'codex-skill',
      target: 'codex',
      path: path.join(os.tmpdir(), 'codex-skill-dest'),
      success: true,
    });

    await runBrowseTUI({ noBanner: true });

    const picker = mode === 'search'
      ? vi.mocked(prompts.autocompleteMultiselect)
      : vi.mocked(prompts.groupMultiselect);
    expect(picker.mock.calls[1][0].initialValues).toEqual(selectedBeforeRetry);
    const notes = vi.mocked(prompts.note).mock.calls.map(([message]) => String(message));
    expect(notes.some(message =>
      message.includes('codex-skill (supports: codex)') && message.includes('claude-skill (supports: claude)'),
    )).toBe(true);
  });
});

test('browse preflight prepares every selected skill before entering the write phase', async () => {
  const root = path.join(os.tmpdir(), `od-browse-${randomUUID()}`);
  const firstDestination = path.join(root, 'codex', 'first');
  const manifestPath = path.join(root, 'manifest.json');
  fs.mkdirSync(root, { recursive: true });

  const { loadRegistry } = await import('../registry');
  vi.mocked(loadRegistry).mockResolvedValue([universal('first'), universal('second')]);
  vi.mocked(prompts.select).mockResolvedValue('all');
  vi.mocked(prompts.autocompleteMultiselect).mockResolvedValue(['first', 'second']);
  vi.mocked(prompts.confirm).mockResolvedValue(true);
  vi.mocked(prepareInstallSkill)
    .mockResolvedValueOnce({
      skillName: 'first',
      target: 'codex',
      success: true,
      preparation: {
        skillName: 'first',
        target: 'codex',
        skillDir: path.join(root, 'source', 'first'),
        manifestName: 'first',
        destPath: firstDestination,
        version: '1.0.0',
      },
    })
    .mockResolvedValueOnce({
      skillName: 'second',
      target: 'codex',
      success: false,
      error: new Error('source disappeared'),
    });

  try {
    await runBrowseTUI({ target: 'codex', noBanner: true });

    expect(vi.mocked(installPreparedSkill)).not.toHaveBeenCalled();
    expect(fs.existsSync(firstDestination)).toBe(false);
    expect(fs.existsSync(manifestPath)).toBe(false);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
