"""Embedding pipeline using sentence-transformers (free, local, no API needed)."""

from langchain_community.embeddings import HuggingFaceEmbeddings

from utils.constants import EMBEDDING_MODEL


def get_embeddings():
    """Get the sentence-transformers embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )
