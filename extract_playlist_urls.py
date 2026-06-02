#!/usr/bin/env python3
"""
Extract all video URLs from a YouTube playlist and save them to a text file.

Usage:
  python extract_playlist_urls.py
  python extract_playlist_urls.py "https://www.youtube.com/playlist?list=..." output.txt

Requires:
  pip install yt-dlp
"""

from __future__ import annotations

import sys
from pathlib import Path

import yt_dlp

DEFAULT_PLAYLIST_URL = (
    "https://www.youtube.com/watch?v=pzqhbvKtY_A&list=PLj8b8hRxlEnW8LMf3mmsjV7EJrmnL54uO"
)
DEFAULT_OUTPUT_FILE = "playlist_urls.txt"


def extract_playlist_urls(playlist_url: str) -> list[str]:
    """Return canonical watch URLs for every video in the playlist."""
    ydl_opts = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    entries = info.get("entries") or []
    urls: list[str] = []

    for entry in entries:
        if not entry:
            continue

        video_id = entry.get("id")
        if video_id:
            urls.append(f"https://www.youtube.com/watch?v={video_id}")
            continue

        url = entry.get("url") or entry.get("webpage_url")
        if url:
            urls.append(url)

    return urls


def main() -> int:
    playlist_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PLAYLIST_URL
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_FILE)

    urls = extract_playlist_urls(playlist_url)
    if not urls:
        print("No video URLs found in the playlist.", file=sys.stderr)
        return 1

    output_path.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"Saved {len(urls)} URL(s) to {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
