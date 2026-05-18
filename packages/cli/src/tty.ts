export function isInteractive(): boolean {
  // True only when BOTH stdout and stdin are real TTYs AND not in CI.
  // Checking both prevents launching the TUI when stdin is redirected
  // (e.g. `echo … | opendirectory list`) — clack would otherwise wait
  // forever for keypresses that never arrive.
  return Boolean(process.stdout.isTTY) && Boolean(process.stdin.isTTY) && !process.env.CI;
}

export function noColor(): boolean {
  // Standard NO_COLOR honor: https://no-color.org/
  return process.env.NO_COLOR !== undefined && process.env.NO_COLOR !== '';
}

export function terminalWidth(): number {
  return process.stdout.columns || 80;
}

export function isPiped(): boolean {
  // Either stdout OR stdin redirected means we cannot trust a full TUI.
  return !process.stdout.isTTY || !process.stdin.isTTY;
}
