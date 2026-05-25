#!/usr/bin/env python3
"""Phase 1C — migrate menu photo refs from legacy *600.webp to kebab-case."""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
FOOD = ROOT / "images" / "food"
ARCHIVE = ROOT / "assets_archive"
LOG = ROOT.parent / "debug-4d29ee.log"

LEGACY_TO_KEBAB = {
    "Soup_Index_Menu_2048x2048600.webp": "soups.webp",
    "Salt_and_Pepper_Vegetable600.webp": "salt-and-pepper-vegetable.webp",
    "Chilli_Garlic_Paneer600.webp": "chilli-garlic-paneer.webp",
    "Rolls_for_Index600.webp": "vegetable-springrolls.webp",
    "Spring_Rolls600.webp": "spring-rolls.webp",
    "Chicken_Wings600.webp": "chicken-wings.webp",
    "Lolli_Kid600.webp": "lollipop-kiddie.webp",
    "Beef_Manchurian600.webp": "beef-manchurian.webp",
    "Beef_Strips600.webp": "beef-strips.webp",
    "Lamb_Ribs600.webp": "lamb-ribs.webp",
    "Shangai_Lemon_Prawns600.webp": "shanghai-lemon-prawns.webp",
    "Golden_Fried_Prawns600.webp": "golden-fried-prawns.webp",
    "Chilli_Fish600.webp": "chilli-fish.webp",
    "Dim_Sum600.webp": "dim-sum-main-index.webp",
    "Dumplings600.webp": "dumplings.webp",
    "Chicken_Cashewnuts600.webp": "chicken-cashewnuts.webp",
    "Chicken_Baby_Corn_Broco600.webp": "shanghai-veg-tofu-mushroom-brocolli.webp",
    "Sweet_Sour_Prawns600.webp": "sweet-sour-prawns.webp",
    "Sizzler600.webp": "veg-sizzler.webp",
    "Beef_Mushroom600.webp": "beef-mushroom.webp",
    "Beef_Brocolli600.webp": "beef-brocolli.webp",
    "Beef_Noodles600.webp": "noodles-beef.webp",
    "Dry_Chilli_Beef600.webp": "beef-strips.webp",
    "Lamb_in_Schezuan_Sauce600.webp": "lamb-in-schezuan-sauce.webp",
    "Fish600.webp": "chilli-fish.webp",
    "Fish_In_Garlic600.webp": "fish-in-garlic.webp",
    "Tofu_in_Black_Bean_Sauce600.webp": "tofu-in-black-bean-sauce.webp",
    "Schezuan_Paneer600.webp": "chilli-garlic-paneer.webp",
    "Veg_Fried_Rice600.webp": "veg-rice.webp",
    "Chilli_Garlic_Noodles600.webp": "chilli-garlic-noodles.webp",
    "Lifestyle_Wrap600.webp": "shanghai-veg-withcashew.webp",
    "Kiddie_Menu600.webp": "lollipop-kiddie.webp",
    "Soups600.webp": "soups.webp",
    "Rice_Noodles600.webp": "wok-toss-rice.webp",
    "COMBO600.webp": "prawn-sizzler.webp",
    "Takeaway600.webp": "takeaway.webp",
    "Slider_Toss600.webp": "wok-toss-rice.webp",
    "Healthy_Wrap600.webp": "shanghai-veg-withcashew.webp",
}

SCAN_EXT = {".html", ".js", ".json", ".jsonld"}
SKIP_DIRS = {".git", "assets_archive", "old-working-files"}


def log(msg, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "phase-1c",
        "hypothesisId": "PHOTO_MIGRATE",
        "location": "migrate_menu_photos.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def patch_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in LEGACY_TO_KEBAB.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return sum(original.count(old) for old in LEGACY_TO_KEBAB)
    return 0


def main():
    patched = []
    total_replacements = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SCAN_EXT:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith("_frag"):
            continue
        count = patch_file(path)
        if count:
            patched.append({"file": str(path.relative_to(ROOT)), "replacements": count})
            total_replacements += count

    # Verify no *600.webp refs remain in production files
    remaining = []
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SCAN_EXT:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in ("migrate_menu_photos.py", "validate_checklist.py", "convert-location-images.py"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hits = re.findall(r"[\w_]+600\.webp", text)
        if hits:
            remaining.append({"file": str(path.relative_to(ROOT)), "hits": sorted(set(hits))})

    # Verify menu-photos targets exist on disk
    mp = ROOT / "assets" / "js" / "menu-photos.js"
    mp_text = mp.read_text(encoding="utf-8")
    targets = re.findall(r'"([^"]+\.webp)"', mp_text)
    on_disk = {p.name for p in FOOD.glob("*.webp")}
    missing_targets = sorted(set(t for t in targets if t not in on_disk))

    result = {
        "files_patched": patched,
        "total_replacements": total_replacements,
        "remaining_600_refs": remaining,
        "menu_photos_missing_targets": missing_targets,
        "pass": len(remaining) == 0 and len(missing_targets) == 0,
    }
    log("phase 1c migration complete", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
