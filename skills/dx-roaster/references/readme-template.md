# Ideal README Skeleton

When generating `dx-roast/ideal-readme.md`, fill this template with the project's actual name, tagline (extracted from existing README or proposed), badges, hero placeholder, install, quick-start, and links. Use placeholders for missing assets — never invent URLs.

---

## Template

```markdown
<p align="center">
  <img src="docs/hero.gif" alt="<project name> in action" width="600" />
</p>

<h1 align="center"><project name></h1>

<p align="center"><strong><one-sentence tagline></strong></p>

<p align="center">
  <a href="<homepage_or_docs_url_or_placeholder>">Website</a> ·
  <a href="<docs_url_or_placeholder>">Docs</a> ·
  <a href="<twitter_or_discord_or_placeholder>">Community</a>
</p>

<p align="center">
  <img src="https://img.shields.io/npm/v/<package>" alt="npm" />
  <img src="https://img.shields.io/github/stars/<owner>/<repo>" alt="stars" />
  <img src="https://img.shields.io/github/license/<owner>/<repo>" alt="license" />
</p>

---

## What is this?

<2–3 sentence description in plain English. Lead with the user benefit, not the tech.>

## Install

\`\`\`bash
<one-command install>
\`\`\`

## Quick start

\`\`\`<language>
<runnable example, 5–10 lines, produces visible output>
\`\`\`

Expected output:

\`\`\`
<output>
\`\`\`

## What you can do

- <Use case 1, one line each>
- <Use case 2>
- <Use case 3>

## Documentation

- [Full docs](<docs_url>)
- [API reference](<api_ref>)
- [Examples](<examples_url>)

## Community

- [Discord](<discord_url>)
- [Twitter / X](<twitter_url>)
- [Discussions](https://github.com/<owner>/<repo>/discussions)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All PRs welcome.

## License

<license name> — see [LICENSE](LICENSE).
```

---

## Filling rules

1. **Tagline:** extract from existing README first sentence. If too vague, propose one from `package.json.description` or repo description. Length: <12 words.
2. **Hero image:** always include the placeholder. Roast tells maintainer to record one.
3. **Install:** use the cleanest single-command install detected. If none exists, write a placeholder `# TODO: provide one-command install` so maintainer notices.
4. **Quick-start:** extract from existing README if any code block is runnable. Else propose based on `examples/` content. Else placeholder.
5. **Links:** use placeholders `<homepage_url>` etc. — never invent URLs.
6. **Length:** keep under 100 lines. Anything more belongs in `docs/`.
