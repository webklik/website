"""Retry transcript extraction for videos that failed on the first sweep."""

import json
import subprocess
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    IpBlocked,
    NoTranscriptFound,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
)

DELAY_SECONDS = 15
MAX_ATTEMPTS = 3
TRANSCRIPTS_FILE = Path("kula_cooler_transcripts.json")
FAILED_FILE = Path("kula_cooler_failed.json")
PLAYLIST_FILE = Path("playlist_urls.txt")
SUBS_DIR = Path("subs")


def get_video_id(url: str) -> str:
    return url.split("watch?v=")[-1].split("&")[0]


def load_url_map() -> dict[str, str]:
    urls = PLAYLIST_FILE.read_text(encoding="utf-8").splitlines()
    return {get_video_id(url.strip()): url.strip() for url in urls if url.strip()}


def fetch_via_api(yt_api: YouTubeTranscriptApi, vid_id: str) -> list[dict]:
    return yt_api.fetch(vid_id).to_raw_data()


def fetch_via_ytdlp(vid_id: str, url: str) -> list[dict] | None:
    """Fallback: download auto-captions with yt-dlp and convert to API format."""
    SUBS_DIR.mkdir(exist_ok=True)
    out_template = str(SUBS_DIR / vid_id)

    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--write-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sub-format", "json3",
        "-o", out_template,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None

    sub_files = list(SUBS_DIR.glob(f"{vid_id}*.json3"))
    if not sub_files:
        return None

    data = json.loads(sub_files[0].read_text(encoding="utf-8"))
    events = data.get("events") or []
    transcript: list[dict] = []

    for event in events:
        if "segs" not in event:
            continue
        text = "".join(seg.get("utf8", "") for seg in event["segs"]).strip()
        if not text or text == "\n":
            continue
        start_ms = event.get("tStartMs", 0)
        duration_ms = event.get("dDurationMs", 0)
        transcript.append({
            "text": text,
            "start": start_ms / 1000.0,
            "duration": duration_ms / 1000.0,
        })

    return transcript or None


def fetch_transcript(vid_id: str, url: str, yt_api: YouTubeTranscriptApi) -> list[dict]:
    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fetch_via_api(yt_api, vid_id)
        except (IpBlocked, RequestBlocked) as e:
            last_error = e
            wait = DELAY_SECONDS * attempt
            print(f"  Rate limited (attempt {attempt}/{MAX_ATTEMPTS}), waiting {wait}s...")
            time.sleep(wait)
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
            raise

    transcript = fetch_via_ytdlp(vid_id, url)
    if transcript:
        return transcript

    if last_error:
        raise last_error
    raise RuntimeError("Could not fetch transcript")


def main() -> int:
    failed_entries = json.loads(FAILED_FILE.read_text(encoding="utf-8"))
    retry_ids = [entry["video_id"] for entry in failed_entries]
    if not retry_ids:
        print("No failed videos to retry.")
        return 0

    url_map = load_url_map()
    existing = json.loads(TRANSCRIPTS_FILE.read_text(encoding="utf-8"))
    existing_ids = {entry["video_id"] for entry in existing}

    yt_api = YouTubeTranscriptApi()
    new_results = []
    still_failed = []

    print(
        f"Retrying {len(retry_ids)} video(s) "
        f"({DELAY_SECONDS}s base delay, up to {MAX_ATTEMPTS} attempts each)...\n"
    )

    for i, vid_id in enumerate(retry_ids):
        if i > 0:
            time.sleep(DELAY_SECONDS)

        url = url_map.get(vid_id, f"https://www.youtube.com/watch?v={vid_id}")
        try:
            transcript = fetch_transcript(vid_id, url, yt_api)
            source = "yt-dlp" if any(
                (SUBS_DIR / f"{vid_id}.en.json3").exists()
                or list(SUBS_DIR.glob(f"{vid_id}*.json3"))
                for _ in [0]
            ) else "api"
            new_results.append({
                "video_id": vid_id,
                "video_url": url,
                "transcript": transcript,
            })
            print(f"OK — {vid_id}" + (f" (via {source})" if source == "yt-dlp" else ""))
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            still_failed.append({"video_id": vid_id, "error": str(e)})
            print(f"NO TRANSCRIPT — {vid_id}")
        except VideoUnavailable:
            still_failed.append({"video_id": vid_id, "error": "unavailable"})
            print(f"UNAVAILABLE — {vid_id}")
        except Exception as e:
            still_failed.append({"video_id": vid_id, "error": str(e)})
            print(f"ERROR — {vid_id}: {type(e).__name__}")

    merged = existing + [
        entry for entry in new_results if entry["video_id"] not in existing_ids
    ]

    TRANSCRIPTS_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    FAILED_FILE.write_text(
        json.dumps(still_failed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nDone.")
    print(f"Retry succeeded: {len(new_results)}")
    print(f"Still failed: {len(still_failed)}")
    print(f"Total transcripts now: {len(merged)}")

    if still_failed:
        print(
            "\nYouTube is still rate-limiting this IP. "
            "Wait 1–2 hours, then run: python extract_transcripts_retry.py"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
