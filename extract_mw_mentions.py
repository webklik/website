import json

with open("kula_cooler_transcripts.json", encoding="utf-8") as f:
    data = json.load(f)

KEYWORDS = [
    "mister wok", "mr wok", "misterwok",
    "chicken lollipop", "spring roll", "wok hei",
    "parklands", "capital centre", "two rivers",
    "obinna wok", "wok restaurant"
]

mentions = []

for episode in data:
    vid_id = episode["video_id"]
    vid_url = episode["video_url"]
    transcript = episode["transcript"]
    
    for i, segment in enumerate(transcript):
        text = segment["text"].lower()
        if any(kw in text for kw in KEYWORDS):
            # Grab context window: 2 segments before and after
            start_i = max(0, i - 2)
            end_i = min(len(transcript) - 1, i + 2)
            context = " ".join(
                t["text"] for t in transcript[start_i:end_i+1]
            )
            timestamp = int(segment["start"])
            minutes = timestamp // 60
            seconds = timestamp % 60
            mentions.append({
                "video_id": vid_id,
                "video_url": vid_url,
                "timestamp_seconds": timestamp,
                "timestamp_formatted": f"{minutes}:{seconds:02d}",
                "deeplink": f"{vid_url}&t={timestamp}s",
                "matched_keyword": next(
                    kw for kw in KEYWORDS if kw in text
                ),
                "context": context.strip()
            })

with open("mw_mentions.json", "w", encoding="utf-8") as f:
    json.dump(mentions, f, ensure_ascii=False, indent=2)

print(f"Total Mister Wok mentions found: {len(mentions)}")
for m in mentions:
    print(f"\n[{m['timestamp_formatted']}] {m['video_id']}")
    print(f"  Match: {m['matched_keyword']}")
    print(f"  Context: {m['context'][:120]}")
    print(f"  Deeplink: {m['deeplink']}")
