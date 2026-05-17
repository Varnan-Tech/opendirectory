import gradient from 'gradient-string';
import chalk from 'chalk';
import { isInteractive, noColor, terminalWidth } from './tty';

const BANNER_LINES = [
  ` ___________ _____ _   _______ ___________ _____ _____ _____ _____________   __`,
  `|  _  | ___ \\  ___| \\ | |  _  \\_   _| ___ \\  ___/  __ \\_   _|  _  | ___ \\ \\ / /`,
  `| | | | |_/ / |__ |  \\| | | | | | | | |_/ / |__ | /  \\/ | | | | | | |_/ /\\ V / `,
  `| | | |  __/|  __|| . \` | | | | | | |    /|  __|| |     | | | | | |    /  \\ /  `,
  `\\ \\_/ / |   | |___| |\\  | |/ / _| |_| |\\ \\| |___| \\__/\\ | | \\ \\_/ / |\\ \\  | |  `,
  ` \\___/\\_|   \\____/\\_| \\_/___/  \\___/\\_| \\_\\____/ \\____/ \\_/  \\___/\\_| \\_| \\_/  `,
];

const COMPACT_LINES = [
  ` ___________ _____ _   _ `,
  `|  _  | ___ \\  ___| \\ | |`,
  `| | | | |_/ / |__ |  \\| |`,
  `| | | |  __/|  __|| . \` |`,
  `\\ \\_/ / |   | |___| |\\  |`,
  ` \\___/\\_|   \\____/\\_| \\_/`,
];

const TAGLINE = 'agent skills for founders who hate marketing';

const BRAND_PURPLE_LIGHT = '#A88BFF';
const BRAND_PURPLE = '#856FE6';
const BRAND_PURPLE_DEEP = '#5B42F3';
const BRAND_PURPLE_DIM = '#6E5BC1';

const FULL_BANNER_WIDTH = 80;
const COMPACT_BANNER_WIDTH = 26;

export interface BannerOptions {
  forceShow?: boolean;
  hidden?: boolean;
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function renderTagline(): string {
  if (noColor()) {
    return `  ${TAGLINE}`;
  }
  return '  ' + chalk.hex(BRAND_PURPLE_DIM).italic(TAGLINE);
}

function paintLines(lines: string[], colorStops: string[]): string {
  const grad = gradient(colorStops);
  return lines.map(line => (line.length === 0 ? '' : grad(line))).join('\n');
}

export function printBanner(opts: BannerOptions = {}): void {
  if (opts.hidden) return;
  if (!opts.forceShow && !isInteractive()) return;

  const width = terminalWidth();

  if (width < COMPACT_BANNER_WIDTH) {
    if (noColor()) {
      console.log('\n  OPENDIRECTORY');
      console.log('  ' + TAGLINE + '\n');
    } else {
      console.log('\n  ' + chalk.hex(BRAND_PURPLE).bold('OPENDIRECTORY'));
      console.log('  ' + chalk.hex(BRAND_PURPLE_DIM).italic(TAGLINE) + '\n');
    }
    return;
  }

  const useCompact = width < FULL_BANNER_WIDTH;
  const lines = useCompact ? COMPACT_LINES : BANNER_LINES;

  if (noColor()) {
    console.log();
    for (const line of lines) console.log(line);
    console.log(renderTagline());
    console.log();
    return;
  }

  const stops = [BRAND_PURPLE_LIGHT, BRAND_PURPLE, BRAND_PURPLE_DEEP];
  console.log();
  console.log(paintLines(lines, stops));
  console.log(renderTagline());
  console.log();
}

export async function printAnimatedBanner(opts: BannerOptions = {}): Promise<void> {
  if (opts.hidden) return printBanner(opts);
  if (!opts.forceShow && !isInteractive()) return printBanner(opts);
  if (noColor()) return printBanner(opts);

  const width = terminalWidth();
  if (width < FULL_BANNER_WIDTH) {
    printBanner(opts);
    return;
  }

  const phases = [
    ['#3F3F46', '#52525B', '#71717A'],
    ['#71717A', '#9E85D9', BRAND_PURPLE],
    [BRAND_PURPLE_LIGHT, BRAND_PURPLE, BRAND_PURPLE_DEEP]
  ];

  const totalLines = BANNER_LINES.length;
  console.log();
  for (let i = 0; i < phases.length; i++) {
    if (i > 0) {
      process.stdout.write('\x1b[' + (totalLines + 1) + 'A');
    }
    console.log(paintLines(BANNER_LINES, phases[i]));
    if (i < phases.length - 1) await sleep(70);
  }
  console.log(renderTagline());
  console.log();
}
