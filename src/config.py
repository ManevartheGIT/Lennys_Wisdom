from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Data Sources
    GITHUB_REPO_URL: str = "https://github.com/ChatPRD/lennys-podcast-transcripts"
    DATA_PATH: Path = Path("./data")
    TRANSCRIPTS_REPO_PATH: Path = Path("./data/repo")
    DATABASE_PATH: Path = Path("./data/lenny.db")

    # Search and Pagination
    MAX_SEARCH_RESULTS: int = 20
    TRANSCRIPT_CHUNK_SIZE: int = 1000  # characters

    # Update Interval
    DATA_REFRESH_INTERVAL_HOURS: int = 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
