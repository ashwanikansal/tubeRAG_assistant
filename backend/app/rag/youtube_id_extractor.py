import re
from typing import Optional

def youtube_id_extractor(url: str) -> Optional[str]:
    """
    Extracts the YouTube video ID from many YouTube URL formats.
    Returns the video ID, or raises ValueError if invalid.
    """

    # Try matching all common YouTube URL patterns
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",              # typical ?v=ID
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",      # youtu.be/ID
        r"(?:shorts/)([A-Za-z0-9_-]{11})",         # shorts/ID
        r"(?:embed/)([A-Za-z0-9_-]{11})",          # embed/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            print("Video ID : ",match.group(1))
            return match.group(1)

    # If nothing matched
    raise ValueError("Invalid YouTube URL or video ID")