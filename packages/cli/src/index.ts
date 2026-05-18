#!/usr/bin/env node

import { noColor, isInteractive, isPiped } from './tty';
if (noColor()) {
  process.env.FORCE_COLOR = '0';
}

import { Command } from 'commander';
import * as fsSync from 'node:fs';
import * as path from 'node:path';
import chalk from 'chalk';
import ora from 'ora';
import Table from 'cli-table3';

import { loadRegistry } from './registry';
import { installSkill } from './install-core';
import { uninstallSkill } from './uninstall-core';
import { updateSkill } from './update-core';
import { runBrowseTUI } from './tui/browse';
import { runInstalledTUI } from './tui/installed';
import { getDefaultTarget } from './config';
import { readManifest, reconcile } from './manifest';
import { enableTabJumpForGroupMultiselect, enableWindowsSafeClose } from './clack-patch';

enableWindowsSafeClose();
enableTabJumpForGroupMultiselect();

const program = new Command();

const pkg = JSON.parse(fsSync.readFileSync(path.join(__dirname, '../package.json'), 'utf-8'));

const SUPPORTED_TARGETS = 'opencode, claude, codex, gemini, anti-gravity, openclaw, hermes';

program
  .name('@opendirectory.dev/skills')
  .description(chalk.blue.bold('CLI to install OpenDirectory skills'))
  .version(pkg.version)
  .option('--no-banner', 'Hide the ASCII banner')
  .option('--plain', 'Force plain (non-interactive) output');

program.addHelpText('after', `
Examples:
  $ npx @opendirectory.dev/skills                          (interactive browser)
  $ npx @opendirectory.dev/skills list                     (interactive — install many)
  $ npx @opendirectory.dev/skills list --plain             (print table)
  $ npx @opendirectory.dev/skills install brand-alchemy -t claude
  $ npx @opendirectory.dev/skills install brand-alchemy    (uses saved default target)
  $ npx @opendirectory.dev/skills update brand-alchemy -t claude
  $ npx @opendirectory.dev/skills uninstall brand-alchemy -t claude
  $ npx @opendirectory.dev/skills installed                (manage installed)
  $ npx @opendirectory.dev/skills installed --plain        (list installed as a table)

Supported targets: ${SUPPORTED_TARGETS}
`);

async function printPlainTable() {
  const spinner = ora({
    text: 'Fetching available skills...',
    isEnabled: isInteractive()
  }).start();
  try {
    const skills = await loadRegistry();
    spinner.stop();
    console.log(chalk.green('Successfully loaded Open Directory registry!\n'));

    const table = new Table({
      head: [chalk.hex('#856FE6').bold('Skill Name'), chalk.hex('#856FE6').bold('Description')],
      colWidths: [35, 75],
      wordWrap: true,
      chars: noColor() ? {
        'top': '-', 'top-mid': '+', 'top-left': '+', 'top-right': '+',
        'bottom': '-', 'bottom-mid': '+', 'bottom-left': '+', 'bottom-right': '+',
        'left': '|', 'left-mid': '+', 'mid': '-', 'mid-mid': '+',
        'right': '|', 'right-mid': '+', 'middle': '|'
      } : undefined
    });

    for (const skill of skills) {
      let desc = skill.description || '';
      if (desc.length > 100) desc = desc.substring(0, 97) + '...';
      table.push([chalk.white.bold(skill.name), desc]);
    }

    console.log(table.toString());
    console.log(chalk.gray(`\nRun \`${chalk.white('npx "@opendirectory.dev/skills" install <skill-name> --target <agent>')}\` to install a skill.`));
  } catch (error) {
    spinner.stop();
    console.error(chalk.red('Failed to list skills.'));
    console.error(error);
  }
}

async function printInstalledPlainTable() {
  try {
    const { removed, added } = await reconcile();
    if (removed > 0) console.log(chalk.gray(`(removed ${removed} stale manifest entries)`));
    if (added > 0) console.log(chalk.gray(`(added ${added} pre-manifest installs)`));
    const m = await readManifest();
    if (m.skills.length === 0) {
      console.log('No skills installed.');
      return;
    }
    const table = new Table({
      head: ['Skill', 'Target', 'Version', 'Installed At'],
      colWidths: [30, 14, 12, 30],
      wordWrap: true,
    });
    for (const s of m.skills) {
      table.push([s.name, s.target, s.version, s.installedAt]);
    }
    console.log(table.toString());
  } catch (error) {
    console.error(chalk.red('Failed to read installed skills.'));
    console.error(error);
    process.exit(1);
  }
}

program.action(async () => {
  const globalOpts = program.opts();
  const wantsPlain = globalOpts.plain || isPiped() || !isInteractive();
  if (wantsPlain) {
    await printPlainTable();
  } else {
    await runBrowseTUI({ target: globalOpts.target, noBanner: !globalOpts.banner });
  }
});

program.command('list')
  .description('List available skills')
  .option('--plain', 'Print plain text table (no TUI)')
  .action(async (cmdOpts, command) => {
    const globalOpts = command.optsWithGlobals();
    const wantsPlain = cmdOpts.plain || globalOpts.plain || isPiped() || !isInteractive();
    if (wantsPlain) {
      await printPlainTable();
    } else {
      await runBrowseTUI({ target: globalOpts.target, noBanner: !globalOpts.banner });
    }
  });

program.command('install <skill>')
  .description('Install a skill for your AI agent')
  .option('-t, --target <tool>', `Target agent (${SUPPORTED_TARGETS}). Falls back to saved default.`)
  .action(async (skillName, opts) => {
    const target = (opts.target as string | undefined) || await getDefaultTarget();
    if (!target) {
      console.error(chalk.red('Error: No target specified and no default set.'));
      console.log(chalk.gray('Pass `--target <agent>` or run `npx @opendirectory.dev/skills` to set a default.'));
      console.log(chalk.gray(`Supported targets: ${SUPPORTED_TARGETS}`));
      process.exit(1);
    }
    const spinner = ora({
      text: `Installing ${chalk.white.bold(skillName)}...`,
      isEnabled: isInteractive()
    }).start();
    const result = await installSkill(skillName, target);

    if (result.success) {
      spinner.stop();
      console.log(chalk.green(`Successfully installed ${chalk.bold(result.skillName)}!`));
      console.log(`\n  ${chalk.hex('#856FE6')('Agent:')}   ${result.target}`);
      console.log(`  ${chalk.hex('#856FE6')('Scope:')}   Global`);
      console.log(`  ${chalk.hex('#856FE6')('Path:')}    ${result.path}\n`);
    } else {
      spinner.stop();
      if (result.error?.message.includes('Unsupported target')) {
        console.error(chalk.red(`Error: ${result.error.message}`));
        console.log(chalk.gray(`Supported targets: ${SUPPORTED_TARGETS}`));
      } else if (result.error?.message.includes('not found')) {
        console.error(chalk.red(`Error: ${result.error.message}`));
        console.log(chalk.gray(`Try running \`${chalk.white('npx "@opendirectory.dev/skills" list')}\` to see available skills.`));
      } else if (result.error?.message.includes('missing SKILL.md')) {
        console.error(chalk.red(`Error: ${result.error.message}`));
      } else {
        console.error(chalk.red('Failed to install skill.'));
        console.error(result.error);
      }
      process.exit(1);
    }
  });

program.command('update <skill>')
  .description('Update an installed skill')
  .option('-t, --target <tool>', 'Target agent (default: from config)')
  .action(async (skillName, opts) => {
    const target = opts.target || await getDefaultTarget();
    if (!target) {
      console.error(chalk.red('Error: No target specified and no default set.'));
      console.log(chalk.gray('Run `npx @opendirectory.dev/skills` to set a default.'));
      process.exit(1);
    }
    const spinner = ora({
      text: `Updating ${chalk.white.bold(skillName)}...`,
      isEnabled: isInteractive()
    }).start();
    const result = await updateSkill(skillName, target);
    if (result.success) {
      spinner.stop();
      console.log(chalk.green(`Successfully updated ${chalk.bold(skillName)}!`));
    } else {
      spinner.stop();
      console.error(chalk.red(`Failed to update: ${result.error?.message}`));
      process.exit(1);
    }
  });

program.command('uninstall <skill>')
  .description('Uninstall a skill')
  .option('-t, --target <tool>', 'Target agent (default: from config)')
  .action(async (skillName, opts) => {
    const target = opts.target || await getDefaultTarget();
    if (!target) {
      console.error(chalk.red('Error: No target specified and no default set.'));
      console.log(chalk.gray('Run `npx @opendirectory.dev/skills` to set a default.'));
      process.exit(1);
    }
    const spinner = ora({
      text: `Uninstalling ${chalk.white.bold(skillName)}...`,
      isEnabled: isInteractive()
    }).start();
    const result = await uninstallSkill(skillName, target);
    if (result.removed) {
      spinner.stop();
      console.log(chalk.green(`Successfully uninstalled ${chalk.bold(skillName)}!`));
    } else {
      spinner.stop();
      console.error(chalk.red(`Failed to uninstall: ${result.error?.message ?? 'Skill not found in manifest.'}`));
      console.log(chalk.gray(`Run \`npx @opendirectory.dev/skills installed\` to see what is installed.`));
      process.exit(1);
    }
  });

program.command('installed')
  .description('Manage installed skills (interactive)')
  .option('--plain', 'Print plain text table (no TUI)')
  .action(async (cmdOpts, command) => {
    const globalOpts = command.optsWithGlobals();
    const wantsPlain = cmdOpts.plain || globalOpts.plain || isPiped() || !isInteractive();
    if (wantsPlain) {
      await printInstalledPlainTable();
    } else {
      await runInstalledTUI();
    }
  });

program.parse();
