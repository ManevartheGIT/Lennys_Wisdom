from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.models.schemas import EpisodeSummary, Transcript, GuestProfile, Insight

class BaseFetcher(ABC):
    @abstractmethod
    async def fetch_all_episodes(self) -> List[Dict[str, Any]]:
        """Fetch all raw episode data from the source (e.g., GitHub)."""
        pass

    @abstractmethod
    async def check_for_updates(self) -> List[Dict[str, Any]]:
        """Check for new or modified episodes since the last fetch."""
        pass

class BaseParser(ABC):
    @abstractmethod
    def parse_episode(self, raw_data: Dict[str, Any]) -> EpisodeSummary:
        """Parse raw metadata into an EpisodeSummary model."""
        pass

    @abstractmethod
    def parse_transcript(self, raw_data: Dict[str, Any], episode_id: str) -> Transcript:
        """Parse raw content into a Transcript model with segments."""
        pass

class BaseStore(ABC):
    @abstractmethod
    def initialize(self):
        """Setup the database schema."""
        pass

    @abstractmethod
    def save_episode(self, episode: EpisodeSummary, transcript: Transcript):
        """Atomically save an episode and its transcript to the store."""
        pass

    @abstractmethod
    def search_episodes(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> List[EpisodeSummary]:
        """Search episodes by keyword and filters."""
        pass

    @abstractmethod
    def get_transcript(self, episode_id: str) -> Optional[Transcript]:
        """Retrieve a full transcript by ID."""
        pass

    @abstractmethod
    def get_all_topics(self) -> List[str]:
        """Retrieve a list of all unique topics."""
        pass

    @abstractmethod
    def get_all_guests(self) -> List[str]:
        """Retrieve a list of all guest names."""
        pass

    @abstractmethod
    def get_latest(self, limit: int = 10) -> List[EpisodeSummary]:
        """Retrieve the most recent episodes."""
        pass
