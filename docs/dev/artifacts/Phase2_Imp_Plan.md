# Phase 2: Proposal & Business Development

## Goal Description

Implement the "Proposal Writer Agent" to automate the creation of technical proposals.
This agent will use RAG (Retrieval Augmented Generation) to access TDC's past proposals, CVs, and technical methodology, ensuring new proposals match the firm's style and experience.

## User Review Required

> [!IMPORTANT]
>
> - **Vector Database**: We will use ChromaDB (local) for storing embeddings of past proposals.
> - **Privacy**: Ensure scanned PDFs do not contain PII if processed by external LLMs.

## Proposed Changes

### Core Infrastructure

#### [NEW] [src/core/rag_engine.py](file:///home/deployer/projects/tdc-agent-platform/src/core/rag_engine.py)

- `ingest_document(path)`: Reads PDF/Docx, chunks text, creates embeddings.
- `query_knowledge_base(query)`: Returns top-k relevant context chunks.

### Tools Layer

#### [NEW] [src/tools/proposal_tools.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/proposal_tools.py)

- `search_past_proposals(keyword)`: Wraps RAG engine.
- `get_consultant_cv(skill_set)`: specific lookup for staff CVs.

### Agents

#### [NEW] [src/agents/proposal_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/proposal_agent.py)

- Role: "Senior Proposal Writer".
- Capabilities: Drafting methodology, matching CVs to ToR (Terms of Reference).
- Logic: `analyze_tor` -> `search_similar_projects` -> `draft_section`.

### API

#### [NEW] [src/api/routes/proposal_routes.py](file:///home/deployer/projects/tdc-agent-platform/src/api/routes/proposal_routes.py)

- `POST /proposal/draft`: Input ToR text -> Output Draft Proposal Markdown.

## Verification Plan

### Automated Tests

- **Unit**: `pytest tests/core/test_rag_engine.py` (Mock embeddings).
- **Integration**: Ingest a dummy PDF -> Query it -> Verify exact text retrieval.

### Manual Verification

- Upload a sample "DHIS2 Training ToR" (text file).
- Ask Agent: "Draft the methodology section based on our past work."
- Verify the output cites/uses phrases from the ingested dummy PDF.
