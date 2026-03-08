from datetime import date
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, HttpUrl, Field

class EpisodeSummary(BaseModel):
    id: str  # YouTube ID
    title: str
    guest: str
    guest_role: str
    guest_company: str
    date: date
    duration: str
    topics: List[str]
    view_count: int = 0
    summary: str
    url: Optional[HttpUrl] = None
    transcript_available: bool = True

class Segment(BaseModel):
    start_time: str  # "MM:SS" or "HH:MM:SS"
    end_time: str
    text: str
    topics: List[str] = []

class Link(BaseModel):
    title: str
    url: HttpUrl

class Book(BaseModel):
    title: str
    author: Optional[str] = None
    url: Optional[HttpUrl] = None

class Framework(BaseModel):
    name: str
    description: Optional[str] = None

class Transcript(BaseModel):
    episode_id: str
    full_text: str
    segments: List[Segment]
    referenced_links: List[Link] = []
    books_mentioned: List[Book] = []
    frameworks_mentioned: List[Framework] = []

class Company(BaseModel):
    name: str
    role: Optional[str] = None

class Insight(BaseModel):
    content: str
    episode_id: str
    timestamp: str
    context: str  # Surrounding text for context

class GuestProfile(BaseModel):
    name: str
    bio: str
    current_role: str
    companies: List[Company] = []
    episodes: List[EpisodeSummary] = []
    key_insights: List[Insight] = []
    social_links: Dict[str, HttpUrl] = {}
