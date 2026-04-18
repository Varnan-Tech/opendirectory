import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { execSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';

describe('CLI End-to-End Tests', () => {
  let tempDir: string;
  let cliPath: string;

  beforeAll(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'opendirectory-cli-test-'));
    cliPath = path.resolve(__dirname, '../dist/index.js');
    
    if (!fs.existsSync(cliPath)) {
      execSync('pnpm run build', { cwd: path.resolve(__dirname, '..') });
    }
  });

  afterAll(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  it('should install a skill for opencode locally', () => {
    const skillName = 'claude-md-generator';
    
    // Set HOME and USERPROFILE to tempDir so that ~ resolves to tempDir
    const env = { ...process.env, HOME: tempDir, USERPROFILE: tempDir };
    
    execSync(`node "${cliPath}" install ${skillName} --target opencode`, { cwd: tempDir, env });
    
    const expectedPath = path.join(tempDir, '.config', 'opencode', 'skills', skillName, 'SKILL.md');
    expect(fs.existsSync(expectedPath)).toBe(true);
    
    const content = fs.readFileSync(expectedPath, 'utf-8');
    expect(content.length).toBeGreaterThan(0);
  });
});
