import chalk from 'chalk';
import { isInteractive, noColor } from './tty';

export const BRAILLE_SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
export const BLOCK_PROGRESS_FRAMES = ['▏', '▎', '▍', '▌', '▋', '▊', '▉'];

const BRAND_PURPLE = '#856FE6';
const BRAND_PURPLE_DEEP = '#5B42F3';

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function renderProgressBar(current: number, total: number, width = 24): string {
  const ratio = total === 0 ? 0 : Math.min(1, Math.max(0, current / total));
  const filled = Math.round(ratio * width);
  const empty = width - filled;
  const filledBar = '█'.repeat(filled);
  const emptyBar = '░'.repeat(empty);
  if (noColor()) {
    return `[${filledBar}${emptyBar}] ${current}/${total}`;
  }
  const colored = chalk.hex(BRAND_PURPLE)(filledBar) + chalk.hex(BRAND_PURPLE_DEEP).dim(emptyBar);
  const counter = chalk.dim(`${current}/${total}`);
  return `${colored} ${counter}`;
}

export async function typewriter(text: string, speedMs = 14): Promise<void> {
  if (!isInteractive() || noColor()) {
    console.log(text);
    return;
  }
  for (const char of text) {
    process.stdout.write(char);
    await sleep(speedMs);
  }
  process.stdout.write('\n');
}

export async function ribbonSweep(text: string, lengthMs = 320): Promise<void> {
  if (!isInteractive() || noColor()) {
    console.log(text);
    return;
  }
  const total = text.length;
  const steps = Math.max(6, Math.min(total, 16));
  const stepMs = lengthMs / steps;
  for (let i = 1; i <= steps; i++) {
    const cut = Math.round((i / steps) * total);
    const visible = text.slice(0, cut);
    const ghost = text.slice(cut);
    process.stdout.write('\r' + chalk.hex(BRAND_PURPLE).bold(visible) + chalk.dim(ghost));
    await sleep(stepMs);
  }
  process.stdout.write('\n');
}
