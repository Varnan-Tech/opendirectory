import fs from 'node:fs';
import path from 'node:path';
import { inspectSkillFrontmatter } from '../packages/cli/src/frontmatter';
import { findSkillSourceSync } from '../packages/cli/src/skill-discovery';

const ROOT_DIR = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(ROOT_DIR, 'skills');
const REGISTRY_PATH = path.join(ROOT_DIR, 'packages', 'cli', 'registry.json');
const CONTRIBUTING_PATH = path.join(ROOT_DIR, 'CONTRIBUTING.md');
const DOCS_DIR = path.join(ROOT_DIR, 'docs');
const DOCS_SKILLS_DIR = path.join(DOCS_DIR, 'skills');
const DOCS_JSON_PATH = path.join(DOCS_DIR, 'docs.json');

interface SkillEntry {
  name: string;
  description: string;
  version: string;
  author: string;
  compatibility: string;
  category: string;
  categorySlug: string;
  docRoute: string;
}

const CATEGORY_ORDER = [
  'Visual & Media',
  'Content',
  'Launch',
  'GTM Intelligence',
  'Outreach',
  'Research',
  'Developer Tools',
  'Other',
];

const TAG_TO_CATEGORY: Record<string, string> = {
  'AI': 'Developer Tools',
  'Branding': 'Launch',
  'Copywriting': 'Content',
  'Developer Tools': 'Developer Tools',
  'Email': 'Outreach',
  'Marketing': 'GTM Intelligence',
  'SEO': 'Research',
  'Social Media': 'Content',
};

const ALLOWED_HTML_TAGS = new Set([
  'a', 'b', 'i', 'u', 's', 'em', 'strong', 'sub', 'sup', 'code', 'pre',
  'div', 'span', 'p', 'br', 'hr', 'img', 'video', 'picture', 'source',
  'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'ul', 'ol', 'li',
  'dl', 'dt', 'dd', 'details', 'summary', 'blockquote', 'h1', 'h2', 'h3',
  'h4', 'h5', 'h6', 'kbd', 'mark', 'small',
  'Info', 'Note', 'Tip', 'Warning', 'Check', 'Tabs', 'Tab', 'Card',
  'CardGroup', 'Steps', 'Step', 'Frame', 'Accordion', 'AccordionGroup',
  'CodeGroup', 'Callout',
]);

function categoryToSlug(category: string): string {
  return category
    .toLowerCase()
    .replace(/&/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function getCategoryFromPkg(skillDir: string): string | null {
  const pkgPath = path.join(skillDir, 'package.json');
  if (!fs.existsSync(pkgPath)) return null;
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    if (typeof pkg.category === 'string' && pkg.category.trim()) {
      return pkg.category.trim();
    }
  } catch (_) {}
  return null;
}

function detectCategoryFromContent(name: string, description: string): string {
  const n = name.toLowerCase();
  const text = (name + ' ' + description).toLowerCase();

  if (/^(vid-|graphic-|blog-cover-image)/.test(n)) return 'Visual & Media';
  if (/^(email-newsletter|cook-the-blog|noise2blog|human-tone|linkedin-post|tweet-thread|noise-to-linkedin|newsletter)/.test(n)) return 'Content';
  if (/^(producthunt|show-hn|oss-launch|brand-alchemy|product-update-logger)/.test(n)) return 'Launch';
  if (/^(hackernews|reddit-icp|reddit-post|npm-downloads|yc-intent|twitter-gtm|sdk-adoption|gh-issue|map-your-market|competitor-pr|google-trends|meta-ads|meta-tribe|company-radar)/.test(n)) return 'GTM Intelligence';
  if (/^(outreach-sequence|cold-email)/.test(n)) return 'Outreach';
  if (/^(pricing-|position-me|meeting-brief|linkedin-job-post|where-your-customer|vc-)/.test(n)) return 'Research';
  if (/^(kill-the-standup|dependency-update|docs-from-code|pr-description|explain-this-pr|claude-md|llms-txt|schema-markup)/.test(n)) return 'Developer Tools';

  if (/\b(gif|mp4|motion.graphic|animation|slide.?deck|e.?book|cover.image|chart|graphic|png|video)\b/.test(text)) return 'Visual & Media';
  if (/pull.request|\bstandup\b|\bdependency\b|llms\.txt|json.?ld|schema.markup|claude\.md|agents\.md|codebase.scan|docs.from.code/.test(text)) return 'Developer Tools';
  if (/product.hunt|show.hn|\boss.launch\b|\bbrand.strateg|\bnaming.expert\b|\blaunch.kit\b|\bproduct.update\b/.test(text)) return 'Launch';
  if (/cold.email|outreach.sequence|email.verif/.test(text)) return 'Outreach';
  if (/pricing.page|venture.capital|\binvestor\b|\bvc\b|buyer.pain|pre.call.brief|where.*customer|icp.*channel/.test(text)) return 'Research';
  if (/hacker.news|npm.*download|yc.*startup|sdk.*adopt|google.trends|meta.ads|demand.signal|competitor.*pr|map.*market|\bgtm\b|tribe.v2|reddit.*monitor|twitter.*gtm/.test(text)) return 'GTM Intelligence';
  if (/\breddit\b|\bblog\b|newsletter|linkedin.post|carousel|tweet.thread/.test(text)) return 'Content';
  return 'Other';
}

function getCategory(name: string, description: string, tags?: string[], skillDir?: string): string {
  if (skillDir) {
    const pkg = getCategoryFromPkg(skillDir);
    if (pkg) return pkg;
  }
  const fromContent = detectCategoryFromContent(name, description);
  if (fromContent !== 'Other') return fromContent;
  if (tags && tags.length > 0) {
    for (const tag of tags) {
      if (TAG_TO_CATEGORY[tag]) return TAG_TO_CATEGORY[tag];
    }
  }
  return 'Other';
}

function extractReadmeDescription(skillDir: string): string {
  const readmePath = path.join(skillDir, 'README.md');
  if (!fs.existsSync(readmePath)) return '';

  const content = fs.readFileSync(readmePath, 'utf-8');
  const lines = content.split('\n');

  for (const line of lines) {
    const trimmed = line.trim().replace(/^\uFEFF/, '');
    if (!trimmed) continue;
    if (trimmed.startsWith('#')) continue;
    if (trimmed.startsWith('<')) continue;
    if (trimmed.startsWith('![')) continue;
    if (trimmed.startsWith('```')) continue;
    if (trimmed.startsWith('---')) continue;
    if (trimmed.startsWith('[![')) continue;
    if (trimmed.startsWith('| ')) continue;
    if (trimmed === '**') continue;
    if (trimmed.startsWith('> ')) {
      const text = trimmed.slice(2).trim().replace(/\*\*/g, '').replace(/`/g, '');
      if (text.length > 20) return sanitizePlainText(text);
    }
    if (trimmed.length > 20) {
      return sanitizePlainText(trimmed.replace(/\*\*/g, '').replace(/`/g, ''));
    }
  }
  return '';
}

function sanitizePlainText(raw: string): string {
  return raw
    .replace(/<img[^>]*>/gm, '')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/(\*\*|__|\*|_)/g, '')
    .replace(/`/g, '')
    .replace(/\r?\n/g, ' ')
    .trim();
}

function buildInstallTabsMdx(skillName: string): string {
  const githubUrl = encodeURIComponent(`https://github.com/Varnan-Tech/opendirectory/tree/main/skills/${skillName}`);
  const manusUrl = `https://manus.im/import-skills?githubUrl=${githubUrl}&utm_source=opendirectory`;

  return `<Tabs>
  <Tab title="npx CLI (Recommended)">
    \`\`\`bash
    npx "@opendirectory.dev/skills" install ${skillName} --target claude
    \`\`\`
  </Tab>
  <Tab title="skills.sh">
    \`\`\`bash
    npx skills add Varnan-Tech/opendirectory --skill ${skillName}
    \`\`\`
  </Tab>
  <Tab title="Claude Code Native">
    \`\`\`bash
    /plugin marketplace add Varnan-Tech/opendirectory
    /plugin install opendirectory-gtm-skills@opendirectory-marketplace
    \`\`\`
  </Tab>
  <Tab title="Claude Desktop">
    <video
      controls
      className="w-full aspect-video rounded-xl mb-4"
      src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c"
    ></video>

    1. Copy \`https://github.com/Varnan-Tech/opendirectory/tree/main/skills/${skillName}\` into [download-directory.github.io](https://download-directory.github.io/) to download the ZIP.
    2. Open **Claude Desktop** -> **Customize** -> **Skills** -> **+** -> **Upload a skill** and drop the folder containing \`SKILL.md\`.
  </Tab>
  <Tab title="Manus AI">
    <video
      controls
      className="w-full aspect-video rounded-xl mb-4"
      src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4"
    ></video>

    [**Install ${skillName} in Manus AI**](${manusUrl})
  </Tab>
</Tabs>`;
}

const IMAGE_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']);

interface SanitizeContext {
  skillRouteMap: Map<string, string>;
  skill?: SkillEntry;
  skillDir?: string;
  extraMdxPages?: Array<{ route: string; title: string; sourcePath: string }>;
}

function resolveSkillLocalTarget(
  rawTarget: string,
  isImage: boolean,
  ctx: SanitizeContext,
): string {
  const trimmed = rawTarget.trim();
  if (
    !trimmed ||
    trimmed.startsWith('http://') ||
    trimmed.startsWith('https://') ||
    trimmed.startsWith('mailto:') ||
    trimmed.startsWith('#') ||
    trimmed.startsWith('/')
  ) {
    return rawTarget;
  }

  const crossSkillMatch = trimmed.match(/^\.\.\/([a-zA-Z0-9_-]+)\/?$/);
  if (crossSkillMatch) {
    const route = ctx.skillRouteMap.get(crossSkillMatch[1]);
    if (route) return `/${route}`;
  }

  if (!ctx.skill || !ctx.skillDir) {
    return `https://github.com/Varnan-Tech/opendirectory/blob/main/${trimmed.replace(/^\.\//, '')}`;
  }

  let relClean = trimmed.replace(/^\.\//, '');
  let absPath = path.resolve(ctx.skillDir, relClean);

  if (!fs.existsSync(absPath) && relClean === 'results_showcase.md') {
    const fallback = path.resolve(ctx.skillDir, 'showcase.md');
    if (fs.existsSync(fallback)) {
      relClean = 'showcase.md';
      absPath = fallback;
    }
  }

  if (fs.existsSync(absPath) && fs.statSync(absPath).isFile()) {
    const ext = path.extname(relClean).toLowerCase();
    const posixRel = relClean.split(path.sep).join('/');

    if (isImage || IMAGE_EXTENSIONS.has(ext)) {
      const destAssetRel = `assets/skills/${ctx.skill.name}/${posixRel}`;
      const destAssetAbs = path.join(DOCS_DIR, destAssetRel);
      fs.mkdirSync(path.dirname(destAssetAbs), { recursive: true });
      fs.copyFileSync(absPath, destAssetAbs);
      return `/${destAssetRel}`;
    }

    if (ext === '.md' || ext === '.mdx') {
      const withoutExt = posixRel.replace(/\.(md|mdx)$/i, '');
      const subRoute = `${ctx.skill.docRoute}/${withoutExt}`;
      if (ctx.extraMdxPages && !ctx.extraMdxPages.some(p => p.route === subRoute)) {
        ctx.extraMdxPages.push({
          route: subRoute,
          title: `${ctx.skill.name} - ${path.basename(withoutExt)}`,
          sourcePath: absPath,
        });
      }
      return `/${subRoute}`;
    }

    return `https://github.com/Varnan-Tech/opendirectory/blob/main/skills/${ctx.skill.name}/${posixRel}`;
  }

  return `https://github.com/Varnan-Tech/opendirectory/blob/main/skills/${ctx.skill.name}/${relClean}`;
}

function sanitizeNonCodeLine(line: string, ctx: SanitizeContext): string {
  let updated = line.replace(/(!?\[[^\]]*\])\(([^)]+)\)/g, (full, prefix, target) => {
    const isImg = prefix.startsWith('!');
    const resolved = resolveSkillLocalTarget(target, isImg, ctx);
    return `${prefix}(${resolved})`;
  });

  updated = updated.replace(
    /(<img\b[^>]*?\bsrc=["'])([^"']+)(["'][^>]*>)/gi,
    (full, before, srcVal, after) => {
      const resolved = resolveSkillLocalTarget(srcVal, true, ctx);
      return `${before}${resolved}${after}`;
    },
  );

  // Self-close void HTML tags (<img ...>, <br>, <hr>, <source ...>)
  updated = updated.replace(/<(img|source)\b([^>]*?)(?<!\/)>/gi, '<$1$2 />');
  updated = updated.replace(/<br\s*>/gi, '<br />');
  updated = updated.replace(/<hr\s*>/gi, '<hr />');

  // Split by inline code spans (`...`) so we never touch characters inside backticks
  const segments = updated.split(/(`+[^`]*`+)/g);
  for (let i = 0; i < segments.length; i++) {
    if (i % 2 === 1) continue; // inside inline code span
    let seg = segments[i];

    // Escape { and } in regular text
    seg = seg.replace(/\{/g, '\\{').replace(/\}/g, '\\}');

    // Escape bare < that are not valid HTML/MDX tags
    seg = seg.replace(/<(\/?)([a-zA-Z0-9_-]+)?([^>]*>)?/g, (match, slash, tagName, rest) => {
      if (tagName && rest !== undefined && ALLOWED_HTML_TAGS.has(tagName)) {
        return match;
      }
      return '&lt;' + match.slice(1);
    });

    segments[i] = seg;
  }

  return segments.join('');
}

function escapeHtmlAttribute(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\{/g, '&#123;')
    .replace(/\}/g, '&#125;');
}

function convertShieldBadgeLineToHtml(line: string): string | null {
  const trimmed = line.trim();
  const linkedMatch = trimmed.match(/^\[!\[([^\]]*)\]\((https:\/\/img\.shields\.io\/[^)]+)\)\]\(([^)]+)\)$/);
  if (linkedMatch) {
    const alt = escapeHtmlAttribute(linkedMatch[1]);
    const src = escapeHtmlAttribute(linkedMatch[2]);
    const href = escapeHtmlAttribute(linkedMatch[3]);
    return `<a href="${href}" target="_blank" rel="noreferrer"><img noZoom src="${src}" alt="${alt}" /></a>`;
  }
  const plainMatch = trimmed.match(/^!\[([^\]]*)\]\((https:\/\/img\.shields\.io\/[^)]+)\)$/);
  if (plainMatch) {
    const alt = escapeHtmlAttribute(plainMatch[1]);
    const src = escapeHtmlAttribute(plainMatch[2]);
    return `<img noZoom src="${src}" alt="${alt}" />`;
  }
  return null;
}

function convertMarkdownToMdxBody(
  rawMarkdown: string,
  ctx: SanitizeContext,
  stripFirstH1 = true,
): string {
  let content = rawMarkdown.replace(/^\uFEFF/, '').replace(/\r\n/g, '\n');

  if (content.startsWith('---\n')) {
    const endIdx = content.indexOf('\n---\n', 4);
    if (endIdx !== -1) {
      content = content.slice(endIdx + 5);
    }
  }

  const installPlaceholder = '___MINTLIFY_INSTALL_TABS_PLACEHOLDER___';
  content = content.replace(
    /<!--\s*OPENDIRECTORY_INSTALL_START\s*-->[\s\S]*?<!--\s*OPENDIRECTORY_INSTALL_END\s*-->/g,
    installPlaceholder,
  );

  content = content.replace(/<!--[\s\S]*?-->/g, '');

  const lines = content.split('\n');
  const outLines: string[] = [];
  let inCodeFence = false;
  let fenceMarker = '';
  let h1Stripped = !stripFirstH1;
  let badgeBuffer: string[] = [];

  const flushBadges = () => {
    if (badgeBuffer.length > 0) {
      outLines.push(`<div className="od-badge-row">${badgeBuffer.join(' ')}</div>`);
      badgeBuffer = [];
    }
  };

  for (const line of lines) {
    const trimmed = line.trim();

    const fenceMatch = trimmed.match(/^(`{3,}|~{3,})/);
    if (fenceMatch) {
      flushBadges();
      if (!inCodeFence) {
        inCodeFence = true;
        fenceMarker = fenceMatch[1][0].repeat(fenceMatch[1].length);
      } else if (trimmed.startsWith(fenceMarker[0].repeat(fenceMarker.length))) {
        inCodeFence = false;
        fenceMarker = '';
      }
      outLines.push(line);
      continue;
    }

    if (inCodeFence) {
      outLines.push(line);
      continue;
    }

    const badgeHtml = convertShieldBadgeLineToHtml(line);
    if (badgeHtml) {
      badgeBuffer.push(badgeHtml);
      continue;
    }
    flushBadges();

    if (!h1Stripped && /^#\s+/.test(trimmed)) {
      h1Stripped = true;
      continue;
    }

    if (trimmed === installPlaceholder) {
      outLines.push(installPlaceholder);
      continue;
    }

    outLines.push(sanitizeNonCodeLine(line, ctx));
  }

  flushBadges();
  return outLines.join('\n').trim();
}

function loadSkills(): SkillEntry[] {
  let registry: any[] = [];
  if (fs.existsSync(REGISTRY_PATH)) {
    try {
      registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
    } catch (_) {}
  }

  const folders = fs
    .readdirSync(SKILLS_DIR)
    .filter(name => fs.statSync(path.join(SKILLS_DIR, name)).isDirectory())
    .sort((a, b) => a.localeCompare(b));

  return folders.map(name => {
    const skillDir = path.join(SKILLS_DIR, name);
    const regEntry = registry.find(r => r.name === name);
    const readmeDesc = extractReadmeDescription(skillDir);
    const description = readmeDesc || regEntry?.description || `Documentation for the ${name} skill.`;

    let version = regEntry?.version || '1.0.0';
    let author = regEntry?.author || 'opendirectory';
    let compatibility = 'All targets (claude, codex, opencode, gemini, anti-gravity, openclaw, hermes)';

    const source = findSkillSourceSync(skillDir);
    if (source && fs.existsSync(source.skillMdPath)) {
      try {
        const parsed = inspectSkillFrontmatter(fs.readFileSync(source.skillMdPath, 'utf-8'));
        if (parsed.data.version) version = String(parsed.data.version);
        if (parsed.data.author) author = String(parsed.data.author);
        if (parsed.compatibility.kind === 'valid') {
          compatibility = parsed.compatibility.targets.join(', ');
        }
      } catch (_) {}
    }

    const category = getCategory(name, description, regEntry?.tags, skillDir);
    const categorySlug = categoryToSlug(category);
    const docRoute = `skills/${categorySlug}/${name}`;

    return {
      name,
      description,
      version,
      author,
      compatibility,
      category,
      categorySlug,
      docRoute,
    };
  });
}

function buildMintlifyDocs() {
  const skills = loadSkills();
  const skillRouteMap = new Map<string, string>();
  for (const s of skills) {
    skillRouteMap.set(s.name, s.docRoute);
  }

  if (fs.existsSync(DOCS_SKILLS_DIR)) {
    fs.rmSync(DOCS_SKILLS_DIR, { recursive: true, force: true });
  }
  fs.mkdirSync(DOCS_SKILLS_DIR, { recursive: true });

  const docsSkillAssetsDir = path.join(DOCS_DIR, 'assets', 'skills');
  if (fs.existsSync(docsSkillAssetsDir)) {
    fs.rmSync(docsSkillAssetsDir, { recursive: true, force: true });
  }

  const extraMdxPages: Array<{ route: string; title: string; sourcePath: string }> = [];

  for (const skill of skills) {
    const skillDir = path.join(SKILLS_DIR, skill.name);
    const readmePath = path.join(skillDir, 'README.md');
    const source = findSkillSourceSync(skillDir);
    const rawContent = fs.existsSync(readmePath)
      ? fs.readFileSync(readmePath, 'utf-8')
      : source && fs.existsSync(source.skillMdPath)
        ? fs.readFileSync(source.skillMdPath, 'utf-8')
        : `# ${skill.name}\n\n${skill.description}`;

    const ctx: SanitizeContext = {
      skillRouteMap,
      skill,
      skillDir,
      extraMdxPages,
    };

    let body = convertMarkdownToMdxBody(rawContent, ctx, true);
    const installTabs = buildInstallTabsMdx(skill.name);

    if (body.includes('___MINTLIFY_INSTALL_TABS_PLACEHOLDER___')) {
      body = body.replace('___MINTLIFY_INSTALL_TABS_PLACEHOLDER___', `## Install\n\n${installTabs}`);
    } else {
      body = `## Install\n\n${installTabs}\n\n${body}`;
    }

    const shortDesc = skill.description.length > 160
      ? skill.description.slice(0, 157).trim() + '...'
      : skill.description;

    const mdx = `---
title: ${JSON.stringify(skill.name)}
description: ${JSON.stringify(shortDesc)}
---

<Info>
  **Category:** ${skill.category} · **Version:** \`${skill.version}\` · **Author:** \`${skill.author}\` · **Compatibility:** ${skill.compatibility}
</Info>

${body}
`;

    const outDir = path.join(DOCS_SKILLS_DIR, skill.categorySlug);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, `${skill.name}.mdx`), mdx, 'utf-8');
  }

  for (const extra of extraMdxPages) {
    const rawExtra = fs.readFileSync(extra.sourcePath, 'utf-8');
    const extraBody = convertMarkdownToMdxBody(rawExtra, { skillRouteMap }, true);
    const extraMdx = `---
title: ${JSON.stringify(extra.title)}
description: ${JSON.stringify(`Reference documentation for ${extra.title}.`)}
---

${extraBody}
`;
    const extraOutPath = path.join(DOCS_DIR, `${extra.route}.mdx`);
    fs.mkdirSync(path.dirname(extraOutPath), { recursive: true });
    fs.writeFileSync(extraOutPath, extraMdx, 'utf-8');
  }

  const grouped = new Map<string, SkillEntry[]>();
  for (const skill of skills) {
    if (!grouped.has(skill.category)) grouped.set(skill.category, []);
    grouped.get(skill.category)!.push(skill);
  }

  const orderedCategories = [
    ...CATEGORY_ORDER.filter(c => grouped.has(c)),
    ...[...grouped.keys()].filter(c => !CATEGORY_ORDER.includes(c)).sort(),
  ];

  let overviewBody = `---
title: "Skills Catalog"
description: "Browse all ${skills.length} opendirectory agent skills across ${orderedCategories.length} categories."
---

opendirectory includes **${skills.length} specialized skills** across GTM intelligence, content generation, launch orchestration, outreach, research, visual media, and developer tooling.

`;

  for (const category of orderedCategories) {
    const catSkills = grouped.get(category)!;
    overviewBody += `## ${category}\n\n`;
    overviewBody += `| Skill | Description | Version |\n|---|---|---|\n`;
    for (const s of catSkills) {
      const safeDesc = sanitizeNonCodeLine(s.description.replace(/\|/g, '&#124;'), { skillRouteMap });
      overviewBody += `| [\`${s.name}\`](/${s.docRoute}) | ${safeDesc} | \`${s.version}\` |\n`;
    }
    overviewBody += `\n`;
  }

  fs.writeFileSync(path.join(DOCS_SKILLS_DIR, 'overview.mdx'), overviewBody, 'utf-8');

  if (fs.existsSync(CONTRIBUTING_PATH)) {
    const rawContributing = fs.readFileSync(CONTRIBUTING_PATH, 'utf-8');
    const contributingBody = convertMarkdownToMdxBody(rawContributing, { skillRouteMap }, true);
    const contributingMdx = `---
title: "Contributing Guide"
description: "How to build, test, and submit an AI Agent Skill to opendirectory."
---

${contributingBody}
`;
    fs.writeFileSync(path.join(DOCS_DIR, 'contributing.mdx'), contributingMdx, 'utf-8');
  }

  const skillGroups = [
    {
      group: 'Catalog',
      pages: ['skills/overview'],
    },
    ...orderedCategories.map(category => ({
      group: category,
      pages: grouped.get(category)!.map(s => s.docRoute),
    })),
  ];

  const docsJson = {
    $schema: 'https://mintlify.com/docs.json',
    theme: 'mint',
    name: 'opendirectory',
    description: 'The open-source registry of AI agent skills for founders who hate marketing.',
    logo: {
      light: '/assets/logo-light.webp',
      dark: '/assets/logo-dark.webp',
      href: 'https://www.opendirectory.dev',
    },
    favicon: '/assets/favicon.png',
    colors: {
      primary: '#3B82F6',
      light: '#58A6FF',
      dark: '#1D4ED8',
    },
    appearance: {
      default: 'dark',
    },
    contextual: {
      options: ['copy', 'view', 'claude', 'chatgpt', 'mcp', 'cursor', 'vscode'],
    },
    navbar: {
      links: [
        {
          label: 'Website',
          href: 'https://www.opendirectory.dev',
        },
        {
          label: 'npm',
          href: 'https://www.npmjs.com/package/@opendirectory.dev/skills',
        },
      ],
      primary: {
        type: 'button',
        label: 'GitHub',
        href: 'https://github.com/Varnan-Tech/opendirectory',
      },
    },
    footer: {
      socials: {
        github: 'https://github.com/Varnan-Tech/opendirectory',
      },
    },
    navigation: {
      tabs: [
        {
          tab: 'Documentation',
          icon: 'book-open',
          groups: [
            {
              group: 'Getting Started',
              pages: ['introduction', 'installation', 'contributing'],
            },
            {
              group: 'CLI Reference',
              pages: ['cli/overview', 'cli/compatibility'],
            },
          ],
        },
        {
          tab: 'Skills Catalog',
          icon: 'layer-group',
          groups: skillGroups,
        },
      ],
    },
  };

  fs.writeFileSync(DOCS_JSON_PATH, JSON.stringify(docsJson, null, 2) + '\n', 'utf-8');
  console.log(`Successfully generated Mintlify docs for ${skills.length} skills across ${orderedCategories.length} categories in ${DOCS_DIR}`);
}

buildMintlifyDocs();
