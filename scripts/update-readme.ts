import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const SKILLS_DIR = path.join(__dirname, '../skills');
const REGISTRY_PATH = path.join(__dirname, '../packages/cli/registry.json');
const README_PATH = path.join(__dirname, '../README.md');

interface SkillEntry {
  name: string;
  description: string;
  version: string;
  path: string;
  tags?: string[];
  category?: string;
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

function getCategoryFromPkg(skillDir: string): string | null {
  const pkgPath = path.join(skillDir, 'package.json');
  if (!fs.existsSync(pkgPath)) return null;
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    if (typeof pkg.category === 'string' && CATEGORY_ORDER.includes(pkg.category)) return pkg.category;
  } catch (_) {}
  return null;
}

function detectCategoryFromContent(name: string, description: string): string {
  const n = name.toLowerCase();
  const text = (name + ' ' + description).toLowerCase();

  // Name-prefix patterns — most reliable signal, covers all existing skills
  if (/^(vid-|graphic-|blog-cover-image)/.test(n)) return 'Visual & Media';
  if (/^(email-newsletter|cook-the-blog|noise2blog|human-tone|linkedin-post|tweet-thread|noise-to-linkedin|newsletter)/.test(n)) return 'Content';
  if (/^(producthunt|show-hn|oss-launch|brand-alchemy|product-update-logger)/.test(n)) return 'Launch';
  if (/^(hackernews|reddit-icp|reddit-post|npm-downloads|yc-intent|twitter-gtm|sdk-adoption|gh-issue|map-your-market|competitor-pr|google-trends|meta-ads|meta-tribe)/.test(n)) return 'GTM Intelligence';
  if (/^(outreach-sequence|cold-email)/.test(n)) return 'Outreach';
  if (/^(pricing-|position-me|meeting-brief|linkedin-job-post|where-your-customer|vc-)/.test(n)) return 'Research';
  if (/^(kill-the-standup|dependency-update|docs-from-code|pr-description|explain-this-pr|claude-md|llms-txt|schema-markup)/.test(n)) return 'Developer Tools';

  // Description-based fallback for future skills
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
  // 1. Explicit override in skill's own package.json
  if (skillDir) {
    const pkg = getCategoryFromPkg(skillDir);
    if (pkg) return pkg;
  }
  // 2. Name-prefix regex — most reliable; tags are too broad to use first
  const fromContent = detectCategoryFromContent(name, description);
  if (fromContent !== 'Other') return fromContent;
  // 3. Registry tags — fallback for future skills whose names don't match any pattern
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

function getVersionFromSkillMd(name: string): string | null {
  const skillMdPath = path.join(SKILLS_DIR, name, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) return null;
  try {
    const content = fs.readFileSync(skillMdPath, 'utf-8');
    const { data } = matter(content);
    if (data.version) return String(data.version);
  } catch (_) {}
  return null;
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

  const skillMdVersion = getVersionFromSkillMd(name);
  if (skillMdVersion) return skillMdVersion;

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
    const desc = description || registryEntry?.description || 'No description available.';

    return {
      name,
      description: desc,
      version,
      path: `skills/${name}`,
      tags: registryEntry?.tags,
      category: getCategory(name, desc, registryEntry?.tags, skillDir),
    };
  }).sort((a: SkillEntry, b: SkillEntry) => a.name.localeCompare(b.name));
}

function generateSkillsTable(skills: SkillEntry[]): string {
  const grouped = new Map<string, SkillEntry[]>();

  for (const skill of skills) {
    const category = skill.category ?? getCategory(skill.name, skill.description, skill.tags);
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

    let updatedContent = readmeContent.replace(
      regex,
      `${startMarker}\n\n${table}\n\n${endMarker}`
    );

    // Sync all hardcoded skill counts
    updatedContent = updatedContent.replace(
      /\d+\+pre-built\+AI\+Agent\+Skills/,
      `${skills.length}+pre-built+AI+Agent+Skills`
    );
    updatedContent = updatedContent.replace(
      /\/badge\/skills-\d+-blue/,
      `/badge/skills-${skills.length}-blue`
    );
    updatedContent = updatedContent.replace(
      /Explore our growing library of \d+ specialized skills/,
      `Explore our growing library of ${skills.length} specialized skills`
    );
    updatedContent = updatedContent.replace(
      /\d+ skills across GTM/,
      `${skills.length} skills across GTM`
    );

    fs.writeFileSync(README_PATH, updatedContent, 'utf-8');

    const grouped = new Map<string, number>();
    for (const s of skills) {
      const cat = s.category ?? getCategory(s.name, s.description, s.tags);
      grouped.set(cat, (grouped.get(cat) || 0) + 1);
    }
    console.log(`Successfully updated README.md with ${skills.length} skills in ${grouped.size} categories.`);
  } catch (error) {
    console.error('Error updating README:', error);
    process.exit(1);
  }
}

updateReadme();
