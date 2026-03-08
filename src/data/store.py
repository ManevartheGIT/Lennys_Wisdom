import sqlite_utils
import sqlite3
from typing import List, Optional, Dict, Any
from pathlib import Path
from src.models.schemas import EpisodeSummary, Transcript, Segment
from src.data.interfaces import BaseStore

class SQLiteStore(BaseStore):
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        # Create directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Create a connection that can be used across multiple threads (standard for MCP tool servers)
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.db = sqlite_utils.Database(conn)

    def initialize(self):
        """Setup tables and FTS indexing."""
        if not self.db["episodes"].exists():
            self.db["episodes"].create(
                {
                    "id": str, 
                    "title": str, 
                    "guest": str, 
                    "guest_role": str, 
                    "guest_company": str, 
                    "date": str, 
                    "duration": str, 
                    "view_count": int, 
                    "summary": str, 
                    "url": str,
                    "transcript_available": int, # 1 for True, 0 for False
                    "topics": str # Store list as JSON string
                },
                pk="id"
            )
            self.db["transcripts"].create(
                {"episode_id": str, "full_text": str},
                pk="episode_id",
                foreign_keys=[("episode_id", "episodes", "id")]
            )
            # Enable Full-Text Search
            self.db["transcripts"].enable_fts(["full_text"], create_triggers=True)
            self.db["episodes"].enable_fts(["title", "guest", "summary"], create_triggers=True)

    def save_episode(self, episode: EpisodeSummary, transcript: Transcript):
        """Save episode and transcript atomically."""
        data = episode.model_dump(mode="json")
        # Ensure topics are stored correctly in SQLite
        if isinstance(data.get("topics"), list):
            import json
            data["topics"] = json.dumps(data["topics"])
            
        with self.db.conn:
            self.db["episodes"].insert(data, pk="id", replace=True)
            self.db["transcripts"].insert(
                transcript.model_dump(mode="json", include={"episode_id", "full_text"}), 
                pk="episode_id", 
                replace=True
            )

    def search_episodes(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> List[EpisodeSummary]:
        """Search episodes using FTS ranking."""
        results = []
        import json
        for row in self.db["episodes"].search(query, limit=limit):
            if "topics" in row and isinstance(row["topics"], str):
                row["topics"] = json.loads(row["topics"])
            results.append(EpisodeSummary.model_validate(row))
        return results

    def get_transcript(self, episode_id: str) -> Optional[Transcript]:
        """Retrieve a full transcript by ID."""
        try:
            row = self.db["transcripts"].get(episode_id)
            # For now, we return the full text. Segment logic can be added in v1.1
            return Transcript(
                episode_id=row["episode_id"],
                full_text=row["full_text"],
                segments=[]
            )
        except sqlite_utils.db.NotFoundError:
            return None

    def get_all_topics(self) -> List[str]:
        """Collect all unique topics from metadata."""
        import json
        topics = set()
        for row in self.db["episodes"].rows:
            t_list = row.get("topics")
            if t_list:
                topics.update(json.loads(t_list))
        return sorted(list(topics))

    def get_all_guests(self) -> List[str]:
        """Collect all unique guest names."""
        return sorted(list(set([row["guest"] for row in self.db["episodes"].rows])))

    def get_latest(self, limit: int = 10) -> List[EpisodeSummary]:
        """Retrieve the most recent episodes sorted by date."""
        import json
        rows = self.db["episodes"].rows_where(order_by="date desc", limit=limit)
        results = []
        for row in rows:
            if "topics" in row and isinstance(row["topics"], str):
                row["topics"] = json.loads(row["topics"])
            results.append(EpisodeSummary.model_validate(row))
        return results
