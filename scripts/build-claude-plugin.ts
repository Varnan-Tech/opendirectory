import fs from 'fs';
import path from 'path';

const ROOT_DIR = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(ROOT_DIR, 'skills');
const PLUGIN_DIR = path.join(ROOT_DIR, '.claude-plugin');
const PLUGIN_JSON_PATH = path.join(PLUGIN_DIR, 'plugin.json');
const MARKETPLACE_JSON_PATH = path.join(PLUGIN_DIR, 'marketplace.json');
const PKG_JSON_PATH = path.join(ROOT_DIR, 'package.json');

function readPluginVersion(): string {
  const pkg = JSON.parse(fs.readFileSync(PKG_JSON_PATH, 'utf-8'));
  if (typeof pkg.version !== 'string' || !/^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$/.test(pkg.version)) {
    throw new Error(`Root package.json is missing a valid semver "version" field; got: ${JSON.stringify(pkg.version)}`);
  }
  return pkg.version;
}

function countSkills(): number {
  if (!fs.existsSync(SKILLS_DIR)) return 0;
  return fs.readdirSync(SKILLS_DIR).filter(file => {
    if (file.startsWith('.')) return false;
    return fs.statSync(path.join(SKILLS_DIR, file)).isDirectory();
  }).length;
}

function buildPlugin() {
  if (!fs.existsSync(PLUGIN_DIR)) {
    fs.mkdirSync(PLUGIN_DIR, { recursive: true });
  }

  const skillCount = countSkills();
  const version = readPluginVersion();

  const pluginData = {
    name: "opendirectory-gtm-skills",
    version,
    description: `A collection of ${skillCount} GTM skills for Claude Code`,
    author: { name: "Varnan" },
    homepage: "https://github.com/Varnan-Tech/opendirectory",
    repository: "https://github.com/Varnan-Tech/opendirectory",
    license: "MIT",
    keywords: ["gtm", "marketing", "growth", "claude-code", "skills", "ai-agents"]
  };

  fs.writeFileSync(PLUGIN_JSON_PATH, JSON.stringify(pluginData, null, 2));
  console.log(`Generated ${PLUGIN_JSON_PATH} (v${version}, ${skillCount} skills).`);

  const marketplaceData = {
    name: "opendirectory-marketplace",
    description: "Official marketplace for OpenDirectory skills",
    owner: { name: "Varnan" },
    plugins: [
      {
        name: "opendirectory-gtm-skills",
        source: "./",
        description: `${skillCount} GTM and Marketing Skills`
      }
    ]
  };

  fs.writeFileSync(MARKETPLACE_JSON_PATH, JSON.stringify(marketplaceData, null, 2));
  console.log(`Generated ${MARKETPLACE_JSON_PATH} (v${version}, ${skillCount} skills).`);
}

buildPlugin();
