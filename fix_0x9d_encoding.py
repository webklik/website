#!/usr/bin/env python3
"""One-shot fix for corrupted 0x9D / U+009D bytes in production HTML. Dev only — excluded from deploy."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEP = "\x9d"  # raw byte / U+009D control char used as corrupted punctuation


def fix_text(text: str) -> str:
    if SEP not in text:
        return text

    # Degree sign before C (300°C)
    text = re.sub(rf"(\d){SEP}C", r"\1°C", text)

    # En-dash between digits (prices, year ranges)
    text = re.sub(rf"(\d[\d,]*){SEP}(\d[\d,]*)", r"\1–\2", text)

    # Copyright lead-in
    text = text.replace(f"{SEP} 2004", "© 2004")

    # Em-dash in titles and headings
    for old, new in (
        ("404 " + SEP + " Page", "404 — Page"),
        ("Page not found " + SEP + " return", "Page not found — return"),
        ("Mister Wok in Action " + SEP + " Video", "Mister Wok in Action — Video"),
        ("Mister Wok Nairobi " + SEP + " Halal", "Mister Wok Nairobi — Halal"),
        ("SCHEMA.ORG " + SEP + " RESTAURANT", "SCHEMA.ORG — RESTAURANT"),
        ("Mister Wok Parklands " + SEP + " premium", "Mister Wok Parklands — premium"),
        ("Mister Wok Capital Centre " + SEP + " Halal", "Mister Wok Capital Centre — Halal"),
        ("Mister Wok Two Rivers " + SEP + " curated", "Mister Wok Two Rivers — curated"),
        ("The Wok Journal " + SEP + " featured", "The Wok Journal — featured"),
        ("Wok Hei Physics " + SEP + " 300", "Wok Hei Physics — 300"),
        ("Halal-Assured " + SEP + " 22", "Halal-Assured — 22"),
        ("NTV AM Live " + SEP + " 2014", "NTV AM Live — 2014"),
        ("upload before launch", "upload before launch"),  # anchor for nearby fix below
    ):
        text = text.replace(old, new)

    # Dish / schema item subtitles (em dash)
    text = re.sub(
        rf"([A-Za-z&]+){SEP} (Whole Fish|Bone-In Bites|300°C Seared|Wok-Tossed|Wok-Fired)",
        r"\1 — \2",
        text,
    )
    text = re.sub(
        rf"([A-Za-z ]+){SEP} (Whole Fish|Bone-In|Wok-Tossed)",
        r"\1 — \2",
        text,
    )

    # Nav dropdown sub-labels use slash (matches catering.html / site-nav convention)
    text = re.sub(rf"(<span>[^<]*?){SEP} ", r"\1 / ", text)

    # Brand tag and similar middle-dot separators
    text = text.replace(f"Handcrafted {SEP} Since", "Handcrafted · Since")
    text = text.replace(f"Mister Wok {SEP} Nairobi", "Mister Wok · Nairobi")

    # Title / location chains (homepage meta)
    text = re.sub(
        rf"(Cuisine|Parklands|Capital Centre|Two Rivers|Since 2004){SEP} ",
        r"\1 · ",
        text,
    )
    text = re.sub(rf" {SEP} (Parklands|Capital Centre|Two Rivers|Since 2004)", r" · \1", text)
    text = re.sub(rf"Wok Cuisine{SEP} ", "Wok Cuisine · ", text)

    # Stat counters in schema comment block
    text = re.sub(rf"(\d[\d,]+) {SEP} (Capital Centre|Two Rivers)", r"\1 · \2", text)

    # Footer pipe separators
    text = text.replace(f"&nbsp;{SEP}&nbsp;", " · ")

    # Remaining corrupted separators default to middle dot
    text = text.replace(SEP, "·")

    return text


def fix_index_html(path: Path) -> None:
    raw = path.read_bytes()
    try:
        raw.decode("utf-8")
        return
    except UnicodeDecodeError:
        pass
    text = raw.decode("latin-1")
    fixed = fix_text(text)
    path.write_text(fixed, encoding="utf-8")


def fix_utf8_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    fixed = fix_text(text)
    path.write_text(fixed, encoding="utf-8")


def fix_menu_comment(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    new = text.replace("\u201cchin\u201d", '"chin"')
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\r\n")


def main() -> None:
    fix_index_html(ROOT / "index.html")
    for name in ("404.html", "videos.html"):
        fix_utf8_html(ROOT / name)
    for name in ("parklands/menu.html", "capital-centre/menu.html"):
        fix_menu_comment(ROOT / name)

    # Verify
    for rel in (
        "index.html",
        "404.html",
        "videos.html",
        "parklands/menu.html",
        "capital-centre/menu.html",
    ):
        data = (ROOT / rel).read_bytes()
        bad = sum(
            1
            for i, b in enumerate(data)
            if b == 0x9D
            and not (i >= 2 and data[i - 2 : i + 1] == bytes([0xE2, 0x80, 0x9D]))
        )
        try:
            data.decode("utf-8")
            valid = "valid UTF-8"
        except UnicodeDecodeError as exc:
            valid = f"INVALID at {exc.start}"
        print(f"{rel}: raw 0x9D={bad}, {valid}")


if __name__ == "__main__":
    main()
