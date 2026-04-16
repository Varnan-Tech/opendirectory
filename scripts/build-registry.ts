import fs from 'fs';
import path from 'path';
import { z } from 'zod';

const SkillSchema = z.object({
  name: z.string(),
  description: z.string(),
  tags: z.array(z.string()).optional().default([]),
  author: z.string().optional().default('Unknown'),
  version: z.string().optional().default('0.0.1'),
  path: z.string(),
});

type Skill = z.infer<typeof SkillSchema>;

const SKILLS_DIR = path.join(process.cwd(), 'skills');
const OUTPUT_FILE = path.join(process.cwd(), 'packages', 'cli', 'registry.json');

function extractMetadataFromMarkdown(content: string): any {
  const metadata: any = {};
  const frontmatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  
  let body = content;
  if (frontmatterMatch) {
    const frontmatter = frontmatterMatch[1];
    body = content.slice(frontmatterMatch[0].length);
    
    const lines = frontmatter.split('\n');
    for (const line of lines) {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length > 0) {
        const value = valueParts.join(':').trim();
        if (value.startsWith('[') && value.endsWith(']')) {
          metadata[key.trim()] = value.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
        } else {
          metadata[key.trim()] = value.replace(/^["']|["']$/g, '');
        }
      }
    }
  }

  if (!metadata.description) {
    const lines = body.split('\n').map(line => line.trim()).filter(line => line.length > 0);
    const firstNonTitleLine = lines.find(line => !line.startsWith('#'));
    metadata.description = firstNonTitleLine;
  }

  return metadata;
}

function buildRegistry() {
  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`Skills directory not found at ${SKILLS_DIR}`);
    process.exit(1);
  }

  const skillFolders = fs.readdirSync(SKILLS_DIR).filter(file => {
    return fs.statSync(path.join(SKILLS_DIR, file)).isDirectory();
  });

  const registry: Skill[] = [];

  for (const folder of skillFolders) {
    const folderPath = path.join(SKILLS_DIR, folder);
    let metadata: any = {
      name: folder,
      path: `skills/${folder}`,
    };

    const metaJsonPath = path.join(folderPath, 'skill.meta.json');
    if (fs.existsSync(metaJsonPath)) {
      try {
        const content = JSON.parse(fs.readFileSync(metaJsonPath, 'utf-8'));
        metadata = { ...metadata, ...content };
      } catch (e) {
        console.warn(`Warning: Failed to parse skill.meta.json in ${folder}`);
      }
    } else {
      let skillMdPath = path.join(folderPath, 'SKILL.md');
      
      if (!fs.existsSync(skillMdPath)) {
        try {
          const subDirs = fs.readdirSync(folderPath, { withFileTypes: true });
          for (const entry of subDirs) {
            if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git') {
              const possiblePath = path.join(folderPath, entry.name, 'SKILL.md');
              if (fs.existsSync(possiblePath)) {
                skillMdPath = possiblePath;
                break;
              }
              const subSubDirs = fs.readdirSync(path.join(folderPath, entry.name), { withFileTypes: true });
              for (const subEntry of subSubDirs) {
                if (subEntry.isDirectory()) {
                  const possiblePath2 = path.join(folderPath, entry.name, subEntry.name, 'SKILL.md');
                  if (fs.existsSync(possiblePath2)) {
                    skillMdPath = possiblePath2;
                    break;
                  }
                }
              }
            }
          }
        } catch (e) {}
      }

      const readmeMdPath = path.join(folderPath, 'README.md');
      const mdPath = fs.existsSync(skillMdPath) ? skillMdPath : (fs.existsSync(readmeMdPath) ? readmeMdPath : null);

      if (mdPath) {
        const content = fs.readFileSync(mdPath, 'utf-8');
        const mdMetadata = extractMetadataFromMarkdown(content);
        metadata = { ...metadata, ...mdMetadata };
      }

      const pkgJsonPath = path.join(folderPath, 'package.json');
      if (fs.existsSync(pkgJsonPath)) {
        try {
          const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf-8'));
          metadata.name = metadata.name === folder ? (pkg.name || metadata.name) : metadata.name;
          metadata.description = metadata.description || pkg.description;
          metadata.version = metadata.version || pkg.version;
          metadata.author = metadata.author || (typeof pkg.author === 'string' ? pkg.author : pkg.author?.name);
        } catch (e) {
          console.warn(`Warning: Failed to parse package.json in ${folder}`);
        }
      }
    }

    metadata.description = metadata.description || 'No description available';
    metadata.name = folder;

    const result = SkillSchema.safeParse(metadata);
    if (result.success) {
      registry.push(result.data);
    } else {
      console.warn(`Warning: Skill in ${folder} failed validation:`, result.error.format());
      const fallback = {
        ...metadata,
        description: metadata.description || 'No description available',
      };
      const fallbackResult = SkillSchema.safeParse(fallback);
      if (fallbackResult.success) {
        registry.push(fallbackResult.data);
      }
    }
  }

  const outputDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(registry, null, 2));
  console.log(`Successfully built registry with ${registry.length} skills at ${OUTPUT_FILE}`);
}

buildRegistry();
