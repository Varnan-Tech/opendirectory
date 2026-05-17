import * as p from '@clack/prompts';
import chalk from 'chalk';
import { printAnimatedBanner } from '../banner';
import { loadRegistry, type Skill } from '../registry';
import { pickTarget, CancelledError } from './target-picker';
import { installSkill } from '../install-core';
import { terminalWidth } from '../tty';
import { categoryFor, CATEGORY_ORDER } from '../categories';

type BrowseMode = 'all' | 'category';

function truncate(text: string, len: number): string {
  return text.length > len ? text.slice(0, len - 3) + '...' : text;
}

function groupSkillsByCategory(skills: Skill[]): Record<string, Skill[]> {
  const groups: Record<string, Skill[]> = {};
  for (const skill of skills) {
    const cat = categoryFor(skill.name);
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(skill);
  }
  const ordered: Record<string, Skill[]> = {};
  for (const cat of CATEGORY_ORDER) {
    if (groups[cat]) ordered[cat] = groups[cat].sort((a, b) => a.name.localeCompare(b.name));
  }
  for (const cat of Object.keys(groups)) {
    if (!ordered[cat]) ordered[cat] = groups[cat].sort((a, b) => a.name.localeCompare(b.name));
  }
  return ordered;
}

async function selectFromAll(skills: Skill[]): Promise<string[] | symbol> {
  return p.autocompleteMultiselect({
    message: 'Type to filter · Space to select · Enter to confirm',
    options: skills.map(skill => ({
      value: skill.name,
      label: skill.name,
      hint: truncate(skill.description, 80)
    })),
    maxItems: 18,
    required: false
  });
}

async function selectFromCategories(skills: Skill[]): Promise<string[] | symbol> {
  const grouped = groupSkillsByCategory(skills);
  const options: Record<string, Array<{ value: string; label: string; hint?: string }>> = {};
  for (const [cat, list] of Object.entries(grouped)) {
    const count = list.length;
    const groupLabel = `${cat} ${chalk.dim(`(${count})`)}`;
    options[groupLabel] = list.map(skill => ({
      value: skill.name,
      label: skill.name,
      hint: truncate(skill.description, 70)
    }));
  }
  return p.groupMultiselect({
    message: 'Space to select · Enter to confirm · a to toggle category',
    options,
    maxItems: 18,
    required: false,
    selectableGroups: true
  });
}

export async function runBrowseTUI(opts: { target?: string; noBanner?: boolean } = {}): Promise<void> {
  try {
    await printAnimatedBanner({ hidden: opts.noBanner });
    p.intro(chalk.hex('#856FE6').bold(' OpenDirectory ') + chalk.dim('— agent skills for founders who hate marketing'));

    if (terminalWidth() < 60) {
      p.log.warn('Terminal is narrow — list may wrap awkwardly.');
    }

    const s = p.spinner();
    s.start('Loading skills...');
    const skills = await loadRegistry();
    s.stop(`${skills.length} skills loaded.`);

    if (skills.length === 0) {
      p.note('No skills found in registry.', 'Empty');
      process.exit(0);
    }

    const mode = await p.select<BrowseMode>({
      message: 'How would you like to browse?',
      options: [
        { value: 'category', label: 'Browse by category', hint: `${Object.keys(groupSkillsByCategory(skills)).length} categories` },
        { value: 'all', label: 'Search all skills', hint: 'Type to filter across all skills' }
      ],
      initialValue: 'category'
    });

    if (p.isCancel(mode)) {
      p.cancel('Cancelled.');
      process.exit(0);
    }

    const selectedSkills = mode === 'all'
      ? await selectFromAll(skills)
      : await selectFromCategories(skills);

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
