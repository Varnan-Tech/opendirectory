import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const skillsDir = path.join(process.cwd(), 'skills');

const disallowedExtensions = ['.exe', '.dll', '.bat', '.zip', '.gz', '.tar'];
const dangerousPatterns = [
  /rm\s+-rf\s+\//,
  /curl.*\|.*bash/,
  /wget.*\|.*sh/,
  /(?<!\.)eval\(/,
  /(?<!\.)exec\(/,
];

function scanDirectory(dir: string, errors: string[]) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;

    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      scanDirectory(fullPath, errors);
    } else {
      const ext = path.extname(entry.name).toLowerCase();

      if (disallowedExtensions.includes(ext)) {
        errors.push(`Disallowed file extension found: ${fullPath}`);
        continue;
      }

      if (['.sh', '.py', '.js', '.ts'].includes(ext)) {
        const content = fs.readFileSync(fullPath, 'utf-8');
        for (const pattern of dangerousPatterns) {
          if (pattern.test(content)) {
            errors.push(`Dangerous pattern ${pattern.toString()} found in file: ${fullPath}`);
          }
        }
      }
    }
  }
}

function findSkillMd(dir: string, depth: number = 0): string | null {
  if (depth > 4) return null;
  
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (e) {
    return null;
  }
  
  for (const entry of entries) {
    if ((entry.isFile() || entry.isSymbolicLink()) && entry.name.toLowerCase() === 'skill.md') {
      return path.join(dir, entry.name);
    }
  }
  
  for (const entry of entries) {
    if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git') {
      const found = findSkillMd(path.join(dir, entry.name), depth + 1);
      if (found) return found;
    }
  }
  
  return null;
}

function findReadmeMd(dir: string, depth: number = 0): string | null {
  if (depth > 4) return null;
  
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (e) {
    return null;
  }
  
  for (const entry of entries) {
    if ((entry.isFile() || entry.isSymbolicLink()) && entry.name.toLowerCase() === 'readme.md') {
      return path.join(dir, entry.name);
    }
  }
  
  for (const entry of entries) {
    if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git') {
      const found = findReadmeMd(path.join(dir, entry.name), depth + 1);
      if (found) return found;
    }
  }
  
  return null;
}

function validateSkills() {
  if (!fs.existsSync(skillsDir)) {
    console.log('No skills directory found.');
    return;
  }

  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  let hasErrors = false;

  for (const entry of entries) {
    if (entry.isDirectory()) {
      const skillPath = path.join(skillsDir, entry.name);
      const skillMdPath = findSkillMd(skillPath);
      const errors: string[] = [];

      if (!skillMdPath) {
        errors.push(`Error: Skill '${entry.name}' is missing a SKILL.md file anywhere inside its folder.`);
      } else {
        const readmePath = findReadmeMd(skillPath);
        
        if (!readmePath) {
          errors.push(`Error: Skill '${entry.name}' is missing a README.md file anywhere inside its folder.`);
        }

        try {
          const fileContent = fs.readFileSync(skillMdPath, 'utf-8');
          const parsed = matter(fileContent);
          
          if (typeof parsed.data.name !== 'string') {
            errors.push(`Error: Skill '${entry.name}' is missing 'name' in SKILL.md frontmatter.`);
          }
          if (typeof parsed.data.description !== 'string') {
            errors.push(`Error: Skill '${entry.name}' is missing 'description' in SKILL.md frontmatter.`);
          }
        } catch (err: any) {
          errors.push(`Error: Failed to parse SKILL.md for '${entry.name}': ${err.message}`);
        }
      }

      scanDirectory(skillPath, errors);

      if (errors.length > 0) {
        hasErrors = true;
        for (const error of errors) {
          console.error(error);
        }
      } else {
        console.log(`Skill '${entry.name}' is valid.`);
      }
    }
  }

  if (hasErrors) {
    console.error('\nValidation failed: One or more skills have errors.');
    process.exit(1);
  } else {
    console.log('\nAll skills are valid!');
  }
}

validateSkills();
