# Architecture & Feature Mapping: Lenny's Wisdom MCP

This document maps the implementation to the `techspec.md` to ensure feature alignment and prevent scope creep.

## 1. Core Architecture (Agentic Standard)

We follow **Schema-Driven Development (SDD)**. All components are bound by interfaces defined in `src/data/interfaces.py`.

| Component | Responsibility | Mapping to Tech Spec | Status |
|-----------|----------------|----------------------|--------|
| `src/models/schemas.py` | Pydantic data models | Section 5: Data Models | ✅ Completed |
| `src/data/interfaces.py` | Abstract Base Classes (Contracts) | Section 2.2: Functional Requirements | ✅ Completed |
| `src/data/fetcher.py` | GitHub transcript ingestion | Section 6.4: Ingestion Strategy | ✅ Completed |
| `src/data/parser.py` | YAML & Markdown parsing | Section 6.1: Project Structure | ✅ Completed |
| `src/data/store.py` | SQLite caching & search | Section 3.1: System Diagram | ✅ Completed |
| `src/server.py` | MCP Server Entry Point | Section 4: MCP Interface Spec | ✅ Completed |

---

## 2. Feature Mapping (v1.0 - Podcast First)

### 2.1 MCP Tools Implementation
| Tool Name | Status | Schema Used | Functional Target |
|-----------|--------|-------------|-------------------|
| `search_episodes` | ✅ Completed | `EpisodeSummary` | Full-text search across transcripts |
| `get_transcript` | ✅ Completed | `Transcript` | Detailed transcript retrieval |
| `get_latest_episodes`| ✅ Completed | `EpisodeSummary` | Feed of the most recent episodes |
| `get_episode_insights` | 🕒 Planned | `Insight` | Extract frameworks, books, advice |
| `search_by_topic` | 🕒 Planned | `EpisodeSummary` | Filtered browsing by taxonomy |
| `get_guest_profile` | 🕒 Planned | `GuestProfile` | Guest history and bios |

### 2.2 MCP Resources Implementation
| URI | Status | Description |
|-----|--------|-------------|
| `lenny://topics` | ✅ Completed | List of unique topics from `src/data/store.py` |
| `lenny://guests` | ✅ Completed | List of all guests from `src/data/store.py` |
| `lenny://latest` | ✅ Completed | Top 10 recent episodes |

## 3. Data Strategy & Rationale

### 3.1 The "Build-Time Database" Pattern
We have chosen **SQLite** as the primary storage engine, even for potential cloud deployment (Vercel/Netlify).

**Rationale:**
- **Zero Latency:** The database file sits on the same "disk" as the server, eliminating network round-trips to external DBs (like Supabase).
- **CI/CD Driven Ingestion:** Our GitHub Actions (CI/CD) acts as the "Ingestion Worker." It fetches transcripts, parses them, and builds a fresh `lenny.db` snapshot on every deployment.
- **Portability:** The entire knowledge base is a single file, making it easy to version-control and deploy as a static asset.
- **Cost-Effective:** Zero infrastructure costs for a dedicated database server.

---

## 4. Scope Control & Deviations

### ✅ In Scope (v1.0)
- **Primary Source:** [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts)
- **Storage:** SQLite with `sqlite-utils` for FTS (Full-Text Search)
- **Transport:** stdio (Claude Desktop/Cursor)

### ❌ Deferred (v1.1+)
- **Newsletter Scraping:** Postponed (Requires robust HTML parsing/authentication)
- **Vector Search:** Postponed (Semantic search with sentence-transformers)
- **Detailed Insight Extraction:** Postponed (Requires LLM processing during ingestion)
