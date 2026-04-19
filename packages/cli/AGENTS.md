# packages/cli

**Purpose:** Main CLI package for the OpenDirectory skills registry. Provides install, list, and discovery commands for AI agent skills.

---

## STRUCTURE

```
packages/cli/
├── src/
│   ├── index.ts           # CLI entry, command routing (install, list, etc.)
│   ├── fs-adapters.ts     # File system utilities (temp dirs, skill copying, validation)
│   ├── fs-adapters.test.ts # Unit tests for fs utilities
│   └── e2e.test.ts        # End-to-end CLI installation flow tests
├── skills/                # Post-build copy of ../../skills (DO NOT EDIT)
├── dist/                  # Compiled JavaScript + skills copy
├── package.json           # CLI package config (@opendirectory.dev/skills)
├── tsconfig.json          # Extends root, sets rootDir/outDir
└── build output
```

---

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **CLI commands** | `src/index.ts` | Command handlers (install, list, etc.) |
| **File system logic** | `src/fs-adapters.ts` | Temp dir creation, skill validation, installation |
| **Unit tests** | `src/fs-adapters.test.ts` | Test fs utilities in isolation |
| **E2E tests** | `src/e2e.test.ts` | Full CLI flow: build → install → verify |
| **Build output** | `dist/` | Compiled CLI with embedded skills/ |

---

## BUILD PROCESS

```bash
cd packages/cli && pnpm run build
```

**Steps:**
1. TypeScript compiles `src/*.ts` → `dist/`
2. Node.js copies `../../skills/` into `dist/skills/` (entire directory)
3. Result: CLI binary ready to use, with all skills embedded

**Key:** Skills are NOT part of source; they're injected post-compile. Do NOT edit `dist/skills/` directly.

---

## CONVENTIONS (CLI-SPECIFIC)

1. **Temp Directories:** Tests create temp dirs with `fs.mkdtempSync`, clean up in `afterEach`
2. **CLI Entry:** `bin` field in `package.json` points to `dist/index.js`
3. **Skills Injection:** Post-build via Node.js script (not TypeScript) → executed as part of build
4. **E2E Order:** Build CLI first, THEN run e2e tests (tests depend on compiled binary)

---

## TESTING

```bash
cd packages/cli && pnpm run test:e2e  # Runs Vitest, requires built CLI binary
```

**E2E Pattern:** Create temp dir → run CLI install command → verify skill files exist → cleanup

---

## COMMANDS (CLI-SPECIFIC)

| Command | Purpose |
|---------|---------|
| `pnpm run build` | Compile TS + copy skills |
| `pnpm run test:e2e` | Run end-to-end tests |
| `npm publish --access public` | Publish to NPM registry |

