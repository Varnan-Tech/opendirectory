import fs from 'fs';
import path from 'path';

function scaffoldProject() {
  const root = process.cwd();
  
  if (fs.existsSync(path.join(root, 'SKILL.md'))) {
    console.error('[ERROR] You are running this inside the skill directory. Please run this in your target project folder.');
    process.exit(1);
  }

  const dirs = ['assets', 'compositions', 'references', 'scripts'];
  
  console.log('[INFO] Initializing Product Launch Video project structure...');

  dirs.forEach(dir => {
    const dirPath = path.join(root, dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
      console.log(`[SUCCESS] Created directory: ${dir}`);
    } else {
      console.log(`[INFO] Directory already exists: ${dir}`);
    }
  });

  const placeholders = [
    'sfx-whoosh.txt',
    'sfx-impact.txt',
    'sfx-shimmer.txt',
    'bg-music-placeholder.txt'
  ];

  placeholders.forEach(file => {
    const filePath = path.join(root, 'assets', file);
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, 'PLACEHOLDER - Replace with actual audio file');
      console.log(`[SUCCESS] Created placeholder asset reference: ${file}`);
    }
  });

  const brandDnaTemplate = {
    "colors": {
      "primary": "#000000",
      "secondary": "#ffffff",
      "accent": "#3b82f6",
      "background": "#000000",
      "text": "#ffffff"
    },
    "typography": {
      "body": "Inter, sans-serif",
      "heading": "Inter, sans-serif"
    },
    "copy": {
      "headline": "Your Product Name",
      "subheadline": "The future of [Your Industry]"
    },
    "assets": {
      "logoUrl": null,
      "localPaths": {
        "logo": "assets/logo.png"
      }
    }
  };

  const dnaPath = path.join(root, 'brand_dna.json');
  if (!fs.existsSync(dnaPath)) {
    fs.writeFileSync(dnaPath, JSON.stringify(brandDnaTemplate, null, 2));
    console.log('[SUCCESS] Created brand_dna.json template');
  }

  console.log('[SUCCESS] Project scaffolding complete.');
  console.log('[INFO] Next steps:');
  console.log('   1. Replace placeholder assets in /assets');
  console.log('   2. Update brand_dna.json with your brand details');
  console.log('   3. Run npx hyperframes init to initialize the core engine');
}

scaffoldProject();
