# @opendirectory.dev/skills

**Agent skills for founders who hate marketing.**

The official CLI for browsing, installing, and managing OpenDirectory skills for AI agents. Equip your AI assistant with expert-level domain knowledge for GTM, marketing, growth, and developer tooling tasks — in seconds, with zero setup.

You can run the CLI directly using `npx`:

```bash
npx "@opendirectory.dev/skills" [command] [options]
```

## Interactive Mode

Run the CLI without any arguments to enter the interactive mode:

```bash
npx "@opendirectory.dev/skills"
```

The interactive mode provides a TUI (Terminal User Interface) to browse, search, and manage skills easily.

## Commands

- `list`: List all available skills.
- `install <skill-name>`: Install a specific skill.
- `update <skill-name>`: Update an installed skill.
- `uninstall <skill-name>`: Uninstall a skill.
- `installed`: List all installed skills.

## Global Flags

- `--target <target>`: Specify the target agent (e.g., `claude`, `cursor`).
- `--plain`: Disable TUI and use plain text output. Useful for CI environments or screen readers.
- `--no-banner`: Do not show the OpenDirectory banner.

## Environment Variables

- `NO_COLOR`: Disable colored output.
- `CI`: Set to `true` to automatically enable `--plain` mode.

## Accessibility

The CLI is designed to be accessible. If you are using a screen reader, we recommend using the `--plain` flag for a better experience.

## Available Skills

For the full list of 55+ skills, detailed documentation, and contribution guidelines, visit the [OpenDirectory GitHub Repository](https://github.com/Varnan-Tech/opendirectory).

## Contributing

We welcome new skills across GTM, growth automation, and developer tooling. See [CONTRIBUTING.md](https://github.com/Varnan-Tech/opendirectory/blob/main/CONTRIBUTING.md) for the skill format and submission process.

## License

MIT
