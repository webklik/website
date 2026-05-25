#!/usr/bin/env python3
"""
fix_encoding.py — Mister Wok CRLF/BOM cleanup
Strips UTF-8 BOM and converts CRLF to LF across all HTML, CSS, JS, JSON files.
Run from: Mister_Wok_MNFVSS/
Idempotent: safe to re-run.
"""
import os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS = ['*.html', '*.css', '*.js', '*.json', '*.jsonld', '*.xml', '*.py', '*.txt']

fixed = 0
skipped = 0

for ext in EXTENSIONS:
    for path in glob.glob(os.path.join(BASE, '**', ext), recursive=True):
        # Skip .git, assets_archive
        if any(skip in path for skip in ['.git', 'node_modules', 'assets_archive', '__pycache__']):
            continue
        try:
            with open(path, 'rb') as f:
                raw = f.read()

            original = raw

            # Strip UTF-8 BOM
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]

            # Convert CRLF to LF, then stray CR to LF
            cleaned = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')

            if cleaned != original:
                with open(path, 'wb') as f:
                    f.write(cleaned)
                print(f'  FIXED    {os.path.relpath(path, BASE)}')
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'  ERROR    {path}: {e}')

print(f'\nDone. {fixed} files cleaned, {skipped} already clean.')
