# 🎙️ Lenny's Wisdom MCP Server

A high-performance [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server providing AI assistants with structured access to **Lenny Rachitsky's** podcast transcripts, guest insights, and product/growth frameworks.

Built with **Python**, **FastMCP**, and **SQLite (FTS5)**. Optimized for local use and CI/CD-driven "Build-Time Database" deployments.

---

## 🚀 Features

- **⚡ Instant Search:** Full-text search across 300+ episodes using SQLite's FTS5 engine.
- **📜 Transcript Retrieval:** Fetch full transcripts or specific segments by episode ID.
- **🗂️ Rich Resources:** Browse the knowledge base by topics, guest directories, or latest releases.
- **🔄 Auto-Ingestion:** A unified pipeline that clones the latest transcripts from GitHub and indexes them automatically.
- **🛠️ Schema-Driven:** Built according to the *2026 Agentic Software Engineering Standard* for modularity and reliability.

---

## 🛠️ Tech Stack

- **Runtime:** [uv](https://docs.astral.sh/uv/) (Python 3.12+)
- **Server:** [FastMCP](https://github.com/jlowin/fastmcp)
- **Database:** SQLite with `sqlite-utils` for Full-Text Search
- **Data Source:** [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts)

---

## 📦 Installation & Setup

### 1. Prerequisites
Ensure you have `uv` installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Initialize
```bash
git clone <your-repo-url>
cd Lennys_Wisdom
uv sync
```

### 3. Build the Knowledge Base
This will clone the transcripts and build the `lenny.db` file locally:
```bash
uv run python -m src.data.orchestrator
```

---

## 🔌 MCP Configuration

### **Anti-Gravity Configuration**
Add the following to your Anti-Gravity MCP configuration file (usually found in your settings or `mcp_config.json`):

```json
{
  "mcpServers": {
    "lennys-wisdom": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/ananthavijaya/Library/CloudStorage/GoogleDrive-ananthavijaya@gmail.com/My Drive/Projects/Lennys_Wisdom",
        "run",
        "python",
        "-m",
        "src.server"
      ]
    }
  }
}
```

### **Claude Desktop / Cursor**
The configuration is identical to the above. Ensure the path to the project directory is absolute.

---

## 🧰 Available Tools & Resources

### **Tools**
- `search_episodes(query: str)`: Full-text search across titles, guests, and summaries.
- `get_transcript(episode_id: str)`: Retrieve the full transcript for an episode (e.g., `brian-chesky`).
- `get_latest_episodes(limit: int)`: Feed of the most recent podcast releases.

### **Resources**
- `lenny://topics`: A complete taxonomy of product, growth, and AI topics.
- `lenny://guests`: A directory of every guest who has appeared on the show.
- `lenny://latest`: A quick-glance list of the 10 most recent episodes.

---

## 📂 Project Structure

```text
├── src/
│   ├── data/           # Fetcher, Parser, and SQLite Store logic
│   ├── models/         # Pydantic schemas (Source of Truth)
│   ├── config.py       # Environment configuration
│   └── server.py       # MCP Server entry point
├── data/               # Local cache & SQLite database (Gitignored)
├── architecture.md     # Detailed implementation mapping
└── techspec.md         # Original product requirements
```

---

## 📜 Data Rationale (Build-Time DB)
This server uses a **Build-Time Database** strategy. Ingestion happens during CI/CD (GitHub Actions), producing a static `lenny.db` file. This ensures zero-latency searches and zero-cost hosting on platforms like Vercel or Netlify.
