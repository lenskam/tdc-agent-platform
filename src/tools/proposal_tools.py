import os
import json
import logging
from typing import Optional
from langchain_core.tools import tool
from ..core.rag_engine import rag_engine

logger = logging.getLogger(__name__)


class ProposalTools:
    @tool("search_past_proposals")
    def search_past_proposals(keyword: str, top_k: int = 5) -> str:
        """
        Searches past proposals and methodology documents for relevant content.

        Args:
            keyword: Keywords to search for (e.g., "DHIS2 training", "data migration")
            top_k: Number of top results to return (default: 5)

        Returns:
            JSON string with relevant proposal sections
        """
        try:
            result = rag_engine.search_past_proposals(keyword, top_k)
            return result
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return json.dumps({"error": str(e), "results": []})

    @tool("get_consultant_cv")
    def get_consultant_cv(skill_set: str, top_k: int = 3) -> str:
        """
        Searches consultant CVs for specific skills or expertise.

        Args:
            skill_set: Skills to search for (e.g., "DHIS2, Python, PostgreSQL")
            top_k: Number of top CVs to return (default: 3)

        Returns:
            JSON string with matching consultant profiles
        """
        try:
            result = rag_engine.get_consultant_cv(skill_set, top_k)
            return result
        except Exception as e:
            logger.error(f"CV search failed: {e}")
            return json.dumps({"error": str(e), "results": []})

    @tool("ingest_proposal_document")
    def ingest_proposal_document(file_path: str, title: str = "", year: int = 0) -> str:
        """
        Ingests a proposal document into the knowledge base for future retrieval.

        Args:
            file_path: Path to the document (PDF, DOCX, TXT, or MD)
            title: Title of the proposal
            year: Year of the proposal

        Returns:
            JSON string with ingestion status
        """
        if not os.path.exists(file_path):
            return json.dumps({"success": False, "error": "File not found"})

        metadata = {}
        if title:
            metadata["title"] = title
        if year:
            metadata["year"] = year

        try:
            result = rag_engine.ingest_document(
                file_path=file_path,
                document_type="proposal",
                metadata=metadata
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            return json.dumps({"success": False, "error": str(e)})

    @tool("ingest_consultant_cv")
    def ingest_consultant_cv(file_path: str, consultant_name: str = "", expertise: str = "") -> str:
        """
        Ingests a consultant CV into the knowledge base.

        Args:
            file_path: Path to the CV (PDF, DOCX, TXT, or MD)
            consultant_name: Name of the consultant
            expertise: Comma-separated expertise areas

        Returns:
            JSON string with ingestion status
        """
        if not os.path.exists(file_path):
            return json.dumps({"success": False, "error": "File not found"})

        metadata = {}
        if consultant_name:
            metadata["consultant_name"] = consultant_name
        if expertise:
            metadata["expertise"] = expertise

        try:
            result = rag_engine.ingest_document(
                file_path=file_path,
                document_type="cv",
                metadata=metadata
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"CV ingestion failed: {e}")
            return json.dumps({"success": False, "error": str(e)})


proposal_tools = [
    ProposalTools.search_past_proposals,
    ProposalTools.get_consultant_cv,
    ProposalTools.ingest_proposal_document,
    ProposalTools.ingest_consultant_cv,
]
