import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const SKILLS_DIR = path.join(process.cwd(), 'skills');
const PLACEHOLDER_RE = /^A skill for [a-z0-9-]+$/i;

type Failure = { file: string; reason: string; value: string };

function findSkillMd(dir: string): string[] {
  const out: string[] = [];
  const direct = path.join(dir, 'SKILL.md');
  if (fs.existsSync(direct)) out.push(direct);
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (['node_modules', '.git', 'references', 'evals'].includes(entry.name)) continue;
    out.push(...findSkillMd(path.join(dir, entry.name)));
  }
  return out;
}

const failures: Failure[] = [];
for (const folder of fs.readdirSync(SKILLS_DIR)) {
  const folderPath = path.join(SKILLS_DIR, folder);
  if (!fs.statSync(folderPath).isDirectory()) continue;
  const files = findSkillMd(folderPath);
  if (files.length === 0) {
    failures.push({ file: folderPath, reason: 'no SKILL.md found', value: '' });
    continue;
  }
  for (const file of files) {
    const { data } = matter(fs.readFileSync(file, 'utf-8'));
    const desc = data.description;
    if (desc === undefined || desc === null) {
      failures.push({ file, reason: 'no description in frontmatter', value: '' });
    } else if (typeof desc !== 'string') {
      failures.push({ file, reason: 'description is not a string', value: String(desc) });
    } else if (desc.includes('\n')) {
      // build-registry.ts uses a line-based YAML parser that mangles block scalars
      // (description: |). Reject multiline descriptions until both parsers are unified.
      failures.push({ file, reason: 'multiline description not supported by registry builder', value: desc });
    } else if (desc.trim() === '') {
      failures.push({ file, reason: 'empty description', value: desc });
    } else if (PLACEHOLDER_RE.test(desc.trim())) {
      failures.push({ file, reason: 'placeholder description', value: desc });
    } else if (desc.trim().length < 20) {
      failures.push({ file, reason: 'description shorter than 20 chars', value: desc });
    }
  }
}

if (failures.length > 0) {
  console.error(`\n[validate-skill-descriptions] ${failures.length} skill(s) failed:\n`);
  for (const f of failures) {
    console.error(`  - ${f.file}\n      reason: ${f.reason}\n      value:  ${JSON.stringify(f.value)}`);
  }
  process.exit(1);
}
console.log(`[validate-skill-descriptions] OK — all SKILL.md descriptions are populated.`);
