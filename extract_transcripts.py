import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, 
    NoTranscriptFound,
    VideoUnavailable
)

with open("playlist_urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

def get_video_id(url):
    return url.split("watch?v=")[-1].split("&")[0]

results = []
failed = []
yt_api = YouTubeTranscriptApi()

for url in urls:
    vid_id = get_video_id(url)
    try:
        transcript = yt_api.fetch(vid_id).to_raw_data()
        results.append({
            "video_id": vid_id,
            "video_url": url,
            "transcript": transcript
        })
        print(f"OK — {vid_id}")
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        failed.append({"video_id": vid_id, "error": str(e)})
        print(f"NO TRANSCRIPT — {vid_id}")
    except VideoUnavailable as e:
        failed.append({"video_id": vid_id, "error": "unavailable"})
        print(f"UNAVAILABLE — {vid_id}")
    except Exception as e:
        failed.append({"video_id": vid_id, "error": str(e)})
        print(f"ERROR — {vid_id}: {e}")

with open("kula_cooler_transcripts.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

with open("kula_cooler_failed.json", "w", encoding="utf-8") as f:
    json.dump(failed, f, ensure_ascii=False, indent=2)

print(f"\nDone.")
print(f"Successful: {len(results)}")
print(f"Failed: {len(failed)}")
