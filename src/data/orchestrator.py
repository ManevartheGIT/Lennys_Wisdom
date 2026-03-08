import asyncio
import logging
from src.config import settings
from src.data.fetcher import GithubFetcher
from src.data.parser import TranscriptParser
from src.data.store import SQLiteStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IngestionOrchestrator:
    def __init__(self):
        self.fetcher = GithubFetcher(settings.GITHUB_REPO_URL, str(settings.TRANSCRIPTS_REPO_PATH))
        self.parser = TranscriptParser()
        self.store = SQLiteStore(str(settings.DATABASE_PATH))

    async def run(self):
        """Build the complete knowledge base from the GitHub repo."""
        # 1. Setup the database
        logger.info("Initializing database...")
        self.store.initialize()

        # 2. Fetch all raw data (clones/pulls repo)
        logger.info(f"Fetching transcripts from {settings.GITHUB_REPO_URL}...")
        try:
            raw_episodes = await self.fetcher.fetch_all_episodes()
            logger.info(f"Found {len(raw_episodes)} potential episodes.")
        except Exception as e:
            logger.error(f"Failed to fetch transcripts: {e}")
            return

        # 3. Parse and save each episode
        count = 0
        for raw_data in raw_episodes:
            try:
                episode = self.parser.parse_episode(raw_data)
                transcript = self.parser.parse_transcript(raw_data, episode.id)
                self.store.save_episode(episode, transcript)
                count += 1
                if count % 10 == 0:
                    logger.info(f"Progress: {count} episodes ingested...")
            except Exception as e:
                logger.error(f"Failed to ingest {raw_data.get('episode_id')}: {e}")

        logger.info(f"Ingestion complete. Total episodes: {count}")

if __name__ == "__main__":
    orchestrator = IngestionOrchestrator()
    asyncio.run(orchestrator.run())
