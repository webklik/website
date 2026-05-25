#!/usr/bin/env python3
"""Architect Phase 1B — 9 binary validation checks."""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
ARCHIVE = ROOT / "assets_archive"
FOOD = ROOT / "images" / "food"
INDEX = ROOT / "index.html"
LOG = ROOT.parent / "debug-4d29ee.log"

LEGACY_10 = [
    "Beef Brocolli.webp", "Beef Mushroom.webp", "Chicken Baby Corn Broco.webp",
    "Chicken Cashewnuts.webp", "COMBO.webp", "Lamb in Schezuan Sauce.webp",
    "Lolli Kid.webp", "Shangai Lemon Prawns.webp", "Soups.webp", "Tofu in Black Bean Sauce.webp",
]


def log(msg, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "architect-1b",
        "hypothesisId": "ARCHITECT",
        "location": "validate_architect_1b.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def check1():
    jpegs = [p for p in ARCHIVE.iterdir() if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg")]
    return {
        "pass": ARCHIVE.is_dir() and len(jpegs) == 38,
        "archive_exists": ARCHIVE.is_dir(),
        "jpeg_count": len(jpegs),
        "files": sorted(p.name for p in jpegs),
    }


def check2():
    on_disk = {p.name for p in FOOD.glob("*.webp")}
    remaining = [f for f in LEGACY_10 if f in on_disk]
    return {
        "pass": len(remaining) == 0,
        "remaining": remaining,
        "on_disk_legacy_check": sorted(on_disk & set(LEGACY_10)),
    }


def check3():
    on_disk = {p.name for p in FOOD.glob("*.webp")}
    return {
        "pass": "soups.webp" in on_disk and "Soups.webp" not in on_disk,
        "soups_exists": "soups.webp" in on_disk,
        "capital_variant_in_listing": "Soups.webp" in on_disk,
    }


def css_checks():
    css = INDEX.read_text(encoding="utf-8")
    base_grid = re.search(r"\.dish-grid\s*\{([^}]+)\}", css, re.S)
    base_body = base_grid.group(1) if base_grid else ""
    desktop = re.search(r"@media\s*\(min-width:\s*960px\)\s*\{[^}]*\.dish-grid\s*\{([^}]+)\}", css, re.S)
    desktop_body = desktop.group(1) if desktop else ""

    return {
        "4_mobile_1col_24px": {
            "pass": "grid-template-columns: 1fr" in base_body and "gap: 24px" in base_body,
            "base_grid_snippet": base_body.strip()[:200],
        },
        "5_desktop_40px": {
            "pass": "gap: 40px" in desktop_body,
            "desktop_snippet": desktop_body.strip(),
        },
        "6_border_0_2": {
            "pass": bool(re.search(r"\.dish-card\s*\{[^}]*border:\s*1px\s+solid\s+rgba\(212,\s*175,\s*55,\s*0\.2\)", css, re.S)),
        },
        "7_dish_name_rest": {
            "pass": bool(re.search(r"\.dish-name\s*\{[^}]*opacity:\s*0[^}]*transition:\s*opacity\s+0\.3s\s+ease\s+0\.1s", css, re.S)),
        },
        "8_dish_name_hover": {
            "pass": bool(re.search(r"\.dish-card:hover\s+\.dish-name\s*\{\s*opacity:\s*1", css)),
        },
        "9_button_delays_unchanged": {
            "pass": "transition: opacity 0.3s ease 0.1s" in css
                    and "opacity 0.3s ease 0.15s" in css,
            "ql_delay": "transition: opacity 0.3s ease 0.1s" in css,
            "order_delay": "opacity 0.3s ease 0.15s" in css,
        },
        "hover_chain": {
            "gold_bar": ".dish-card::before" in css and ".dish-card:hover::before { width: 100%; }" in css,
            "border_hover": bool(re.search(r"\.dish-card:hover\s*\{[^}]*border-color:\s*#d4af37", css)),
        },
    }


def main():
    results = {
        "1_archive_38_jpegs": check1(),
        "2_legacy_webps_absent": check2(),
        "3_soups_lowercase": check3(),
    }
    css = css_checks()
    results.update({
        "4_mobile_1col_24px": css["4_mobile_1col_24px"],
        "5_desktop_40px": css["5_desktop_40px"],
        "6_border_0_2": css["6_border_0_2"],
        "7_dish_name_rest": css["7_dish_name_rest"],
        "8_dish_name_hover": css["8_dish_name_hover"],
        "9_button_delays": css["9_button_delays_unchanged"],
        "_hover_chain_ok": css["hover_chain"],
    })

    passed = sum(1 for k, v in results.items() if not k.startswith("_") and v.get("pass"))
    summary = {"passed": passed, "total": 9, "all_pass": passed == 9}
    log("architect 1b validation", {"results": results, "summary": summary})

    print("ARCHITECT PHASE 1B — VALIDATION CHECKLIST")
    print("=" * 50)
    labels = [
        ("1_archive_38_jpegs", "assets_archive/ exists with 38 JPEGs"),
        ("2_legacy_webps_absent", "10 legacy Pascal/space WebPs absent"),
        ("3_soups_lowercase", "soups.webp lowercase on disk"),
        ("4_mobile_1col_24px", "Mobile grid 1fr / 24px gap"),
        ("5_desktop_40px", "Desktop gap 40px"),
        ("6_border_0_2", "Default border rgba(212,175,55,0.2)"),
        ("7_dish_name_rest", ".dish-name opacity:0 + delay 0.1s"),
        ("8_dish_name_hover", ".dish-card:hover .dish-name opacity:1"),
        ("9_button_delays", "Quick Look 0.1s / Order 0.15s unchanged"),
    ]
    for key, label in labels:
        v = results[key]
        status = "PASS" if v.get("pass") else "FAIL"
        print(f"[{status}] #{label.split('_')[0]} {label}")
        for ek, ev in v.items():
            if ek != "pass":
                print(f"       {ek}: {ev}")
    print("=" * 50)
    print(f"SCORE: {passed}/9")
    print(f"Logged to {LOG}")


if __name__ == "__main__":
    main()
