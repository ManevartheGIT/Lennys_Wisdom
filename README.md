# 🎙️ Lenny's Wisdom: The Definitive MCP Server for Lenny's Podcast

[![MCP](https://img.shields.io/badge/MCP-1.0-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)

**Lenny's Wisdom** is the most comprehensive **Model Context Protocol (MCP) server** designed specifically for **Lenny's Podcast** and the **Lenny's Newsletter** ecosystem. 

Search through over **300+ high-quality transcripts** featuring world-class product leaders, growth experts, and founders. Whether you are using **Claude Desktop**, **Cursor**, or **Anti-Gravity**, this server provides instant, structured access to the world's best product management and growth wisdom.

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

### **Anti-Gravity / Cursor Configuration**

The configuration is identical for both **Anti-Gravity** and **Cursor**. 

#### **Cursor Setup:**
1. Open **Cursor Settings** (Settings icon or `Cmd + Shift + J`).
2. Navigate to **Features** > **MCP**.
3. Click **+ Add New MCP Server**.
4. Enter the following details:
   - **Name:** `lennys-wisdom`
   - **Type:** `command`
   - **Command:**
     ```bash
     uv --directory "<ABSOLUTE_PATH_TO_PROJECT_ROOT>" run python -m src.server
     ```

#### **JSON Configuration (Claude Desktop / mcp_config.json):**
```json
{
  "mcpServers": {
    "lennys-wisdom": {
      "command": "uv",
      "args": [
        "--directory",
        "<ABSOLUTE_PATH_TO_PROJECT_ROOT>",
        "run",
        "python",
        "-m",
        "src.server"
      ]
    }
  }
}
```


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
