#!/usr/bin/env node

import { Command } from 'commander';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { Skill } from './transformers';
import { safeWriteFile } from './fs-adapters';
import chalk from 'chalk';
import ora from 'ora';
import Table from 'cli-table3';

const program = new Command();

program
  .name('@opendirectory.dev/skills')
  .description(chalk.blue.bold('CLI to install OpenDirectory skills'))
  .version('0.1.0');

const getProjectRoot = () => {
  return path.resolve(__dirname, '..');
};

program
  .command('list')
  .description('List available skills in the Open Directory registry')
  .action(async () => {
    const spinner = ora('Fetching available skills...').start();
    try {
      const root = getProjectRoot();
      const registryPath = path.join(root, 'registry.json');
      
      let skills: any[] = [];
      try {
        const registryContent = await fs.readFile(registryPath, 'utf-8');
        skills = JSON.parse(registryContent);
      } catch (e) {
        const skillsDir = path.join(root, 'skills');
        const entries = await fs.readdir(skillsDir, { withFileTypes: true });
        skills = entries
          .filter(entry => entry.isDirectory())
          .map(entry => ({ name: entry.name, description: `Skill: ${entry.name}` }));
      }

      spinner.stop();
      console.log(chalk.green('Successfully loaded Open Directory registry!\n'));

      const table = new Table({
        head: [chalk.cyan.bold('Skill Name'), chalk.cyan.bold('Description')],
        colWidths: [35, 75],
        wordWrap: true
      });

      for (const skill of skills) {
        let desc = skill.description || '';
        desc = desc.replace(/<img[^>]*>/g, '').trim();
        if (desc.length > 100) desc = desc.substring(0, 97) + '...';
        
        table.push([chalk.yellow(skill.name), desc]);
      }
      
      console.log(table.toString());
      console.log(chalk.gray(`\nRun \`${chalk.white('npx "@opendirectory.dev/skills" install <skill-name> --target <agent>')}\` to install a skill.`));

    } catch (error) {
      spinner.stop();
      console.error(chalk.red('Failed to list skills.'));
      console.error(error);
    }
  });

program
  .command('install <skill>')
  .description('Install a skill for your AI agent')
  .requiredOption('-t, --target <tool>', 'Target agent (opencode, claude, codex, gemini, anti-gravity, openclaw, hermes)')
  .action(async (skillName, options) => {
    const spinner = ora(`Installing ${chalk.yellow(skillName)}...`).start();
    try {
      const root = getProjectRoot();
      const repoDir = path.join(root, 'skills', skillName);
      
      let skillDir = repoDir;
      let skillMdPath = path.join(skillDir, 'SKILL.md');
      
      try {
        await fs.access(skillMdPath);
      } catch (e) {
        try {
          const entries = await fs.readdir(repoDir, { withFileTypes: true });
          for (const entry of entries) {
            if (entry.isDirectory()) {
              const possiblePath = path.join(repoDir, entry.name, 'SKILL.md');
              try {
                await fs.access(possiblePath);
                skillDir = path.join(repoDir, entry.name);
                skillMdPath = possiblePath;
                break;
              } catch (err) {}
            }
          }
          if (skillDir === repoDir) {
            for (const entry of entries) {
              if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git') {
                const subDir = path.join(repoDir, entry.name);
                const subEntries = await fs.readdir(subDir, { withFileTypes: true });
                for (const subEntry of subEntries) {
                  if (subEntry.isDirectory()) {
                    const possiblePath = path.join(subDir, subEntry.name, 'SKILL.md');
                    try {
                      await fs.access(possiblePath);
                      skillDir = path.join(subDir, subEntry.name);
                      skillMdPath = possiblePath;
                      break;
                    } catch (err) {}
                  }
                }
              }
            }
          }
        } catch (dirErr) {
          spinner.stop();
          console.error(chalk.red(`Error: Repository '${skillName}' not found.`));
          console.log(chalk.gray(`Try running \`${chalk.white('npx "@opendirectory.dev/skills" list')}\` to see available skills.`));
          process.exit(1);
        }
      }

      try {
        await fs.access(skillMdPath);
      } catch (e) {
        spinner.stop();
        console.error(chalk.red(`Error: Skill '${skillName}' missing SKILL.md in registry.`));
        process.exit(1);
      }
      
      const actualSkillFolderName = path.basename(skillDir);
      const finalSkillName = actualSkillFolderName === skillName ? skillName : actualSkillFolderName;

      const target = options.target.toLowerCase();

      const validTargets = ['opencode', 'claude', 'codex', 'gemini', 'anti-gravity', 'openclaw', 'hermes'];

      if (validTargets.includes(target)) {
        let targetFolder = '';
        if (target === 'opencode') targetFolder = `~/.config/opencode/skills/${finalSkillName}`;
        if (target === 'claude') targetFolder = `~/.claude/skills/${finalSkillName}`;
        if (target === 'codex') targetFolder = `~/.codex/skills/${finalSkillName}`;
        if (target === 'gemini') targetFolder = `~/.gemini/skills/${finalSkillName}`;
        if (target === 'anti-gravity') targetFolder = `~/.gemini/antigravity/skills/${finalSkillName}`;
        if (target === 'openclaw') targetFolder = `~/.openclaw/skills/${finalSkillName}`;
        if (target === 'hermes') targetFolder = `~/.hermes/skills/${finalSkillName}`;
        
        const { resolvePath } = require('./fs-adapters');
        const resolvedDest = resolvePath(targetFolder);
        await fs.mkdir(resolvedDest, { recursive: true });
        await fs.cp(skillDir, resolvedDest, { recursive: true });
        
        spinner.stop();
        console.log(chalk.green(`Successfully installed ${chalk.bold(finalSkillName)}!`));
        console.log(`\n  ${chalk.cyan('Agent:')}   ${target}`);
        console.log(`  ${chalk.cyan('Scope:')}   Global`);
        console.log(`  ${chalk.cyan('Path:')}    ${targetFolder}\n`);
      } else {
        spinner.stop();
        console.error(chalk.red(`Error: Unsupported target '${target}'.`));
        console.log(chalk.gray(`Supported targets: ${validTargets.join(', ')}`));
        process.exit(1);
      }
    } catch (error) {
      spinner.stop();
      console.error(chalk.red('Failed to install skill.'));
      console.error(error);
      process.exit(1);
    }
  });

program.parse();