#!/usr/bin/env python3
"""Generate food-images.jsonld RAG manifest from disk + menu-photos.js + alt map."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FOOD = ROOT / "images" / "food"
OUT = ROOT / "food-images.jsonld"
MP = ROOT / "assets" / "js" / "menu-photos.js"

GALLERY_ORDER = [
    "soups.webp", "spring-rolls.webp", "golden-fried-prawns.webp",
    "chilli-garlic-paneer.webp", "lamb-ribs.webp", "lollipop-kiddie.webp",
    "salt-and-pepper-vegetable.webp", "beef-manchurian.webp", "veg-rice.webp",
    "chilli-garlic-noodles.webp", "sweet-sour-prawns.webp", "ginger-crab.webp",
]

GALLERY_TAGS = {
    "soups.webp": "Made to Order",
    "spring-rolls.webp": "Gold Bars · Crisp",
    "golden-fried-prawns.webp": "Seafood · Crisp",
    "chilli-garlic-paneer.webp": "Vegetarian · Bold",
    "lamb-ribs.webp": "Most-Ordered Starter",
    "lollipop-kiddie.webp": "Obinna's Pick · Family First",
    "salt-and-pepper-vegetable.webp": "Vegetarian · Crisp",
    "beef-manchurian.webp": "Tangy · Crisp",
    "veg-rice.webp": "Falcon Rice · Wok-Hei",
    "chilli-garlic-noodles.webp": "2mm Noodles · Aromatic",
    "sweet-sour-prawns.webp": "Seafood · Tangy",
    "ginger-crab.webp": "Seafood · Aromatic",
}

PROTEIN = {
    "beef-brocolli.webp": "beef", "beef-manchurian.webp": "beef", "beef-mushroom.webp": "beef",
    "beef-strips.webp": "beef", "noodles-beef.webp": "beef",
    "chicken-cashewnuts.webp": "chicken", "chicken-wings.webp": "chicken",
    "honey-chilli-chicken.webp": "chicken", "lollipop-kiddie.webp": "chicken", "lollipops.webp": "chicken",
    "lamb-in-schezuan-sauce.webp": "lamb", "lamb-ribs.webp": "lamb",
    "chilli-fish.webp": "fish", "fish-in-garlic.webp": "fish", "red-snapper-hero.webp": "fish",
    "ginger-crab.webp": "seafood", "golden-fried-prawns.webp": "seafood", "prawn-sizzler.webp": "seafood",
    "shanghai-lemon-prawns.webp": "seafood", "sweet-sour-prawns.webp": "seafood", "tom-yum-prawn.webp": "seafood",
    "chilli-garlic-paneer.webp": "vegetarian", "salt-and-pepper-vegetable.webp": "vegetarian",
    "shanghai-veg-tofu-mushroom-brocolli.webp": "chicken", "shanghai-veg-withcashew.webp": "vegetarian",
    "sesame-tofu-bites.webp": "vegetarian", "tofu-in-black-bean-sauce.webp": "vegetarian",
    "veg-rice.webp": "vegetarian", "plain-fried-rice.webp": "vegetarian", "veg-sizzler.webp": "vegetarian",
    "shan-tung-potato-wedges.webp": "vegetarian", "dumplings.webp": "vegetarian",
    "vegetable-springrolls.webp": "vegetarian", "vegetable-spring-rolls-portion.webp": "vegetarian",
    "chilli-garlic-noodles.webp": "vegetarian", "soups.webp": "mixed", "spring-rolls.webp": "mixed",
    "dim-sum-main-index.webp": "mixed", "wok-toss-rice.webp": "mixed",
    "hero-shot.webp": "brand", "wok-toss-rice.webp": "brand", "takeaway.webp": "service",
}

ALLERGENS = {
    "beef": ["soy"], "chicken": ["soy", "egg"], "lamb": ["soy"], "fish": ["fish", "soy"],
    "seafood": ["seafood", "soy"], "vegetarian": ["soy", "gluten"], "mixed": ["soy", "gluten", "egg"],
    "brand": [], "service": ["soy", "gluten"],
}


def load_alt_map() -> dict[str, str]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("pgv2", ROOT / "process_gallery_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.FULL_ALT_TEXT_MAP)


def load_dish_map() -> dict[str, list[str]]:
    text = MP.read_text(encoding="utf-8")
    rev: dict[str, list[str]] = {}
    for dish, webp in re.findall(r'"([^"]+)":\s*"([^"]+\.webp)"', text):
        rev.setdefault(webp, []).append(dish)
    return rev


def main() -> None:
    alt = load_alt_map()
    dishes = load_dish_map()
    gallery_pos = {name: i + 1 for i, name in enumerate(GALLERY_ORDER)}

    items = []
    for path in sorted(FOOD.glob("*.webp")):
        name = path.name
        stem = path.stem
        protein = PROTEIN.get(name, "mixed")
        items.append({
            "@type": "ImageObject",
            "@id": f"https://misterwok.net/images/food/{name}#image",
            "name": stem.replace("-", " ").title(),
            "contentUrl": f"https://misterwok.net/images/food/{name}",
            "encodingFormat": "image/webp",
            "width": 600,
            "height": 600,
            "description": alt.get(stem, alt.get(stem.replace("_", "-"), "")),
            "additionalProperty": [
                {"@type": "PropertyValue", "name": "sizeKB", "value": round(path.stat().st_size / 1024, 1)},
                {"@type": "PropertyValue", "name": "primaryProtein", "value": protein},
                {"@type": "PropertyValue", "name": "galleryPosition", "value": gallery_pos.get(name)},
                {"@type": "PropertyValue", "name": "dishTag", "value": GALLERY_TAGS.get(name)},
                {"@type": "PropertyValue", "name": "mappedDishes", "value": dishes.get(name, [])},
                {"@type": "PropertyValue", "name": "allergenFlags", "value": ALLERGENS.get(protein, [])},
                {"@type": "PropertyValue", "name": "inMenuPhotosManifest", "value": name in dishes},
            ],
        })

    doc = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Mister Wok Food Image Manifest",
        "description": "Machine-readable index of production WebP food images for DEO and RAG.",
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": item}
            for i, item in enumerate(items)
        ],
    }

    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} images -> {OUT}")


if __name__ == "__main__":
    main()
