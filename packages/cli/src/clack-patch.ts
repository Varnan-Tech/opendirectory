import { GroupMultiSelectPrompt } from '@clack/core';

let patched = false;

export function enableTabJumpForGroupMultiselect(): void {
  if (patched) return;
  patched = true;

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
