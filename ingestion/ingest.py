"""
IRS document ingestion pipeline.

Downloads IRS PDFs, chunks them, embeds with sentence-transformers,
and stores in ChromaDB. Run manually: python ingestion/ingest.py
"""
from __future__ import annotations

import logging
import os
import sys
import tempfile
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.irs_sources import IRS_SOURCES
from rag.embedder import get_embeddings
from utils.constants import CHUNK_OVERLAP, CHUNK_SIZE, CHROMA_COLLECTION_NAME

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_chroma_client():
    """Get or create the ChromaDB client and collection."""
    import chromadb

    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./rag/chroma_store")
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_dir)
    return client


def download_pdf(url: str) -> bytes | None:
    """Download a PDF from a URL. Returns bytes or None on failure."""
    try:
        logger.info(f"Downloading: {url}")
        response = requests.get(url, timeout=60, headers={
            "User-Agent": "Mozilla/5.0 (OpenReturn Tax Education Tool)"
        })
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        return None


def extract_text_from_pdf(pdf_bytes: bytes) -> list[dict]:
    """Extract text from PDF bytes, returning list of {page, text}."""
    pages = []
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        reader = PdfReader(tmp_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append({"page_number": i + 1, "text": text.strip()})
    finally:
        os.unlink(tmp_path)

    return pages


def is_already_ingested(collection, source_name: str, year: int) -> bool:
    """Check if a source has already been ingested by querying metadata."""
    try:
        results = collection.get(
            where={"source_name": source_name},
            limit=1,
        )
        if results and results["ids"]:
            return True
    except Exception:
        pass
    return False


def chunk_pages(pages: list[dict], source: dict) -> list[dict]:
    """Split page texts into chunks with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for page_data in pages:
        page_chunks = splitter.split_text(page_data["text"])
        for chunk_text in page_chunks:
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "source_name": source["name"],
                    "source_url": source["url"],
                    "page_number": page_data["page_number"],
                    "year": source["year"],
                    "relevant_forms": ",".join(source["forms"]),
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                },
            })

    return chunks


def ingest_source(collection, embedding_fn, source: dict) -> int:
    """Ingest a single IRS source. Returns number of chunks added."""
    if is_already_ingested(collection, source["name"], source["year"]):
        logger.info(f"Already ingested: {source['name']} ({source['year']})")
        return 0

    pdf_bytes = download_pdf(source["url"])
    if pdf_bytes is None:
        logger.warning(f"Skipping {source['name']} — download failed")
        return 0

    pages = extract_text_from_pdf(pdf_bytes)
    if not pages:
        logger.warning(f"Skipping {source['name']} — no text extracted")
        return 0

    chunks = chunk_pages(pages, source)
    if not chunks:
        logger.warning(f"Skipping {source['name']} — no chunks produced")
        return 0

    # Embed and store in batches
    batch_size = 50
    total_added = 0

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        texts = [c["text"] for c in batch]
        metadatas = [c["metadata"] for c in batch]
        ids = [
            f"{source['name']}_{source['year']}_chunk_{i + j}"
            for j in range(len(batch))
        ]

        embeddings = embedding_fn.embed_documents(texts)

        collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )
        total_added += len(batch)

    logger.info(f"Ingested {total_added} chunks from: {source['name']}")
    return total_added


def run_ingestion():
    """Run the full ingestion pipeline."""
    logger.info("=" * 60)
    logger.info("OpenReturn IRS Document Ingestion Pipeline")
    logger.info("=" * 60)

    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    embedding_fn = get_embeddings()

    total_chunks = 0
    successful = 0
    failed = 0

    for source in IRS_SOURCES:
        try:
            added = ingest_source(collection, embedding_fn, source)
            total_chunks += added
            successful += 1
        except Exception as e:
            logger.error(f"Error ingesting {source['name']}: {e}")
            failed += 1

    logger.info("=" * 60)
    logger.info(f"Ingestion complete: {successful} sources processed, {failed} failed")
    logger.info(f"Total chunks in collection: {collection.count()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_ingestion()
