import * as p from '@clack/prompts';
import chalk from 'chalk';
import { printBanner } from '../banner';
import { loadRegistry } from '../registry';
import { pickTarget, CancelledError } from './target-picker';
import { installSkill } from '../install-core';
import { terminalWidth } from '../tty';

export async function runBrowseTUI(opts: { target?: string; noBanner?: boolean } = {}): Promise<void> {
  try {
    printBanner({ hidden: opts.noBanner });
    p.intro(chalk.hex('#856FE6').bold(' OpenDirectory ') + chalk.dim('— agent skills for founders who hate marketing'));

    if (terminalWidth() < 60) {
      p.log.warn('Terminal is narrow — list may wrap awkwardly.');
    }

    const s = p.spinner();
    s.start('Loading skills...');
    const skills = await loadRegistry();
    s.stop('Skills loaded.');

    if (skills.length === 0) {
      p.note('No skills found in registry.', 'Empty');
      process.exit(0);
    }

    const selectedSkills = await p.autocompleteMultiselect({
      message: 'Type to filter · Space to select · Enter to confirm',
      options: skills.map(skill => ({
        value: skill.name,
        label: skill.name,
        hint: skill.description.length > 80
          ? skill.description.slice(0, 77) + '...'
          : skill.description
      })),
      maxItems: 10,
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

    let target = opts.target;
    if (!target) {
      target = await pickTarget();
    }

    const skillNames = selectedSkills as string[];
    p.note(`About to install: ${skillNames.join(', ')}\nTarget: ${target}`, 'Summary');

    const proceed = await p.confirm({
      message: 'Continue?',
      initialValue: true
    });

    if (p.isCancel(proceed) || !proceed) {
      p.cancel('Cancelled.');
      process.exit(0);
    }

    const successes: string[] = [];
    const failures: { name: string; error: string }[] = [];

    for (const name of skillNames) {
      const spinner = p.spinner();
      spinner.start(`Installing ${name}...`);
      const result = await installSkill(name, target);
      if (result.success) {
        spinner.stop(`✔ ${name}`);
        successes.push(name);
      } else {
        spinner.stop(`✗ ${name}: ${result.error?.message}`);
        failures.push({ name, error: result.error?.message || 'Unknown error' });
      }
    }

    p.outro(`Installed ${successes.length}/${skillNames.length} skills.`);

    if (failures.length > 0) {
      for (const f of failures) {
        p.log.error(`${f.name}: ${f.error}`);
      }
      process.exit(1);
    }

    process.exit(0);
  } catch (error) {
    if (error instanceof CancelledError) {
      p.cancel('Cancelled.');
      process.exit(0);
    }
    p.log.error(String(error));
    process.exit(1);
  }
}
