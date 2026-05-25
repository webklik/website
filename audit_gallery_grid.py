#!/usr/bin/env python3
"""Audit homepage dish grid vs canonical 12 gallery batch."""
import json
import re
import time
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "debug-4d29ee.log"
INDEX = Path(__file__).parent / "index.html"
FOOD = Path(__file__).parent / "images" / "food"

CANONICAL_12 = [
    "soups.webp",
    "spring-rolls.webp",
    "golden-fried-prawns.webp",
    "chilli-garlic-paneer.webp",
    "lamb-ribs.webp",
    "lollipop-kiddie.webp",
    "salt-and-pepper-vegetable.webp",
    "beef-manchurian.webp",
    "veg-rice.webp",
    "chilli-garlic-noodles.webp",
    "sweet-sour-prawns.webp",
    "ginger-crab.webp",
]


def log(hypothesis_id, message, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "post-fix",
        "hypothesisId": hypothesis_id,
        "location": "audit_gallery_grid.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


html = INDEX.read_text(encoding="utf-8")
grid_match = re.search(r'<div class="dish-grid"[^>]*>(.*?)</div>\s*\n\s*<section class="takeaway-banner"', html, re.S)
grid_html = grid_match.group(1) if grid_match else ""
homepage_imgs = re.findall(r'data-ql-src="/images/food/([^"]+)"', grid_html)

on_disk = {name: (FOOD / name).exists() for name in CANONICAL_12}
canonical_set = set(CANONICAL_12)
homepage_set = set(homepage_imgs)

log("H1", "homepage uses images/food directory", {
    "food_dir": str(FOOD),
    "all_homepage_paths_start_with_food": all("/images/food/" in p for p in re.findall(r'src="/images/food/[^"]+"', grid_html)),
})

log("H2", "migration was path-replace only not grid rebuild", {
    "homepage_card_count": len(homepage_imgs),
    "expected_card_count": 12,
    "homepage_order": homepage_imgs,
})

log("H3", "homepage dishes differ from canonical batch", {
    "in_homepage_not_in_batch": sorted(homepage_set - canonical_set),
    "in_batch_not_on_homepage": sorted(canonical_set - homepage_set),
    "order_matches_canonical": homepage_imgs == CANONICAL_12,
})

log("H4", "non-batch images sourced from legacy conversions", {
    "extra_homepage_files_exist": {f: (FOOD / f).exists() for f in sorted(homepage_set - canonical_set)},
})

log("H5", "all 12 batch webps exist on disk but unused", {
    "batch_on_disk": on_disk,
    "batch_unused_on_homepage": sorted(canonical_set - homepage_set),
})

print("Homepage grid images:", homepage_imgs)
print("Canonical 12:", CANONICAL_12)
print("Match:", homepage_imgs == CANONICAL_12)
print("Logged to", LOG)
