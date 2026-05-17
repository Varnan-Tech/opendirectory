import gradient from 'gradient-string';
import chalk from 'chalk';
import { isInteractive, noColor, terminalWidth } from './tty';

const BANNER_ART = `
   ▄██████  ██████  ███████ ███    ██    ██████  ██ ██████  
  ██    ██ ██   ██ ██      ████   ██    ██   ██ ██ ██   ██ 
  ██    ██ ██████  █████   ██ ██  ██    ██   ██ ██ ██████  
  ██    ██ ██      ██      ██  ██ ██    ██   ██ ██ ██   ██ 
   ▀██████ ██      ███████ ██   ████    ██████  ██ ██   ██
`;

const COMPACT_ART = `
  ◇ OPEN·DIR
`;

const TAGLINE = 'agent skills for founders who hate marketing';
const DECOR_STARS = '✦ ✦ ✦';

const BRAND_COLORS = ['#22D3EE', '#856FE6', '#EC4899'];
const BRAND_PRIMARY = '#856FE6';
const BRAND_DIM = '#6E5BC1';

const FULL_BANNER_WIDTH = 64;
const COMPACT_BANNER_WIDTH = 18;

export interface BannerOptions {
  forceShow?: boolean;
  hidden?: boolean;
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function renderTaglineLine(): string {
  if (noColor()) {
    return `   ◇ ${TAGLINE} ◇`;
  }
  const diamond = chalk.hex(BRAND_PRIMARY)('◇');
  const text = chalk.hex(BRAND_DIM).italic(TAGLINE);
  return `   ${diamond} ${text} ${diamond}`;
}

function renderStars(): string {
  if (noColor()) return `   ${DECOR_STARS}`;
  return '   ' + chalk.hex(BRAND_PRIMARY).dim(DECOR_STARS);
}

export function printBanner(opts: BannerOptions = {}): void {
  if (opts.hidden) return;
  if (!opts.forceShow && !isInteractive()) return;

  const width = terminalWidth();

  if (width < COMPACT_BANNER_WIDTH) {
    if (noColor()) {
      console.log('\n  ◇ OPENDIRECTORY');
      console.log('  ' + TAGLINE + '\n');
    } else {
      console.log('\n  ' + chalk.hex(BRAND_PRIMARY).bold('◇ OPENDIRECTORY'));
      console.log('  ' + chalk.hex(BRAND_DIM).italic(TAGLINE) + '\n');
    }
    return;
  }

  const useCompact = width < FULL_BANNER_WIDTH;
  const art = useCompact ? COMPACT_ART : BANNER_ART;

  if (noColor()) {
    console.log(art);
    console.log(renderTaglineLine());
    console.log(renderStars());
    console.log();
    return;
  }

  const grad = gradient(BRAND_COLORS);
  console.log(grad.multiline(art));
  console.log(renderTaglineLine());
  console.log(renderStars());
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
    ['#71717A', '#A78BFA', '#C084FC'],
    BRAND_COLORS
  ];

  const bannerLines = BANNER_ART.split('\n').length;
  for (let i = 0; i < phases.length; i++) {
    if (i > 0) {
      process.stdout.write('\x1b[' + bannerLines + 'A');
    }
    const grad = gradient(phases[i]);
    console.log(grad.multiline(BANNER_ART));
    if (i < phases.length - 1) await sleep(80);
  }
  console.log(renderTaglineLine());
  console.log(renderStars());
  console.log();
}
