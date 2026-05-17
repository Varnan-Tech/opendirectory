export function isInteractive(): boolean {
  // True only when stdout is a real TTY AND not in CI
  return Boolean(process.stdout.isTTY) && !process.env.CI;
}

export function noColor(): boolean {
  // Standard NO_COLOR honor: https://no-color.org/
  return process.env.NO_COLOR !== undefined && process.env.NO_COLOR !== '';
}

export function terminalWidth(): number {
  return process.stdout.columns || 80;
}

export function isPiped(): boolean {
  return !process.stdout.isTTY;
}
