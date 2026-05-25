#!/usr/bin/env python3
"""
Mister Wok Image Processing Pipeline v2
- Windows path support
- 12 boutique gallery items (priority)
- 34-image batch flexibility
- Alt-text generation from semantic mapping
"""

import os
import sys
from PIL import Image
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = r"C:\Users\HUSSEIN\Desktop\Mister_Wok_Website\old-working-files\Cleaned_Images"
OUTPUT_DIR = r"C:\Users\HUSSEIN\Desktop\Mister_Wok_Website\Mister_Wok_MNFVSS\images\food"
TARGET_SIZE = 600
QUALITY = 80

# ============================================================================
# BOUTIQUE GALLERY (12 Priority Items)
# Format: "source_filename_without_ext" → "output_kebab_name.webp"
# ============================================================================

GALLERY_PRIORITY = {
    "soups": "soups.webp",
    "spring-rolls": "spring-rolls.webp",
    "golden-fried-prawns": "golden-fried-prawns.webp",
    "chilli-garlic-paneer": "chilli-garlic-paneer.webp",
    "lamb-ribs": "lamb-ribs.webp",
    "lollipop-kiddie": "lollipop-kiddie.webp",
    "salt-and-pepper-vegetable": "salt-and-pepper-vegetable.webp",
    "beef-manchurian": "beef-manchurian.webp",
    "veg-rice": "veg-rice.webp",
    "chilli-garlic-noodles": "chilli-garlic-noodles.webp",
    "sweet-sour-prawns": "sweet-sour-prawns.webp",
    "ginger-crab": "ginger-crab.webp",
}

# ============================================================================
# ALT-TEXT SEMANTIC MAP
# Canonical format: "[Dish] - [Key Ingredients] - [Cooking Character]"
# Used for SEO, RAG indexing, and AI agent comprehension
# ============================================================================

ALT_TEXT_MAP = {
    "soups": "Soup - aromatic broth with aged aromatic long-grain rice noodles and wok-seared garnish",
    "spring-rolls": "Spring Rolls - crispy pastry with vegetable and protein filling, served with sweet chilli sauce",
    "golden-fried-prawns": "Golden Fried Prawns - succulent prawns in tempura batter, wok-tossed to golden perfection",
    "chilli-garlic-paneer": "Chilli Garlic Paneer - Indian cottage cheese cubes seared in wok with dry chilli and garlic",
    "lamb-ribs": "Lamb Ribs - fall-off-the-bone lamb in spiced wok reduction",
    "lollipop-kiddie": "Lollipop Kiddie - playful chicken lollipops seasoned with mild spices",
    "salt-and-pepper-vegetable": "Salt and Pepper Vegetable - seasonal vegetables with wok-hei char and cracked pepper",
    "beef-manchurian": "Beef Manchurian - tender beef in tangy Manchurian sauce with fried onions",
    "veg-rice": "Vegetable Fried Rice - aged aromatic long-grain rice with garden vegetables, egg, and wok-hei seasoning",
    "chilli-garlic-noodles": "Chilli Garlic Noodles - stir-fried noodles with aromatic garlic, dry chilli, and fresh herbs",
    "sweet-sour-prawns": "Sweet and Sour Prawns - prawns in balanced sweet-tangy sauce with pineapple and bell peppers",
    "ginger-crab": "Ginger Crab - fresh crab meat wok-cooked with young ginger and Shaoxing wine",
}

# Full alt-text map for all production WebPs (RAG / DEO indexing)
FULL_ALT_TEXT_MAP = {
    **ALT_TEXT_MAP,
    "beef-brocolli": "Beef Broccoli - premium beef sirloin seared at high wok heat with fresh broccoli florets",
    "beef-mushroom": "Beef with Mushroom - sliced beef and button mushrooms in garlic soy reduction",
    "beef-strips": "Chilli Lamb Strips - tender lamb strips wok-tossed with dry chilli and aromatics",
    "chicken-cashewnuts": "Chicken with Cashewnuts - diced chicken breast tossed with roasted cashews and capsicum",
    "chicken-wings": "House Chicken Wings - dry-style Chinese wings on red onion and colour capsicum",
    "chilli-fish": "Tilapia Fish - fresh Kenyan tilapia wok-cooked in bold Chinese sauce",
    "dim-sum-main-index": "Dim Sum - hand-wrapped dumplings steamed to order",
    "dumplings": "Garden Veg Dumpling - vegetable filling in delicate steamed pastry",
    "fish-in-garlic": "Tilapia Fish in Garlic Sauce - fresh tilapia in aromatic garlic base",
    "hero-shot": "Tilapia - whole fish seared at 300°C wok temperature crispy skin moist flesh",
    "honey-chilli-chicken": "Honey Chilli Chicken - golden chicken nuggets glazed with honey and sesame",
    "lamb-in-schezuan-sauce": "Lamb in Schezuan Sauce - tender lamb strands in spicy tangy Schezuan reduction",
    "lollipops": "Dry Chilli Chicken - spiced chicken nuggets wok-tossed dry with bold chilli heat",
    "noodles-beef": "Beef Noodles - hand-cut noodles wok-tossed with tender beef and seasoning",
    "plain-fried-rice": "Plain Fried Rice - premium long-grain aromatic rice wok-fried with egg",
    "prawn-sizzler": "Prawns Sizzler - queen prawns on hot sizzling platter with vegetables",
    "sesame-tofu-bites": "Sesame Tofu Bites - soft tofu cubes in teriyaki glaze with sesame",
    "shanghai-lemon-prawns": "Shanghai Lemon Prawns - king prawns in crisp batter with house lemon glaze",
    "shanghai-veg-tofu-mushroom-brocolli": "Chicken Baby Corn Broccoli - chicken with baby corn broccoli and light soy glaze",
    "shanghai-veg-withcashew": "Vegetable Wrap - wok-tossed vegetables with cashews in fresh wrap",
    "shan-tung-potato-wedges": "Shan Tung Potato Wedges - spicy potato wedges with wok-hei char",
    "takeaway": "Takeaway Box - stir-fry premium aromatic rice and spring roll feeds 1 to 2",
    "tofu-in-black-bean-sauce": "Tofu in Black Bean Sauce - soft tofu cubes in fermented black bean and garlic",
    "tom-yum-prawn": "Tom Yum Prawn Soup - prawns in hot sour fragrant Thai coconut broth",
    "vegetable-springrolls": "Veg Spring Rolls - crispy pastry with fresh vegetable filling",
    "vegetable-spring-rolls-portion": "Veg Spring Rolls Portion - four gold-bar spring rolls served crisp",
    "veg-sizzler": "Vegetable Sizzler - seasonal vegetables on hot sizzling platter",
    "wok-toss-rice": "Wok Hei - high-heat wok toss at 300 degrees breath of the wok",
    "wok-toss-rice": "Yong Chow Fried Rice - premium aromatic rice with shrimp egg and chicken",
}


def center_crop_to_square(img, size=600):
    """Center-crop image to 600x600."""
    width, height = img.size
    if width == height:
        return img.resize((size, size), Image.Resampling.LANCZOS)

    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    cropped = img.crop((left, top, right, bottom))
    return cropped.resize((size, size), Image.Resampling.LANCZOS)


def process_image(source_path, output_path, alt_text=None):
    """Process single image: crop, convert to WebP."""
    try:
        img = Image.open(source_path)

        # Convert RGBA/LA/Palette → RGB
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (10, 10, 10))  # Black #0a0a0a
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Center-crop & resize
        img = center_crop_to_square(img, TARGET_SIZE)

        # Save WebP
        img.save(
            output_path,
            "WEBP",
            quality=QUALITY,
            method=6,  # Slowest encoding, best compression
        )

        size_kb = os.path.getsize(output_path) / 1024
        status = "GALLERY" if alt_text else "MENU"
        print(f"  OK {status:<7} {Path(output_path).name:<40} {size_kb:>6.1f}KB")

        return True

    except Exception as e:
        print(f"  ERR         {Path(output_path).name}: {e}")
        return False


def normalize_base(name):
    """Normalize filename stem for kebab-case matching."""
    return name.lower().replace("_", "-").replace(" ", "-")


def find_source_file(source_dir, base_name):
    """Find source file by name (case-insensitive, hyphen/underscore tolerant)."""
    target = normalize_base(base_name)
    for file in os.listdir(source_dir):
        stem, ext = os.path.splitext(file)
        if ext.lower() not in (".webp", ".jpg", ".jpeg", ".png", ".gif", ".bmp"):
            continue
        if normalize_base(stem) == target:
            return os.path.join(source_dir, file)
    return None


def main():
    # Validate paths
    if not os.path.isdir(SOURCE_DIR):
        print(f"ERROR: Source directory not found:\n  {SOURCE_DIR}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 80)
    print("MISTER WOK IMAGE PROCESSING PIPELINE v2")
    print("=" * 80)
    print(f"\nSource: {SOURCE_DIR}")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}\n")

    # ========================================================================
    # PHASE 1: BOUTIQUE GALLERY (12 Priority Items)
    # ========================================================================
    print("PHASE 1: BOUTIQUE GALLERY (12 Items)")
    print("-" * 80)

    gallery_success = 0
    for base_name, output_name in GALLERY_PRIORITY.items():
        source_path = find_source_file(SOURCE_DIR, base_name)

        if not source_path:
            print(f"  MISS        {base_name} (skipped)")
            continue

        output_path = os.path.join(OUTPUT_DIR, output_name)
        alt_text = ALT_TEXT_MAP.get(base_name)

        if process_image(source_path, output_path, alt_text):
            gallery_success += 1

    print(f"\nGallery Complete: {gallery_success}/12 processed\n")

    # ========================================================================
    # PHASE 2: MENU IMAGES (Remaining 22 Items)
    # Auto-process any files in source_dir NOT in GALLERY_PRIORITY
    # ========================================================================
    print("PHASE 2: MENU IMAGES (Auto-Process Remaining)")
    print("-" * 80)

    processed_names = {normalize_base(k) for k in GALLERY_PRIORITY.keys()}
    menu_success = 0

    for filename in sorted(os.listdir(SOURCE_DIR)):
        # Skip non-image files
        if not filename.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            continue

        # Skip already-processed gallery items
        base_name = normalize_base(os.path.splitext(filename)[0])
        if base_name in processed_names:
            continue

        # Convert filename to kebab-case output name
        output_name = base_name + ".webp"
        source_path = os.path.join(SOURCE_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, output_name)

        if process_image(source_path, output_path, alt_text=None):
            menu_success += 1

    print(f"\nMenu Images Complete: {menu_success} processed\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("=" * 80)
    print(f"TOTAL: {gallery_success + menu_success} images processed")
    print(f"Gallery: {gallery_success}/12")
    print(f"Menu: {menu_success}")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 80)
    print("\nNext: inject ALT_TEXT_MAP into gallery HTML templates")


if __name__ == "__main__":
    main()
