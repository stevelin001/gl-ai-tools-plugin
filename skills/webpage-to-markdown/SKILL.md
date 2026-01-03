---
name: webpage-to-markdown
description: Extract webpage content and convert to Markdown format using Playwright browser automation. Use when you need to fetch and convert web content to Markdown, handle JavaScript-rendered pages, or preserve webpage formatting as Markdown. Supports extracting text, images, links, and formatting from any URL.
---

# Webpage to Markdown Converter

## Overview

Convert webpage content to Markdown format using Playwright browser automation. This skill uses a real browser to handle JavaScript-rendered content, ensuring accurate extraction of dynamic webpages.

**Key capabilities:**
- Fetch content from JavaScript-rendered pages
- Preserve text formatting, links, images, and structure
- Customize conversion options (heading styles, image inclusion, etc.)
- Handle timeouts and wait conditions for slow-loading pages

## When to Use This Skill

**Use this skill when:**
- Converting webpage content to Markdown for documentation
- Extracting article/blog post content in readable format
- Archiving web content in a portable format
- Processing JavaScript-heavy single-page applications (SPAs)

**Do NOT use this skill for:**
- Testing web applications (use `webapp-testing` skill instead)
- Taking screenshots of webpages (use screenshot tools)
- Scraping structured data (consider dedicated scraping tools)
- Accessing APIs (use direct API requests)

## Quick Start

### Basic Usage

```bash
# Convert webpage to Markdown (output to stdout)
python3 scripts/fetch_as_markdown.py https://example.com

# Save to file
python3 scripts/fetch_as_markdown.py https://example.com -o output.md

# See all options
python3 scripts/fetch_as_markdown.py --help
```

### Common Patterns

**1. Convert blog post:**
```bash
python3 scripts/fetch_as_markdown.py https://blog.example.com/article -o article.md
```

**2. Handle slow-loading page:**
```bash
python3 scripts/fetch_as_markdown.py https://slow-site.com \
  --timeout 60000 --wait-for networkidle --verbose
```

**3. Batch conversion:**
```bash
for url in $(cat urls.txt); do
  filename=$(echo "$url" | sed 's|https://||' | sed 's|/|_|g').md
  python3 scripts/fetch_as_markdown.py "$url" -o "$filename"
done
```

## Options Reference

### Required Arguments
- `url` - URL to fetch (must start with http:// or https://)

### Optional Arguments
- `-o, --output FILE` - Save to file instead of stdout
- `--timeout MS` - Page load timeout in milliseconds (default: 30000)
- `--wait-for STATE` - Wait condition: load, domcontentloaded, networkidle (default: networkidle)
- `--no-strip-scripts` - Keep script/style tags (default: remove them)
- `--no-images` - Exclude image references (default: include them)
- `--heading-style STYLE` - Heading style: atx (#) or underlined (default: atx)
- `--verbose` - Print verbose output to stderr

### Wait States Explained

- **load**: Wait for 'load' event (fast, may miss dynamic content)
- **domcontentloaded**: Wait for DOM ready (medium, misses async content)
- **networkidle**: Wait for no network activity (slow, most complete)

**Recommendation**: Use `networkidle` (default) for JavaScript-heavy sites.

## Troubleshooting

**Issue: "Error fetching webpage: Timeout"**
- Increase timeout: `--timeout 60000` (60 seconds)
- Check URL is accessible
- Try different wait state: `--wait-for load`

**Issue: "Extracted Markdown is incomplete"**
- Use `--wait-for networkidle` to ensure full page load
- Add `--verbose` to see execution details
- Check if content requires authentication

**Issue: "Too much unwanted content"**
- Script automatically removes common non-content elements (nav, footer, ads)
- Post-process Markdown to remove specific sections
- See [references/examples.md](references/examples.md) for custom filtering

**Issue: "command not found: python"**
- Use `python3` instead of `python`
- Or create alias: `alias python=python3`

### Debugging

Use `--verbose` flag for detailed execution steps:
```bash
python3 scripts/fetch_as_markdown.py https://example.com --verbose
```

## Advanced Usage

For complex scenarios and edge case handling, see [references/examples.md](references/examples.md):
- Authentication and cookies
- Custom element filtering
- Batch processing strategies
- Performance optimization

## Dependencies

Required packages:
```bash
pip install playwright markdownify beautifulsoup4
playwright install chromium
```

**Requirements:**
- Python 3.8+
- playwright>=1.40.0
- markdownify>=0.11.0
- beautifulsoup4>=4.12.0

**Installation:**
```bash
# Install Python packages
pip3 install playwright markdownify beautifulsoup4

# Install Playwright browsers (required)
python3 -m playwright install chromium
```

## Resources

This skill includes:

### scripts/
- `fetch_as_markdown.py` - Main conversion script with Playwright automation

### references/
- `examples.md` - Advanced usage patterns and edge cases
