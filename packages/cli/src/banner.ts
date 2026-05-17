import gradient from 'gradient-string';
import chalk from 'chalk';
import { isInteractive, noColor, terminalWidth } from './tty';

const BANNER_TEXT = `
 ██████  ██████  ███████ ███    ██     ██████  ██ ██████  ███████  ██████ ████████  ██████  ██████  ██    ██
██    ██ ██   ██ ██      ████   ██     ██   ██ ██ ██   ██ ██      ██         ██    ██    ██ ██   ██  ██  ██
██    ██ ██████  █████   ██ ██  ██     ██   ██ ██ ██████  █████   ██         ██    ██    ██ ██████    ████
██    ██ ██      ██      ██  ██ ██     ██   ██ ██ ██   ██ ██      ██         ██    ██    ██ ██   ██    ██
 ██████  ██      ███████ ██   ████     ██████  ██ ██   ██ ███████  ██████    ██     ██████  ██   ██    ██
`;

const COMPACT_BANNER = `
 ██████  ██████  ███████ ███    ██
██    ██ ██   ██ ██      ████   ██
██    ██ ██████  █████   ██ ██  ██
██    ██ ██      ██      ██  ██ ██
 ██████  ██      ███████ ██   ████
`;

const TAGLINE = 'Agent skills for founders who hate marketing';
const BRAND_PURPLE = '#856FE6';
const BRAND_PURPLE_DARK = '#5B42F3';

const FULL_BANNER_WIDTH = 110;
const COMPACT_BANNER_WIDTH = 35;

export interface BannerOptions {
  forceShow?: boolean;
  hidden?: boolean;
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
      console.log('  ' + chalk.dim(TAGLINE) + '\n');
    }
    return;
  }

  const useCompact = width < FULL_BANNER_WIDTH;
  const art = useCompact ? COMPACT_BANNER : BANNER_TEXT;
  const labelLine = useCompact ? '  DIRECTORY' : null;

  if (noColor()) {
    console.log(art);
    if (labelLine) console.log(labelLine);
    console.log('  ' + TAGLINE + '\n');
    return;
  }

  const grad = gradient([BRAND_PURPLE, BRAND_PURPLE_DARK]);
  console.log(grad.multiline(art));
  if (labelLine) console.log(chalk.hex(BRAND_PURPLE).bold(labelLine));
  console.log('  ' + chalk.dim(TAGLINE) + '\n');
}
