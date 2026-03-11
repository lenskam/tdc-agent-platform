import os
import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings


class KnowledgeBase:
    def __init__(self, collection_name: str = "help_docs"):
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.client = chromadb.PersistentClient(
            path=os.getenv("CHROMA_DB_PATH", "./data/chroma"),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Help documentation and SOPs"}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        chunks = self.text_splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{i}"
            self.collection.upsert(
                ids=chunk_id,
                documents=[chunk],
                metadatas=[{**(metadata or {}), "doc_id": doc_id}]
            )

    def search(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0
                })
        
        return formatted_results

    def list_documents(self) -> List[str]:
        return self.collection.get().get("ids", [])


knowledge_base = KnowledgeBase()


@tool
def search_help_docs(query: str, n_results: int = 3) -> str:
    """
    Search the help documentation knowledge base for relevant articles.

    Args:
        query: The search query (e.g., "password reset", "data entry error")
        n_results: Number of results to return (default 3)

    Returns:
        JSON string with matching help documents and their content
    """
    results = knowledge_base.search(query, n_results=n_results)
    
    if not results:
        return json.dumps({
            "message": "No matching documents found",
            "suggestion": "Try different keywords or contact support"
        })
    
    formatted = []
    for r in results:
        formatted.append({
            "content": r["content"],
            "doc_id": r["metadata"].get("doc_id", "unknown"),
            "relevance_score": 1 - r["distance"]
        })
    
    return json.dumps(formatted, indent=2)


@tool
def add_help_document(title: str, content: str, category: str = "general") -> str:
    """
    Add a new document to the help knowledge base.

    Args:
        title: Document title
        content: Full document content
        category: Category (e.g., "SOP", "FAQ", "Tutorial")

    Returns:
        Confirmation message
    """
    doc_id = title.lower().replace(" ", "_")
    knowledge_base.add_document(
        doc_id=doc_id,
        content=content,
        metadata={"title": title, "category": category}
    )
    
    return json.dumps({
        "status": "success",
        "message": f"Document '{title}' added to knowledge base",
        "doc_id": doc_id
    })


@tool
def list_help_categories() -> str:
    """
    List all categories in the help knowledge base.

    Returns:
        JSON string with available categories and document counts
    """
    return json.dumps({
        "categories": ["SOP", "FAQ", "Tutorial", "Troubleshooting", "general"],
        "note": "Use add_help_document to add new documents"
    })


knowledge_search_tools = [
    search_help_docs,
    add_help_document,
    list_help_categories
]
