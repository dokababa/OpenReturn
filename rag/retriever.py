"""ChromaDB query logic for RAG retrieval."""
from __future__ import annotations

import logging
import os

import chromadb
from dotenv import load_dotenv

from rag.embedder import get_embeddings
from utils.constants import CHROMA_COLLECTION_NAME

load_dotenv()
logger = logging.getLogger(__name__)


class IRSRetriever:
    """Retrieves relevant IRS document chunks from ChromaDB."""

    def __init__(self):
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./rag/chroma_store")
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME
        )
        self._embeddings = get_embeddings()

    def has_documents(self) -> bool:
        """Check if any documents have been ingested."""
        try:
            return self._collection.count() > 0
        except Exception:
            return False

    def query(
        self,
        query_text: str,
        n_results: int = 3,
        form_filter: str | None = None,
    ) -> list[dict]:
        """
        Query ChromaDB for relevant IRS document chunks.

        Args:
            query_text: The search query.
            n_results: Number of results to return.
            form_filter: Optional form name to filter results.

        Returns:
            List of dicts with 'text', 'metadata', and 'distance' keys.
        """
        try:
            query_embedding = self._embeddings.embed_query(query_text)

            where_filter = None
            if form_filter:
                where_filter = {
                    "relevant_forms": {"$contains": form_filter}
                }

            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter,
            )

            output = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    output.append({
                        "text": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else None,
                    })

            return output
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return []

    def get_guidance_context(
        self, form: str, line: str, n_results: int = 3
    ) -> str:
        """Get concatenated IRS context for a specific form line."""
        query = f"{form} {line} instructions how to fill"
        results = self.query(query, n_results=n_results, form_filter=form)
        return "\n\n".join([r["text"] for r in results])


def chromadb_has_documents() -> bool:
    """Quick check if ChromaDB has any ingested documents."""
    try:
        retriever = IRSRetriever()
        return retriever.has_documents()
    except Exception:
        return False
