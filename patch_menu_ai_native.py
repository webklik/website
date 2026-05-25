#!/usr/bin/env python3
"""
patch_menu_ai_native.py — Mister Wok AI-Native Menu Attributes
Injects data-dietary, data-spice-level, data-signature, data-protein
onto every .menu-item-row across all three branch menu files.

Run from: Mister_Wok_MNFVSS/
Requires: pip install beautifulsoup4
Idempotent: safe to re-run at any time.
"""

from bs4 import BeautifulSoup
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. SIGNATURE DISHES ───────────────────────────────────────────────
# Canonical set — lowercase, partial match on dish name
SIGNATURES = {
    'dry chilli chicken',
    'ginger crab',
    'crab in garlic',
    'crab in black bean',
    'ginger lobster',
    'lobster in garlic',
    'lobster in black bean',
    'shrimp egg & chicken yong chow rice',
    'shrimp bang-bang noodles',
    'coconut fish special',
    'mister wok lamb ribs',
    'mister wok chicken lollipops',
    'mister wok - chicken lollipops',
    'mister wok golden 5 special',
    's4 - special schezuan style saucy chips',
    'tom yum goong',
    'tom kha goong',
    'mandarin steamed whole fish',
    'prawns sizzler',
    'prawn sizzler',
    'lamb sizzler',
    'beef sizzler',
    'chicken sizzler',
    'tilapia fish sizzler',
}

# ── 2. SPICE LEVEL RULES ──────────────────────────────────────────────
# Evaluated in order; first match wins. Level 3 = signature heat.
SPICE_RULES = [
    (3, ['hot and sour', 'hot & sour', 'tom yum', 'tom yum goong',
         'tom yum gai', 'tom yum hed', 'tom yum spicy thai',
         'schezuan spicy noodles', 'bang-bang', 'dry chilli', 'pili-pili',
         'kung pao', 'man chow', 'manchow']),
    (2, ['schezuan', 'chilli garlic', 'chilli calamari', 'hot garlic',
         'spicy', 'thai red', 'thai green', 'thai prawn',
         'thai chicken', 'thai vegetable', 'black pepper',
         'sweet chilli lamb', 'honey chilli', 'shan tung',
         'salt & pepper', 'salt and pepper']),
    (1, ['ginger', 'lemon prawn', 'black bean', 'soya sauce',
         'garlic sauce', 'teriyaki', 'sweet & sour', 'sweet and sour',
         'manchurian', 'tom kha', 'pepper tofu', 'satay',
         'beijing', 'kung pao okra']),
]

# ── 3. PROTEIN RULES ──────────────────────────────────────────────────
# Evaluated in order; first match wins.
PROTEIN_RULES = [
    ('lobster',  ['lobster']),
    ('crab',     ['crab']),
    ('prawn',    ['prawn', 'prawns', 'shrimp', 'har-gow']),
    ('fish',     ['fish', 'tilapia', 'calamari', 'seafood']),
    ('chicken',  ['chicken']),
    ('beef',     ['beef']),
    ('lamb',     ['lamb']),
    ('tofu',     ['tofu', 'beancurd']),
    ('paneer',   ['paneer']),
    ('egg',      ['egg-fried', 'egg fried', 'fuyong', 'fu yong']),
    ('mushroom', ['mushroom plain', 'mushroom dumpling',
                  'mushroom fuyong', 'mushroom chicken']),
]
# If no rule matches, section default is used.

# ── 4. DIETARY MODIFIER RULES ─────────────────────────────────────────
SHELLFISH_KEYWORDS  = ['prawn', 'prawns', 'shrimp', 'crab', 'lobster',
                        'har-gow', 'prawn shumai', 'prawn dumpling',
                        'prawn and mushroom']
FISH_KEYWORDS       = ['fish', 'tilapia', 'calamari', 'seafood tempura',
                        'coconut fish', 'fish coriander', 'seafood soup',
                        'winglets of tilapia', 'fish fingers',
                        'fish in garlic', 'sweet and sour fish',
                        'sweet & sour fish']
NUT_KEYWORDS        = ['cashewnut', 'cashew', 'peanut', 'bang-bang',
                        'satay', 'kung pao']
DAIRY_KEYWORDS      = ['paneer', 'milkshake', 'ice cream', 'cappuccino',
                        'caffe latte', 'chai latte', 'hot chocolate',
                        'latte macchiato', 'mocha', 'cake']
EGG_KEYWORDS        = ['fuyong', 'fu yong', 'egg-fried', 'egg fried',
                        'egg fried rice', 'yong chow']
GLUTEN_KEYWORDS     = ['dumpling', 'wonton', 'shumai', 'spring roll',
                        'tempura', 'noodle', 'noodles', 'chowmein',
                        'batter', 'fritter', 'pancake']
ALCOHOL_KEYWORDS    = ['wine', 'beer', 'gin', 'vodka', 'rum', 'cognac',
                        'brandy', 'whisky', 'chivas', 'jack daniels',
                        'glenfiddich', 'johnnie walker', 'liqueur',
                        'shooter', 'cocktail', 'aperitif', 'sherry',
                        'smirnoff ice', 'imported beer', 'kenyan beer',
                        'mocktail']

# ── 5. SECTION-LEVEL DEFAULTS ─────────────────────────────────────────
# Keys must match the id="" attribute on each <details> element.
SECTION_DEFAULTS = {
    'soups': {
        'dietary': ['halal'],
        'protein': 'veg',
        'spice':   None,   # None = derive from name
        'is_veg':  False,
    },
    'salads-wraps': {
        'dietary': ['halal'],
        'protein': 'veg',
        'spice':   0,
        'is_veg':  False,
    },
    'dim-sum': {
        'dietary': ['halal', 'contains-gluten'],
        'protein': 'veg',
        'spice':   0,
        'is_veg':  False,
    },
    'seafood-appetizers': {
        'dietary': ['halal', 'contains-fish'],
        'protein': 'fish',
        'spice':   1,
        'is_veg':  False,
    },
    'chicken-appetizers': {
        'dietary': ['halal'],
        'protein': 'chicken',
        'spice':   None,
        'is_veg':  False,
    },
    'lamb-appetizers': {
        'dietary': ['halal'],
        'protein': 'lamb',
        'spice':   None,
        'is_veg':  False,
    },
    'beef-appetizers': {
        'dietary': ['halal'],
        'protein': 'beef',
        'spice':   None,
        'is_veg':  False,
    },
    'vegetarian-appetizers': {
        'dietary': ['vegetarian', 'halal'],
        'protein': 'veg',
        'spice':   None,
        'is_veg':  True,
    },
    'seafood-main': {
        'dietary': ['halal', 'contains-fish'],
        'protein': 'fish',
        'spice':   None,
        'is_veg':  False,
    },
    'chicken-main': {
        'dietary': ['halal'],
        'protein': 'chicken',
        'spice':   None,
        'is_veg':  False,
    },
    'beef-main': {
        'dietary': ['halal'],
        'protein': 'beef',
        'spice':   None,
        'is_veg':  False,
    },
    'lamb-main': {
        'dietary': ['halal'],
        'protein': 'lamb',
        'spice':   None,
        'is_veg':  False,
    },
    'vegetarian-main': {
        'dietary': ['vegetarian', 'halal'],
        'protein': 'veg',
        'spice':   None,
        'is_veg':  True,
    },
    'fuyong': {
        'dietary': ['halal', 'contains-egg'],
        'protein': 'egg',
        'spice':   0,
        'is_veg':  False,
    },
    'rice': {
        'dietary': ['halal'],
        'protein': 'veg',
        'spice':   0,
        'is_veg':  False,
    },
    'chowmein': {
        'dietary': ['halal', 'contains-gluten'],
        'protein': 'veg',
        'spice':   None,
        'is_veg':  False,
    },
    'combos': {
        'dietary': ['halal'],
        'protein': 'mixed',
        'spice':   1,
        'is_veg':  False,
    },
    'kiddie-menu': {
        'dietary': ['halal'],
        'protein': 'chicken',
        'spice':   0,
        'is_veg':  False,
    },
    'desserts': {
        'dietary': ['halal', 'contains-dairy', 'contains-egg',
                    'contains-gluten'],
        'protein': 'none',
        'spice':   0,
        'is_veg':  False,
    },
    'hot-beverages': {
        'dietary': ['halal', 'contains-dairy'],
        'protein': 'none',
        'spice':   0,
        'is_veg':  True,
    },
    'beverages': {
        'dietary': ['halal'],
        'protein': 'none',
        'spice':   0,
        'is_veg':  True,
    },
}

# Section ID aliases — maps actual HTML ids to canonical defaults
SECTION_DEFAULTS['veg-apps']             = SECTION_DEFAULTS['vegetarian-appetizers']
SECTION_DEFAULTS['veg-main']             = SECTION_DEFAULTS['vegetarian-main']
SECTION_DEFAULTS['seafood-apps']         = SECTION_DEFAULTS['seafood-appetizers']
SECTION_DEFAULTS['chicken-apps']         = SECTION_DEFAULTS['chicken-appetizers']
SECTION_DEFAULTS['lamb-apps']            = SECTION_DEFAULTS['lamb-appetizers']
SECTION_DEFAULTS['beef-apps']            = SECTION_DEFAULTS['beef-appetizers']
SECTION_DEFAULTS['noodles']              = SECTION_DEFAULTS['chowmein']
SECTION_DEFAULTS['rice-noodles-combos']  = SECTION_DEFAULTS['combos']
SECTION_DEFAULTS['kiddie']               = SECTION_DEFAULTS['kiddie-menu']
SECTION_DEFAULTS['hot-drinks']           = SECTION_DEFAULTS['hot-beverages']
SECTION_DEFAULTS['drinks']               = SECTION_DEFAULTS['beverages']

FALLBACK_SECTION = {
    'dietary': ['halal'],
    'protein': 'veg',
    'spice':   None,
    'is_veg':  False,
}


# ── RULE ENGINE ───────────────────────────────────────────────────────

def resolve_spice(name_lower, section_default):
    """Return spice level 0-3 as string."""
    for level, keywords in SPICE_RULES:
        if any(kw in name_lower for kw in keywords):
            return str(level)
    if section_default is None:
        return '0'
    return str(section_default)


def resolve_protein(name_lower, section_default):
    """Return canonical protein string."""
    for protein, keywords in PROTEIN_RULES:
        if any(kw in name_lower for kw in keywords):
            return protein
    return section_default


def resolve_dietary(name_lower, section_dietary, is_veg):
    """Build dietary tag list with modifiers applied."""
    tags = list(section_dietary)

    def add(tag):
        if tag not in tags:
            tags.append(tag)

    def remove(tag):
        if tag in tags:
            tags.remove(tag)

    # Shellfish — overrides contains-fish
    if any(kw in name_lower for kw in SHELLFISH_KEYWORDS):
        add('contains-shellfish')
        remove('contains-fish')

    # Fish (only if not shellfish)
    elif any(kw in name_lower for kw in FISH_KEYWORDS):
        add('contains-fish')

    # Nuts
    if any(kw in name_lower for kw in NUT_KEYWORDS):
        add('contains-nuts')

    # Dairy
    if any(kw in name_lower for kw in DAIRY_KEYWORDS):
        add('contains-dairy')
        remove('vegan')

    # Egg
    if any(kw in name_lower for kw in EGG_KEYWORDS):
        add('contains-egg')
        remove('vegan')

    # Gluten
    if any(kw in name_lower for kw in GLUTEN_KEYWORDS):
        add('contains-gluten')

    # Alcohol — strip halal, add contains-alcohol
    if any(kw in name_lower for kw in ALCOHOL_KEYWORDS):
        remove('halal')
        remove('vegetarian')
        remove('vegan')
        add('contains-alcohol')
        return ','.join(tags)

    # Vegan promotion: vegetarian + no animal modifiers
    non_vegan = {'contains-dairy', 'contains-egg',
                 'contains-shellfish', 'contains-fish'}
    if is_veg and 'vegetarian' in tags and not non_vegan.intersection(tags):
        animal_proteins = ['chicken', 'beef', 'lamb', 'prawn',
                           'crab', 'lobster', 'fish']
        if not any(p in name_lower for p in animal_proteins):
            add('vegan')

    return ','.join(tags)


def resolve_signature(name_lower):
    return 'true' if any(s in name_lower for s in SIGNATURES) else 'false'


# ── FILE PROCESSOR ────────────────────────────────────────────────────

def process_file(rel_path):
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print(f'  SKIP     {rel_path}  (file not found)')
        return 0

    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    count = 0

    for details in soup.find_all('details', class_='menu-accordion'):
        section_id = details.get('id', '')
        defs = SECTION_DEFAULTS.get(section_id, FALLBACK_SECTION)

        for row in details.find_all('li', class_='menu-item-row'):
            name_el = (row.find(attrs={'itemprop': 'name'}) or
                       row.find(class_='item-dish-name'))
            if not name_el:
                continue

            name_lower = name_el.get_text(strip=True).lower()

            row['data-dietary']    = resolve_dietary(
                                         name_lower,
                                         defs['dietary'],
                                         defs['is_veg'])
            row['data-spice-level'] = resolve_spice(
                                         name_lower,
                                         defs['spice'])
            row['data-protein']    = resolve_protein(
                                         name_lower,
                                         defs['protein'])
            row['data-signature']  = resolve_signature(name_lower)
            count += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f'  WRITTEN  {rel_path}  ({count} items tagged)')
    return count


# ── ENTRY POINT ───────────────────────────────────────────────────────

TARGET_FILES = [
    'parklands/menu.html',
    'capital-centre/menu.html',
    'two-rivers/menu.html',
]

if __name__ == '__main__':
    print('patch_menu_ai_native.py — Mister Wok AI-Native Attributes')
    print('=' * 60)
    total = sum(process_file(f) for f in TARGET_FILES)
    print('=' * 60)
    print(f'Done. {total} menu items tagged across {len(TARGET_FILES)} files.')
