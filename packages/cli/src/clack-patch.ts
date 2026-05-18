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
 * WINDOWS TTY FREEZE FIX (Escape-key root cause).
 *
 * The bug:
 *   On Windows cmd.exe / conhost.exe, pressing Escape in a clack prompt and
 *   then having the next prompt open in the same tick wedges the terminal.
 *   No keys register on the new prompt, and the terminal stays broken after
 *   the process exits (user must close the window).
 *
 * Root cause (per Node.js issue #38663, "stdin keypress event lost after
 * escape pressed", and clack #408):
 *   1. Pressing Escape sends \x1b. readline waits `escapeCodeTimeout` (50ms)
 *      to see if more bytes follow (arrow keys, function keys, etc.).
 *   2. After the timeout, readline emits a `keypress` event with name='escape'.
 *   3. clack's onKeypress sets state='cancel' and SYNCHRONOUSLY calls close().
 *   4. close() does: unpipe() -> setRawMode(false) -> rl.close().
 *   5. But on Windows, rl.close() while readline is still retiring the escape
 *      sequence corrupts conhost mode flags. The next prompt's setRawMode(true)
 *      lands on a broken console: keypress events are silently dropped.
 *
 *   The Enter (submit) path doesn't trigger this because \r is processed
 *   instantly by readline with no pending-sequence state.
 *
 *   clack's own block() utility (used by spinners) already has these
 *   protections - sets rl.terminal=false, skips setRawMode on Windows -
 *   but the base Prompt.close() inherited none of them. See clack #408,
 *   #176, #76 and node #38663, #31762.
 *
 * The fix (on win32 TTY only):
 *   a) Set rl.terminal=false BEFORE close - prevents readline from emitting
 *      trailing ANSI cleanup codes that hang Windows mid-sequence.
 *   b) SKIP this.input.unpipe() - it corrupts process.stdin's internal state
 *      and was never matched by a pipe() anyway.
 *   c) SKIP setRawMode(false) - matches what clack's own block() does on
 *      Windows. The next prompt's setRawMode(true) is then a no-op; on
 *      process exit Node's built-in TTY teardown restores cooked mode.
 *   d) DEFER rl.close() and the cancel/submit event emit via setTimeout(0).
 *      This gives readline one event-loop tick to finish retiring the escape
 *      sequence before we tear it down - the critical fix for the freeze.
 *   e) Drain any stray bytes via input.read() so they don't poison the next
 *      readline interface.
 *   f) KEEP removeListener('keypress',...) - otherwise the old listener
 *      double-fires on the next prompt.
 *
 *   On non-Windows or non-TTY, delegate to the original close().
 *
 * Safety:
 *   Idempotent (guarded by `windowsClosePatched`). If a future clack release
 *   fixes this upstream the patch still runs but is functionally redundant.
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

    const captured = {
      rl: this.rl,
      input: this.input,
      output: this.output,
      onKeypress: this.onKeypress,
      state: this.state ?? 'cancel',
      value: this.value,
      emit: this.emit?.bind(this),
      unsubscribe: this.unsubscribe?.bind(this)
    };

    const swallow = (fn: () => unknown) => { try { fn(); } catch (_) { return; } };

    swallow(() => {
      if (captured.onKeypress && typeof captured.input?.removeListener === 'function') {
        captured.input.removeListener('keypress', captured.onKeypress);
      }
    });

    swallow(() => captured.output?.write('\n'));
    swallow(() => { if (captured.rl) (captured.rl as any).terminal = false; });

    this.rl = undefined;

    setTimeout(() => {
      swallow(() => {
        if (typeof captured.input?.read === 'function') captured.input.read();
      });
      swallow(() => captured.rl?.close?.());
      swallow(() => captured.emit?.(captured.state, captured.value));
      swallow(() => captured.unsubscribe?.());
    }, 0);
  };
}
