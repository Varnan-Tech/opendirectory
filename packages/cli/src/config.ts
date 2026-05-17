import { resolvePath } from './fs-adapters';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

export interface UserConfig {
  defaultTarget?: string;
  version: number; // schema version
}

const CONFIG_PATH_TILDE = '~/.opendirectory/config.json';
const CURRENT_SCHEMA = 1;

// CRITICAL: Node.js `fs` does NOT expand `~`. Always use resolvePath() before any fs.* call.
// Helper to get the absolute path:
function getConfigPath(): string {
  return resolvePath(CONFIG_PATH_TILDE);
}

export async function readConfig(): Promise<UserConfig> {
  const resolvedPath = getConfigPath();
  try {
    const content = await fs.readFile(resolvedPath, 'utf-8');
    const parsed = JSON.parse(content);
    if (parsed.version !== CURRENT_SCHEMA) {
      console.warn(`Warning: Config schema version mismatch. Expected ${CURRENT_SCHEMA}, got ${parsed.version}`);
    }
    return parsed;
  } catch (e) {
    return { version: CURRENT_SCHEMA };
  }
}

export async function writeConfig(config: UserConfig): Promise<void> {
  const resolvedPath = getConfigPath();
  const parentDir = path.dirname(resolvedPath);
  await fs.mkdir(parentDir, { recursive: true });
  
  const tmpPath = resolvedPath + '.tmp.' + process.pid;
  await fs.writeFile(tmpPath, JSON.stringify(config, null, 2), 'utf-8');
  await fs.rename(tmpPath, resolvedPath);
}

export async function setDefaultTarget(target: string): Promise<void> {
  const config = await readConfig();
  config.defaultTarget = target;
  await writeConfig(config);
}

export async function getDefaultTarget(): Promise<string | undefined> {
  const config = await readConfig();
  return config.defaultTarget;
}
