"""
IRS document update monitor.

Checks IRS.gov for updated documents and re-ingests if newer versions found.
Run manually: python ingestion/monitor.py
"""
from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.ingest import get_chroma_client, ingest_source
from ingestion.irs_sources import IRS_SOURCES
from rag.embedder import get_embeddings
from utils.constants import CHROMA_COLLECTION_NAME

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def check_pdf_updated(url: str) -> str | None:
    """Check the Last-Modified header of an IRS PDF."""
    try:
        response = requests.head(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (OpenReturn Tax Education Tool)"
        })
        response.raise_for_status()
        return response.headers.get("Last-Modified")
    except requests.RequestException as e:
        logger.warning(f"Could not check {url}: {e}")
        return None


def remove_source_chunks(collection, source_name: str):
    """Remove all chunks for a given source from ChromaDB."""
    try:
        results = collection.get(where={"source_name": source_name})
        if results and results["ids"]:
            collection.delete(ids=results["ids"])
            logger.info(f"Removed {len(results['ids'])} chunks for: {source_name}")
    except Exception as e:
        logger.error(f"Error removing chunks for {source_name}: {e}")


def check_for_updates():
    """Check all IRS sources for updates and re-ingest if needed."""
    logger.info("=" * 60)
    logger.info("OpenReturn IRS Document Update Monitor")
    logger.info(f"Check time: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 60)

    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    embedding_fn = get_embeddings()

    updates_found = 0

    for source in IRS_SOURCES:
        last_modified = check_pdf_updated(source["url"])
        if last_modified:
            logger.info(f"{source['name']}: Last-Modified = {last_modified}")

            # Check if we have a newer year than what's stored
            try:
                results = collection.get(
                    where={"source_name": source["name"]},
                    limit=1,
                )
                if results and results["metadatas"]:
                    stored_year = results["metadatas"][0].get("year", 0)
                    if source["year"] > stored_year:
                        logger.info(
                            f"Update found for {source['name']}: "
                            f"stored year {stored_year} < source year {source['year']}"
                        )
                        remove_source_chunks(collection, source["name"])
                        ingest_source(collection, embedding_fn, source)
                        updates_found += 1
                else:
                    # Not ingested yet
                    logger.info(f"New source found: {source['name']}")
                    ingest_source(collection, embedding_fn, source)
                    updates_found += 1
            except Exception as e:
                logger.error(f"Error checking {source['name']}: {e}")
        else:
            logger.warning(f"Could not check {source['name']}")

    logger.info("=" * 60)
    logger.info(f"Monitor complete: {updates_found} updates applied")
    logger.info(f"Total chunks in collection: {collection.count()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    check_for_updates()
