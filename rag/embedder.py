"""Embedding pipeline using FastEmbed (ONNX-based, no PyTorch required)."""

from langchain_community.embeddings import FastEmbedEmbeddings

from utils.constants import EMBEDDING_MODEL


def get_embeddings():
    """Get the FastEmbed embedding model (ONNX, no PyTorch dependency)."""
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
