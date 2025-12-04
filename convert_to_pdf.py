#!/usr/bin/env python3
"""
Simple HTML to PDF converter using pdfkit or weasyprint alternatives.
Falls back to instructions if libraries unavailable.
"""
import subprocess
import sys
import os

def convert_with_pandoc_html(input_md, output_pdf):
    """Convert markdown to HTML then print instructions for PDF conversion."""
    html_file = input_md.replace('.md', '.html')

    # Generate styled HTML with pandoc
    cmd = [
        'pandoc',
        input_md,
        '-s',
        '-o', html_file,
        '--metadata', 'title=Performance Review',
        '--css', 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css',
        '--self-contained'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Generated HTML: {html_file}")
        print(f"\nTo convert to PDF, you can:")
        print(f"1. Open {html_file} in Safari/Chrome")
        print(f"2. Press Cmd+P (Print)")
        print(f"3. Click 'PDF' dropdown → 'Save as PDF'")
        print(f"4. Save as: {output_pdf}")
        print(f"\nAlternatively, run this AppleScript command:")
        print(f'  osascript -e \'tell application "Safari" to open POSIX file "{os.path.abspath(html_file)}"\'')
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating HTML: {e}")
        return False

if __name__ == '__main__':
    input_file = 'Rosannys_Ruiz_Review.md'
    output_file = 'Rosannys_Ruiz_Review.pdf'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    convert_with_pandoc_html(input_file, output_file)
