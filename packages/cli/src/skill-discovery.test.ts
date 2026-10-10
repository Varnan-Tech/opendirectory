import { afterEach, describe, expect, test } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { randomUUID } from 'node:crypto';
import { findSkillSource, findSkillSourceSync, loadSkillSource } from './skill-discovery';

const roots: string[] = [];

afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

function makeRoot(): string {
  const root = path.join(os.tmpdir(), `od-discovery-${randomUUID()}`);
  fs.mkdirSync(root, { recursive: true });
  roots.push(root);
  return root;
}

function writeSkill(root: string, parts: string[], content = '---\nname: nested\n---\n'): string {
  const dir = path.join(root, ...parts);
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, 'SKILL.md');
  fs.writeFileSync(file, content);
  return file;
}

describe('skill source discovery', () => {
  test.each([3, 4])('finds SKILL.md at depth %i', async depth => {
    const root = makeRoot();
    const parts = Array.from({ length: depth }, (_, index) => `level-${index}`);
    const expected = writeSkill(root, parts);

    expect(findSkillSourceSync(root)?.skillMdPath).toBe(expected);
    expect((await findSkillSource(root))?.skillMdPath).toBe(expected);
  });

  test('selects the lexically first source deterministically', () => {
    const root = makeRoot();
    const expected = writeSkill(root, ['a']);
    writeSkill(root, ['b']);
    expect(findSkillSourceSync(root)?.skillMdPath).toBe(expected);
  });

  test('prefers a shallow source over a deeper lexical branch for async and sync discovery', async () => {
    const root = makeRoot();
    const expected = writeSkill(root, ['src']);
    writeSkill(root, ['docs', 'examples']);

    expect(findSkillSourceSync(root)?.skillMdPath).toBe(expected);
    expect((await findSkillSource(root))?.skillMdPath).toBe(expected);
  });

  test('never selects sources below .git or node_modules', () => {
    const root = makeRoot();
    writeSkill(root, ['.git', 'hidden']);
    writeSkill(root, ['node_modules', 'hidden']);
    expect(findSkillSourceSync(root)).toBeNull();
  });

  test('missing roots are treated as no source', async () => {
    const root = path.join(os.tmpdir(), `od-missing-${randomUUID()}`);
    expect(findSkillSourceSync(root)).toBeNull();
    expect(await findSkillSource(root)).toBeNull();
  });

  test('source read failures produce an invalid compatibility state', async () => {
    const root = makeRoot();
    writeSkill(root, []);
    const loaded = await loadSkillSource(root, async () => {
      throw new Error('EACCES: permission denied');
    });
    expect(loaded?.frontmatter.compatibility).toEqual({
      kind: 'invalid',
      error: expect.stringContaining('Unable to read discovered SKILL.md'),
    });
  });
});
