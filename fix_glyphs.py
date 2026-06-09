#!/usr/bin/env python3
"""Fix corrupted glyph characters — use ASCII-safe CSS escapes and SVG sprites."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DRAWER_CHEVRON_CSS = """.drawer-accordion summary::after {
  content: '';
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid currentColor;
  margin-left: 6px;
  vertical-align: middle;
  opacity: 0.6;
  transition: transform 0.2s ease;
}"""

ACCORDION_CHEVRON_CSS = """.accordion-trigger::after {
  content: '\\25BE';
  font-size: 0.95rem;
  line-height: 1;
  color: var(--color-gold, #d4af37);
  background: rgba(212, 175, 55, 0.10);
  border: 1px solid rgba(212, 175, 55, 0.35);
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: transform 280ms cubic-bezier(0.16, 1, 0.3, 1),
              background var(--t-fast, 150ms),
              border-color var(--t-fast, 150ms);
  flex-shrink: 0;
}"""

ITEM_THUMB_CSS = """.item-thumb::after {
  content: '+';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  font-weight: 300;
  line-height: 1;
  color: var(--color-gold, #d4af37);
  background: rgba(10, 10, 10, 0.55);
  opacity: 0;
  transition: opacity var(--t-fast, 150ms);
}"""

SVG_CLOSE = '<svg width="16" height="16" aria-hidden="true"><use href="#ico-close"/></svg>'
SVG_ARROW = '<svg width="16" height="16" aria-hidden="true"><use href="#ico-arrow-right"/></svg>'


def replace_css_block(text: str, selector: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(selector) + r"\s*\{[^}]*\}",
        re.DOTALL,
    )
    if not pattern.search(text):
        return text
    return pattern.sub(lambda _m: new_block, text, count=1)


def fix_menu_css(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_css_block(text, ".drawer-accordion summary::after", DRAWER_CHEVRON_CSS)
    text = replace_css_block(text, ".accordion-trigger::after", ACCORDION_CHEVRON_CSS)
    text = replace_css_block(text, ".item-thumb::after", ITEM_THUMB_CSS)
    path.write_text(text, encoding="utf-8", newline="\n")


def fix_two_rivers_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # Drawer / nav shell (match parklands structure, two-rivers branch URLs)
    drawer_old = re.search(
        r'<div class="drawer" id="drawer".*?</div>\s*</div>\s*<div aria-hidden="true".*?</div>\s*</div>',
        text,
        re.DOTALL,
    )
    if drawer_old:
        drawer_new = """<div class="drawer" id="drawer" role="dialog" aria-label="Navigation menu" aria-hidden="true">
  <nav class="drawer-nav" aria-label="Site pages">
    <a href="/locations/" class="drawer-nav-row">LOCATIONS</a>
    <details class="drawer-accordion">
      <summary>Branch Pages</summary>
      <div class="drawer-accordion-panel">
        <a href="/parklands/">Parklands <span>Kolobot Rd</span></a>
        <a href="/capital-centre/">Capital Centre <span>Halal-assured</span></a>
        <a href="/two-rivers/">Two Rivers <span>Gigiri</span></a>
      </div>
    </details>
    <details class="drawer-accordion">
      <summary>MENU</summary>
      <div class="drawer-accordion-panel">
        <a href="/parklands/menu.html">Parklands Menu</a>
        <a href="/capital-centre/menu.html">Capital Centre Menu</a>
        <a href="/two-rivers/menu.html" aria-current="page">Two Rivers Menu</a>
      </div>
    </details>
    <details class="drawer-accordion">
      <summary>RESERVE</summary>
      <div class="drawer-accordion-panel">
        <a href="https://www.foodbooking.com/api/res/67_y_m" target="_blank" rel="noopener">Parklands <span aria-hidden="true">&rsaquo;</span></a>
        <a href="https://www.foodbooking.com/api/res/d_yq_g" target="_blank" rel="noopener">Capital Centre <span aria-hidden="true">&rsaquo;</span></a>
        <a href="https://www.foodbooking.com/api/res/k8_d_z" target="_blank" rel="noopener">Two Rivers <span aria-hidden="true">&rsaquo;</span></a>
      </div>
    </details>
    <div class="drawer-order-row">
      <a class="drawer-order-btn" href="https://www.foodbooking.com/api/fb/k8_d_z" target="_blank" rel="noopener" data-cta="direct" data-order-btn="true" aria-label="Order from Two Rivers">
        <span class="cta-flame mw-flame" aria-hidden="true"><svg width="16" height="16" style="vertical-align:-2px"><use href="#ico-flame"/></svg></span> Order Now
      </a>
    </div>
    <details class="drawer-accordion">
      <summary>DISCOVER</summary>
      <div class="drawer-accordion-panel">
        <a href="/journal/">The Journal <span>Stories from the kitchen</span></a>
        <a href="/social-proof.html">As Seen On <span>Kula Cooler / Press / Reviews</span></a>
        <a href="/catering.html">Catering <span>Events / Corporate / Private</span></a>
      </div>
    </details>
  </nav>
</div>

<div aria-hidden="true" aria-labelledby="modal-title" aria-modal="true" id="modal" role="dialog">
<div class="modal-inner">
<div aria-hidden="true" class="modal-handle"></div>
<button aria-label="Close branch selection" class="modal-close" id="modal-close" type="button">""" + SVG_CLOSE + """</button>
<h2 class="modal-title" id="modal-title">Choose Your Branch</h2>
<p class="modal-sub">Delivery radius varies by branch. Pick the one nearest you.</p>
<div class="modal-options" role="list">
<a aria-label="Order from Mister Wok Parklands" class="modal-opt" data-branch="Parklands" data-branch-hours="11am-11pm" data-branch-location="Kolobot Road, Parklands" data-branch-phone="+254724100100" data-branch-rating="4.3" data-branch-slug="parklands" data-cta="direct" data-order-btn="true" data-order-url="https://www.foodbooking.com/api/fb/67_y_m" data-reserve-url="https://www.foodbooking.com/api/res/67_y_m" href="https://www.foodbooking.com/api/fb/67_y_m" rel="noopener" role="listitem" target="_blank">
<div>
<div class="modal-opt-name">Parklands</div>
<div class="modal-opt-meta">Kolobot Rd &middot; 4.3&starf; &middot; 11am &ndash; 11pm</div>
</div>
<span aria-hidden="true" class="modal-opt-arrow">""" + SVG_ARROW + """</span>
</a>
<a aria-label="Order from Mister Wok Capital Centre" class="modal-opt" data-branch="Capital Centre" data-branch-hours="11am-9:30pm" data-branch-location="Capital Centre Mall, Mombasa Road, South B" data-branch-phone="+254722248248" data-branch-rating="4.2" data-branch-slug="capital-centre" data-cta="direct" data-order-btn="true" data-order-url="https://www.foodbooking.com/api/fb/d_yq_g" data-reserve-url="https://www.foodbooking.com/api/res/d_yq_g" href="https://www.foodbooking.com/api/fb/d_yq_g" rel="noopener" role="listitem" target="_blank">
<div>
<div class="modal-opt-name">Capital Centre</div>
<div class="modal-opt-meta">Mombasa Rd, South B &middot; 4.2&starf; &middot; 11am &ndash; 9:30pm</div>
</div>
<span aria-hidden="true" class="modal-opt-arrow">""" + SVG_ARROW + """</span>
</a>
<a aria-label="Order from Mister Wok Two Rivers" class="modal-opt" data-branch="Two Rivers" data-branch-hours="11am-9pm" data-branch-location="Two Rivers Mall, Limuru Road, Gigiri" data-branch-phone="+254753222222" data-branch-rating="4.1" data-branch-slug="two-rivers" data-cta="direct" data-order-btn="true" data-order-url="https://www.foodbooking.com/api/fb/k8_d_z" data-reserve-url="https://www.foodbooking.com/api/res/k8_d_z" href="https://www.foodbooking.com/api/fb/k8_d_z" rel="noopener" role="listitem" target="_blank">
<div>
<div class="modal-opt-name">Two Rivers</div>
<div class="modal-opt-meta">Limuru Rd, Gigiri &middot; 4.1&starf; &middot; 11am &ndash; 9pm</div>
</div>
<span aria-hidden="true" class="modal-opt-arrow">""" + SVG_ARROW + """</span>
</a>
</div>

</div>
</div>"""
        text = text[: drawer_old.start()] + drawer_new + text[drawer_old.end() :]

    # Breadcrumb + header block
    text = re.sub(
        r'<nav aria-label="Breadcrumb" class="breadcrumb">.*?</nav>\s*<h1 class="menu-page-title">.*?</h1>\s*<p class="menu-page-sub">.*?</p>\s*<div class="branch-identity">.*?</div>',
        """<nav aria-label="Breadcrumb" class="breadcrumb">
<a class="bc-link" href="/">Home</a>
<span aria-hidden="true" class="bc-sep">&rsaquo;</span>
<a class="bc-link" href="/two-rivers/">Two Rivers</a>
<span aria-hidden="true" class="bc-sep">&rsaquo;</span>
<span aria-current="page" class="bc-current">Menu</span>
</nav>
<h1 class="menu-page-title">Mister Wok <em>Two Rivers</em><br/>Full Menu 2026</h1>
<p class="menu-page-sub">145 dishes &middot; Hand-cut noodles &middot; premium aromatic rice &middot; Made-to-order at 300&deg;C</p>
<div class="branch-identity">
<span class="branch-pill">Two Rivers Mall &middot; Limuru Road, Gigiri</span>
<span class="branch-hours">Open daily 11:00 AM &ndash; 9:00 PM</span>
</div>""",
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Lightbox close
    text = text.replace(
        '<button aria-label="Close dish detail" class="lx-close" id="lx-close">?</button>',
        '<button aria-label="Close dish detail" class="lx-close" id="lx-close">&times;</button>',
    )

    # Body text: fix corrupted separators (avoid URLs)
    lines = []
    for line in text.splitlines(keepends=True):
        if "http" in line and "?" in line:
            lines.append(line)
            continue
        line = line.replace("?? ", "")
        line = re.sub(r"(\d)C\b", r"\1&deg;C", line) if "300" in line else line
        line = line.replace("300?C", "300&deg;C")
        line = re.sub(r"(\d\.\d)\?", r"\1&starf;", line)
        line = re.sub(r"\s\?\s", " &middot; ", line)
        line = re.sub(r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\s*\?\s*(\d)", r"\1 &ndash; \2", line)
        line = line.replace("&middot; &middot; ", "&middot; ")
        lines.append(line)
    text = "".join(lines)

    text = finish_two_rivers_pass(text)
    path.write_text(text, encoding="utf-8", newline="\n")


def finish_two_rivers_pass(text: str) -> str:
    pairs = [
        ('<a href="/locations/" class="drawer-nav-row">LOCATIONS <span aria-hidden="true"></span></a>',
         '<a href="/locations/" class="drawer-nav-row">LOCATIONS</a>'),
        ('<a href="https://www.foodbooking.com/api/res/67_y_m" target="_blank" rel="noopener">?? Parklands <span>?</span></a>',
         '<a href="https://www.foodbooking.com/api/res/67_y_m" target="_blank" rel="noopener">Parklands <span aria-hidden="true">&rsaquo;</span></a>'),
        ('<a href="https://www.foodbooking.com/api/res/d_yq_g" target="_blank" rel="noopener">?? Capital Centre <span>?</span></a>',
         '<a href="https://www.foodbooking.com/api/res/d_yq_g" target="_blank" rel="noopener">Capital Centre <span aria-hidden="true">&rsaquo;</span></a>'),
        ('<a href="https://www.foodbooking.com/api/res/k8_d_z" target="_blank" rel="noopener">?? Two Rivers <span>?</span></a>',
         '<a href="https://www.foodbooking.com/api/res/k8_d_z" target="_blank" rel="noopener">Two Rivers <span aria-hidden="true">&rsaquo;</span></a>'),
        ('<a href="/journal/">? The Journal <span>Stories from the kitchen</span></a>',
         '<a href="/journal/">The Journal <span>Stories from the kitchen</span></a>'),
        ('<a href="/social-proof.html">? As Seen On <span>Kula Cooler &middot; Press &middot; Reviews</span></a>',
         '<a href="/social-proof.html">As Seen On <span>Kula Cooler / Press / Reviews</span></a>'),
        ('<a href="/catering.html">? Catering <span>Events &middot; Corporate &middot; Private</span></a>',
         '<a href="/catering.html">Catering <span>Events / Corporate / Private</span></a>'),
        ('<button aria-label="Close branch selection" class="modal-close" id="modal-close" type="button">?</button>',
         f'<button aria-label="Close branch selection" class="modal-close" id="modal-close" type="button">{SVG_CLOSE}</button>'),
        ('<span aria-hidden="true" class="modal-opt-arrow">?</span>',
         f'<span aria-hidden="true" class="modal-opt-arrow">{SVG_ARROW}</span>'),
        ('<li role="menuitem"><a href="https://www.foodbooking.com/api/res/67_y_m" target="_blank" rel="noopener">?? Parklands <span>Reserve a table</span></a></li>',
         '<li role="menuitem"><a href="https://www.foodbooking.com/api/res/67_y_m" target="_blank" rel="noopener">Parklands <span>Reserve a table</span></a></li>'),
        ('<li role="menuitem"><a href="https://www.foodbooking.com/api/res/d_yq_g" target="_blank" rel="noopener">?? Capital Centre <span>Reserve ? Halal-assured</span></a></li>',
         '<li role="menuitem"><a href="https://www.foodbooking.com/api/res/d_yq_g" target="_blank" rel="noopener">Capital Centre <span>Reserve / Halal-assured</span></a></li>'),
        ('<li role="menuitem"><a href="https://www.foodbooking.com/api/res/k8_d_z" target="_blank" rel="noopener">?? Two Rivers <span>Reserve a table</span></a></li>',
         '<li role="menuitem"><a href="https://www.foodbooking.com/api/res/k8_d_z" target="_blank" rel="noopener">Two Rivers <span>Reserve a table</span></a></li>'),
        ('<li role="menuitem"><a href="/journal/">? The Journal <span>Stories from the kitchen</span></a></li>',
         '<li role="menuitem"><a href="/journal/">The Journal <span>Stories from the kitchen</span></a></li>'),
        ('<li role="menuitem"><a href="/social-proof.html">? As Seen On <span>Kula Cooler &middot; Press &middot; Reviews</span></a></li>',
         '<li role="menuitem"><a href="/social-proof.html">As Seen On <span>Kula Cooler / Press / Reviews</span></a></li>'),
        ('<li role="menuitem"><a href="/catering.html">? Catering <span>Events &middot; Corporate &middot; Private</span></a></li>',
         '<li role="menuitem"><a href="/catering.html">Catering <span>Events / Corporate / Private</span></a></li>'),
        ('11am &middot; 11pm', '11am &ndash; 11pm'),
        ('11am &middot; 9:30pm', '11am &ndash; 9:30pm'),
        ('11am &middot; 9pm', '11am &ndash; 9pm'),
        ('Saut?ed', 'Saut&eacute;ed'),
        ('saut?ed', 'saut&eacute;ed'),
        ('yu?nbao', 'yuanbao'),
        ('? Showpiece', 'Showpiece'),
        ('Order Takeaway ?', 'Order Takeaway &rarr;'),
        ('Order This Dish ?', 'Order This Dish &rarr;'),
        ('Explore the full Journal ?', 'Explore the full Journal &rarr;'),
        ('/* Mobile / tablet: reserve space for sticky bottom ?chin? */',
         '/* Mobile / tablet: reserve space for sticky bottom chin */'),
        ('/* --- CANONICAL CHIN NAV SPECIFICATIONS (?2A) --- */',
         '/* --- CANONICAL CHIN NAV SPECIFICATIONS (2A) --- */'),
    ]
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def fix_simple_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<button class="modal-close" id="modal-close" type="button" aria-label="Close branch selection">?</button>',
        f'<button class="modal-close" id="modal-close" type="button" aria-label="Close branch selection">{SVG_CLOSE}</button>',
    )
    text = text.replace(
        '<button class="modal-close" id="modal-close" type="button" aria-label="Close branch selection">?</button>',
        f'<button class="modal-close" id="modal-close" type="button" aria-label="Close branch selection">{SVG_CLOSE}</button>',
    )
    text = re.sub(
        r'<span class="modal-opt-arrow" aria-hidden="true">\?</span>',
        f'<span class="modal-opt-arrow" aria-hidden="true">{SVG_ARROW}</span>',
        text,
    )
    text = re.sub(
        r'<span aria-hidden="true" class="modal-opt-arrow">\?</span>',
        f'<span aria-hidden="true" class="modal-opt-arrow">{SVG_ARROW}</span>',
        text,
    )
    text = text.replace("?? Parklands", "Parklands")
    text = text.replace("?? Capital Centre", "Capital Centre")
    text = text.replace("?? Two Rivers", "Two Rivers")
    text = text.replace("?? Menu", "MENU")
    text = text.replace("?? Reserve", "RESERVE")
    text = re.sub(
        r'<span>\?</span>',
        '<span aria-hidden="true">&rsaquo;</span>',
        text,
    )
    text = text.replace(
        '<button class="ql-close" id="ql-close" aria-label="Close quick look" type="button">?</button>',
        f'<button class="ql-close" id="ql-close" aria-label="Close quick look" type="button">{SVG_CLOSE}</button>',
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for menu in ("parklands/menu.html", "capital-centre/menu.html", "two-rivers/menu.html"):
        fix_menu_css(ROOT / menu)
    fix_two_rivers_html(ROOT / "two-rivers/menu.html")
    for page in ("404.html", "videos.html", "index.html"):
        fix_simple_html(ROOT / page)
    print("Done. Re-run scan_glyphs.py to verify.")


if __name__ == "__main__":
    main()
