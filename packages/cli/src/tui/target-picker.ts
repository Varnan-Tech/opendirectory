import * as p from '@clack/prompts';
import chalk from 'chalk';
import { detectAgents, AGENT_PATHS, isValidAgent } from '../detect';
import { getDefaultTarget, setDefaultTarget } from '../config';
import { normalizeTarget } from '../compat';

export interface TargetPickerOptions {
  disabledTargets?: ReadonlySet<string>;
  explicitTarget?: string;
}

export function shouldPersistDefault(explicitTarget: string | undefined, shouldSave: boolean): boolean {
  return shouldSave && !explicitTarget;
}

export class CancelledError extends Error {
  constructor() {
    super('Cancelled');
    this.name = 'CancelledError';
  }
}

export async function pickTarget(pickerOptions: TargetPickerOptions = {}): Promise<string> {
  if (pickerOptions.explicitTarget) {
    const target = normalizeTarget(pickerOptions.explicitTarget);
    if (!isValidAgent(target)) {
      throw new Error(`Unsupported target '${pickerOptions.explicitTarget}'.`);
    }
    return target;
  }

  const agents = await detectAgents();
  const configuredTarget = await getDefaultTarget();
  const defaultTarget = configuredTarget ? normalizeTarget(configuredTarget) : undefined;

  const targetOptions = Object.keys(AGENT_PATHS).map(name => {
    const agent = agents.find(a => a.name === name);
    const isDefault = name === defaultTarget;
    const isDetected = agent?.installed;
    const isUnsupported = pickerOptions.disabledTargets?.has(name) ?? false;

    let label = name;
    if (isDefault) {
      label += chalk.hex('#856FE6')(' (default)');
    } else if (isDetected) {
      label += chalk.green(' (detected)');
    }
    if (isUnsupported) {
      label += chalk.red(' (unsupported)');
    }

    return {
      value: name,
      label,
      disabled: isUnsupported,
    };
  });

  const enabledOptions = targetOptions.filter(option => !option.disabled);
  let initialValue = enabledOptions[0]?.value;
  if (defaultTarget && enabledOptions.some(o => o.value === defaultTarget)) {
    initialValue = defaultTarget;
  } else {
    const detected = agents.find(a => a.installed && enabledOptions.some(option => option.value === a.name));
    if (detected) {
      initialValue = detected.name;
    }
  }

  if (!initialValue) {
    throw new Error('No target supports every selected skill. Return to the skill picker and choose a compatible set.');
  }

  const target = await p.select({
    message: 'Select target agent:',
    options: targetOptions,
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

  if (shouldPersistDefault(pickerOptions.explicitTarget, shouldSave)) {
    await setDefaultTarget(target as string);
  }

  return target as string;
}
