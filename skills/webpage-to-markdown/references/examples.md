# Advanced Usage Examples

This document contains advanced usage patterns and edge case handling for the webpage-to-markdown skill.

## Table of Contents

- [Batch Processing](#batch-processing)
- [Handling Authentication](#handling-authentication)
- [Custom Element Filtering](#custom-element-filtering)
- [Performance Optimization](#performance-optimization)
- [Error Recovery](#error-recovery)

## Batch Processing

### Converting Multiple URLs from a File

```bash
#!/bin/bash
# batch_convert.sh

# Read URLs from file and convert each
while IFS= read -r url; do
    # Skip comments and empty lines
    [[ "$url" =~ ^#.*$ ]] && continue
    [[ -z "$url" ]] && continue

    # Create safe filename from URL
    filename=$(echo "$url" | sed 's|https\?://||' | sed 's|[^a-zA-Z0-9]|_|g').md

    echo "Converting: $url"
    python3 scripts/fetch_as_markdown.py "$url" -o "output/$filename" --verbose 2>&1 | \
        grep -E "(Error|Saved)"

    # Rate limiting
    sleep 2
done < urls.txt

echo "Batch conversion complete!"
```

### Parallel Processing with GNU Parallel

```bash
# Install GNU parallel first: brew install parallel

cat urls.txt | parallel -j 4 \
    'python3 scripts/fetch_as_markdown.py {} -o output/{#}.md'
```

## Handling Authentication

### Using Cookies (Manual Approach)

For pages requiring authentication, you may need to modify the script to accept cookies:

```python
# Modified fetch_webpage_content function
def fetch_webpage_content_with_cookies(url, cookies_file, timeout=30000):
    """Fetch webpage with authentication cookies"""
    import json

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Load cookies from file
        if cookies_file:
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
                context.add_cookies(cookies)

        page = context.new_page()
        page.goto(url, timeout=timeout)
        page.wait_for_load_state('networkidle')

        html_content = page.content()
        browser.close()

        return html_content, None
```

### Exporting Cookies from Browser

1. Install a browser extension like "EditThisCookie" (Chrome) or "Cookie-Editor" (Firefox)
2. Navigate to the authenticated page
3. Export cookies as JSON
4. Save to `cookies.json`

## Custom Element Filtering

### Removing Specific Elements

Modify the `convert_html_to_markdown` function to remove specific elements:

```python
# Add to the script
def convert_html_to_markdown_custom(html_content, remove_selectors=None):
    """
    Convert HTML to Markdown with custom element removal

    Args:
        html_content: HTML string
        remove_selectors: List of CSS selectors to remove
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove default unwanted elements
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()

    # Remove custom selectors
    if remove_selectors:
        for selector in remove_selectors:
            for element in soup.select(selector):
                element.decompose()

    html_content = str(soup)

    # Continue with normal conversion...
    return md(html_content, heading_style='atx', bullets='-')
```

### Usage Example

```python
# Remove specific elements
remove_selectors = [
    '.sidebar',
    '#comments',
    '.advertisement',
    'div[class*="promo"]'
]

markdown = convert_html_to_markdown_custom(html, remove_selectors)
```

## Performance Optimization

### Faster Conversion for Static Pages

For pages that don't require JavaScript, use a faster wait state:

```bash
# Use 'load' instead of 'networkidle' for static pages
python3 scripts/fetch_as_markdown.py https://example.com \
    --wait-for load \
    -o output.md
```

### Reducing Timeout for Fast Sites

```bash
# 10-second timeout for fast-loading sites
python3 scripts/fetch_as_markdown.py https://fast-site.com \
    --timeout 10000 \
    -o output.md
```

### Processing Only Main Content

For large pages, extract only the main content area:

```python
# Custom extraction focusing on main content
soup = BeautifulSoup(html_content, 'html.parser')

# Try common main content selectors
main_content = (
    soup.find('main') or
    soup.find('article') or
    soup.find(class_='content') or
    soup.find(id='content')
)

if main_content:
    html_content = str(main_content)
```

## Error Recovery

### Retry Logic

```bash
#!/bin/bash
# retry_fetch.sh

url="$1"
output="$2"
max_retries=3
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    echo "Attempt $((retry_count + 1))/$max_retries for $url"

    if python3 scripts/fetch_as_markdown.py "$url" -o "$output" --verbose; then
        echo "Success!"
        exit 0
    fi

    retry_count=$((retry_count + 1))

    # Exponential backoff
    sleep $((2 ** retry_count))
done

echo "Failed after $max_retries attempts"
exit 1
```

### Handling Network Issues

```bash
# Increase timeout and use verbose mode to diagnose issues
python3 scripts/fetch_as_markdown.py https://slow-site.com \
    --timeout 120000 \
    --wait-for networkidle \
    --verbose \
    2> error.log
```

### Fallback for Failed Conversions

```bash
#!/bin/bash
# fetch_with_fallback.sh

url="$1"
output="$2"

# Try with default settings
if ! python3 scripts/fetch_as_markdown.py "$url" -o "$output"; then
    echo "Default fetch failed, trying with extended timeout..."

    # Fallback: longer timeout, different wait state
    if ! python3 scripts/fetch_as_markdown.py "$url" \
        --timeout 60000 \
        --wait-for load \
        -o "$output"; then

        echo "Fallback also failed, check the URL manually"
        exit 1
    fi
fi

echo "Conversion successful"
```

## Best Practices

1. **Always use `--verbose` for debugging** - Helps identify where the process fails
2. **Test with simple URLs first** - Verify setup before processing complex sites
3. **Respect rate limits** - Add delays between batch conversions
4. **Save error logs** - Redirect stderr to a file for later analysis: `2> error.log`
5. **Check output quality** - Verify the first few conversions before batch processing
6. **Keep dependencies updated** - Run `pip install --upgrade playwright markdownify beautifulsoup4` periodically

## Common Edge Cases

### JavaScript-Heavy SPAs

```bash
# Use longer timeout and ensure networkidle
python3 scripts/fetch_as_markdown.py https://react-app.com \
    --timeout 60000 \
    --wait-for networkidle \
    --verbose
```

### PDF Links in Pages

The script converts the HTML page, not embedded PDFs. For PDFs:
1. Download PDF separately
2. Use a PDF-to-Markdown tool
3. Or check if the site offers an HTML version

### Pages with Lazy Loading

```bash
# Wait longer and use networkidle to ensure all content loads
python3 scripts/fetch_as_markdown.py https://site-with-lazy-load.com \
    --timeout 90000 \
    --wait-for networkidle
```

### Pages Requiring User Interaction

For pages that require clicking/scrolling to load content, you'll need to modify the script to add those interactions before extraction. This goes beyond the current scope and may require custom Playwright scripting.

## Integration Examples

### With Git for Version Control

```bash
#!/bin/bash
# Save webpage and commit to git

url="$1"
filename=$(date +%Y-%m-%d)_snapshot.md

python3 scripts/fetch_as_markdown.py "$url" -o "$filename"

git add "$filename"
git commit -m "Snapshot of $url on $(date)"
git push
```

### With Cron for Scheduled Archiving

```bash
# Add to crontab (run daily at 2 AM)
# crontab -e

0 2 * * * cd /path/to/skill && python3 scripts/fetch_as_markdown.py https://news-site.com/daily -o ~/archives/news-$(date +\%Y-\%m-\%d).md
```
