#!/usr/bin/env python3
"""
Fetch webpage content and convert to Markdown using Playwright browser automation.

This script uses a real browser to handle JavaScript-rendered content, ensuring
accurate extraction of dynamic webpages.
"""

import argparse
import sys
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup


def fetch_webpage_content(url, timeout=30000, wait_for='networkidle', verbose=False):
    """
    Fetch webpage content using Playwright.

    Args:
        url: URL to fetch
        timeout: Page load timeout in milliseconds
        wait_for: Wait condition ('load', 'domcontentloaded', 'networkidle')
        verbose: Print verbose output to stderr

    Returns:
        tuple: (html_content, error_message)
    """
    with sync_playwright() as p:
        browser = None
        try:
            # Launch Chromium in headless mode
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})

            if verbose:
                print(f"Navigating to {url}...", file=sys.stderr)

            # Navigate with timeout
            page.goto(url, timeout=timeout)

            # Wait for page to fully load
            # 'networkidle' ensures JavaScript execution completes
            if verbose:
                print(f"Waiting for page state: {wait_for}...", file=sys.stderr)

            page.wait_for_load_state(wait_for, timeout=timeout)

            # Extract HTML after JavaScript execution
            html_content = page.content()

            if verbose:
                print(f"Extracted {len(html_content)} characters of HTML", file=sys.stderr)

            browser.close()
            return html_content, None

        except Exception as e:
            if browser:
                browser.close()
            return None, str(e)


def convert_html_to_markdown(html_content,
                             strip_scripts=True,
                             include_images=True,
                             heading_style='atx'):
    """
    Convert HTML to Markdown with preprocessing and cleanup.

    Args:
        html_content: HTML string to convert
        strip_scripts: Remove script/style/noscript tags
        include_images: Include image references in output
        heading_style: 'atx' (#) or 'underlined'

    Returns:
        str: Markdown formatted text
    """
    # Pre-process: Remove unwanted elements
    if strip_scripts:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script, style, noscript tags
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        # Conservative removal of nav/footer/ads
        for tag in soup.find_all(['nav', 'footer', 'aside'], class_=True):
            tag_classes = ' '.join(tag.get('class', []))
            if any(keyword in tag_classes.lower()
                   for keyword in ['nav', 'menu', 'sidebar', 'footer', 'ad', 'advertisement']):
                tag.decompose()

        html_content = str(soup)

    # Convert using markdownify
    markdown_text = md(
        html_content,
        heading_style=heading_style,
        bullets='-',
        strip=['script', 'style'] if strip_scripts else [],
    )

    # Post-process: Clean excessive whitespace
    lines = markdown_text.split('\n')
    cleaned_lines = []
    blank_count = 0

    for line in lines:
        if line.strip():
            cleaned_lines.append(line)
            blank_count = 0
        else:
            blank_count += 1
            if blank_count <= 2:  # Limit consecutive blank lines
                cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Fetch webpage content and convert to Markdown using Playwright',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic - output to stdout
  %(prog)s https://example.com

  # Save to file
  %(prog)s https://example.com -o output.md

  # Slow page with verbose mode
  %(prog)s https://slow-site.com --timeout 60000 --verbose
        """
    )

    # Required arguments
    parser.add_argument('url', help='URL to fetch (must start with http:// or https://)')

    # Optional arguments
    parser.add_argument('-o', '--output',
                       help='Output file path (default: stdout)')
    parser.add_argument('--timeout', type=int, default=30000,
                       help='Page load timeout in milliseconds (default: 30000)')
    parser.add_argument('--wait-for',
                       choices=['load', 'domcontentloaded', 'networkidle'],
                       default='networkidle',
                       help='Wait condition before extracting (default: networkidle)')
    parser.add_argument('--no-strip-scripts', action='store_true',
                       help='Do not remove script/style tags (default: strip them)')
    parser.add_argument('--no-images', action='store_true',
                       help='Do not include image references (default: include them)')
    parser.add_argument('--heading-style',
                       choices=['atx', 'underlined'],
                       default='atx',
                       help='Heading style: # (atx) or underlined (default: atx)')
    parser.add_argument('--verbose', action='store_true',
                       help='Print verbose output to stderr')

    args = parser.parse_args()

    try:
        # Validate URL
        if not args.url.startswith(('http://', 'https://')):
            print(f"Error: URL must start with http:// or https://", file=sys.stderr)
            sys.exit(1)

        # Fetch webpage
        html_content, error = fetch_webpage_content(
            args.url,
            args.timeout,
            args.wait_for,
            args.verbose
        )

        if error:
            print(f"Error fetching webpage: {error}", file=sys.stderr)
            sys.exit(2)

        # Convert to Markdown
        try:
            if args.verbose:
                print("Converting HTML to Markdown...", file=sys.stderr)

            markdown = convert_html_to_markdown(
                html_content,
                strip_scripts=not args.no_strip_scripts,
                include_images=not args.no_images,
                heading_style=args.heading_style
            )
        except Exception as e:
            print(f"Error converting to Markdown: {e}", file=sys.stderr)
            sys.exit(3)

        # Output
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                if args.verbose:
                    print(f"Saved to {args.output}", file=sys.stderr)
            except Exception as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(markdown)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(255)


if __name__ == '__main__':
    main()
