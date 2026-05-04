import fs from 'node:fs';
import path from 'node:path';

const SKILLS_DIR = path.join(__dirname, '../skills');
const REGISTRY_PATH = path.join(__dirname, '../packages/cli/registry.json');
const README_PATH = path.join(__dirname, '../README.md');

interface SkillEntry {
  name: string;
  description: string;
  version: string;
  path: string;
  tags?: string[];
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

const NAME_TO_CATEGORY: Record<string, string> = {
  'graphic-chart': 'Visual & Media',
  'graphic-gif': 'Visual & Media',
  'graphic-ebook': 'Visual & Media',
  'graphic-slide-deck': 'Visual & Media',
  'graphic-case-study': 'Visual & Media',
  'vid-motion-graphics': 'Visual & Media',
  'blog-cover-image-cli': 'Visual & Media',
  'email-newsletter': 'Content',
  'cook-the-blog': 'Content',
  'noise2blog': 'Content',
  'human-tone': 'Content',
  'linkedin-post-generator': 'Content',
  'tweet-thread-from-blog': 'Content',
  'noise-to-linkedin-carousel': 'Content',
  'newsletter-digest': 'Content',
  'producthunt-launch-kit': 'Launch',
  'show-hn-writer': 'Launch',
  'oss-launch-kit': 'Launch',
  'brand-alchemy': 'Launch',
  'product-update-logger': 'Launch',
  'hackernews-intel': 'GTM Intelligence',
  'reddit-icp-monitor': 'GTM Intelligence',
  'reddit-post-engine': 'GTM Intelligence',
  'npm-downloads-to-leads': 'GTM Intelligence',
  'yc-intent-radar-skill': 'GTM Intelligence',
  'twitter-GTM-find-skill': 'GTM Intelligence',
  'sdk-adoption-tracker': 'GTM Intelligence',
  'gh-issue-to-demand-signal': 'GTM Intelligence',
  'map-your-market': 'GTM Intelligence',
  'competitor-pr-finder': 'GTM Intelligence',
  'google-trends-api-skills': 'GTM Intelligence',
  'meta-ads-skill': 'GTM Intelligence',
  'meta-tribeV2-skill': 'GTM Intelligence',
  'pricing-page-psychology-audit': 'Research',
  'pricing-finder': 'Research',
  'position-me': 'Research',
  'meeting-brief-generator': 'Research',
  'linkedin-job-post-to-buyer-pain-map': 'Research',
  'where-your-customer-lives': 'Research',
  'vc-finder': 'Research',
  'vc-curated-match': 'Research',
  'outreach-sequence-builder': 'Outreach',
  'cold-email-verifier': 'Outreach',
  'kill-the-standup': 'Developer Tools',
  'dependency-update-bot': 'Developer Tools',
  'docs-from-code': 'Developer Tools',
  'pr-description-writer': 'Developer Tools',
  'explain-this-pr': 'Developer Tools',
  'claude-md-generator': 'Developer Tools',
  'llms-txt-generator': 'Developer Tools',
  'schema-markup-generator': 'Developer Tools',
};

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

function detectCategoryFromContent(name: string, description: string): string {
  const text = (name + ' ' + description).toLowerCase();
  if (/\b(gif|mp4|motion.graphic|animation|slide.?deck|e.?book|cover.image|chart|graphic|png)\b/.test(text)) return 'Visual & Media';
  if (/pull.request|\bstandup\b|\bdependency\b|llms\.txt|json.?ld|schema.markup|claude\.md|agents\.md|codebase.scan|docs.from.code/.test(text)) return 'Developer Tools';
  if (/product.hunt|show.hn|\boss.launch\b|\bbrand.strateg|\bnaming.expert\b|\blaunch.kit\b|\bproduct.update\b/.test(text)) return 'Launch';
  if (/cold.email|outreach.sequence|email.verif/.test(text)) return 'Outreach';
  if (/pricing.page|venture.capital|\binvestor\b|\bvc\b|buyer.pain|pre.call.brief|where.*customer|icp.*channel/.test(text)) return 'Research';
  if (/hacker.news|npm.*download|yc.*startup|sdk.*adopt|google.trends|meta.ads|demand.signal|competitor.*pr|map.*market|\bgtm\b|tribe.v2|reddit.*monitor|twitter.*gtm/.test(text)) return 'GTM Intelligence';
  if (/\breddit\b|\bblog\b|newsletter|linkedin.post|carousel|tweet.thread/.test(text)) return 'Content';
  return 'Other';
}

function getCategory(name: string, description: string, tags?: string[]): string {
  if (NAME_TO_CATEGORY[name]) return NAME_TO_CATEGORY[name];
  if (tags && tags.length > 0) {
    for (const tag of tags) {
      if (TAG_TO_CATEGORY[tag]) return TAG_TO_CATEGORY[tag];
    }
  }
  return detectCategoryFromContent(name, description);
}

function extractReadmeDescription(skillDir: string): string {
  const readmePath = path.join(skillDir, 'README.md');
  if (!fs.existsSync(readmePath)) return '';

  const content = fs.readFileSync(readmePath, 'utf-8');
  const lines = content.split('\n');

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.startsWith('#')) continue;
    if (trimmed.startsWith('<img')) continue;
    if (trimmed.startsWith('<')) continue;
    if (trimmed.startsWith('![')) continue;
    if (trimmed.startsWith('```')) continue;
    if (trimmed.startsWith('---')) continue;
    if (trimmed.startsWith('[![')) continue;
    if (trimmed.startsWith('| ')) continue;
    if (trimmed === '**') continue;
    if (trimmed.startsWith('> ')) {
      const text = trimmed.slice(2).trim().replace(/\*\*/g, '').replace(/`/g, '');
      if (text.length > 20) return sanitizeDesc(text);
    }
    if (trimmed.length > 20) {
      return sanitizeDesc(trimmed.replace(/\*\*/g, '').replace(/`/g, ''));
    }
  }
  return '';
}

function sanitizeDesc(raw: string): string {
  return raw
    .replace(/<img[^>]*>/gm, '')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/(\*\*|__|\*|_)/g, '')
    .replace(/`/g, '')
    .replace(/\n/g, ' ')
    .replace(/\|/g, '&#124;')
    .trim() || 'No description provided.';
}

function getVersionFromRegistry(registry: SkillEntry[], name: string): string {
  const entry = registry.find(s => s.name === name);
  if (entry?.version) return entry.version;

  const pkgPath = path.join(SKILLS_DIR, name, 'package.json');
  if (fs.existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
      if (pkg.version) return pkg.version;
    } catch (_) {}
  }
  return '0.0.1';
}

function loadAllSkills(): SkillEntry[] {
  let registry: SkillEntry[] = [];
  try {
    registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
  } catch (_) {
    console.warn('Warning: Could not read registry.json, deriving versions from skill folders.');
  }

  const skillFolders = fs.readdirSync(SKILLS_DIR).filter((name: string) =>
    fs.statSync(path.join(SKILLS_DIR, name)).isDirectory()
  );

  return skillFolders.map((name: string) => {
    const skillDir = path.join(SKILLS_DIR, name);
    const description = extractReadmeDescription(skillDir);
    const registryEntry = registry.find(s => s.name === name);
    const version = getVersionFromRegistry(registry, name);

    return {
      name,
      description: description || registryEntry?.description || 'No description available.',
      version,
      path: `skills/${name}`,
      tags: registryEntry?.tags,
    };
  }).sort((a: SkillEntry, b: SkillEntry) => a.name.localeCompare(b.name));
}

function generateSkillsTable(skills: SkillEntry[]): string {
  const grouped = new Map<string, SkillEntry[]>();

  for (const skill of skills) {
    const category = getCategory(skill.name, skill.description, skill.tags);
    if (!grouped.has(category)) grouped.set(category, []);
    grouped.get(category)!.push(skill);
  }

  const usedCategories = CATEGORY_ORDER.filter(c => (grouped.get(c)?.length ?? 0) > 0);

  let html = `<summary><b>${skills.length} skills across ${usedCategories.length} categories</b> — click to expand</summary>\n<br>\n\n<table>\n`;

  for (const category of CATEGORY_ORDER) {
    const categorySkills = grouped.get(category);
    if (!categorySkills || categorySkills.length === 0) continue;

    const escapedCategory = category.replace(/&/g, '&amp;');
    html += `  <tr><th colspan="3" align="left">${escapedCategory}</th></tr>\n`;
    html += `  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>\n`;

    for (const skill of categorySkills) {
      html += `  <tr>\n`;
      html += `    <td><a href="${skill.path}"><code>${skill.name}</code></a></td>\n`;
      html += `    <td>${skill.description}</td>\n`;
      html += `    <td><code>${skill.version}</code></td>\n`;
      html += `  </tr>\n`;
    }
  }

  html += '</table>\n';
  return html;
}

function updateReadme() {
  try {
    const skills = loadAllSkills();
    const table = generateSkillsTable(skills);

    const readmeContent = fs.readFileSync(README_PATH, 'utf-8');

    const startMarker = '<!-- SKILLS_LIST_START -->';
    const endMarker = '<!-- SKILLS_LIST_END -->';
    const regex = new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`);

    if (!regex.test(readmeContent)) {
      console.error('Could not find SKILLS_LIST markers in README.md');
      process.exit(1);
    }

    const updatedContent = readmeContent.replace(
      regex,
      `${startMarker}\n\n${table}\n\n${endMarker}`
    );

    fs.writeFileSync(README_PATH, updatedContent, 'utf-8');

    const grouped = new Map<string, number>();
    for (const s of skills) {
      const cat = getCategory(s.name, s.description, s.tags);
      grouped.set(cat, (grouped.get(cat) || 0) + 1);
    }
    console.log(`Successfully updated README.md with ${skills.length} skills in ${grouped.size} categories.`);
  } catch (error) {
    console.error('Error updating README:', error);
    process.exit(1);
  }
}

updateReadme();
