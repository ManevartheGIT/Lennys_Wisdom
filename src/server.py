from typing import List, Optional
from fastmcp import FastMCP
from src.config import settings
from src.data.store import SQLiteStore
from src.models.schemas import EpisodeSummary, Transcript

# Initialize the MCP server
mcp = FastMCP("LennysWisdom")

# Initialize the data store (read-only mode for safety in the server)
store = SQLiteStore(str(settings.DATABASE_PATH))
# We assume the database is already initialized by the orchestrator
# but we call initialize() just in case the tables don't exist
store.initialize()

@mcp.tool()
def search_episodes(query: str, limit: int = 10) -> List[EpisodeSummary]:
    """
    Search for podcast episodes by keywords in the title, guest name, or summary.
    Returns a list of matching episodes with metadata.
    """
    return store.search_episodes(query, limit=limit)

@mcp.tool()
def get_transcript(episode_id: str) -> Optional[Transcript]:
    """
    Retrieve the full transcript for a specific episode using its ID (e.g., 'brian-chesky').
    Returns the transcript text and metadata.
    """
    return store.get_transcript(episode_id)

@mcp.tool()
def get_latest_episodes(limit: int = 10) -> List[EpisodeSummary]:
    """
    Retrieve the most recent 10-20 episodes from Lenny's Podcast.
    """
    return store.get_latest(limit=limit)

@mcp.resource("lenny://topics")
def get_all_topics() -> str:
    """
    List all available topics across all episodes (e.g., Product Management, Growth, AI).
    """
    topics = store.get_all_topics()
    return "\n".join(topics)

@mcp.resource("lenny://guests")
def get_all_guests() -> str:
    """
    A directory of all guests that have appeared on Lenny's Podcast.
    """
    guests = store.get_all_guests()
    return "\n".join(guests)

@mcp.resource("lenny://latest")
def get_latest_resource() -> str:
    """
    A list of the 10 most recent episodes for quick browsing.
    """
    latest = store.get_latest(limit=10)
    lines = [f"- {e.title} (Guest: {e.guest}) - {e.url}" for e in latest]
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()
