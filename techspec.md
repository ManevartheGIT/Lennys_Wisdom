# MCP Server Specification: Lenny's Knowledge Base

---

## 1. Overview

| Field | Details |
|-------|---------|
| **Project Name** | `lennys-mcp-server` |
| **Purpose** | Provide AI assistants with structured access to Lenny Rachitsky's podcast transcripts, newsletter articles, and curated resources via the Model Context Protocol (MCP). |
| **Target Users** | AI coding agents, product managers, researchers, and business professionals seeking insights from Lenny's content. |
| **Tech Stack** | Python 3.11+, FastMCP, SQLite/PostgreSQL, HTTP client libraries. |

---

## 2. Core Requirements

### 2.1 Data Sources to Integrate

| Source | Priority | Format | Update Frequency |
|--------|----------|--------|-----------------|
| Podcast Transcripts (GitHub) | P0 | Markdown/JSON | Weekly |
| Podcast Metadata (YouTube/Apple) | P0 | JSON/API | Weekly |
| Newsletter Articles | P1 | HTML/Markdown | Weekly |
| Community Tools Index | P2 | JSON | Monthly |
| Guest Information | P1 | Structured JSON | Weekly |

### 2.2 Functional Requirements

- **Search:** Full-text search across transcripts, articles, and show notes
- **Semantic Retrieval:** Vector search for conceptually related content (optional v1.1)
- **Filtering:** By topic, guest, date, company, role, episode duration
- **Summarization:** On-the-fly summarization of episodes or segments
- **Citation:** Return source URLs and timestamps for all information
- **Recommendations:** Suggest related episodes based on topics

---

## 3. Architecture

### 3.1 System Diagram

```
┌─────────────────┐
│   MCP Client    │ (Claude, Cursor, etc.)
│   (AI Agent)    │
└────────┬────────┘
         │ MCP Protocol (stdio/sse)
         ▼
┌─────────────────┐
│  FastMCP Server │
│  (Python)       │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌──────────┐
│SQLite │  │ External │
│Cache  │  │ APIs     │
└───────┘  └──────────┘
```

### 3.2 Data Pipeline

1. **Ingestion:** Fetch from GitHub repo, newsletter RSS, YouTube API
2. **Processing:** Parse transcripts, extract metadata, chunk text
3. **Storage:** SQLite for local cache, JSON for raw data
4. **Serving:** FastMCP tools and resources

---

## 4. MCP Interface Specification

### 4.1 Tools (Functions)

#### `search_episodes`
Search podcast episodes by keywords, topics, or guest names.

```python
@tool
def search_episodes(
    query: str,
    filters: Optional[dict] = None,  # {topic: str, guest: str, date_range: tuple}
    limit: int = 10
) -> list[EpisodeSummary]:
    """
    Returns: List of episodes with title, guest, date, topics, snippet, url
    """
```

#### `get_transcript`
Retrieve full transcript for a specific episode.

```python
@tool
def get_transcript(
    episode_id: str,  # YouTube ID or slug
    include_timestamps: bool = True,
    segment_start: Optional[str] = None,  # "MM:SS" format
    segment_end: Optional[str] = None
) -> Transcript:
    """
    Returns: Full text, timestamps, guest info, referenced links
    """
```

#### `get_episode_insights`
Extract key frameworks, books, and actionable advice from an episode.

```python
@tool
def get_episode_insights(
    episode_id: str,
    insight_type: Literal["frameworks", "books", "quotes", "tools"] = "all"
) -> Insights:
    """
    Returns: Structured insights with citations to timestamps
    """
```

#### `search_by_topic`
Browse episodes by curated topics (Product-Market Fit, AI/ML, Growth, etc.).

```python
@tool
def search_by_topic(
    topic: str,  # From predefined taxonomy
    subtopic: Optional[str] = None,
    sort_by: Literal["date", "relevance", "views"] = "date"
) -> list[EpisodeSummary]:
```

#### `get_guest_profile`
Get all episodes and key insights from a specific guest.

```python
@tool
def get_guest_profile(
    guest_name: str,
    include_companies: bool = True
) -> GuestProfile:
```

#### `get_newsletter_article`
Retrieve specific newsletter articles by URL or title search.

```python
@tool
def get_newsletter_article(
    query: str,  # Title keywords or exact URL
    include_archived: bool = True
) -> Article:
```

#### `recommend_episodes`
Get personalized recommendations based on interest areas.

```python
@tool
def recommend_episodes(
    interests: list[str],
    previously_viewed: list[str],
    count: int = 5
) -> list[EpisodeSummary]:
```

### 4.2 Resources (Static Content)

| Resource URI | Description |
|-------------|-------------|
| `lenny://topics` | List of all available topics and subtopics with episode counts. |
| `lenny://guests` | Directory of all guests with their roles, companies, and episode counts. |
| `lenny://frameworks` | Library of product/growth frameworks mentioned across episodes. |
| `lenny://books` | All books recommended by Lenny and guests with frequency counts. |
| `lenny://latest` | Most recent 10 episodes and articles (auto-updating). |

---

## 5. Data Models (Pydantic)

```python
class EpisodeSummary(BaseModel):
    id: str  # YouTube ID
    title: str
    guest: str
    guest_role: str
    guest_company: str
    date: date
    duration: str
    topics: list[str]
    view_count: int
    summary: str
    url: HttpUrl
    transcript_available: bool

class Transcript(BaseModel):
    episode_id: str
    full_text: str
    segments: list[Segment]  # Timestamped chunks
    referenced_links: list[Link]
    books_mentioned: list[Book]
    frameworks_mentioned: list[Framework]

class Segment(BaseModel):
    start_time: str  # "MM:SS"
    end_time: str
    text: str
    topics: list[str]

class GuestProfile(BaseModel):
    name: str
    bio: str
    current_role: str
    companies: list[Company]
    episodes: list[EpisodeSummary]
    key_insights: list[Insight]
    social_links: dict[str, HttpUrl]

class Insight(BaseModel):
    content: str
    episode_id: str
    timestamp: str
    context: str  # Surrounding text for context
```

---

## 6. Implementation Details

### 6.1 Project Structure

```
lennys-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py           # FastMCP app initialization
│   ├── tools/              # Tool implementations
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── transcripts.py
│   │   ├── insights.py
│   │   └── recommendations.py
│   ├── resources/          # Resource handlers
│   │   ├── __init__.py
│   │   ├── topics.py
│   │   └── guests.py
│   ├── models/             # Pydantic models
│   │   └── schemas.py
│   ├── data/               # Data layer
│   │   ├── fetcher.py      # GitHub/YouTube fetching
│   │   ├── parser.py       # Transcript parsing
│   │   └── store.py        # SQLite operations
│   └── utils/
│       └── helpers.py
├── data/                   # Local cache (gitignored)
│   ├── transcripts/
│   ├── articles/
│   └── lenny.db
├── tests/
├── pyproject.toml
├── README.md
└── .env.example
```

### 6.2 Key Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.11"
fastmcp = "^0.4.0"  # Or latest
pydantic = "^2.0"
httpx = "^0.27.0"
sqlite-utils = "^3.36"
markdownify = "^0.13"  # HTML to MD conversion
python-frontmatter = "^1.0"  # YAML frontmatter parsing
```

### 6.3 Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GITHUB_REPO_URL: str = "https://github.com/ChatPRD/lennys-podcast-transcripts"
    DATA_REFRESH_INTERVAL_HOURS: int = 24
    MAX_SEARCH_RESULTS: int = 20
    TRANSCRIPT_CHUNK_SIZE: int = 1000  # characters
    DEFAULT_DATABASE_PATH: str = "./data/lenny.db"
    
    class Config:
        env_file = ".env"
```

### 6.4 Data Ingestion Strategy

1. **Initial Load:** Clone GitHub repo, parse all JSON files into SQLite
2. **Incremental Updates:** Check repo commit history, fetch new/changed files
3. **Newsletter Scraping:** Use RSS feed or archive page parsing (respect robots.txt)
4. **Metadata Enrichment:** YouTube Data API for view counts, descriptions

---

## 7. Error Handling & Edge Cases

| Scenario | Handling |
|----------|----------|
| GitHub API rate limit | Implement exponential backoff, cache last known good state |
| Missing transcript | Return 404 with suggestion to check official archive |
| Malformed timestamp | Log warning, return raw text without segmentation |
| Guest name variations | Normalize names using alias mapping (e.g., "Lenny" vs "Leonard") |
| Large transcript (>100KB) | Implement pagination with `page` parameter |

---

## 8. Testing Strategy

- **Unit Tests:** Mock external APIs, test parsing logic
- **Integration Tests:** Test with sample transcript files
- **MCP Inspector:** Validate protocol compliance
- **Performance Tests:** Search latency <500ms for 10k episodes

---

## 9. Deployment Options

### 9.1 Local Development

```bash
# Stdio transport (for Claude Desktop)
python -m lennys_mcp_server

# SSE transport (for web clients)
python -m lennys_mcp_server --transport sse --port 8000
```

### 9.2 Configuration for Claude Desktop

```json
{
  "mcpServers": {
    "lennys-knowledge": {
      "command": "python",
      "args": ["-m", "lennys_mcp_server"],
      "env": {
        "LENNY_DATA_PATH": "/path/to/data"
      }
    }
  }
}
```

---

## 10. Future Enhancements (v1.1+)

- [ ] **Vector Search:** Embed transcripts with sentence-transformers
- [ ] **Audio Clips:** Generate/share specific timestamp audio segments
- [ ] **Community Notes:** Integration with community tools (Lenny Playbook, etc.)
- [ ] **Slack/Discord Bot:** MCP server as backend for chatbots
- [ ] **Analytics:** Track most-searched topics, popular guests

---

## 11. Success Criteria

- [ ] All 320+ transcripts searchable via `search_episodes`
- [ ] Transcript retrieval includes accurate timestamps
- [ ] Tool responses include source URLs for verification
- [ ] <1s response time for common queries
- [ ] Graceful degradation when offline (using cached data)

---

## Questions for Clarification

1. **Authentication:** Do you need API keys for YouTube/Data sources, or stick to public GitHub data only?
2. **Hosting:** Is this for local use only, or do you need a deployed server?
3. **Update frequency:** Real-time sync with GitHub or daily batch updates sufficient?
4. **Scope:** Focus on podcasts only, or include full newsletter articles (requires scraping)?
