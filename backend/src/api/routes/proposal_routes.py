import os
import json
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from ...agents.proposal_agent import ProposalWriterAgent
from ...core.rag_engine import rag_engine
from crewai import Crew

logger = logging.getLogger(__name__)

router = APIRouter()


class ProposalDraftRequest(BaseModel):
    tor_text: str
    section: Optional[str] = None


class DocumentIngestRequest(BaseModel):
    file_path: str
    document_type: str
    title: Optional[str] = None
    year: Optional[int] = None
    consultant_name: Optional[str] = None
    expertise: Optional[str] = None


@router.post("/proposal/draft")
async def draft_proposal(request: ProposalDraftRequest):
    """
    Draft a proposal or specific section based on Terms of Reference.
    
    - If `section` is provided, drafts only that section
    - If `section` is omitted, drafts a full proposal
    """
    try:
        agent = ProposalWriterAgent()

        if request.section:
            task = agent.draft_proposal_section(request.section, request.tor_text)
        else:
            task = agent.draft_full_proposal(request.tor_text)

        crew = Crew(
            agents=[agent.get_agent()],
            tasks=[task]
        )

        result = crew.kickoff()

        return {
            "success": True,
            "proposal": result,
            "section": request.section or "full_proposal"
        }

    except Exception as e:
        logger.error(f"Proposal drafting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proposal/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    title: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    consultant_name: Optional[str] = Form(None),
    expertise: Optional[str] = Form(None)
):
    """
    Upload and ingest a document into the knowledge base.
    
    - document_type: "proposal" or "cv"
    - For proposals: provide title and year
    - For CVs: provide consultant_name and expertise
    """
    try:
        upload_dir = "./uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        metadata = {}
        if title:
            metadata["title"] = title
        if year:
            metadata["year"] = year
        if consultant_name:
            metadata["consultant_name"] = consultant_name
        if expertise:
            metadata["expertise"] = expertise

        result = rag_engine.ingest_document(
            file_path=file_path,
            document_type=document_type,
            metadata=metadata if metadata else None
        )

        os.remove(file_path)

        return result

    except Exception as e:
        logger.error(f"Document ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proposal/search")
async def search_proposals(keyword: str, top_k: int = 5):
    """
    Search past proposals for relevant content.
    """
    try:
        result = rag_engine.search_past_proposals(keyword, top_k)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proposal/consultants")
async def search_consultants(skills: str, top_k: int = 3):
    """
    Search consultant CVs by skills.
    """
    try:
        result = rag_engine.get_consultant_cv(skills, top_k)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proposal/documents")
async def list_documents(document_type: str = "proposal"):
    """
    List all indexed documents.
    """
    try:
        docs = rag_engine.list_documents(document_type)
        return {"documents": docs, "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
