import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { z } from 'zod';
import { inspectSkillFrontmatter } from '../packages/cli/src/frontmatter';
import { findSkillSourceSync } from '../packages/cli/src/skill-discovery';

const SkillSchema = z.object({
  name: z.string(),
  description: z.string(),
  tags: z.array(z.string()).optional().default([]),
  author: z.string().optional().default('Unknown'),
  version: z.string().optional().default('0.0.1'),
  path: z.string(),
  compatibility: z.unknown().optional(),
});

type Skill = z.infer<typeof SkillSchema>;

const SKILLS_DIR = path.join(process.cwd(), 'skills');
const OUTPUT_FILE = path.join(process.cwd(), 'packages', 'cli', 'registry.json');

function extractMetadataFromSkillMd(content: string): { metadata: Record<string, unknown>; compatibility: ReturnType<typeof inspectSkillFrontmatter>['compatibility'] } {
  const frontmatter = inspectSkillFrontmatter(content);
  const metadata: Record<string, unknown> = flattenFrontmatterMetadata(frontmatter.data);

  if (!metadata.description) {
    const lines = frontmatter.content.split('\n').map(line => line.trim()).filter(line => line.length > 0);
    const firstNonTitleLine = lines.find(line => !line.startsWith('#'));
    metadata.description = firstNonTitleLine;
  }

  return { metadata, compatibility: frontmatter.compatibility };
}

function flattenFrontmatterMetadata(data: Record<string, unknown>): Record<string, unknown> {
  const nested = data.metadata;
  if (!nested || typeof nested !== 'object' || Array.isArray(nested)) {
    return data;
  }

  // Some skills keep author/version under `metadata`; retain top-level fields
  // as the explicit override while exposing nested values to the registry schema.
  const { compatibility: _nestedCompatibility, ...nestedMetadata } = nested as Record<string, unknown>;
  const { metadata: _nestedMetadata, ...topLevel } = data;
  return { ...nestedMetadata, ...topLevel };
}

export function buildRegistry(skillsDir = SKILLS_DIR, outputFile = OUTPUT_FILE): Skill[] {
  if (!fs.existsSync(skillsDir)) {
    console.error(`Skills directory not found at ${skillsDir}`);
    process.exit(1);
  }

  const skillFolders = fs.readdirSync(skillsDir).filter(file => {
    return fs.statSync(path.join(skillsDir, file)).isDirectory();
  }).sort(); // deterministic order across all OS/filesystems

  const registry: Skill[] = [];

  for (const folder of skillFolders) {
    const folderPath = path.join(skillsDir, folder);
    const jsonMetadata: Record<string, unknown> = {};
    let metadata: any = {
      name: folder,
      path: `skills/${folder}`,
    };

    const metaJsonPath = path.join(folderPath, 'skill.meta.json');
    if (fs.existsSync(metaJsonPath)) {
      try {
        const content = JSON.parse(fs.readFileSync(metaJsonPath, 'utf-8'));
        const { compatibility: _ignoredCompatibility, ...ordinaryMetadata } = content;
        Object.assign(jsonMetadata, ordinaryMetadata);
        metadata = { ...metadata, ...ordinaryMetadata };
      } catch (e) {
        console.warn(`Warning: Failed to parse skill.meta.json in ${folder}`);
      }
    }

    const source = findSkillSourceSync(folderPath);
    if (source) {
      const sourceMetadata = extractMetadataFromSkillMd(fs.readFileSync(source.skillMdPath, 'utf-8'));
      if (sourceMetadata.compatibility.kind === 'invalid') {
        throw new Error(`Skill '${folder}' has an invalid compatibility declaration: ${sourceMetadata.compatibility.error}`);
      }
      metadata = { ...metadata, ...sourceMetadata.metadata, ...jsonMetadata };
      if (sourceMetadata.compatibility.kind === 'valid') {
        metadata.compatibility = sourceMetadata.compatibility.targets;
      } else {
        delete metadata.compatibility;
      }
    } else {
      delete metadata.compatibility;
    }

    const pkgJsonPath = path.join(folderPath, 'package.json');
    if (fs.existsSync(pkgJsonPath)) {
      try {
        const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf-8'));
        metadata.name = metadata.name === folder ? (pkg.name || metadata.name) : metadata.name;
        metadata.description = metadata.description || pkg.description;
        metadata.version = metadata.version || pkg.version;
        metadata.author = metadata.author || (typeof pkg.author === 'string' ? pkg.author : pkg.author?.name) || 'opendirectory';
      } catch (e) {
        console.warn(`Warning: Failed to parse package.json in ${folder}`);
        metadata.author = metadata.author || 'opendirectory';
      }
    } else {
      metadata.author = metadata.author || 'opendirectory';
    }

    metadata.description = metadata.description || 'No description available';
    if (metadata.description.length > 130) {
      // Split by sentence and take the first one or two
      const sentences = metadata.description.match(/[^\.!\?]+[\.!\?]+/g) || [metadata.description];
      metadata.description = sentences.slice(0, 1).join(' ').trim();
      if (metadata.description.length > 150) {
        metadata.description = metadata.description.substring(0, 147).trim() + '...';
      }
    }
    metadata.name = folder;

    // Auto-generate tags based on description keywords if tags are empty
    if (!metadata.tags || metadata.tags.length === 0) {
      const lowerDesc = metadata.description.toLowerCase();
      const generatedTags = [];
      if (lowerDesc.includes('seo') || lowerDesc.includes('search')) generatedTags.push('SEO');
      if (lowerDesc.includes('market') || lowerDesc.includes('gtm') || lowerDesc.includes('growth')) generatedTags.push('Marketing');
      if (lowerDesc.includes('brand') || lowerDesc.includes('nam') || lowerDesc.includes('identity')) generatedTags.push('Branding');
      if (lowerDesc.includes('email') || lowerDesc.includes('outreach')) generatedTags.push('Email');
      if (lowerDesc.includes('social') || lowerDesc.includes('linkedin') || lowerDesc.includes('twitter') || lowerDesc.includes('tweet')) generatedTags.push('Social Media');
      if (lowerDesc.includes('ai ') || lowerDesc.includes(' llm') || lowerDesc.includes('prompt')) generatedTags.push('AI');
      if (lowerDesc.includes('write') || lowerDesc.includes('copy') || lowerDesc.includes('content') || lowerDesc.includes('blog')) generatedTags.push('Copywriting');
      if (lowerDesc.includes('code') || lowerDesc.includes('github') || lowerDesc.includes('pr ')) generatedTags.push('Developer Tools');
      
      metadata.tags = generatedTags;
    }

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

  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputFile, JSON.stringify(registry, null, 2));
  console.log(`Successfully built registry with ${registry.length} skills at ${outputFile}`);
  return registry;
}

const executedFile = process.argv[1] ? path.resolve(process.argv[1]) : '';
if (executedFile === path.resolve(fileURLToPath(import.meta.url))) {
  buildRegistry();
}
