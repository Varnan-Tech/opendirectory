import gradient from 'gradient-string';
import { isInteractive, noColor, terminalWidth } from './tty';

const BANNER_TEXT = `
 ██████╗ ██████╗ ███████╗███╗   ██╗    ██████╗ ██╗██████╗ 
██╔═══██╗██╔══██╗██╔════╝████╗  ██║    ██╔══██╗██║██╔══██╗
██║   ██║██████╔╝█████╗  ██╔██╗ ██║    ██║  ██║██║██████╔╝
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║    ██║  ██║██║██╔══██╗
╚██████╔╝██║     ███████╗██║ ╚████║    ██████╔╝██║██║  ██║
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝    ╚═════╝ ╚═╝╚═╝  ╚═╝
`;

const BANNER_WIDTH = 60; // measured from the rendered art

export interface BannerOptions {
  forceShow?: boolean;
  hidden?: boolean;
}

export function printBanner(opts: BannerOptions = {}): void {
  if (opts.hidden) return;
  if (!opts.forceShow && !isInteractive()) return;
  if (terminalWidth() < BANNER_WIDTH) {
    // Narrow terminal: print compact fallback
    if (noColor()) {
      console.log('\n  ◆ OPEN DIRECTORY\n  Skills for AI agents\n');
    } else {
      console.log('\n  ' + gradient(['#00ffff', '#ff00ff'])('◆ OPEN DIRECTORY') + '\n  Skills for AI agents\n');
    }
    return;
  }
  if (noColor()) {
    console.log(BANNER_TEXT);
    console.log('  Skills for AI agents\n');
    return;
  }
  console.log(gradient(['#00ffff', '#ff00ff']).multiline(BANNER_TEXT));
  console.log('  Skills for AI agents\n');
}
