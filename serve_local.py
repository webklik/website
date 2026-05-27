#!/usr/bin/env python3
"""Local dev server with journal clean-URL rewrites (mirrors .htaccess)."""
from __future__ import annotations

import argparse
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent

# Explicit journal slug -> file (same as .htaccess)
JOURNAL_REWRITES = {
    'ntv-am-live': 'ntv-am-live-mister-wok-2014.html',
    'spring-rolls-gold': 'spring-rolls-gold-prosperity.html',
    'wok-hei-physics': 'wok-hei-physics.html',
    'birthday-catering-guide': 'birthday-catering-guide.html',
    'long-grain-aromatic-rice': 'long-grain-aromatic-rice.html',
    'halal-wok-nairobi': 'halal-wok-nairobi.html',
    'decade-at-the-flame': 'decade-at-the-flame.html',
    'spring-rolls-gold-prosperity': 'spring-rolls-gold-prosperity.html',
}


class MisterWokHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def translate_path(self, path: str) -> str:
        path = unquote(path)
        path = path.split('?', 1)[0].split('#', 1)[0]
        if path in ('', '/'):
            return super().translate_path('/index.html')

        if path == '/menu.html':
            return super().translate_path('/parklands/menu.html')

        m = re.match(r'^/journal/([a-z0-9-]+)/?$', path)
        if m:
            slug = m.group(1)
            if slug in JOURNAL_REWRITES:
                return super().translate_path(f'/journal/{JOURNAL_REWRITES[slug]}')
            candidate = ROOT / 'journal' / f'{slug}.html'
            if candidate.is_file():
                return str(candidate)

        if path.endswith('/') and path != '/':
            index = ROOT / path.lstrip('/') / 'index.html'
            if index.is_file():
                return str(index)

        return super().translate_path(path)

    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith('GET /'):
            super().log_message(fmt, *args)


def main():
    parser = argparse.ArgumentParser(description='Mister Wok local preview server')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--bind', default='127.0.0.1')
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.bind, args.port), MisterWokHandler)
    print(f'Serving Mister Wok from: {ROOT}')
    print(f'  Home:    http://{args.bind}:{args.port}/')
    print(f'  Journal: http://{args.bind}:{args.port}/journal/')
    print('  Clean journal URLs enabled (matches .htaccess)')
    print('Press Ctrl+C to stop.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')


if __name__ == '__main__':
    main()
