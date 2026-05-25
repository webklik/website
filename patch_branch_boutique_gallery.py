#!/usr/bin/env python3
"""Restore boutique signature gallery (Quick Look + takeaway) on branch landing pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"

QL_SVG = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
          </svg>"""

QL_MODAL = """
  <div id="ql-modal" class="ql-modal" role="dialog" aria-modal="true" aria-label="Dish quick look" aria-hidden="true">
    <div class="ql-backdrop" id="ql-backdrop"></div>
    <div class="ql-sheet">
      <button class="ql-close" id="ql-close" aria-label="Close quick look" type="button">✕</button>
      <div class="ql-img-wrap">
        <img id="ql-img" src="" alt="" loading="eager" decoding="async" class="ql-img">
      </div>
      <div class="ql-details">
        <div id="ql-tag" class="ql-tag"></div>
        <h2 id="ql-name" class="ql-name"></h2>
        <p id="ql-desc" class="ql-desc"></p>
        <div id="ql-price" class="ql-price"></div>
      </div>
      <div class="ql-order-wrap">
        <a id="ql-order-btn" class="ql-order-btn" href="#" target="_blank" rel="noopener" data-cta="direct" data-order-btn="true" aria-label="Order this dish"><span aria-hidden="true">🛒</span> Order Now</a>
      </div>
    </div>
  </div>
"""

DISHES = [
    {
        "id": "soups",
        "webp": "soups.webp",
        "name": "Wok Soups",
        "ql_name": "Wok Soups — House Broths Daily",
        "ql_desc": "House-made broths simmered daily. Tom Yum: hot, sour, aromatic. Cream of Mushroom: rich, velvety. Clear Broth: delicate, restorative. Made-to-order.",
        "price": "KES 450",
        "tag": "Made to Order",
        "alt": "Soup - aromatic broth with aged long-grain aromatic rice noodles and wok-seared garnish",
    },
    {
        "id": "spring-rolls",
        "webp": "spring-rolls.webp",
        "name": "Spring Rolls",
        "ql_name": "Spring Rolls — Gold Bars",
        "ql_desc": "Handcrafted vegetarian spring rolls — thin crisp pastry, fresh-cut vegetables, wok-fried to order. Nairobi's original gold bars. Served with house chilli sauce.",
        "price": "From KES 550",
        "tag": "Gold Bars · Crisp",
        "alt": "Spring Rolls - crispy pastry with vegetable and protein filling, served with sweet chilli sauce",
    },
    {
        "id": "golden-fried-prawns",
        "webp": "golden-fried-prawns.webp",
        "name": "Golden Fried Prawns",
        "ql_name": "Golden Fried Prawns — Tempura Crisp",
        "ql_desc": "Succulent prawns in tempura batter, wok-tossed to golden perfection. Clean batter, lime-ready finish.",
        "price": "KES 1,350",
        "tag": "Seafood · Crisp",
        "alt": "Golden Fried Prawns - succulent prawns in tempura batter, wok-tossed to golden perfection",
    },
    {
        "id": "chilli-garlic-paneer",
        "webp": "chilli-garlic-paneer.webp",
        "name": "Chilli Garlic Paneer",
        "ql_name": "Chilli Garlic Paneer — Wok-Seared",
        "ql_desc": "Indian cottage cheese cubes seared in wok with dry chilli and garlic. Bold vegetarian main.",
        "price": "KES 1,100",
        "tag": "Vegetarian · Bold",
        "alt": "Chilli Garlic Paneer - Indian cottage cheese cubes seared in wok with dry chilli and garlic",
    },
    {
        "id": "lamb-ribs",
        "webp": "lamb-ribs.webp",
        "name": "Lamb Ribs",
        "ql_name": "Lamb Ribs — Fall-Tender",
        "ql_desc": "Young Dopa lamb ribs prepared in three stages to achieve fall-tender texture. Sticky-sweet sauce with a quiet punch — one of the most ordered starters.",
        "price": "KES 1,400",
        "tag": "Most-Ordered Starter",
        "alt": "Lamb Ribs - fall-off-the-bone lamb in spiced wok reduction",
        "menu_href": True,
    },
    {
        "id": "lollipop-kiddie",
        "webp": "lollipop-kiddie.webp",
        "name": "Chicken Lollipops",
        "ql_name": "Chicken Lollipops — Bone-In Bites",
        "ql_desc": "Chicken drumette, marinated 3-4 hours, double-fried for crispy exterior and tender meat. Obinna-endorsed signature.",
        "price": "KES 1,000 – 1,200",
        "tag": "Obinna's Pick · Bone-In",
        "alt": "Lollipop Kiddie - playful chicken lollipops seasoned with mild spices",
    },
    {
        "id": "salt-and-pepper-vegetable",
        "webp": "salt-and-pepper-vegetable.webp",
        "name": "Salt &amp; Pepper Vegetable",
        "ql_name": "Salt &amp; Pepper Vegetable — Wok-Hei",
        "ql_desc": "Seasonal vegetables with wok-hei char and cracked pepper. Light, crisp, vegetarian.",
        "price": "KES 950",
        "tag": "Vegetarian · Crisp",
        "alt": "Salt and Pepper Vegetable - seasonal vegetables with wok-hei char and cracked pepper",
    },
    {
        "id": "beef-manchurian",
        "webp": "beef-manchurian.webp",
        "name": "Beef Manchurian",
        "ql_name": "Beef Manchurian — Tangy &amp; Crisp",
        "ql_desc": "Tender beef in tangy Manchurian sauce with fried onions. High-heat wok finish.",
        "price": "KES 1,200",
        "tag": "Tangy · Crisp",
        "alt": "Beef Manchurian - tender beef in tangy Manchurian sauce with fried onions",
    },
    {
        "id": "veg-rice",
        "webp": "veg-rice.webp",
        "name": "Vegetable Fried Rice",
        "ql_name": "Vegetable Fried Rice — Aged Long-Grain",
        "ql_desc": "Premium aged long-grain aromatic rice with garden vegetables, egg, and wok-hei seasoning.",
        "price": "KES 650",
        "tag": "Aged Long-Grain · Wok-Hei",
        "alt": "Vegetable Fried Rice - aged aromatic long-grain rice with garden vegetables, egg, and wok-hei seasoning",
    },
    {
        "id": "chilli-garlic-noodles",
        "webp": "chilli-garlic-noodles.webp",
        "name": "Chilli Garlic Noodles",
        "ql_name": "Chilli Garlic Noodles — 2mm Hand-Cut",
        "ql_desc": "Stir-fried noodles with aromatic garlic, dry chilli, and fresh herbs. Fresh 2mm noodles cut daily.",
        "price": "KES 700",
        "tag": "2mm Noodles · Aromatic",
        "alt": "Chilli Garlic Noodles - stir-fried noodles with aromatic garlic, dry chilli, and fresh herbs",
    },
    {
        "id": "sweet-sour-prawns",
        "webp": "sweet-sour-prawns.webp",
        "name": "Sweet &amp; Sour Prawns",
        "ql_name": "Sweet &amp; Sour Prawns — Balanced Tang",
        "ql_desc": "Prawns in balanced sweet-tangy sauce with pineapple and bell peppers.",
        "price": "KES 1,450",
        "tag": "Seafood · Tangy",
        "alt": "Sweet and Sour Prawns - prawns in balanced sweet-tangy sauce with pineapple and bell peppers",
    },
]

LAST_DISH = {
    "parklands": {
        "id": "ginger-crab",
        "webp": "ginger-crab.webp",
        "name": "Ginger Crab",
        "ql_name": "Ginger Crab — Shaoxing &amp; Young Ginger",
        "ql_desc": "Fresh crab meat wok-cooked with young ginger and Shaoxing wine. Aromatic seafood signature.",
        "price": "KES 1,350",
        "tag": "Seafood · Aromatic",
        "alt": "Ginger Crab - fresh crab meat wok-cooked with young ginger and Shaoxing wine",
    },
    "default": {
        "id": "shanghai-vegetables-stir-fry",
        "webp": "shanghai-veg-tofu-mushroom-brocolli.webp",
        "name": "Shanghai Vegetables Stir Fry",
        "ql_name": "Shanghai Vegetables Stir Fry",
        "ql_desc": "Shanghai vegetables stir fry with tofu, broccoli, beansprout and mushroom — light, balanced, vegetarian-forward.",
        "price": "KES 1,050",
        "tag": "Vegetarian · Shanghai",
        "alt": "Shanghai vegetables stir fry with tofu, broccoli, beansprout and mushroom — Mister Wok",
    },
}

BRANCHES = {
    "parklands/index.html": {
        "branch": "Parklands",
        "menu_slug": "parklands",
        "order_url": "https://www.foodbooking.com/api/fb/67_y_m",
        "menu_cta": "🍜 See the full Parklands menu (229 dishes) →",
        "lamb_tag_suffix": " · Molo Lamb",
        "last_key": "parklands",
    },
    "capital-centre/index.html": {
        "branch": "Capital Centre",
        "menu_slug": "capital-centre",
        "order_url": "https://www.foodbooking.com/api/fb/d_yq_g",
        "menu_cta": "🍜 See the full Capital Centre menu →",
        "lamb_tag_suffix": " · ✓ Halal-Assured",
        "last_key": "default",
    },
    "two-rivers/index.html": {
        "branch": "Two Rivers",
        "menu_slug": "two-rivers",
        "order_url": "https://www.foodbooking.com/api/fb/k8_d_z",
        "menu_cta": "🍜 See the full Two Rivers menu →",
        "lamb_tag_suffix": " · Molo Lamb",
        "last_key": "default",
    },
}


def extract_boutique_css():
    text = INDEX.read_text(encoding="utf-8")
    match = re.search(
        r"/\* ─── 12-CARD DISH GRID \+ Quick Look \+ Takeaway \(Phase 1B\) ─ \*/.*?\.dish-cta-row a:hover \{[^}]+\}",
        text,
        re.S,
    )
    if not match:
        raise RuntimeError("Could not extract boutique CSS from index.html")
    css = match.group(0)
    css = css.replace(
        ".dish-card-order {",
        ".dish-card-order {\n    text-decoration: none;\n    display: inline-block;",
        1,
    )
    return css


def dishes_for(cfg):
    items = []
    for dish in DISHES:
        d = dict(dish)
        if d["id"] == "lamb-ribs":
            d["tag"] = d["tag"] + cfg["lamb_tag_suffix"]
        items.append(d)
    last = LAST_DISH[cfg["last_key"]]
    items.append(dict(last))
    return items


def render_order_cta(dish, cfg):
    label = f'Order {dish["name"].replace("&amp;", "&")} from {cfg["branch"]}'
    if dish.get("menu_href"):
        href = f'/{cfg["menu_slug"]}/menu.html#lamb-starters'
        return (
            f'<a class="dish-card-order" href="{href}" data-cta="menu" '
            f'aria-label="{label}">Order</a>'
        )
    return (
        f'<a class="dish-card-order" href="{cfg["order_url"]}" target="_blank" rel="noopener" '
        f'data-cta="direct" data-order-btn="true" data-branch="{cfg["branch"]}" '
        f'aria-label="{label}">Order</a>'
    )


def render_card(dish, cfg, first=False):
    loading = 'loading="eager" decoding="sync"' if first else 'loading="lazy" decoding="async"'
    dims = ' width="600" height="600"' if first else ""
    plain_name = dish["name"].replace("&amp;", "&")
    return f"""      <article class="dish-card" role="listitem" tabindex="0" data-dish-id="{dish["id"]}"
        data-ql-name="{dish["ql_name"]}"
        data-ql-desc="{dish["ql_desc"]}"
        data-ql-price="{dish["price"]}"
        data-ql-tag="{dish["tag"]}"
        data-ql-src="/images/food/{dish["webp"]}"
        data-branch="{cfg["branch"]}"
        aria-label="{plain_name} — Quick Look or order">
        <div class="dish-card-inner">
          <img src="/images/food/{dish["webp"]}" {loading}{dims} alt="{dish["alt"]}">
          <button type="button" class="ql-trigger" aria-label="Quick Look: {plain_name}" data-ql-trigger>
            {QL_SVG}
          </button>
        </div>
        <div class="dish-name">{dish["name"]}</div>
        <div class="dish-price">{dish["price"]}</div>
        <div class="dish-tag">{dish["tag"]}</div>
        {render_order_cta(dish, cfg)}
      </article>"""


def render_gallery_block(cfg):
    cards = [render_card(d, cfg, i == 0) for i, d in enumerate(dishes_for(cfg))]
    grid = "\n".join(cards)
    return f"""    <div class="dish-grid" role="list">
{grid}
    </div>

    <section class="takeaway-banner" aria-label="Order Mister Wok Takeaway Box from {cfg["branch"]}">
      <div class="tb-img-wrap">
        <img src="/images/food/takeaway.webp" loading="lazy" decoding="async" width="600" height="600" alt="Mister Wok takeaway box with stir-fry, premium aromatic rice and spring roll — feeds 1 to 2 people">
      </div>
      <div class="tb-content">
        <div class="tb-tag">Feeds 1–2 · Ready in 15 min · Recyclable packaging</div>
        <h3 class="tb-name">The Takeaway Box</h3>
        <div class="tb-price">KES 1,500</div>
        <a href="{cfg["order_url"]}" class="tb-cta" target="_blank" rel="noopener" data-cta="direct" data-order-btn="true" data-branch="{cfg["branch"]}" aria-label="Order The Takeaway Box from {cfg["branch"]}">Order Takeaway →</a>
      </div>
    </section>

    <div class="dish-cta-row">
      <a href="/{cfg["menu_slug"]}/menu.html" data-cta="menu">{cfg["menu_cta"]}</a>
    </div>"""


def patch_css(html, boutique_css):
    pattern = r"  (?:/\* Dish grid \*/\s*)?\.dishes\{.*?\}\s*\.dish-cta-row a:hover\{[^}]+\}"
    updated, n = re.subn(pattern, boutique_css, html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("CSS replace failed")
    return updated


def patch_gallery(html, cfg):
    pattern = r'    <div class="dish-grid" role="list">.*?</div>\n\n    <div class="dish-cta-row">'
    replacement = render_gallery_block(cfg)
    updated, n = re.subn(pattern, replacement, html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("Gallery replace failed")
    return updated


def patch_ql_modal(html):
    if 'id="ql-modal"' in html:
        return html
    marker = '  <nav class="bottom-nav"'
    if marker not in html:
        raise RuntimeError("bottom-nav marker not found")
    return html.replace(marker, QL_MODAL + "\n\n" + marker, 1)


def patch_file(rel_path, cfg, boutique_css):
    path = ROOT / rel_path
    html = path.read_text(encoding="utf-8")
    html = patch_css(html, boutique_css)
    html = patch_gallery(html, cfg)
    html = patch_ql_modal(html)
    path.write_text(html, encoding="utf-8")
    return len(re.findall(r'<article class="dish-card"', html))


def main():
    boutique_css = extract_boutique_css()
    for rel, cfg in BRANCHES.items():
        count = patch_file(rel, cfg, boutique_css)
        print(f"Patched {rel}: {count} boutique cards + Quick Look modal")


if __name__ == "__main__":
    main()
