#!/usr/bin/env python3
"""Audit index pages for visual regression — image paths, grid structure, legacy collisions."""
import hashlib
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
FOOD = ROOT / "images" / "food"
RESTAURANT = ROOT / "images" / "restaurant"
LOG = ROOT.parent / "debug-9ecc35.log"
SESSION = "9ecc35"

INDEX_PAGES = [
    "index.html",
    "parklands/index.html",
    "capital-centre/index.html",
    "two-rivers/index.html",
]

CANONICAL_12 = {
    "soups.webp", "spring-rolls.webp", "golden-fried-prawns.webp",
    "chilli-garlic-paneer.webp", "lamb-ribs.webp", "lollipop-kiddie.webp",
    "salt-and-pepper-vegetable.webp", "beef-manchurian.webp", "veg-rice.webp",
    "chilli-garlic-noodles.webp", "sweet-sour-prawns.webp", "ginger-crab.webp",
}


def write_log(hypothesis_id, message, data, run_id="pre-fix"):
    entry = {
        "sessionId": SESSION,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": "audit_visual_regression.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def file_fingerprint(path: Path):
    if not path.exists():
        return {"exists": False}
    data = path.read_bytes()
    return {
        "exists": True,
        "bytes": len(data),
        "md5": hashlib.md5(data).hexdigest()[:12],
        "mtime": path.stat().st_mtime,
    }


def case_collision(name: str):
    """On case-insensitive hosts, multiple paths may resolve to one file."""
    stem = name.rsplit(".", 1)[0]
    ext = name.rsplit(".", 1)[-1]
    matches = []
    for p in FOOD.glob(f"*.{ext}"):
        if p.name.lower() == name.lower() and p.name != name:
            matches.append(p.name)
    return matches


def resolve_image_path(src: str):
    if not src:
        return None
    name = src.split("/")[-1]
    if "/restaurant/" in src:
        return RESTAURANT / name
    if "/food/" in src:
        return FOOD / name
    return ROOT / src.lstrip("/")


def audit_page(rel: str):
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    hero = re.search(r'id="lcp-hero"[^>]*src="([^"]+)"', html) or re.search(
        r'class="hero-img"[^>]*src="([^"]+)"', html
    )
    hero_src = hero.group(1) if hero else None
    grid_imgs = re.findall(r'/images/food/([a-zA-Z0-9 _-]+\.webp)', html)
    ql_count = html.count("ql-trigger")
    article_cards = len(re.findall(r'<article class="dish-card"', html))
    anchor_cards = len(re.findall(r'<a class="dish-card"', html))
    img_details = []
    for img in sorted(set(grid_imgs)):
        fp = file_fingerprint(FOOD / img)
        legacy = img[0].isupper() or " " in img or "600" in img
        kebab_ok = img in CANONICAL_12 or img.islower() and " " not in img
        collisions = case_collision(img)
        img_details.append({
            "file": img,
            "fingerprint": fp,
            "legacy_name": legacy,
            "case_collisions": collisions,
        })
    return {
        "page": rel,
        "hero_src": hero_src,
        "hero_fingerprint": file_fingerprint(resolve_image_path(hero_src)) if hero_src else None,
        "grid_image_count": len(set(grid_imgs)),
        "ql_trigger_count": ql_count,
        "article_dish_cards": article_cards,
        "anchor_dish_cards": anchor_cards,
        "grid_images": img_details,
    }


def main():
    import sys

    run_id = sys.argv[1] if len(sys.argv) > 1 else "pre-fix"
    write_log("INIT", "audit started", {"pages": INDEX_PAGES, "run_id": run_id}, run_id=run_id)

    # Hypothesis A: hero swapped away from wok-toss-action-hero
    hero_a = file_fingerprint(FOOD / "wok-toss-action-hero.webp")
    hero_b = file_fingerprint(FOOD / "hero-shot.webp")
    write_log(
        "A",
        "hero asset comparison",
        {
            "wok_toss_action_hero": hero_a,
            "hero_shot": hero_b,
            "same_bytes": hero_a.get("bytes") == hero_b.get("bytes")
            and hero_a.get("md5") == hero_b.get("md5"),
            "slider_toss_600": file_fingerprint(FOOD / "Slider_Toss600.webp"),
        },
        run_id=run_id,
    )

    # Hypothesis E: bulk *600 / Pascal dump on disk
    kebab = [p.name for p in FOOD.glob("*.webp") if p.name == p.name.lower() and " " not in p.name]
    legacy = [p.name for p in FOOD.glob("*.webp") if p.name != p.name.lower() or " " in p.name or "600" in p.name]
    write_log(
        "E",
        "disk image inventory split",
        {"kebab_count": len(kebab), "legacy_or_600_count": len(legacy), "legacy_sample": legacy[:15]},
        run_id=run_id,
    )

    results = []
    for rel in INDEX_PAGES:
        page = audit_page(rel)
        results.append(page)
        write_log(
            "B" if page["anchor_dish_cards"] and not page["ql_trigger_count"] else "D",
            f"page structure {rel}",
            {
                "hero_src": page["hero_src"],
                "hero_exists": page["hero_fingerprint"].get("exists") if page["hero_fingerprint"] else False,
                "ql_triggers": page["ql_trigger_count"],
                "article_cards": page["article_dish_cards"],
                "anchor_cards": page["anchor_dish_cards"],
            },
            run_id=run_id,
        )

    # Hypothesis C: case collisions for canonical refs
    collisions = []
    for page in results:
        for img in page["grid_images"]:
            if img["case_collisions"]:
                collisions.append({"page": page["page"], "ref": img["file"], "collides_with": img["case_collisions"]})
    write_log("C", "case-insensitive collision scan", {"hits": collisions}, run_id=run_id)

    write_log(
        "SUMMARY",
        "audit complete",
        {"pages": results, "collision_count": len(collisions)},
        run_id=run_id,
    )
    print(json.dumps({"pages": results, "collisions": collisions}, indent=2))


if __name__ == "__main__":
    main()
