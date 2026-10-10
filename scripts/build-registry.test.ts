import { afterEach, describe, expect, test } from 'vitest';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { randomUUID } from 'node:crypto';
import { buildRegistry } from './build-registry';

const roots: string[] = [];

afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

describe('buildRegistry metadata precedence', () => {
  test('skill.meta.json fields win while compatibility comes from SKILL.md', () => {
    const root = path.join(os.tmpdir(), `od-registry-${randomUUID()}`);
    const skillsDir = path.join(root, 'skills');
    const outputFile = path.join(root, 'registry.json');
    const skillDir = path.join(skillsDir, 'metadata-fixture');
    roots.push(root);
    fs.mkdirSync(skillDir, { recursive: true });

    fs.writeFileSync(path.join(skillDir, 'SKILL.md'), [
      '---',
      'name: metadata-fixture',
      'description: Frontmatter description',
      'tags: [frontmatter]',
      'author: Frontmatter Author',
      'version: 1.0.0',
      'compatibility: [codex]',
      '---',
      '',
      '# Metadata fixture',
    ].join('\n'));
    fs.writeFileSync(path.join(skillDir, 'skill.meta.json'), JSON.stringify({
      description: 'JSON description',
      tags: ['json'],
      author: 'JSON Author',
      version: '9.9.9',
      compatibility: ['claude'],
    }));

    const registry = buildRegistry(skillsDir, outputFile);
    const entry = registry.find(skill => skill.name === 'metadata-fixture');

    expect(entry).toMatchObject({
      description: 'JSON description',
      tags: ['json'],
      author: 'JSON Author',
      version: '9.9.9',
      compatibility: ['codex'],
    });
    expect(JSON.parse(fs.readFileSync(outputFile, 'utf-8'))).toContainEqual(entry);
  });
});
