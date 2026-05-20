"""
MISTER WOK — Location Image Conversion Script (v2 — 19 May 2026)
Run from: Mister_Wok_MNFVSS/
Command:  python convert-location-images.py

Sources: images/restaurant/ (falls back to project-wide search)
Outputs: images/restaurant/*.webp
"""
from PIL import Image
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESTAURANT_DIR = os.path.join(SCRIPT_DIR, "images", "restaurant")
OUTPUT_DIR = RESTAURANT_DIR
ARCHIVE_DIR = os.path.join(RESTAURANT_DIR, "_archive")
FOOD_DIR = os.path.join(SCRIPT_DIR, "images", "food")
WEBP_QUALITY = 85

# (output_name, crop_box_or_None, max_size_tuple)
JOBS = {
    "001-Kengen.jpg": ("parklandsexterior.webp", None, (1100, 1100)),
    "Main-dining-Group.jpg": ("parklandslounge.webp", None, (1100, 1100)),
    "003-Two-Rivers-Mall.jpg": ("tworiversmall.webp", None, (1100, 1100)),
    "Two-Rivers-Balcony.jpg": ("tworiversfrontage.webp", None, (1100, 1100)),
    "004-Capital-Centre.jpg": ("capitalcentreexterior.webp", None, (1100, 1100)),
    "CND8892.jpg": ("capitalcentreinterior.webp", (220, 0, 1280, 857), (1200, 1200)),
}
SHARED_COPY = ("parklandslounge.webp", "mw-group-dining.webp")
ARCHIVE = []

SLIDER_SRC = os.path.join(FOOD_DIR, "Slider_Toss600.webp")
HERO_DST = os.path.join(FOOD_DIR, "wok-toss-action-hero.webp")


def find_source(name: str) -> str | None:
    candidates = [
        os.path.join(RESTAURANT_DIR, name),
        os.path.join(SCRIPT_DIR, name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    for root, _dirs, files in os.walk(SCRIPT_DIR):
        if name in files:
            return os.path.join(root, name)
    return None


os.makedirs(OUTPUT_DIR, exist_ok=True)
print("\n=== MISTER WOK Location Conversion v2 ===\n")

done, skip, err = [], [], []

for src_name, (dst_name, crop, max_sz) in JOBS.items():
    src = find_source(src_name)
    if not src:
        skip.append(src_name)
        print(f"  MISSING: {src_name}")
        continue

    dst = os.path.join(OUTPUT_DIR, dst_name)
    try:
        img = Image.open(src).convert("RGB")
        if crop:
            img = img.crop(crop)
            note = f" [banner crop x={crop[0]}]"
        else:
            note = ""
        img.thumbnail(max_sz, Image.LANCZOS)
        img.save(dst, "WEBP", quality=WEBP_QUALITY, method=6)
        out_kb = os.path.getsize(dst) / 1024
        print(f"  OK  {src_name}{note}")
        print(f"      -> /images/restaurant/{dst_name}  {img.width}x{img.height}px  {out_kb:.0f}KB\n")
        done.append(
            {
                "web": f"/images/restaurant/{dst_name}",
                "size": f"{img.width}x{img.height}",
                "kb": round(out_kb, 1),
                "crop": bool(crop),
            }
        )
    except Exception as exc:
        err.append(src_name)
        print(f"  ERROR {src_name}: {exc}\n")

print("--- SHARED COPY ---")
src_webp, dst_name = SHARED_COPY
src_path = os.path.join(OUTPUT_DIR, src_webp)
dst_path = os.path.join(OUTPUT_DIR, dst_name)
if os.path.exists(src_path):
    shutil.copy2(src_path, dst_path)
    print(f"  Copied {src_webp} -> {dst_name} ({os.path.getsize(dst_path) / 1024:.0f}KB)")
    done.append(
        {
            "web": f"/images/restaurant/{dst_name}",
            "size": done[[c["web"] for c in done].index(f"/images/restaurant/{src_webp}")]["size"],
            "kb": round(os.path.getsize(dst_path) / 1024, 1),
            "crop": False,
        }
    )
else:
    print(f"  SKIP: {src_webp} not produced — cannot copy to {dst_name}")
print()

if ARCHIVE:
    print("--- ARCHIVE (do not deploy) ---")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for name in ARCHIVE:
        src = find_source(name)
        if src and os.path.dirname(src) != ARCHIVE_DIR:
            dst = os.path.join(ARCHIVE_DIR, name)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"  Moved {name} -> images/restaurant/_archive/")
            else:
                os.remove(src)
                print(f"  Removed duplicate {name} (archive copy exists)")
        elif src:
            print(f"  {name} already in _archive/")
        else:
            print(f"  {name} not found")
    print()

print("--- LCP HERO ---")
if os.path.exists(SLIDER_SRC):
    if not os.path.exists(HERO_DST):
        shutil.copy2(SLIDER_SRC, HERO_DST)
        print(f"  Created /images/food/wok-toss-action-hero.webp ({os.path.getsize(HERO_DST) / 1024:.0f}KB)")
    else:
        print("  wok-toss-action-hero.webp exists — skipped")
else:
    print("  WARN: images/food/Slider_Toss600.webp not found")
print()

print("--- RICE NOODLES CLEANUP ---")
rn = os.path.join(FOOD_DIR, "Rice_Noodles600.webp")
if os.path.exists(rn):
    os.remove(rn)
    print("  Deleted images/food/Rice_Noodles600.webp")
else:
    print("  Clean — Rice_Noodles600.webp not present")
print()

print(f"=== {len(done)} converted / {len(skip)} missing / {len(err)} errors ===\n")
print("BRANCH PATHS:")
for label, key in [
    ("PARKLANDS", "parklands"),
    ("TWO RIVERS", "two-rivers"),
    ("CAPITAL CENTRE", "capital-centre"),
    ("SHARED", "mw-group"),
]:
    items = [c for c in done if key in c["web"]]
    if items:
        print(f"\n  [{label}]")
        for item in items:
            flag = " <- banner cropped" if item["crop"] else ""
            print(f"    {item['web']}  {item['size']}  {item['kb']}KB{flag}")
