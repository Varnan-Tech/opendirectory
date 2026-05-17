import * as p from '@clack/prompts';
import chalk from 'chalk';
import { readManifest, reconcile } from '../manifest';
import { uninstallSkill } from '../uninstall-core';
import { updateSkill } from '../update-core';

export async function runInstalledTUI(): Promise<void> {
  try {
    p.intro(chalk.hex('#856FE6').bold(' OpenDirectory ') + chalk.dim('— installed skills'));

    const s = p.spinner();
    s.start('Reconciling manifest...');
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
        value: `${skill.name}::${skill.target}`,
        label: `${chalk.yellow(skill.name)} ${chalk.gray('(' + skill.target + ')')}`
      })),
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

    let successCount = 0;
    const total = (selectedSkills as string[]).length;

    for (const selection of selectedSkills as string[]) {
      const [name, target] = selection.split('::');
      const spinner = p.spinner();
      
      if (action === 'uninstall') {
        spinner.start(`Removing ${name}...`);
        const result = await uninstallSkill(name, target);
        if (result.removed) {
          spinner.stop(`✔ ${name}`);
          successCount++;
        } else {
          spinner.stop(`✗ ${name}: ${result.error?.message}`);
        }
      } else if (action === 'update') {
        spinner.start(`Updating ${name}...`);
        const result = await updateSkill(name, target);
        if (result.success) {
          spinner.stop(`✔ ${name}`);
          successCount++;
        } else {
          spinner.stop(`✗ ${name}: ${result.error?.message}`);
        }
      }
    }

    p.outro(`Done. ${successCount}/${total} succeeded.`);
    process.exit(successCount > 0 ? 0 : 1);

  } catch (error) {
    p.log.error(String(error));
    process.exit(1);
  }
}
