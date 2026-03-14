import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

logger = logging.getLogger(__name__)

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
COLLECTION_PROPOSALS = "proposals"
COLLECTION_CVS = "consultant_cvs"


class RAGEngine:
    """
    RAG (Retrieval Augmented Generation) Engine using ChromaDB for vector storage.
    Manages ingestion of documents and querying for relevant context.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        self._setup_collections()

    def _setup_collections(self):
        try:
            self.proposals_collection = self.client.get_or_create_collection(
                name=COLLECTION_PROPOSALS,
                metadata={"description": "Past proposals and methodology documents"}
            )
        except Exception as e:
            logger.warning(f"Collection setup issue: {e}")
            self.proposals_collection = self.client.create_collection(
                name=COLLECTION_PROPOSALS,
                metadata={"description": "Past proposals and methodology documents"}
            )

        try:
            self.cvs_collection = self.client.get_or_create_collection(
                name=COLLECTION_CVS,
                metadata={"description": "Consultant CVs and skill profiles"}
            )
        except Exception as e:
            logger.warning(f"CV collection setup issue: {e}")
            self.cvs_collection = self.client.create_collection(
                name=COLLECTION_CVS,
                metadata={"description": "Consultant CVs and skill profiles"}
            )

    def _get_embeddings(self):
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        if provider == "ollama":
            return OllamaEmbeddings(
                model=os.getenv("OLLAMA_MODEL", "llama3"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def _read_file(self, file_path: str) -> str:
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext == ".pdf":
            return self._read_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self._read_docx(file_path)
        elif ext in [".txt", ".md"]:
            return path.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _read_pdf(self, file_path: str) -> str:
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            logger.error("pypdf not installed. Run: pip install pypdf")
            raise

    def _read_docx(self, file_path: str) -> str:
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except ImportError:
            logger.error("python-docx not installed. Run: pip install python-docx")
            raise

    def ingest_document(
        self,
        file_path: str,
        document_type: str = "proposal",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Reads a document, chunks it, and stores embeddings in ChromaDB.

        Args:
            file_path: Path to the document (PDF, DOCX, TXT, MD)
            document_type: Either "proposal" or "cv"
            metadata: Optional metadata dict (e.g., {"title": "...", "year": 2024})

        Returns:
            Dict with success status and document info
        """
        try:
            text = self._read_file(file_path)
            chunks = self.text_splitter.split_text(text)

            if not chunks:
                return {"success": False, "error": "No text extracted from document"}

            collection = (
                self.proposals_collection
                if document_type == "proposal"
                else self.cvs_collection
            )

            doc_metadata = metadata or {}
            doc_metadata["source_file"] = os.path.basename(file_path)

            ids = []
            metadatas = []
            documents = []

            for i, chunk in enumerate(chunks):
                chunk_id = f"{os.path.basename(file_path)}_{i}"
                ids.append(chunk_id)
                metadatas.append({**doc_metadata, "chunk_index": i})
                documents.append(chunk)

            embeddings = self._get_embeddings()
            embedding_vectors = embeddings.embed_documents(documents)

            collection.add(
                ids=ids,
                metadatas=metadatas,
                documents=documents,
                embeddings=embedding_vectors
            )

            logger.info(f"Ingested {len(chunks)} chunks from {file_path}")

            return {
                "success": True,
                "document_type": document_type,
                "file_name": os.path.basename(file_path),
                "chunks_added": len(chunks),
                "collection": collection.name
            }

        except Exception as e:
            logger.error(f"Document ingestion failed: {e}")
            return {"success": False, "error": str(e)}

    def query_knowledge_base(
        self,
        query: str,
        document_type: str = "proposal",
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Queries the knowledge base for relevant context.

        Args:
            query: The search query
            document_type: Either "proposal" or "cv"
            top_k: Number of top results to return

        Returns:
            List of relevant context chunks with metadata
        """
        try:
            collection = (
                self.proposals_collection
                if document_type == "proposal"
                else self.cvs_collection
            )

            embeddings = self._get_embeddings()
            query_embedding = embeddings.embed_query(query)

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            contexts = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    contexts.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0.0
                    })

            return contexts

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

    def search_past_proposals(
        self,
        keyword: str,
        top_k: int = 5
    ) -> str:
        """
        Tool-friendly wrapper for searching past proposals.

        Args:
            keyword: Search keyword
            top_k: Number of results

        Returns:
            JSON string of results
        """
        results = self.query_knowledge_base(keyword, "proposal", top_k)
        if not results:
            return json.dumps({"results": [], "message": "No matching proposals found"})

        return json.dumps({
            "results": results,
            "count": len(results)
        })

    def get_consultant_cv(
        self,
        skill_set: str,
        top_k: int = 3
    ) -> str:
        """
        Tool-friendly wrapper for searching consultant CVs by skill.

        Args:
            skill_set: Skills to search for (e.g., "DHIS2, Python, Data Analysis")
            top_k: Number of results

        Returns:
            JSON string of matching CVs
        """
        results = self.query_knowledge_base(skill_set, "cv", top_k)
        if not results:
            return json.dumps({"results": [], "message": "No matching CVs found"})

        return json.dumps({
            "results": results,
            "count": len(results)
        })

    def list_documents(self, document_type: str = "proposal") -> List[str]:
        """
        Lists all indexed documents of a given type.
        """
        collection = (
            self.proposals_collection
            if document_type == "proposal"
            else self.cvs_collection
        )

        try:
            return collection.get().get("metadatas", [])
        except Exception as e:
            logger.error(f"List documents failed: {e}")
            return []


rag_engine = RAGEngine()
