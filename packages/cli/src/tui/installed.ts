import * as p from '@clack/prompts';
import chalk from 'chalk';
import { readManifest, reconcile } from '../manifest';
import { uninstallSkill } from '../uninstall-core';
import { updateSkill } from '../update-core';
import { noColor } from '../tty';
import { BRAILLE_SPINNER_FRAMES, renderProgressBar } from '../animations';

const BRAND_PURPLE = '#856FE6';

function styledFrame(frame: string): string {
  return noColor() ? frame : chalk.hex(BRAND_PURPLE)(frame);
}

function buildSpinnerOptions(): p.SpinnerOptions | undefined {
  if (noColor()) return undefined;
  return {
    frames: BRAILLE_SPINNER_FRAMES,
    delay: 80,
    styleFrame: styledFrame
  };
}

export async function runInstalledTUI(): Promise<void> {
  try {
    p.intro(chalk.hex(BRAND_PURPLE).bold(' OpenDirectory ') + chalk.dim('— installed skills'));

    const s = p.spinner(buildSpinnerOptions());
    s.start('Reconciling manifest');
    const { removed } = await reconcile();
    s.stop('Manifest reconciled.');

    if (removed > 0) {
      p.log.warn(`Removed ${removed} stale entries (files were deleted manually).`);
    }

    const manifest = await readManifest();
    if (manifest.skills.length === 0) {
      p.note('No skills installed yet. Run `npx @opendirectory.dev/skills` to browse.', 'Empty');
      process.exit(0);
    }

    const action = await p.select({
      message: 'What do you want to do?',
      options: [
        { value: 'update', label: 'Update a skill' },
        { value: 'uninstall', label: 'Uninstall a skill' },
        { value: 'exit', label: 'Exit' }
      ]
    });

    if (p.isCancel(action) || action === 'exit') {
      p.cancel('Exiting.');
      process.exit(0);
    }

    const selectedSkills = await p.multiselect({
      message: `Select skills to ${action} (Space to select, Enter to confirm):`,
      options: manifest.skills.map(skill => ({
        value: JSON.stringify({ name: skill.name, target: skill.target }),
        label: `${skill.name} ${chalk.dim('(' + skill.target + ')')}`
      })),
      maxItems: 18,
      required: false
    });

    if (p.isCancel(selectedSkills)) {
      p.cancel('Cancelled.');
      process.exit(0);
    }

    if (!selectedSkills || (selectedSkills as string[]).length === 0) {
      p.cancel('No skills selected.');
      process.exit(0);
    }

    const proceed = await p.confirm({
      message: `Continue with ${action}?`,
      initialValue: true
    });

    if (p.isCancel(proceed) || !proceed) {
      p.cancel('Cancelled.');
      process.exit(0);
    }

    const selections = selectedSkills as string[];
    const total = selections.length;
    let successCount = 0;
    const startedAt = Date.now();

    for (let i = 0; i < selections.length; i++) {
      const { name, target } = JSON.parse(selections[i]);
      const sp = p.spinner(buildSpinnerOptions());
      const progress = renderProgressBar(i, total);
      sp.start(`${progress}  ${action === 'uninstall' ? 'Removing' : 'Updating'} ${name}`);

      let ok = false;
      let errorMessage = '';
      if (action === 'uninstall') {
        const result = await uninstallSkill(name, target);
        ok = result.removed;
        errorMessage = result.error?.message || '';
      } else if (action === 'update') {
        const result = await updateSkill(name, target);
        ok = result.success;
        errorMessage = result.error?.message || '';
      }

      const finalProgress = renderProgressBar(i + 1, total);
      if (ok) {
        sp.stop(`${finalProgress}  ${chalk.hex(BRAND_PURPLE).bold(name)} ${chalk.dim(action === 'uninstall' ? 'removed' : 'updated')}`);
        successCount++;
      } else {
        sp.stop(`${finalProgress}  ${chalk.red(name)} ${chalk.dim('failed:')} ${errorMessage}`);
      }
    }

    const seconds = ((Date.now() - startedAt) / 1000).toFixed(3);
    p.outro(chalk.hex(BRAND_PURPLE).bold(`Done. ${successCount}/${total} succeeded in ${seconds}s.`));
    process.exit(successCount === total ? 0 : 1);

  } catch (error) {
    p.log.error(String(error));
    process.exit(1);
  }
}
