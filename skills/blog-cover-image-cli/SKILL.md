---
name: blog-cover-generator
description: Use when the user asks to generate a blog cover image, thumbnail, or article header. Automatically uses modern typography, brand logos, and Google Search grounding to create beautiful 16:9 images with Gemini 3.1 Flash Image Preview.
---

# Blog Cover Generator Skill

This skill provides AI agents with the ability to generate stunning, minimalist, technical blog cover images using the `blog-cover-image-cli`. The CLI leverages Gemini 3.1 Flash Image Preview, automatically fetches brand logos from domains, uses local aesthetic reference images, and employs Google Search grounding to inject real-time context.

## Setup & Configuration

**Agent Pre-requisites:**
Before using this tool, verify it is installed. If `blog-cover-cli --help` fails, install it globally:
```bash
npm install -g blog-cover-image-cli
```

If the user wants you to generate an image and you haven't set up the API key yet, you must first configure the CLI using a Gemini API Key. The CLI stores this securely via the `conf` package.

```bash
# 1. Set your Gemini API Key (Required for image generation)
npx -p blog-cover-image-cli blog-cover-cli config set-key <YOUR_GEMINI_API_KEY>

# 2. Set your Brandfetch Client ID (Required to fetch high-res logos)
npx -p blog-cover-image-cli blog-cover-cli config set-brandfetch-id <YOUR_BRANDFETCH_CLIENT_ID>

# Check your keys (masked)
npx -p blog-cover-image-cli blog-cover-cli config get-key
npx -p blog-cover-image-cli blog-cover-cli config get-brandfetch-id
```

## Usage: Generating an Image

When a user asks for a cover image (e.g., "Create a cover image for my blog about Vercel v0"), you should use the `generate` command.

```bash
npx -p blog-cover-image-cli blog-cover-cli generate -t "The Title of the Blog Post" -l "example.com"
```

### Arguments
- `-t, --title <text>`: **(Required)** The title text to display on the cover image. Do not use excessively long titles (keep it under 3 lines of text visually).
- `-l, --logo <domain>`: **(Optional but recommended)** The domain to fetch the brand logo from (e.g., `vercel.com`, `google.com`, `cursor.com`). The CLI automatically converts WebP/SVG/AVIF to PNG for compatibility.
- `-o, --output <path>`: **(Optional)** The file path where the generated image will be saved. If omitted, the CLI automatically saves it to an `output/` directory in the current working folder (e.g., `./output/vercel-cover.png`).

### Examples

**Example 1: Cursor**
```bash
npx -p blog-cover-image-cli blog-cover-cli generate -t "Why Cursor is the Ultimate AI Code Editor" -l "cursor.com"
```

**Example 2: Lovable**
```bash
npx -p blog-cover-image-cli blog-cover-cli generate -t "Building Apps in Minutes with Lovable" -l "lovable.dev"
```

**Example 3: Custom Output Path**
```bash
npx -p blog-cover-image-cli blog-cover-cli generate -t "Mastering React in 2026" -l "reactjs.org" -o "./assets/react-cover.png"
```

## How It Works Under the Hood
As an agent, you should know what the CLI is doing so you can inform the user:
1. **Logo Fetching**: It fetches logos from `Brandfetch` and processes them via `sharp`.
2. **References**: It loads curated reference images from its `examples/` directory to ensure the output is always a clean, minimalist white background with bold typography.
3. **Grounding**: It has `googleSearch` tools enabled, meaning if the title relates to a recent event, Gemini can look it up before generating the image.
4. **Text Enforcement**: It forces Gemini to output the exact title string using typographic placement rules.

## Edge Cases / Troubleshooting
- **No API Key Error**: If you see an API key error, run the `config set-key` command.
- **Logo Fetch Warning**: If the CLI says `Warning: Could not fetch logo`, it will still generate the image but without the logo. You do not need to crash or stop.
- **Strict Modality Limits**: Because it uses Gemini's experimental image models, generation may occasionally fail due to strict safety filters. If this happens, notify the user.