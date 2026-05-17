import * as p from '@clack/prompts';
import chalk from 'chalk';
import { printAnimatedBanner } from '../banner';
import { loadRegistry, type Skill } from '../registry';
import { pickTarget, CancelledError } from './target-picker';
import { installSkill } from '../install-core';
import { terminalWidth, isInteractive, noColor } from '../tty';
import { categoryFor, CATEGORY_ORDER } from '../categories';
import { printRandomTip } from '../tips';
import { BRAILLE_SPINNER_FRAMES, renderProgressBar } from '../animations';

type BrowseMode = 'all' | 'category';

const BRAND_PURPLE = '#856FE6';

function truncate(text: string, len: number): string {
  return text.length > len ? text.slice(0, len - 3) + '...' : text;
}

function styledFrame(frame: string): string {
  return noColor() ? frame : chalk.hex(BRAND_PURPLE)(frame);
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
    message: 'Type to filter (try a category like "social" or "video") · Space to select · Enter to confirm',
    options: skills.map(skill => {
      const cat = categoryFor(skill.name);
      return {
        value: skill.name,
        label: `${skill.name} ${chalk.dim('[' + cat + ']')}`,
        hint: truncate(skill.description, 80)
      };
    }),
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
  p.note(
    'TAB jumps to the next category. SHIFT+TAB jumps back. ' +
    'Press SPACE on a category name to select every skill in that group. ' +
    'Press SPACE on a single skill to toggle just that one. Press ENTER when done.',
    'Keyboard shortcuts'
  );
  return p.groupMultiselect({
    message: 'Select skills (TAB to jump categories, SPACE to select, ENTER to confirm)',
    options,
    maxItems: 18,
    required: true,
    selectableGroups: true
  });
}

function buildSpinnerOptions(): p.SpinnerOptions | undefined {
  if (noColor()) return undefined;
  return {
    frames: BRAILLE_SPINNER_FRAMES,
    delay: 80,
    styleFrame: styledFrame
  };
}

export async function runBrowseTUI(opts: { target?: string; noBanner?: boolean } = {}): Promise<void> {
  try {
    await printAnimatedBanner({ hidden: opts.noBanner });
    if (!opts.noBanner) printRandomTip();
    console.log();
    p.intro(chalk.hex(BRAND_PURPLE).bold(' OpenDirectory ') + chalk.dim('— agent skills for founders who hate marketing'));

    if (terminalWidth() < 60) {
      p.log.warn('Terminal is narrow — list may wrap awkwardly.');
    }

    const s = p.spinner(buildSpinnerOptions());
    s.start('Loading skills');
    const skills = await loadRegistry();
    s.stop(`${skills.length} skills loaded.`);

    if (skills.length === 0) {
      p.note('No skills found in registry.', 'Empty');
      process.exit(0);
    }

    const mode = await p.select<BrowseMode>({
      message: 'How would you like to browse?',
      options: [
        { value: 'category', label: 'Browse by category', hint: `${Object.keys(groupSkillsByCategory(skills)).length} categories, TAB to jump` },
        { value: 'all', label: 'Search all skills', hint: 'Type to filter across name, description, category' }
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
    p.note(`Installing ${skillNames.length} skill${skillNames.length === 1 ? '' : 's'} to ${chalk.hex(BRAND_PURPLE).bold(target)}\n${skillNames.join(', ')}`, 'Summary');

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
    const total = skillNames.length;
    const startedAt = Date.now();

    for (let i = 0; i < skillNames.length; i++) {
      const name = skillNames[i];
      const sp = p.spinner(buildSpinnerOptions());
      const progress = renderProgressBar(i, total);
      sp.start(`${progress}  ${name}`);
      const result = await installSkill(name, target);
      const finalProgress = renderProgressBar(i + 1, total);
      if (result.success) {
        sp.stop(`${finalProgress}  ${chalk.hex(BRAND_PURPLE).bold(name)} ${chalk.dim('installed')}`);
        successes.push(name);
      } else {
        sp.stop(`${finalProgress}  ${chalk.red(name)} ${chalk.dim('failed:')} ${result.error?.message}`);
        failures.push({ name, error: result.error?.message || 'Unknown error' });
      }
    }

    const seconds = ((Date.now() - startedAt) / 1000).toFixed(1);
    const outroLine = `Installed ${successes.length} of ${total} skill${total === 1 ? '' : 's'} in ${seconds}s`;
    if (isInteractive() && !noColor()) {
      p.outro(chalk.hex(BRAND_PURPLE).bold(outroLine));
    } else {
      p.outro(outroLine);
    }

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
