import * as p from '@clack/prompts';
import chalk from 'chalk';
import { detectAgents, AGENT_PATHS, ValidAgent } from '../detect';
import { getDefaultTarget, setDefaultTarget } from '../config';

export class CancelledError extends Error {
  constructor() {
    super('Cancelled');
    this.name = 'CancelledError';
  }
}

export async function pickTarget(): Promise<string> {
  const agents = await detectAgents();
  const defaultTarget = await getDefaultTarget();

  const options = Object.keys(AGENT_PATHS).map(name => {
    const agent = agents.find(a => a.name === name);
    const isDefault = name === defaultTarget;
    const isDetected = agent?.installed;

    let label = name;
    if (isDefault) {
      label += chalk.hex('#856FE6')(' (★ default)');
    } else if (isDetected) {
      label += chalk.green(' (✓ detected)');
    }

    return { value: name, label };
  });

  let initialValue = options[0].value;
  if (defaultTarget && options.some(o => o.value === defaultTarget)) {
    initialValue = defaultTarget;
  } else {
    const detected = agents.find(a => a.installed);
    if (detected) {
      initialValue = detected.name;
    }
  }

  const target = await p.select({
    message: 'Select target agent:',
    options,
    initialValue
  });

  if (p.isCancel(target)) {
    throw new CancelledError();
  }

  const shouldSave = await p.confirm({
    message: 'Save as default for next time?',
    initialValue: !defaultTarget
  });

  if (p.isCancel(shouldSave)) {
    throw new CancelledError();
  }

  if (shouldSave) {
    await setDefaultTarget(target as string);
  }

  return target as string;
}
