#!/usr/bin/env python3
"""MW-SPRINT-08 post-sprint encoding sweep. Run from Mister_Wok_MNFVSS/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# R1 — U+FFFD replacements in 404.html and videos.html
R1_REPLACEMENTS = {
    "Kolobot Rd \ufffd 4.3\ufffd \ufffd 11am \ufffd 11pm": "Kolobot Rd · 4.3★ · 11am – 11pm",
    "Mombasa Rd, South B \ufffd 4.2\ufffd \ufffd 11am \ufffd 9:30pm": "Mombasa Rd, South B · 4.2★ · 11am – 9:30pm",
    "Limuru Rd, Gigiri \ufffd 4.1\ufffd \ufffd 11am \ufffd 9pm": "Limuru Rd, Gigiri · 4.1★ · 11am – 9pm",
    "Handcrafted \ufffd Since 2004": "Handcrafted · Since 2004",
    "Press \ufffd Reviews": "Press · Reviews",
    "Corporate \ufffd Private": "Corporate · Private",
    'aria-hidden="true">\ufffd</span>': 'aria-hidden="true">›</span>',
    "The Wok Journal \ufffd featured articles": "The Wok Journal · featured articles",
    "Wok Hei Physics \ufffd 300\ufffdC": "Wok Hei Physics · 300°C",
    "Halal-Assured \ufffd 22 Years": "Halal-Assured · 22 Years",
    "NTV AM Live \ufffd 2014": "NTV AM Live · 2014",
    "\ufffd 2004\ufffd2026 Mister Wok": "© 2004–2026 Mister Wok",
    "Catering</a>\n         \ufffd \n": "Catering</a>\n         · \n",
    "Journal</a>\n         \ufffd \n": "Journal</a>\n         · \n",
    "404 \ufffd Page Not Found": "404 · Page Not Found",
    "Page not found \ufffd return": "Page not found — return",
    "Mister Wok in Action \ufffd Video Proof": "Mister Wok in Action — Video Proof",
    "mister-wok-nairobi.webp \ufffd upload": "mister-wok-nairobi.webp — upload",
    # modal-opt-meta mixed U+FFFD + literal ? (post-partial-fix state)
    "Kolobot Rd \ufffd 4.3? \ufffd 11am \ufffd 11pm": "Kolobot Rd · 4.3★ · 11am – 11pm",
    "Mombasa Rd, South B \ufffd 4.2? \ufffd 11am \ufffd 9:30pm": "Mombasa Rd, South B · 4.2★ · 11am – 9:30pm",
    "Limuru Rd, Gigiri \ufffd 4.1? \ufffd 11am \ufffd 9pm": "Limuru Rd, Gigiri · 4.1★ · 11am – 9pm",
    "? Halal-Assured": "✓ Halal-Assured",
    "Explore the full Journal ?": "Explore the full Journal →",
}


def fix_r1() -> None:
    for fname in ("404.html", "videos.html"):
        path = ROOT / fname
        content = path.read_text(encoding="utf-8", errors="replace")
        for bad, good in R1_REPLACEMENTS.items():
            content = content.replace(bad, good)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"R1 {fname}: remaining U+FFFD = {content.count(chr(0xFFFD))}")


def fix_r6() -> None:
    fixes = {
        "journal/halal-wok-nairobi.html": [
            (b"\xc3\xb0\xc5\xb8\xc2\x8d\xc5\x93", "🍜".encode("utf-8")),
        ],
        "journal/wok-hei-physics.html": [
            (b"\xc3\xb0\xc5\xb8\xc2\x8d\xc5\x93", "🍜".encode("utf-8")),
        ],
        "journal/birthday-catering-guide.html": [
            (b"\xc3\xa2\xc5\x93\xe2\x80\xb0", "✉".encode("utf-8")),
            (b"\xc3\xb0\xc5\xb8\xc2\x8d\xc5\x93", "🍜".encode("utf-8")),
        ],
    }
    for rel, replacements in fixes.items():
        path = ROOT / rel
        data = path.read_bytes()
        for bad_bytes, good_bytes in replacements:
            count = data.count(bad_bytes)
            data = data.replace(bad_bytes, good_bytes)
            print(f"R6 {rel}: replaced {count}x corrupted sequence")
        path.write_bytes(data)


def fix_0x9d_index() -> None:
    script = ROOT / "fix_0x9d_encoding.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT)


def scan_fffd() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if "_includes" in path.parts or "old-" in str(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        n = text.count("\ufffd")
        if n:
            print(f"WARN {path.relative_to(ROOT)}: {n} U+FFFD remaining")


def main() -> None:
    fix_r1()
    fix_r6()
    fix_0x9d_index()
    scan_fffd()
    print("MW-FIX-ENCODING.py complete.")


if __name__ == "__main__":
    main()
