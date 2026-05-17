import * as fs from 'node:fs/promises';
import { resolvePath } from './fs-adapters';

// Single source of truth — EXPORTED for use across install/uninstall/update cores.
// Maps agent name → base agent directory (where skills/ subdir lives).
export const AGENT_PATHS = {
  claude: '~/.claude',
  opencode: '~/.config/opencode',
  codex: '~/.codex',
  gemini: '~/.gemini',
  'anti-gravity': '~/.gemini/antigravity',
  openclaw: '~/.openclaw',
  hermes: '~/.hermes',
} as const;

export type ValidAgent = keyof typeof AGENT_PATHS;

export function isValidAgent(s: string): s is ValidAgent {
  return s in AGENT_PATHS;
}

// Base agent dir (e.g., ~/.claude) — for detection.
export function getAgentBaseDir(agent: ValidAgent): string {
  return resolvePath(AGENT_PATHS[agent]);
}

// Actual skills install dir (e.g., ~/.claude/skills) — for install/uninstall.
export function getAgentSkillsDir(agent: ValidAgent): string {
  return resolvePath(AGENT_PATHS[agent]) + '/skills';
}

export interface AgentDetection {
  name: ValidAgent;
  installed: boolean;
  path: string;  // absolute base dir
}

export async function detectAgents(): Promise<AgentDetection[]> {
  const results: AgentDetection[] = [];
  for (const [name, p] of Object.entries(AGENT_PATHS)) {
    const resolved = resolvePath(p);
    try {
      const stat = await fs.stat(resolved);
      results.push({ name: name as ValidAgent, installed: stat.isDirectory(), path: resolved });
    } catch {
      results.push({ name: name as ValidAgent, installed: false, path: resolved });
    }
  }
  return results;
}
