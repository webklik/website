#!/usr/bin/env python3
"""Replace branch landing dish grids with canonical 12 gallery WebPs."""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
LOG = ROOT.parent / "debug-4d29ee.log"

CANONICAL = [
    ("soups", "soups.webp", "Wok Soups", "KES 450", "Made to Order",
     "Soup - aromatic broth with Falcon Rice noodles and wok-seared garnish"),
    ("spring-rolls", "spring-rolls.webp", "Spring Rolls", "From KES 550", "Gold Bars · Crisp",
     "Spring Rolls - crispy pastry with vegetable and protein filling, served with sweet chilli sauce"),
    ("golden-fried-prawns", "golden-fried-prawns.webp", "Golden Fried Prawns", "KES 1,350", "Seafood · Crisp",
     "Golden Fried Prawns - succulent prawns in tempura batter, wok-tossed to golden perfection"),
    ("chilli-garlic-paneer", "chilli-garlic-paneer.webp", "Chilli Garlic Paneer", "KES 1,100", "Vegetarian · Bold",
     "Chilli Garlic Paneer - Indian cottage cheese cubes seared in wok with dry chilli and garlic"),
    ("lamb-ribs", "lamb-ribs.webp", "Lamb Ribs", "KES 1,400", "Most-Ordered Starter",
     "Lamb Ribs - fall-off-the-bone lamb in spiced wok reduction"),
    ("lollipop-kiddie", "lollipop-kiddie.webp", "Chicken Lollipops", "KES 1,000 – 1,200", "Obinna's Pick · Bone-In",
     "Lollipop Kiddie - playful chicken lollipops seasoned with mild spices"),
    ("salt-and-pepper-vegetable", "salt-and-pepper-vegetable.webp", "Salt &amp; Pepper Vegetable", "KES 950", "Vegetarian · Crisp",
     "Salt and Pepper Vegetable - seasonal vegetables with wok-hei char and cracked pepper"),
    ("beef-manchurian", "beef-manchurian.webp", "Beef Manchurian", "KES 1,200", "Tangy · Crisp",
     "Beef Manchurian - tender beef in tangy Manchurian sauce with fried onions"),
    ("veg-rice", "veg-rice.webp", "Vegetable Fried Rice", "KES 650", "Falcon Rice · Wok-Hei",
     "Vegetable Fried Rice - Falcon Rice with garden vegetables, egg, and wok-hei seasoning"),
    ("chilli-garlic-noodles", "chilli-garlic-noodles.webp", "Chilli Garlic Noodles", "KES 700", "2mm Noodles · Aromatic",
     "Chilli Garlic Noodles - stir-fried noodles with aromatic garlic, dry chilli, and fresh herbs"),
    ("sweet-sour-prawns", "sweet-sour-prawns.webp", "Sweet &amp; Sour Prawns", "KES 1,450", "Seafood · Tangy",
     "Sweet and Sour Prawns - prawns in balanced sweet-tangy sauce with pineapple and bell peppers"),
    ("shanghai-vegetables-stir-fry", "shanghai-veg-tofu-mushroom-brocolli.webp", "Shanghai Vegetables Stir Fry", "KES 1,050", "Vegetarian · Shanghai",
     "Shanghai vegetables stir fry with tofu, broccoli, beansprout and mushroom — Mister Wok"),
]

BRANCH_LAST_CARD = {
    "parklands/index.html": ("ginger-crab", "ginger-crab.webp", "Ginger Crab", "KES 1,350", "Seafood · Aromatic",
                              "Ginger Crab - fresh crab meat wok-cooked with young ginger and Shaoxing wine"),
    "capital-centre/index.html": CANONICAL[-1],
    "two-rivers/index.html": CANONICAL[-1],
}

BRANCHES = {
    "parklands/index.html": {
        "branch": "Parklands",
        "menu_slug": "parklands",
        "order_url": "https://www.foodbooking.com/api/fb/67_y_m",
        "lamb_tag_suffix": " · Molo Lamb",
    },
    "capital-centre/index.html": {
        "branch": "Capital Centre",
        "menu_slug": "capital-centre",
        "order_url": "https://www.foodbooking.com/api/fb/d_yq_g",
        "lamb_tag_suffix": " · ✓ Halal-Assured",
    },
    "two-rivers/index.html": {
        "branch": "Two Rivers",
        "menu_slug": "two-rivers",
        "order_url": "https://www.foodbooking.com/api/fb/k8_d_z",
        "lamb_tag_suffix": " · Molo Lamb",
    },
}


def log(msg, data):
    entry = {
        "sessionId": "4d29ee",
        "runId": "branch-patch",
        "hypothesisId": "BRANCH",
        "location": "patch_branch_grids.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def dishes_for(rel_path):
    base = CANONICAL[:-1]
    last = BRANCH_LAST_CARD.get(rel_path, CANONICAL[-1])
    return base + [last]


def render_grid(rel_path, cfg):
    dishes = dishes_for(rel_path)
    lines = ['    <div class="dish-grid" role="list">']
    for i, (dish_id, webp, name, price, tag, alt) in enumerate(dishes):
        if dish_id == "lamb-ribs":
            tag = tag + cfg["lamb_tag_suffix"]
            href = f'/{cfg["menu_slug"]}/menu.html#lamb-starters'
            extra = ' data-cta="menu"'
            target = ""
        else:
            href = cfg["order_url"]
            extra = ' data-cta="direct" target="_blank" rel="noopener"'
            target = ""
        loading = 'loading="eager" decoding="sync"' if i == 0 else 'loading="lazy" decoding="async"'
        dims = ' width="600" height="600"' if i == 0 else ""
        label = f'Order {name.replace("&amp;", "&")} from {cfg["branch"]}'
        lines.append(
            f'      <a class="dish-card" role="listitem" href="{href}"{extra} data-dish-id="{dish_id}" '
            f'data-branch="{cfg["branch"]}" aria-label="{label}">'
        )
        lines.append(
            f'        <img src="/images/food/{webp}" {loading}{dims} alt="{alt}">'
        )
        lines.append(f'        <div class="dish-name">{name}</div>')
        lines.append(f'        <div class="dish-price">{price}</div>')
        lines.append(f'        <div class="dish-tag">{tag}</div>')
        lines.append("      </a>")
    lines.append("    </div>")
    return "\n".join(lines)


def patch_file(rel_path, cfg):
    path = ROOT / rel_path
    html = path.read_text(encoding="utf-8")
    new_grid = render_grid(rel_path, cfg)
    pattern = r'    <div class="dish-grid" role="list">.*?</div>\n\n    <div class="dish-cta-row">'
    updated, n = re.subn(pattern, new_grid + '\n\n    <div class="dish-cta-row">', html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"Grid replace failed for {rel_path} (matches={n})")
    path.write_text(updated, encoding="utf-8")
    imgs = re.findall(r'data-ql-src="/images/food/([^"]+)"', updated)
    grid_imgs = re.findall(
        r'<div class="dish-grid"[^>]*>.*?</div>\s*\n\s*<div class="dish-cta-row">',
        updated,
        re.S,
    )
    grid_block = grid_imgs[0] if grid_imgs else ""
    refs = re.findall(r'/images/food/([a-z0-9-]+\.webp)', grid_block)
    return refs


def main():
    results = {}
    for rel, cfg in BRANCHES.items():
        refs = patch_file(rel, cfg)
        results[rel] = {
            "count": len(refs),
            "order": refs,
            "matches_canonical": refs == [w for _, w, *_ in dishes_for(rel)],
            "has_600": any("600" in r for r in refs),
        }
        print(f"Patched {rel}: {len(refs)} cards, canonical={results[rel]['matches_canonical']}")
    log("branch grids patched", results)


if __name__ == "__main__":
    main()
