import { describe, expect, test } from 'vitest';
import { AGENT_PATHS, CANONICAL_TARGETS, isValidAgent } from './detect';

describe('isValidAgent', () => {
  test.each(['constructor', 'toString'])('rejects inherited property name %s', target => {
    expect(isValidAgent(target)).toBe(false);
  });

  test('accepts canonical target names', () => {
    expect(isValidAgent('codex')).toBe(true);
  });

  test('keeps canonical target names in parity with agent paths', () => {
    expect([...CANONICAL_TARGETS].sort()).toEqual(Object.keys(AGENT_PATHS).sort());
  });
});
