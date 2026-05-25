#!/usr/bin/env python3
"""Find which images/food webps are referenced vs orphaned."""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
FOOD = ROOT / "images" / "food"
LOG = ROOT.parent / "debug-4d29ee.log"
SCAN_EXT = {".html", ".js", ".json", ".jsonld", ".xml", ".css", ".txt", ".py"}

LEGACY_SPACE_NAMES = [
    "Beef Brocolli.webp",
    "Beef Mushroom.webp",
    "Chicken Baby Corn Broco.webp",
    "Chicken Cashewnuts.webp",
    "COMBO.webp",
    "Lamb in Schezuan Sauce.webp",
    "Lolli Kid.webp",
    "Shangai Lemon Prawns.webp",
    "Soups.webp",
    "Tofu in Black Bean Sauce.webp",
]


def log(msg, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "orphan-audit",
        "hypothesisId": "ORPHAN",
        "location": "audit_food_orphans.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def collect_refs():
    refs = {}  # filename -> [source files]
    pattern = re.compile(r"/images/food/([^\"'\s>)]+)")
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SCAN_EXT:
            continue
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in pattern.finditer(text):
            name = m.group(1).split("?")[0]
            refs.setdefault(name, set()).add(str(path.relative_to(ROOT)).replace("\\", "/"))
    return {k: sorted(v) for k, v in sorted(refs.items())}


def main():
    on_disk = sorted(p.name for p in FOOD.glob("*.webp"))
    refs = collect_refs()
    referenced = set(refs.keys())
    orphaned = [f for f in on_disk if f not in referenced]
    missing = [f for f in referenced if f not in on_disk]

    legacy_orphan = [f for f in LEGACY_SPACE_NAMES if f in on_disk and f not in referenced]
    legacy_linked = [f for f in LEGACY_SPACE_NAMES if f in referenced]

    dup_pairs = []
    mapping = {
        "Beef Brocolli.webp": "beef-brocolli.webp",
        "Beef Mushroom.webp": "beef-mushroom.webp",
        "Chicken Cashewnuts.webp": "chicken-cashewnuts.webp",
        "Lolli Kid.webp": "lollipop-kiddie.webp",
        "Shangai Lemon Prawns.webp": "shanghai-lemon-prawns.webp",
        "Soups.webp": "soups.webp",
        "Lamb in Schezuan Sauce.webp": "lamb-in-schezuan-sauce.webp",
        "Tofu in Black Bean Sauce.webp": "tofu-in-black-bean-sauce.webp",
        "COMBO.webp": "prawn-sizzler.webp",
    }
    for old, new in mapping.items():
        if old in on_disk and new in on_disk:
            dup_pairs.append({"legacy": old, "replacement": new, "legacy_linked": old in referenced, "replacement_linked": new in referenced})

    result = {
        "total_webp_on_disk": len(on_disk),
        "total_referenced": len(referenced),
        "orphaned_count": len(orphaned),
        "orphaned_files": orphaned,
        "legacy_space_orphan": legacy_orphan,
        "legacy_space_still_linked": legacy_linked,
        "duplicate_pairs": dup_pairs,
        "missing_from_disk": missing,
        "menu_photos_legacy_refs": [],
    }

    mp = ROOT / "assets" / "js" / "menu-photos.js"
    if mp.exists():
        mp_text = mp.read_text(encoding="utf-8")
        for old in re.findall(r'"([A-Za-z0-9_ ]+\.webp)"', mp_text):
            if "600" in old or " " in old or old[0].isupper():
                result["menu_photos_legacy_refs"].append(old)

    log("food folder orphan audit", result)

    print(f"On disk: {len(on_disk)} webp")
    print(f"Referenced: {len(referenced)} unique filenames")
    print(f"Orphaned (not linked): {len(orphaned)}")
    print("\nLegacy space/Pascal files ORPHAN (safe to archive):")
    for f in legacy_orphan:
        print(f"  - {f}")
    print("\nLegacy still linked (should migrate first):")
    for f in legacy_linked:
        print(f"  - {f} -> {refs.get(f, [])[:3]}")
    print("\nmenu-photos.js still uses legacy names:", len(result["menu_photos_legacy_refs"]))


if __name__ == "__main__":
    main()
