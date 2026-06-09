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

# Double-encoding variant (Ã¯Â¿Â½) — 12 bytes
CORRUPT_DOUBLE = 'Ã¯Â¿Â½'.encode('utf-8')
# Quad-encoding variant A — 24 bytes (double re-encoded via latin-1)
CORRUPT_QUAD_A = bytes.fromhex('c383c283c382c2afc383c282c382c2bfc383c282c382c2bd')
# Quad-encoding variant B — 36 bytes (triple re-encoded via latin-1)
CORRUPT_QUAD_B = bytes.fromhex('c383c283c383c282c382c2afc383c283c383c382c382c2bfc383c283c383c382c382c2bd')

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

def fix_file(path):
    if not os.path.exists(path):
        return 0, 0, 0, 0

    data = open(path, 'rb').read()
    original = data

    quad_b_count = data.count(CORRUPT_QUAD_B)
    quad_a_count = data.count(CORRUPT_QUAD_A)
    triple_count = data.count(CORRUPT)
    double_count = data.count(CORRUPT_DOUBLE)

    if quad_b_count == 0 and quad_a_count == 0 and triple_count == 0 and double_count == 0:
        return 0, 0, 0, 0

    data = re.sub(
        rb'(\d+)' + re.escape(CORRUPT) + rb'C',
        lambda m: m.group(1) + DEGREE + b'C',
        data
    )
    data = data.replace(CORRUPT, MIDDOT)

    data = re.sub(
        rb'(\d+)' + re.escape(CORRUPT_DOUBLE) + rb'C',
        lambda m: m.group(1) + DEGREE + b'C',
        data
    )
    data = data.replace(CORRUPT_DOUBLE, MIDDOT)

    # Quad encoding variants
    data = re.sub(
        rb'(\d+)' + re.escape(CORRUPT_QUAD_A) + rb'C',
        lambda m: m.group(1) + DEGREE + b'C',
        data
    )
    data = data.replace(CORRUPT_QUAD_A, MIDDOT)
    data = re.sub(
        rb'(\d+)' + re.escape(CORRUPT_QUAD_B) + rb'C',
        lambda m: m.group(1) + DEGREE + b'C',
        data
    )
    data = data.replace(CORRUPT_QUAD_B, MIDDOT)

    if data != original:
        with open(path, 'wb') as f:
            f.write(data)

    return triple_count, double_count, quad_a_count, quad_b_count


def main():
    print('MW-FIX-TRIPLE-ENCODING.py')
    print('=' * 50)
    total_fixed = 0

    for path in HTML_FILES:
        triple, double, quad_a, quad_b = fix_file(path)
        if triple > 0 or double > 0 or quad_a > 0 or quad_b > 0:
            print(f'FIXED  {path}: {quad_b} quad-B + {quad_a} quad-A + {triple} triple + {double} double')
            total_fixed += quad_b + quad_a + triple + double
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
