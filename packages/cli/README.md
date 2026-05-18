# @opendirectory.dev/skills

**Agent skills for founders who hate marketing.**

The official CLI for browsing, installing, and managing OpenDirectory skills for AI agents. Equip your AI assistant with expert-level domain knowledge for GTM, marketing, growth, and developer tooling tasks — in seconds, with zero setup.

You can run the CLI directly using `npx`:

```bash
npx "@opendirectory.dev/skills" [command] [options]
```

## Interactive Mode

Run the CLI without any arguments to enter the interactive TUI:

```bash
npx "@opendirectory.dev/skills"
```

The interactive mode lets you browse, search, and install skills with arrow keys, multi-select with Space, and confirm with Enter.

### Claude Code Native Plugin

Install the entire OpenDirectory skill marketplace directly inside Claude Code:

```bash
# Add the OpenDirectory marketplace
/plugin marketplace add Varnan-Tech/opendirectory

# Install a skill
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

This gives you instant access to all 55+ skills without running individual install commands.

## Commands

- `list` — List all available skills (interactive by default; pass `--plain` for a static table).
- `install <skill-name> --target <agent>` — Install a specific skill. The `--target` flag is required on first use; later runs reuse the saved default.
- `update <skill-name> [--target <agent>]` — Update an installed skill (safe rollback if the new install fails).
- `uninstall <skill-name> [--target <agent>]` — Uninstall a skill.
- `installed` — Manage installed skills (interactive by default; pass `--plain` for a static table).

## Supported Agents

The CLI installs skills for the following agents (use the lowercase slug with `--target`):

| Target slug   | Agent                  | Install location                |
| ------------- | ---------------------- | ------------------------------- |
| `claude`      | Claude Code            | `~/.claude/skills/`             |
| `opencode`    | opencode               | `~/.config/opencode/skills/`    |
| `codex`       | OpenAI Codex CLI       | `~/.codex/skills/`              |
| `gemini`      | Gemini CLI             | `~/.gemini/skills/`             |
| `anti-gravity`| Gemini AntiGravity     | `~/.gemini/antigravity/skills/` |
| `openclaw`    | OpenClaw               | `~/.openclaw/skills/`           |
| `hermes`      | Hermes                 | `~/.hermes/skills/`             |

`--target` is **case-insensitive** (`--target Claude` and `--target CLAUDE` both work).

## Flags

- `--plain` — Disable TUI and use plain text output. Useful for CI, pipes, and screen readers. Also auto-enabled when stdout/stdin is not a TTY or when `CI=1`.
- `--no-banner` — Do not show the OpenDirectory banner.

## Environment Variables

- `NO_COLOR` — Set to any non-empty value to disable ANSI colors (per https://no-color.org).
- `CI` — Set to any non-empty value to force `--plain` mode automatically.

## Accessibility

The CLI ships with a `--plain` mode that emits a static table instead of a TUI. We recommend it for screen reader users and any CI / scripting context.

## Available Skills

For the full list of skills, detailed documentation, and contribution guidelines, visit the [OpenDirectory GitHub repository](https://github.com/Varnan-Tech/opendirectory).

## Contributing

We welcome new skills across GTM, growth automation, and developer tooling. See [CONTRIBUTING.md](https://github.com/Varnan-Tech/opendirectory/blob/main/CONTRIBUTING.md) for the skill format and submission process.

## License

MIT
