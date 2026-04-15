import fs from 'node:fs';
import path from 'node:path';

const skillsDir = path.join(process.cwd(), 'skills');
const contributingPath = path.join(process.cwd(), 'CONTRIBUTING.md');

function updateContributing() {
  if (!fs.existsSync(skillsDir)) {
    console.error('skills directory not found');
    process.exit(1);
  }

  if (!fs.existsSync(contributingPath)) {
    console.error('CONTRIBUTING.md not found');
    process.exit(1);
  }

  const existingSkills = fs.readdirSync(skillsDir).filter(file => {
    return fs.statSync(path.join(skillsDir, file)).isDirectory();
  });

  let contributingContent = fs.readFileSync(contributingPath, 'utf-8');

  existingSkills.forEach(skill => {
    const escapedSkill = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`- \\[ \\] \`${escapedSkill}\``, 'g');
    contributingContent = contributingContent.replace(regex, `- [x] \`${skill}\``);
  });

  fs.writeFileSync(contributingPath, contributingContent, 'utf-8');
  console.log('Successfully updated CONTRIBUTING.md with claimed skills.');
}

updateContributing();
