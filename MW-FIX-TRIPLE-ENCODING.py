#!/usr/bin/env python3
"""
MW-FIX-TRIPLE-ENCODING.py
Fixes triple-encoded UTF-8 mojibake that appears as ÃÂ¯ÃÂ¿ÃÂ½ in the browser.

Root cause: Cursor re-saved HTML files with wrong encoding during sprint sessions,
converting special characters (·, °, –, ★, etc.) through multiple encoding cycles
until they became unrecognisable to both the browser and sanitizePageText() in engine.js.

Run from project root:
    python3 MW-FIX-TRIPLE-ENCODING.py

Safe to re-run — idempotent.
"""

import os
import re

# The corrupt byte sequence as it appears in the file (UTF-8 encoded mojibake string)
# Browser displays: ÃÂ¯ÃÂ¿ÃÂ½
# File bytes:       C3 83 C2 82 C2 AF  C3 83 C2 82 C2 BF  C3 83 C2 82 C2 BD
CORRUPT = 'ÃÂ¯ÃÂ¿ÃÂ½'.encode('utf-8')

# What the corrupt sequence SHOULD be depends on context:
# Between text phrases → · (middle dot, U+00B7)
# After a number before C → ° (degree, U+00B0)
# These are handled by context-aware replacement below.

MIDDOT  = '·'.encode('utf-8')   # C2 B7
DEGREE  = '°'.encode('utf-8')   # C2 B0
ENDASH  = '–'.encode('utf-8')   # E2 80 93
STAR    = '★'.encode('utf-8')   # E2 98 85

# Also catch double-encoding variant (Ã¯Â¿Â½) in case some files have that
CORRUPT_DOUBLE = 'Ã¯Â¿Â½'.encode('utf-8')

# Quadruple-encoding variant (24 bytes) — same browser glyph, longer file sequence
CORRUPT_QUAD = 'ÃÂ¯ÃÂ¿ÃÂ½'.encode('utf-8')

HTML_FILES = [
    'capital-centre/index.html',
    'capital-centre/menu.html',
    'two-rivers/index.html',
    'two-rivers/menu.html',
    'parklands/index.html',
    'parklands/menu.html',
    'locations/index.html',
    'index.html',
    '404.html',
    'videos.html',
    'catering.html',
    'social-proof.html',
    'journal/halal-wok-nairobi.html',
    'journal/wok-hei-physics.html',
    'journal/birthday-catering-guide.html',
    'journal/long-grain-aromatic-rice.html',
    'journal/decade-at-the-flame.html',
    'journal/spring-rolls-gold-prosperity.html',
    'journal/ntv-am-live-mister-wok-2014.html',
    'journal/index.html',
]

def _apply_fixes(data, corrupt):
    """Replace corrupt byte runs: digit+CORRUPT+C → °C, else → ·."""
    data = re.sub(
        rb'(\d+)' + re.escape(corrupt) + rb'C',
        lambda m: m.group(1) + DEGREE + b'C',
        data
    )
    return data.replace(corrupt, MIDDOT)


def fix_file(path):
    if not os.path.exists(path):
        return 0, 0, 0

    data = open(path, 'rb').read()
    original = data

    quad_count = data.count(CORRUPT_QUAD)
    triple_count = data.count(CORRUPT)
    double_count = data.count(CORRUPT_DOUBLE)

    if quad_count == 0 and triple_count == 0 and double_count == 0:
        return 0, 0, 0

    # Longest pattern first to avoid partial matches
    if quad_count:
        data = _apply_fixes(data, CORRUPT_QUAD)
    if triple_count:
        data = _apply_fixes(data, CORRUPT)
    if double_count:
        data = _apply_fixes(data, CORRUPT_DOUBLE)

    if data != original:
        with open(path, 'wb') as f:
            f.write(data)

    return triple_count, double_count, quad_count


def main():
    print('MW-FIX-TRIPLE-ENCODING.py')
    print('=' * 50)
    total_fixed = 0

    for path in HTML_FILES:
        triple, double, quad = fix_file(path)
        if triple > 0 or double > 0 or quad > 0:
            print(f'FIXED  {path}: {quad} quad + {triple} triple + {double} double instances')
            total_fixed += quad + triple + double
        else:
            if os.path.exists(path):
                print(f'clean  {path}')
            else:
                print(f'skip   {path} (not found)')

    print()
    if total_fixed > 0:
        print(f'Total replacements: {total_fixed}')
        print()
        print('Next steps:')
        print('  1. Verify in browser: · and °C render correctly')
        print('  2. Run MW-FIX-ENCODING.py as well (catches U+FFFD single encoding)')
        print('  3. git add -A && git commit -m "fix: triple-encoding mojibake — CC index + any others"')
        print('  4. cPanel deploy -> SpeedyCache purge')
    else:
        print('All files clean — no triple-encoding corruption found.')
        print('If corruption still shows in browser, check the file is saved as UTF-8')
        print('and the server is sending Content-Type: text/html; charset=utf-8')


if __name__ == '__main__':
    main()
