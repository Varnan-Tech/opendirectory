import chalk from 'chalk';
import { noColor } from './tty';

const TIPS: string[] = [
  'Press TAB to jump to the next category. Shift+TAB jumps back.',
  'Press SPACE on a category name to install every skill in that group at once.',
  'In "Search all skills" mode, type a category like "social" or "video" to filter.',
  'Skip the menu: npx @opendirectory.dev/skills install <skill> -t <agent>',
  'Manage installed skills with: npx @opendirectory.dev/skills installed',
  'Set a default agent so you never have to pass -t again. Pick it once when prompted.',
  'Use --plain to disable the TUI when scripting or running in CI.',
  'Set NO_COLOR=1 to disable all ANSI output (screen-reader friendly).',
  'Multi-select: pick skills across different categories in one go.',
  'Already installed? update <skill> pulls the latest version.',
  'New skills land in OpenDirectory monthly. Run list to see what is new.',
  'Contribute your own skill at github.com/Varnan-Tech/opendirectory',
];

export function randomTip(): string {
  return TIPS[Math.floor(Math.random() * TIPS.length)];
}

export function formatTip(tip: string): string {
  if (noColor()) {
    return `  Tip: ${tip}`;
  }
  const label = chalk.hex('#856FE6').bold('Tip:');
  return `  ${label} ${chalk.dim(tip)}`;
}

export function printRandomTip(): void {
  console.log(formatTip(randomTip()));
}
