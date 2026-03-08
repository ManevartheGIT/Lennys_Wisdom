import re
import frontmatter
from datetime import date
from typing import Dict, Any, List
from src.models.schemas import EpisodeSummary, Transcript, Segment, Link
from src.data.interfaces import BaseParser

class TranscriptParser(BaseParser):
    def parse_episode(self, raw_data: Dict[str, Any]) -> EpisodeSummary:
        """Parse raw metadata from YAML frontmatter into EpisodeSummary."""
        path = raw_data["path"]
        episode_id = raw_data["episode_id"]
        
        post = frontmatter.load(path)
        metadata = post.metadata

        return EpisodeSummary(
            id=episode_id,
            title=metadata.get("title", "Unknown Title"),
            guest=metadata.get("guest", "Unknown Guest"),
            guest_role=metadata.get("guest_role", ""),
            guest_company=metadata.get("guest_company", ""),
            date=metadata.get("publish_date", date.today()),
            duration=str(metadata.get("duration", "00:00")),
            topics=metadata.get("topics", []),
            view_count=metadata.get("view_count", 0),
            summary=metadata.get("description", ""),
            url=metadata.get("youtube_url", "https://youtube.com"),
            transcript_available=True
        )

    def parse_transcript(self, raw_data: Dict[str, Any], episode_id: str) -> Transcript:
        """Parse transcript text into segments based on [HH:MM:SS] timestamps."""
        path = raw_data["path"]
        post = frontmatter.load(path)
        content = post.content

        # Regex for [00:00:00] or [00:00]
        timestamp_pattern = r"\[(\d{1,2}:\d{2}(?::\d{2})?)\]"
        
        parts = re.split(timestamp_pattern, content)
        
        segments = []
        if len(parts) > 1:
            for i in range(1, len(parts), 2):
                start_time = parts[i]
                text = parts[i+1].strip() if i+1 < len(parts) else ""
                # Use next timestamp as end time, or the same if it's the last one
                end_time = parts[i+2] if i+2 < len(parts) else start_time
                
                segments.append(Segment(
                    start_time=start_time,
                    end_time=end_time,
                    text=text
                ))

        return Transcript(
            episode_id=episode_id,
            full_text=content,
            segments=segments,
            referenced_links=[]
        )
