# Phase 2 Implementation Walkthrough

## Overview

This document provides a comprehensive walkthrough of the Phase 2 implementation for the TDC Agent Platform - Proposal & Business Development.

**Implemented:** 2026-03-11

---

## Architecture

### Components Created

```
src/
├── core/
│   └── rag_engine.py          # RAG Engine with ChromaDB
├── tools/
│   └── proposal_tools.py       # Proposal search & CV lookup tools
├── agents/
│   └── proposal_agent.py      # Proposal Writer Agent
└── api/
    └── routes/
        └── proposal_routes.py # API endpoints
```

---

## RAG Engine (`src/core/rag_engine.py`)

### Purpose
Provides document ingestion and semantic search capabilities using ChromaDB vector database.

### Key Functions

#### `ingest_document(file_path, document_type, metadata)`
- Reads PDF, DOCX, TXT, MD files
- Chunks text using RecursiveCharacterTextSplitter
- Creates embeddings using OpenAI or Ollama
- Stores in ChromaDB collection

**Parameters:**
- `file_path`: Path to document
- `document_type`: "proposal" or "cv"
- `metadata`: Optional dict with title, year, etc.

**Returns:**
```json
{
  "success": true,
  "document_type": "proposal",
  "file_name": "dhis2_training.pdf",
  "chunks_added": 15,
  "collection": "proposals"
}
```

#### `query_knowledge_base(query, document_type, top_k)`
- Embeds query text
- Searches ChromaDB for similar chunks
- Returns top-k results with metadata

**Parameters:**
- `query`: Search query string
- `document_type`: "proposal" or "cv"
- `top_k`: Number of results (default: 5)

**Returns:**
```json
[
  {
    "content": "relevant text chunk...",
    "metadata": {"title": "DHIS2 Training", "year": 2024},
    "distance": 0.15
  }
]
```

---

## Proposal Tools (`src/tools/proposal_tools.py`)

### Tools Available

| Tool | Description |
|------|-------------|
| `search_past_proposals` | Search past proposals by keyword |
| `get_consultant_cv` | Search consultant CVs by skill set |
| `ingest_proposal_document` | Upload proposal to knowledge base |
| `ingest_consultant_cv` | Upload CV to knowledge base |

### Usage Example

```python
from src.tools.proposal_tools import proposal_tools

# Search past proposals
result = await search_past_proposals("DHIS2 training", top_k=5)

# Find consultants
cv_result = await get_consultant_cv("Python, PostgreSQL, DHIS2")
```

---

## Proposal Writer Agent (`src/agents/proposal_agent.py`)

### Role
**Senior Proposal Writer** - Creates compelling, technically sound proposals.

### Agent Workflow

1. **Analyze ToR** - Understand client requirements
2. **Search Similar Projects** - Find relevant past proposals
3. **Match Consultants** - Identify suitable CVs
4. **Draft Sections** - Write methodology, implementation, team

### Tasks Available

| Task | Description |
|------|-------------|
| `analyze_tor()` | Parse and structure requirements |
| `search_similar_projects()` | Find relevant past work |
| `find_consultants()` | Match skills to requirements |
| `draft_proposal_section()` | Write specific section |
| `draft_full_proposal()` | Complete proposal draft |

### Integration

```python
from src.agents.proposal_agent import ProposalWriterAgent
from crewai import Crew

agent = ProposalWriterAgent()
task = agent.draft_full_proposal(tor_text)

crew = Crew(
    agents=[agent.get_agent()],
    tasks=[task]
)

result = crew.kickoff()
```

---

## API Routes (`src/api/routes/proposal_routes.py`)

### Endpoints

#### POST `/proposal/draft`
Draft a proposal from Terms of Reference.

**Request:**
```json
{
  "tor_text": "Training for 20 Ministry staff on DHIS2...",
  "section": "methodology"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "proposal": "## Methodology\n\nBased on TDC's proven approach...",
  "section": "full_proposal"
}
```

#### POST `/proposal/ingest`
Upload document to knowledge base.

**Form Data:**
- `file`: File upload
- `document_type`: "proposal" | "cv"
- `title`: (for proposals)
- `year`: (for proposals)
- `consultant_name`: (for CVs)
- `expertise`: (for CVs)

#### GET `/proposal/search`
Search past proposals.

**Query Params:** `keyword`, `top_k`

#### GET `/proposal/consultants`
Search consultant CVs.

**Query Params:** `skills`, `top_k`

#### GET `/proposal/documents`
List indexed documents.

**Query Params:** `document_type`

---

## Database Schema

### ChromaDB Collections

#### `proposals`
Stores past proposal documents.

#### `consultant_cvs`
Stores consultant CVs.

---

## Dependencies Added

```txt
pypdf>=4.0.0        # PDF parsing
python-docx>=1.0.0   # DOCX parsing
chromadb             # Vector database (already present)
```

---

## Usage Flow

### 1. Ingest Documents
```bash
# Upload a past proposal
curl -X POST http://localhost:8000/api/v1/proposal/ingest \
  -F "file=@proposal.pdf" \
  -F "document_type=proposal" \
  -F "title=DHIS2 Training 2024" \
  -F "year=2024"
```

### 2. Draft Proposal
```bash
curl -X POST http://localhost:8000/api/v1/proposal/draft \
  -H "Content-Type: application/json" \
  -d '{
    "tor_text": "Training for 20 Ministry staff on DHIS2 data analysis and visualization..."
  }'
```

### 3. Search Past Proposals
```bash
curl "http://localhost:8000/api/v1/proposal/search?keyword=DHIS2&top_k=5"
```

### 4. Find Consultants
```bash
curl "http://localhost:8000/api/v1/proposal/consultants?skills=Python,PostgreSQL"
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Unsupported file type` | Invalid extension | Use PDF, DOCX, TXT, MD |
| `No text extracted` | Empty file | Check file content |
| `Collection not found` | ChromaDB not initialized | Restart with ChromaDB |
| `Embedding failed` | No API key | Set OPENAI_API_KEY |

---

## Testing

### Manual Test

1. Start the backend:
```bash
uvicorn src.api.main:app --reload
```

2. Upload a test document:
```bash
curl -X POST http://localhost:8000/api/v1/proposal/ingest \
  -F "file=@samples/dhis2_tor.txt" \
  -F "document_type=proposal" \
  -F "title=DHIS2 ToR" \
  -F "year=2024"
```

3. Search:
```bash
curl "http://localhost:8000/api/v1/proposal/search?keyword=DHIS2"
```

4. Draft proposal:
```bash
curl -X POST http://localhost:8000/api/v1/proposal/draft \
  -H "Content-Type: application/json" \
  -d '{"tor_text": "Train Ministry staff on DHIS2"}'
```

---

## Notes

- ChromaDB persists to `./chroma_db` by default
- Embeddings use OpenAI text-embedding-3-small by default
- Falls back to Ollama if configured in environment
- Documents are chunked with 1000 chars overlap 200
