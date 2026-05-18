# @opendirectory.dev/skills

**Agent skills for founders who hate marketing.**

The official CLI for browsing, installing, and managing OpenDirectory skills for AI agents. Equip your AI assistant with expert-level domain knowledge for GTM, marketing, growth, and developer tooling tasks — in seconds, with zero setup.

## Features

- **55+ pre-built skills** — Brand strategy, cold email, content creation, PR intelligence, pricing audits, and more
- **Multi-agent support** — Works with Claude Code, OpenCode, Codex, Gemini CLI, Anti-Gravity, OpenClaw, and Hermes
- **Zero global install** — Runs via `npx`, always fetches the latest version
- **No configuration** — Install any skill in under 30 seconds

## Quick Start

**1. Browse available skills:**
```bash
npx "@opendirectory.dev/skills" list
```

**2. Install a skill for your agent:**
```bash
npx "@opendirectory.dev/skills" install <skill-name> --target <your-agent>
```

**Examples:**
```bash
# Install for Claude Code
npx "@opendirectory.dev/skills" install brand-alchemy --target claude

# Install for OpenCode
npx "@opendirectory.dev/skills" install position-me --target opencode

# Install for Gemini CLI
npx "@opendirectory.dev/skills" install cold-email-verifier --target gemini
```

## Supported Agents

| Agent | Flag |
|---|---|
| Claude Code | `--target claude` |
| OpenCode | `--target opencode` |
| Codex | `--target codex` |
| Gemini CLI | `--target gemini` |
| Anti-Gravity | `--target anti-gravity` |
| OpenClaw | `--target openclaw` |
| Hermes | `--target hermes` |

## Requirements

- **Node.js** — Download from [nodejs.org](https://nodejs.org/) if not installed
- `npx` comes bundled with Node.js and fetches the latest version automatically

## Installation Methods

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install <skill-name> --target <your-agent>
```

### Option B: Claude Code Plugin

Install the entire OpenDirectory skill marketplace directly inside Claude Code:

```bash
# Add the OpenDirectory marketplace
/plugin marketplace add Varnan-Tech/opendirectory

# Install all skills at once
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

This gives you instant access to all 55+ skills without running individual install commands.

## Available Skills

For the full list of 55+ skills, detailed documentation, and contribution guidelines, visit the [OpenDirectory GitHub Repository](https://github.com/Varnan-Tech/opendirectory).

## Contributing

We welcome new skills across GTM, growth automation, and developer tooling. See [CONTRIBUTING.md](https://github.com/Varnan-Tech/opendirectory/blob/main/CONTRIBUTING.md) for the skill format and submission process.

## License

MIT
