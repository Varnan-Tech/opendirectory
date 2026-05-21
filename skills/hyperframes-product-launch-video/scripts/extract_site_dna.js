import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import http from 'http';
import https from 'https';
import { URL } from 'url';

async function extractSiteDNA() {
  const url = process.argv[2];
  if (!url) {
    console.error('[ERROR] Please provide a URL as a command line argument.');
    process.exit(1);
  }

  console.log(`[INFO] Launching browser to analyze: ${url}`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

    console.log('[INFO] Extracting Brand DNA...');

    const dna = await page.evaluate(() => {
      const getComputedStyleValue = (selector, property) => {
        const el = document.querySelector(selector);
        return el ? window.getComputedStyle(el).getPropertyValue(property) : null;
      };

      const colors = {
        primary: getComputedStyleValue('button', 'background-color') || getComputedStyleValue('a', 'color'),
        secondary: getComputedStyleValue('h2', 'color') || getComputedStyleValue('footer', 'background-color'),
        background: getComputedStyleValue('body', 'background-color'),
        text: getComputedStyleValue('body', 'color'),
      };

      const rootStyles = window.getComputedStyle(document.documentElement);
      const cssVars = ['--primary', '--secondary', '--brand', '--accent', '--background'];
      cssVars.forEach(v => {
        const val = rootStyles.getPropertyValue(v).trim();
        if (val) colors[v.replace('--', '')] = val;
      });

      const typography = {
        body: getComputedStyleValue('body', 'font-family'),
        heading: getComputedStyleValue('h1', 'font-family'),
      };

      const copy = {
        headline: document.querySelector('h1')?.innerText?.trim() || '',
        subheadline: document.querySelector('p')?.innerText?.trim() || '',
      };

      const favicon = document.querySelector('link[rel*="icon"]')?.href;
      
      const logoSelectors = [
        'img[alt*="logo" i]',
        'img[src*="logo" i]',
        'img[class*="logo" i]',
        '[class*="logo" i] img',
        'header img',
        'nav img'
      ];
      
      let logoUrl = null;
      for (const selector of logoSelectors) {
        const img = document.querySelector(selector);
        if (img && img.src && (img.src.endsWith('.svg') || img.src.endsWith('.png') || img.src.endsWith('.webp'))) {
          logoUrl = img.src;
          break;
        }
      }

      return { colors, typography, copy, assets: { favicon, logoUrl } };
    });

    console.log('[INFO] Downloading assets...');
    const root = process.cwd();
    if (fs.existsSync(path.join(root, 'SKILL.md'))) {
      console.error('[ERROR] You are running this inside the skill directory. Please run this in your target project folder.');
      process.exit(1);
    }
    
    const assetsDir = path.join(root, 'assets');
    if (!fs.existsSync(assetsDir)) {
      fs.mkdirSync(assetsDir, { recursive: true });
    }

    const downloadedAssets = {};

    if (dna.assets.favicon) {
      try {
        const ext = path.extname(new URL(dna.assets.favicon).pathname) || '.ico';
        const fileName = `favicon${ext}`;
        const filePath = path.join(assetsDir, fileName);
        await downloadFile(dna.assets.favicon, filePath);
        downloadedAssets.favicon = `assets/${fileName}`;
      } catch (e) {
        console.warn(`[WARNING] Failed to download favicon: ${e.message}`);
      }
    }

    if (dna.assets.logoUrl) {
      try {
        const ext = path.extname(new URL(dna.assets.logoUrl).pathname) || '.png';
        const fileName = `logo${ext}`;
        const filePath = path.join(assetsDir, fileName);
        await downloadFile(dna.assets.logoUrl, filePath);
        downloadedAssets.logo = `assets/${fileName}`;
      } catch (e) {
        console.warn(`[WARNING] Failed to download logo: ${e.message}`);
      }
    }

    const finalMetadata = {
      ...dna,
      assets: {
        ...dna.assets,
        localPaths: downloadedAssets
      },
      extractedAt: new Date().toISOString(),
      sourceUrl: url
    };

    fs.writeFileSync('brand_dna.json', JSON.stringify(finalMetadata, null, 2));
    console.log('[SUCCESS] Brand DNA saved to brand_dna.json');
    console.log('[INFO] Summary:');
    console.log(`   Headline: ${dna.copy.headline}`);
    console.log(`   Primary Color: ${dna.colors.primary}`);
    console.log(`   Heading Font: ${dna.typography.heading}`);

  } catch (error) {
    console.error('[ERROR] Error extracting site DNA:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

async function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    protocol.get(url, (response) => {
      // Handle redirects
      if ([301, 302, 303, 307, 308].includes(response.statusCode) && response.headers.location) {
        let redirectUrl = response.headers.location;
        if (!redirectUrl.startsWith('http')) {
          const baseUrl = new URL(url);
          redirectUrl = `${baseUrl.protocol}//${baseUrl.host}${redirectUrl}`;
        }
        return downloadFile(redirectUrl, dest).then(resolve).catch(reject);
      }
      
      if (response.statusCode !== 200) {
        return reject(new Error(`Failed to download file: ${response.statusCode}`));
      }
      
      const file = fs.createWriteStream(dest);
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
      file.on('error', (err) => {
        file.close();
        fs.unlink(dest, () => {});
        reject(err);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => {});
      reject(err);
    });
  });
}

extractSiteDNA();
