# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-19  
**Project:** OpenDirectory – AI Agent Skills Registry + CLI  
**Type:** TypeScript/JavaScript pnpm monorepo  

---

## OVERVIEW

OpenDirectory is a registry and CLI tool for discoverable AI agent skills—modular, reusable integrations (e.g., Twitter GTM radar, Hacker News intel, docs extraction). The main CLI (`@opendirectory.dev/skills`) installs and manages skills. Uses pnpm workspaces, TypeScript strict mode, and Vitest for testing.

---

## STRUCTURE

```
.
├── .github/
│   └── workflows/          # GitHub Actions: publish.yml (NPM + registry), pr-validation.yml
├── .claude-plugin/         # Claude plugin manifest (custom)
├── scripts/                # Registry builder, docs updaters (TypeScript/tsx)
├── packages/
│   └── cli/                # Main CLI package (@opendirectory.dev/skills)
│       ├── src/            # CLI source (index.ts, fs-adapters.ts)
│       ├── skills/         # Skills copied here during build
│       └── dist/           # Built CLI binary
├── skills/                 # Skills registry (multiple independent skills)
│   ├── blog-cover-image-cli/
│   ├── twitter-GTM-find-skill/
│   ├── yc-intent-radar-skill/
│   ├── hackernews-intel/
│   ├── newsletter-digest/
│   ├── docs-from-code/
│   ├── cold-email-verifier/ (Python)
│   └── ...
├── tsconfig.json           # Root TS config (ESNext, NodeNext, strict)
├── pnpm-workspace.yaml     # Workspace packages definition
├── package.json            # Root private package, test/build scripts
└── vitest.config.ts        # Test config (globals, Node env)
```

---

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **CLI logic** | `packages/cli/src/` | Main entry, fs adapters, e2e tests |
| **Skill development** | `skills/*/` | Copy skill template, add to registry.json, build rebuilds |
| **Build system** | `scripts/build-registry.ts`, `pnpm-workspace.yaml` | Workspace auto-detection, registry.json generation |
| **CI/CD** | `.github/workflows/` | Publish on main (auto-version bump), validate on PRs |
| **Tests** | `packages/cli/src/*.test.ts`, `vitest.config.ts` | Unit (fs-adapters) + E2E (skill install flow) |
| **Docs** | `scripts/update-readme.ts`, `update-contributing.ts` | Auto-generated from templates |
| **Plugin integration** | `.claude-plugin/manifest.json` | Claude-specific (non-standard) |

---

## KEY ENTRY POINTS

- **CLI Entry:** `packages/cli/src/index.ts` → exports CLI commands (install, list, etc.)
- **Registry Builder:** `scripts/build-registry.ts` → reads all `skills/*/` dirs, generates `registry.json`
- **Package Main:** Root `package.json` runs tests, registry build, docs update
- **Workspace:** `pnpm-workspace.yaml` defines `packages/**` and `skills/**` as packages

---

## CONVENTIONS (Project-Specific)

1. **No Linting Rules:** No `.eslintrc`, `.prettierrc`, or `.editorconfig` → formatting/style is manual/IDE-default
2. **TypeScript:** Strict mode, ESNext target, NodeNext modules, declaration generation; root config excludes `skills/`
3. **Skills Duplication:** Skills are copied into `packages/cli/skills/` during build → expect duplicate paths post-build
4. **Auto-Generated Files:** README, CONTRIBUTING, registry.json committed with `[skip ci]` tag
5. **Version Bumping:** CLI version auto-bumped via NPM registry query; allows same-version overwrites (non-standard)
6. **Mixed Modules:** Most skills are JS/TS, but `cold-email-verifier` uses Python (requirements.txt)
7. **pnpm workspaces:** All dependency management via pnpm; root private package (no main entry)

---

## ANTI-PATTERNS (AVOID THIS PROJECT)

- **Explicit "DO NOT" rules:** None found in codebase comments (awaiting final scan)
- **Deprecated code:** No legacy markers found yet
- **Linting gaps:** No automated style checking → rely on IDE/manual review

---

## UNIQUE STYLES

- **Skill Template Structure:** Each skill follows `src/`, `package.json`, optional `scripts/` pattern
- **CLI Build:** TypeScript → plain JS, then copies entire `skills/` dir post-compile
- **Async Docs:** Registry and docs auto-updated on every build via scripts
- **E2E Test Pattern:** Build CLI binary first, then run installation tests with temp directories

---

## COMMANDS

```bash
# Install dependencies
pnpm install

# Run tests (root)
pnpm test

# Build registry + docs + CLI
pnpm exec tsx scripts/build-registry.ts
pnpm exec tsx scripts/update-readme.ts
pnpm exec tsx scripts/update-contributing.ts

# Build CLI package
cd packages/cli && pnpm run build

# Test CLI (E2E)
cd packages/cli && pnpm run test:e2e

# Publish CLI to NPM
cd packages/cli && npm publish --access public
```

---

## NOTES & GOTCHAS

1. **Skills Mirrored:** `packages/cli/skills/` is a **post-build copy** → don't edit directly; edit source in `skills/`
2. **No Auto-Commit Loops:** CI auto-commits with `[skip ci]` to prevent infinite loops on doc updates
3. **Version Quirk:** CLI version bumps query NPM for latest, allowing overwrites (non-standard npm behavior)
4. **Python Skill:** `cold-email-verifier` requires separate Python deps; not integrated into pnpm workspace
5. **Plugin Manifest:** `.claude-plugin/` is custom integration; not standard Node.js
6. **Workspace Caveat:** Root package is private (no `main` field); all public exports via `packages/cli/`

---

## COMMANDS (DETAILED)

| Command | Purpose | Notes |
|---------|---------|-------|
| `pnpm install` | Install all workspace deps | Runs in root; syncs all packages |
| `pnpm test` | Run Vitest on root | Runs CLI tests |
| `pnpm exec tsx scripts/build-registry.ts` | Generate registry.json | Reads `skills/*/` dirs, outputs registry |
| `cd packages/cli && pnpm run build` | Compile CLI TypeScript | Copies `../../skills` into `./skills` post-compile |
| `cd packages/cli && pnpm run test:e2e` | E2E CLI install tests | Uses Vitest, builds binary first |
| `npm publish --access public` (CLI) | Publish to NPM | Auto-versioned, allows overwrites |

