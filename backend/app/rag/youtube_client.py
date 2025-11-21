from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from app.rag.youtube_id_extractor import youtube_id_extractor 


def extract_video_id(url_or_id: str) -> str:
    """
    Accepts either a full YouTube URL or a bare video id and returns the id.
    """
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        return youtube_id_extractor(url_or_id)
    return url_or_id


def fetch_transcript_text(video_id: str, language: str = "en") -> Optional[str]:
    """
    Fetches transcript as a single string. Returns None if no transcript.
    """
    try:
        print("Fetching transcript...")
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=[language])

        if not fetched_transcript:
            return None

        # Join all subtitle segments into a single text
        text = " ".join(snippet.text for snippet in fetched_transcript)
        return text

    except TranscriptsDisabled:
        print("Transcriptions are disabled on this video.")
        return None

    except NoTranscriptFound:
        print("No english transcriptions found of this video.")
        return None
