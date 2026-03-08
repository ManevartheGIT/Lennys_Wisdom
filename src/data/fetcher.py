import os
import subprocess
from typing import List, Dict, Any
from pathlib import Path
from src.data.interfaces import BaseFetcher

class GithubFetcher(BaseFetcher):
    def __init__(self, repo_url: str, local_dir: str):
        self.repo_url = repo_url
        self.local_dir = Path(local_dir)

    async def fetch_all_episodes(self) -> List[Dict[str, Any]]:
        """Clone or pull the repository and return paths to all transcript files."""
        if not self.local_dir.exists():
            print(f"Cloning repository: {self.repo_url} to {self.local_dir}")
            subprocess.run(["git", "clone", self.repo_url, str(self.local_dir)], check=True)
        else:
            print(f"Updating repository in {self.local_dir}")
            subprocess.run(["git", "-C", str(self.local_dir), "pull"], check=True)

        episodes_dir = self.local_dir / "episodes"
        transcript_files = []

        for guest_dir in episodes_dir.iterdir():
            if guest_dir.is_dir():
                transcript_path = guest_dir / "transcript.md"
                if transcript_path.exists():
                    transcript_files.append({
                        "path": str(transcript_path),
                        "episode_id": guest_dir.name
                    })

        return transcript_files

    async def check_for_updates(self) -> List[Dict[str, Any]]:
        """In v1.0, we just re-run fetch_all_episodes."""
        return await self.fetch_all_episodes()
