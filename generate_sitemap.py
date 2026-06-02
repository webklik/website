#!/usr/bin/env python3
"""
Mister Wok — Automated XML Sitemap Generator
Scans the site root and writes sitemap.xml.

Usage:
  python generate_sitemap.py                  # default: site root = script directory
  python generate_sitemap.py /path/to/site    # custom root

Bluehost cron (daily at midnight UTC):
  0 0 * * * /usr/bin/python3 /home2/dykbsgmy/public_html/generate_sitemap.py >> /home2/dykbsgmy/logs/sitemap.log 2>&1

Note: generate_sitemap.py is excluded from cPanel rsync deploy (.cpanel.yml).
      Copy this script to the server once, or run locally before git push.
"""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

BASE_URL = "https://misterwok.net"

# Journal filename → clean public URL slug (matches .htaccess)
JOURNAL_SLUGS: dict[str, str] = {
    "ntv-am-live-mister-wok-2014.html": "ntv-am-live",
    "spring-rolls-gold-prosperity.html": "spring-rolls-gold",
    "wok-hei-physics.html": "wok-hei-physics",
    "birthday-catering-guide.html": "birthday-catering-guide",
    "long-grain-aromatic-rice.html": "long-grain-aromatic-rice",
    "halal-wok-nairobi.html": "halal-wok-nairobi",
    "decade-at-the-flame.html": "decade-at-the-flame",
}

EXCLUDE_FILES = frozenset(
    {
        "404.html",
        "menu.html",  # legacy redirect → parklands/menu.html
        "_frag_sig_grid_cc.html",
    }
)

EXCLUDE_DIRS = frozenset(
    {
        "_includes",
        "assets",
        "images",
        "media",
        "__pycache__",
        ".git",
    }
)

# Static pages at site root (non-index .html)
ROOT_STATIC_PAGES = frozenset(
    {
        "catering.html",
        "videos.html",
        "social-proof.html",
    }
)

BRANCH_DIRS = ("parklands", "capital-centre", "two-rivers")


def file_lastmod(path: Path) -> str:
    mtime = path.stat().st_mtime
    return date.fromtimestamp(mtime).isoformat()


def add_url(
    urls: list[dict],
    loc: str,
    path: Path,
    changefreq: str,
    priority: str,
) -> None:
    urls.append(
        {
            "loc": loc,
            "lastmod": file_lastmod(path),
            "changefreq": changefreq,
            "priority": priority,
        }
    )


def collect_urls(site_root: Path) -> list[dict]:
    urls: list[dict] = []
    today_fallback = date.today().isoformat()

    # Homepage
    index = site_root / "index.html"
    if index.is_file():
        add_url(urls, f"{BASE_URL}/", index, "weekly", "1.0")

    # Locations hub
    locations_index = site_root / "locations" / "index.html"
    if locations_index.is_file():
        add_url(urls, f"{BASE_URL}/locations/", locations_index, "monthly", "0.8")

    # Branch landing pages + menus
    for branch in BRANCH_DIRS:
        branch_index = site_root / branch / "index.html"
        if branch_index.is_file():
            add_url(urls, f"{BASE_URL}/{branch}/", branch_index, "weekly", "0.9")

        branch_menu = site_root / branch / "menu.html"
        if branch_menu.is_file():
            priority = "0.9" if branch == "parklands" else "0.85"
            add_url(
                urls,
                f"{BASE_URL}/{branch}/menu.html",
                branch_menu,
                "weekly",
                priority,
            )

    # Root static pages
    for name in sorted(ROOT_STATIC_PAGES):
        page = site_root / name
        if page.is_file():
            add_url(urls, f"{BASE_URL}/{name}", page, "monthly", "0.7")

    # Journal index
    journal_index = site_root / "journal" / "index.html"
    if journal_index.is_file():
        add_url(urls, f"{BASE_URL}/journal/", journal_index, "monthly", "0.7")

    # Journal articles (clean slugs)
    journal_dir = site_root / "journal"
    if journal_dir.is_dir():
        for html_file in sorted(journal_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            slug = JOURNAL_SLUGS.get(html_file.name, html_file.stem)
            priority = "0.8" if slug in ("decade-at-the-flame", "ntv-am-live", "spring-rolls-gold") else "0.7"
            add_url(
                urls,
                f"{BASE_URL}/journal/{slug}",
                html_file,
                "monthly",
                priority,
            )

    # Machine-readable assets
    for asset, priority in (
        ("llms.txt", "0.3"),
        ("menu.jsonld", "0.4"),
        ("entity-map.json", "0.4"),
    ):
        asset_path = site_root / asset
        if asset_path.is_file():
            urls.append(
                {
                    "loc": f"{BASE_URL}/{asset}",
                    "lastmod": file_lastmod(asset_path),
                    "changefreq": "weekly",
                    "priority": priority,
                }
            )

    # Deduplicate by loc (keep first)
    seen: set[str] = set()
    unique: list[dict] = []
    for entry in urls:
        if entry["loc"] not in seen:
            seen.add(entry["loc"])
            unique.append(entry)

    return unique


def build_xml(urls: list[dict]) -> str:
    urlset = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
    )

    for entry in urls:
        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = entry["loc"]
        ET.SubElement(url_el, "lastmod").text = entry["lastmod"]
        ET.SubElement(url_el, "changefreq").text = entry["changefreq"]
        ET.SubElement(url_el, "priority").text = entry["priority"]

    ET.indent(urlset, space="  ")
    xml_body = ET.tostring(urlset, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body + "\n"


def main() -> int:
    site_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    if not site_root.is_dir():
        print(f"Error: site root not found: {site_root}", file=sys.stderr)
        return 1

    urls = collect_urls(site_root)
    output_path = site_root / "sitemap.xml"
    xml_content = build_xml(urls)
    output_path.write_text(xml_content, encoding="utf-8")

    print(f"Wrote {len(urls)} URLs to {output_path}")
    print(f"File size: {output_path.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
