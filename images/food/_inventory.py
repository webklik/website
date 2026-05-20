import struct
from pathlib import Path
from collections import Counter

food = Path(__file__).parent

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a or 1

def ratio_str(w, h):
    g = gcd(w, h)
    return f"{w // g}:{h // g}"

def read_webp_dims(data):
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    i = 12
    while i < len(data) - 8:
        tag = data[i : i + 4]
        sz = struct.unpack("<I", data[i + 4 : i + 8])[0]
        chunk = data[i + 8 : i + 8 + sz]
        if tag == b"VP8 " and len(chunk) >= 10:
            w = struct.unpack("<H", chunk[6:8])[0] & 0x3FFF
            h = struct.unpack("<H", chunk[8:10])[0] & 0x3FFF
            return w, h
        if tag == b"VP8L" and len(chunk) >= 5:
            bits = chunk[1] | (chunk[2] << 8) | (chunk[3] << 16) | (chunk[4] << 24)
            w = (bits & 0x3FFF) + 1
            h = ((bits >> 14) & 0x3FFF) + 1
            return w, h
        if tag == b"VP8X" and len(chunk) >= 10:
            w = 1 + (chunk[4] | (chunk[5] << 8) | (chunk[6] << 16))
            h = 1 + (chunk[7] | (chunk[8] << 8) | (chunk[9] << 16))
            return w, h
        i += 8 + ((sz + 1) // 2) * 2
    return None

def read_jpeg_dims(data):
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while data[i] == 0xFF:
            i += 1
        marker = data[i]
        i += 1
        if marker in (0xD8, 0xD9):
            continue
        if i + 2 > len(data):
            break
        ln = struct.unpack(">H", data[i : i + 2])[0]
        if marker in (
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        ):
            h, w = struct.unpack(">HH", data[i + 3 : i + 7])
            return w, h
        i += ln
    return None

def dims(path):
    data = path.read_bytes()[:512000]
    ext = path.suffix.lower()
    if ext == ".webp":
        return read_webp_dims(data)
    if ext in (".jpg", ".jpeg"):
        return read_jpeg_dims(data)
    return None

def orient(ar):
    if abs(ar - 1) < 0.02:
        return "square (1:1)"
    if ar > 1.05:
        return "landscape"
    if ar < 0.95:
        return "portrait"
    return "near-square"

rows = []
for p in sorted(food.iterdir()):
    if p.suffix.lower() not in (".webp", ".jpg", ".jpeg", ".png"):
        continue
    sz = p.stat().st_size
    d = dims(p)
    if d:
        w, h = d
        ar = w / h
        rows.append((p.name, p.suffix.lower().lstrip("."), sz, w, h, ratio_str(w, h), round(ar, 3), orient(ar)))
    else:
        rows.append((p.name, p.suffix.lower().lstrip("."), sz, None, None, "?", None, "?"))

print("| File | Type | KB | W×H | Ratio | Orientation |")
print("|------|------|-----|-----|-------|-------------|")
for name, typ, sz, w, h, rat, dec, role in rows:
    kb = round(sz / 1024, 1)
    wh = f"{w}×{h}" if w else "?"
    print(f"| {name} | {typ} | {kb} | {wh} | {rat} | {role} |")

print()
print("--- SUMMARY ---")
print(f"Total: {len(rows)} images")
print("Types:", dict(Counter(r[1] for r in rows)))
print("Orientation:", dict(Counter(r[7] for r in rows)))
print("Ratios:", Counter(r[5] for r in rows if r[5] != "?").most_common(10))
hero = [r[0] for r in rows if "hero" in r[0].lower() or "wok-toss" in r[0].lower()]
print("Hero-related:", hero or "(none)")
missing = "wok-toss-action-hero.webp" not in [r[0] for r in rows]
if missing:
    print("MISSING (referenced in index.html): wok-toss-action-hero.webp")
