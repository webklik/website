#!/usr/bin/env python3
"""Validate gallery migration checklist against runtime evidence."""
import json
import re
import struct
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = Path(__file__).parent
FOOD = ROOT / "images" / "food"
ARCHIVE = ROOT / "assets_archive"
INDEX = ROOT / "index.html"
LOG = ROOT.parent / "debug-4d29ee.log"

CANONICAL_12 = [
    "soups.webp", "spring-rolls.webp", "golden-fried-prawns.webp",
    "chilli-garlic-paneer.webp", "lamb-ribs.webp", "lollipop-kiddie.webp",
    "salt-and-pepper-vegetable.webp", "beef-manchurian.webp", "veg-rice.webp",
    "chilli-garlic-noodles.webp", "sweet-sour-prawns.webp", "ginger-crab.webp",
]

LEGACY_SPACE = [
    "Beef Brocolli.webp", "Beef Mushroom.webp", "Chicken Baby Corn Broco.webp",
    "Chicken Cashewnuts.webp", "COMBO.webp", "Lamb in Schezuan Sauce.webp",
    "Lolli Kid.webp", "Shangai Lemon Prawns.webp", "Soups.webp", "Tofu in Black Bean Sauce.webp",
]


def log(msg, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "checklist-validation",
        "hypothesisId": "CHECKLIST",
        "location": "validate_checklist.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def kebab(s):
    return s == s.lower() and " " not in s and "_" not in s


def webp_quality_hint(path):
    """Read WebP VP8/VP8L quality byte when present (approximate)."""
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    if data[12:16] == b"VP8 ":
        # Lossy: quality at offset 20 in frame header (0-127 mapped)
        if len(data) > 30:
            q = data[27]
            return round(q * 100 / 127)
    return "lossless_or_unknown"


def inspect_webp(path):
    info = {"path": path.name, "exists": path.exists()}
    if not path.exists() or Image is None:
        return info
    with Image.open(path) as img:
        info["size"] = img.size
        info["mode"] = img.mode
        icc = img.info.get("icc_profile")
        info["srgb"] = icc is None or b"sRGB" in (icc or b"") or img.mode == "RGB"
        info["quality_hint"] = webp_quality_hint(path)
    info["600x600"] = info.get("size") == (600, 600)
    info["kebab"] = kebab(path.name.replace(".webp", ""))
    return info


def parse_css_checks():
    css = INDEX.read_text(encoding="utf-8")
    checks = {}

    # Gold bar
    checks["gold_bar_width_0"] = "width: 0" in css and ".dish-card::before" in css
    checks["gold_bar_hover_100"] = ".dish-card:hover::before { width: 100%; }" in css

    # Overlay stagger
    checks["ql_trigger_opacity_stagger_0_1s"] = bool(
        re.search(r"\.ql-trigger\s*\{[^}]*opacity:\s*0[^}]*transition:[^}]*0\.1s", css, re.S)
    )
    checks["ql_trigger_hover_opacity_1"] = bool(
        re.search(r"\.dish-card:hover\s+\.ql-trigger[^}]*opacity:\s*1", css)
    )
    checks["order_btn_stagger_0_15s"] = bool(
        re.search(r"\.dish-card-order\s*\{[^}]*opacity:\s*0\.8[^}]*0\.15s", css, re.S)
    )
    checks["dish_name_opacity_stagger"] = bool(
        re.search(r"\.dish-name\s*\{[^}]*opacity:\s*0", css)
    )

    # Border
    checks["border_default_rgba_0_2"] = "rgba(212, 175, 55, 0.2)" in css
    checks["border_default_rgba_0_15"] = "rgba(212, 175, 55, 0.15)" in css
    checks["border_hover_d4af37"] = bool(
        re.search(r"\.dish-card:hover\s*\{[^}]*border-color:\s*#d4af37", css)
    )

    # Grid gaps
    checks["desktop_4col"] = bool(re.search(r"min-width:\s*960px[^}]*repeat\(4,\s*1fr\)", css))
    checks["desktop_gap_40px"] = bool(re.search(r"min-width:\s*960px[^}]*gap:\s*40px", css))
    checks["desktop_gap_s4_16px"] = bool(re.search(r"min-width:\s*960px[^}]*gap:\s*var\(--s-4\)", css))
    checks["mobile_1col"] = bool(
        re.search(r"\.dish-grid\s*\{[^}]*grid-template-columns:\s*1fr[^;]*;", css, re.S)
        and not re.search(r"\.dish-grid\s*\{[^}]*repeat\(2", css, re.S)
    )
    checks["mobile_2col_default"] = bool(
        re.search(r"\.dish-grid\s*\{[^}]*repeat\(2,\s*1fr\)", css, re.S)
    )
    checks["mobile_gap_24px"] = bool(re.search(r"\.dish-grid\s*\{[^}]*gap:\s*var\(--s-5\)", css, re.S))
    checks["mobile_gap_12px"] = bool(re.search(r"\.dish-grid\s*\{[^}]*gap:\s*var\(--s-3\)", css, re.S))

    return checks


def main():
    # 1. Gallery 12 kebab-case on disk
    gallery_inspect = [inspect_webp(FOOD / name) for name in CANONICAL_12]
    missing = [n for n in CANONICAL_12 if not (FOOD / n).exists()]
    wrong_case = []
    for p in FOOD.glob("*.webp"):
        stem = p.stem
        if stem in [c.replace(".webp", "") for c in CANONICAL_12]:
            if p.name not in CANONICAL_12 and p.name.lower() == stem + ".webp":
                wrong_case.append({"expected": stem + ".webp", "actual": p.name})

    all_600 = all(i.get("600x600") for i in gallery_inspect if i.get("exists"))
    all_kebab = all(i.get("kebab") for i in gallery_inspect if i.get("exists"))
    all_srgb = all(i.get("srgb") for i in gallery_inspect if i.get("exists"))

    # 3. Archive
    archive_exists = ARCHIVE.is_dir()
    archive_jpegs = list(ARCHIVE.rglob("*.jp*")) if archive_exists else []
    source_jpegs = list((ROOT.parent / "old-working-files" / "Cleaned_Images").glob("*.jp*"))

    # 4. Legacy purge
    legacy_on_disk = [f for f in LEGACY_SPACE if (FOOD / f).exists()]
    legacy_600 = list(FOOD.glob("*600.webp"))

    css = parse_css_checks()

    # Homepage grid match
    html = INDEX.read_text(encoding="utf-8")
    grid_match = re.search(
        r'<div class="dish-grid"[^>]*>(.*?)</div>\s*\n\s*<section class="takeaway-banner"',
        html, re.S,
    )
    homepage_imgs = re.findall(r'data-ql-src="/images/food/([^"]+)"', grid_match.group(1) if grid_match else "")

    result = {
        "1_gallery_12_kebab": {
            "pass": len(missing) == 0 and all_kebab and len(wrong_case) == 0,
            "missing": missing,
            "wrong_case": wrong_case,
            "homepage_order_match": homepage_imgs == CANONICAL_12,
        },
        "2_image_specs": {
            "pass": all_600 and all_srgb,
            "all_600x600": all_600,
            "all_srgb": all_srgb,
            "samples": gallery_inspect[:3],
        },
        "3_jpegs_archived": {
            "pass": archive_exists and len(archive_jpegs) >= 12,
            "archive_dir_exists": archive_exists,
            "archived_jpeg_count": len(archive_jpegs),
            "source_jpeg_count": len(source_jpegs),
            "note": "JPEGs still in old-working-files/Cleaned_Images, not assets_archive/",
        },
        "4_old_webp_purged": {
            "pass": len(legacy_on_disk) == 0 and len(legacy_600) == 0,
            "legacy_space_files_remaining": legacy_on_disk,
            "legacy_600_remaining": [p.name for p in legacy_600],
        },
        "5_gold_bar_animation": {
            "pass": css["gold_bar_width_0"] and css["gold_bar_hover_100"],
            **{k: css[k] for k in ("gold_bar_width_0", "gold_bar_hover_100")},
        },
        "6_overlay_stagger": {
            "pass": css["ql_trigger_opacity_stagger_0_1s"] and css["ql_trigger_hover_opacity_1"]
                    and css["order_btn_stagger_0_15s"] and css["dish_name_opacity_stagger"],
            "ql_0_1s": css["ql_trigger_opacity_stagger_0_1s"],
            "order_0_15s": css["order_btn_stagger_0_15s"],
            "dish_name_fade": css["dish_name_opacity_stagger"],
        },
        "7_border_highlight": {
            "pass": css["border_default_rgba_0_2"] and css["border_hover_d4af37"],
            "has_0_2_default": css["border_default_rgba_0_2"],
            "has_0_15_default": css["border_default_rgba_0_15"],
            "hover_d4af37": css["border_hover_d4af37"],
        },
        "8_desktop_grid": {
            "pass": css["desktop_4col"] and css["desktop_gap_40px"],
            "4col": css["desktop_4col"],
            "gap_40px": css["desktop_gap_40px"],
            "gap_16px_actual": css["desktop_gap_s4_16px"],
        },
        "9_mobile_grid": {
            "pass": css["mobile_1col"] and css["mobile_gap_24px"],
            "1col": css["mobile_1col"],
            "2col_actual": css["mobile_2col_default"],
            "gap_24px": css["mobile_gap_24px"],
            "gap_12px_actual": css["mobile_gap_12px"],
        },
        "10_pagespeed_99": {
            "pass": False,
            "note": "Not run in this session — requires post-deploy Lighthouse audit",
        },
    }

    passed = sum(1 for k, v in result.items() if v.get("pass"))
    result["summary"] = {"passed": passed, "total": 10, "score": f"{passed}/10"}

    log("checklist validation complete", result)

    print("=" * 60)
    print("MISTER WOK GALLERY CHECKLIST VALIDATION")
    print("=" * 60)
    for key, val in result.items():
        if key == "summary":
            continue
        status = "PASS" if val.get("pass") else "FAIL"
        print(f"\n[{status}] {key}")
        for k, v in val.items():
            if k != "pass":
                print(f"  {k}: {v}")
    print(f"\n{'=' * 60}")
    print(f"SCORE: {result['summary']['score']}")
    print(f"Logged to {LOG}")


if __name__ == "__main__":
    main()
