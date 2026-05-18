import { GroupMultiSelectPrompt, Prompt } from '@clack/core';

let tabPatched = false;
let windowsClosePatched = false;

export function enableTabJumpForGroupMultiselect(): void {
  if (tabPatched) return;
  tabPatched = true;

  const proto = GroupMultiSelectPrompt.prototype as any;
  const originalPrompt = proto.prompt;

  proto.prompt = function () {
    if (!this._tabListenerAdded) {
      this.on('key', (_char: string, key: { name?: string; shift?: boolean }) => {
        if (key?.name !== 'tab') return;
        const optsLength = this.options.length;
        if (optsLength === 0) return;

        let newCursor = this.cursor;

        if (key.shift) {
          for (let i = this.cursor - 1; i >= -optsLength; i--) {
            const index = (i + optsLength) % optsLength;
            if (this.options[index].group === true) {
              newCursor = index;
              break;
            }
          }
        } else {
          for (let i = this.cursor + 1; i < this.cursor + optsLength; i++) {
            const index = i % optsLength;
            if (this.options[index].group === true) {
              newCursor = index;
              break;
            }
          }
        }

        this.cursor = newCursor;
      });
      this._tabListenerAdded = true;
    }
    return originalPrompt.call(this);
  };
}

/**
 * WINDOWS TTY FREEZE FIX.
 *
 * Why this exists:
 *   On Windows cmd.exe / conhost.exe, @clack/core's `Prompt.close()` triggers a
 *   well-known race condition when one prompt closes and another opens in the
 *   same tick (e.g. p.select() resolving and p.autocompleteMultiselect() starting):
 *
 *     1. close() calls `input.unpipe()` on process.stdin - corrupts stream state.
 *     2. close() calls `setRawMode(false)` - this dispatches an async
 *        SetConsoleMode() through libuv's helper thread (libuv #852).
 *     3. The next prompt immediately calls `setRawMode(true)` while step 2's
 *        async toggle is still in flight, racing with libuv's ReadConsole.
 *     4. Result: conhost.exe wedges. Keypress emitter detaches (node #49588).
 *        Terminal renders the new prompt but accepts zero input. Even after
 *        the process dies the console stays in a half-raw state, requiring
 *        the user to close the window.
 *
 *   Clack already knows about this - their `block()` utility (used by spinners)
 *   has an explicit `!isWindows` guard around setRawMode(false). But the base
 *   `Prompt.close()` lacks this guard. See clack #408, #176, #76.
 *
 * The fix:
 *   On win32 only, override `Prompt.prototype.close` to:
 *     - SKIP `input.unpipe()` (preserves stdin internal state).
 *     - SKIP `setRawMode(false)` (avoids the libuv race - the next prompt's
 *       `setRawMode(true)` is a no-op since we're already raw, and on process
 *       exit Node restores cooked mode via its built-in TTY cleanup).
 *     - KEEP `removeListener('keypress', ...)` (otherwise the old listener
 *       fires on the new prompt's input - duplicate handling).
 *     - KEEP `rl.close()`, the newline write, the state emit, and unsubscribe()
 *       (these are not the source of the race).
 *
 *   On non-Windows, this is a no-op - we delegate straight to the original.
 *
 * Safety:
 *   The patch is idempotent (guarded by `windowsClosePatched`). If a future
 *   Clack release adds its own Windows guard to close(), this patch becomes
 *   redundant but not harmful - the platform check short-circuits everything.
 */
export function enableWindowsSafeClose(): void {
  if (windowsClosePatched) return;
  windowsClosePatched = true;

  if (process.platform !== 'win32') return;

  const proto = Prompt.prototype as any;
  const originalClose = proto.close;
  if (typeof originalClose !== 'function') return;

  proto.close = function (this: any): void {
    if (!process.stdin.isTTY) {
      return originalClose.call(this);
    }

    try {
      const onKeypress = this.onKeypress;
      if (onKeypress && typeof this.input?.removeListener === 'function') {
        this.input.removeListener('keypress', onKeypress);
      }

      try { this.output?.write('\n'); } catch { void 0; }

      try { this.rl?.close?.(); } catch { void 0; }
      this.rl = undefined;

      try {
        const state = this.state ?? 'cancel';
        this.emit?.(state, this.value);
      } catch { void 0; }

      try { this.unsubscribe?.(); } catch { void 0; }
    } catch {
      try { return originalClose.call(this); } catch { void 0; }
    }
  };
}
