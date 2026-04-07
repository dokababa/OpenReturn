"""
OpenReturn — Free AI-Powered US Federal Tax Guidance

Main Streamlit entry point.
"""
from __future__ import annotations

import os
import sys
import logging

import streamlit as st
from dotenv import load_dotenv

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from utils.session_state import init_session_state

# Page config
st.set_page_config(
    page_title="OpenReturn — Free Tax Guidance",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state
init_session_state()


def check_groq_key() -> bool:
    """Check that the Groq API key is configured."""
    groq_key = os.getenv("GROQ_API_KEY", "")
    return bool(groq_key) and groq_key != "gsk_your_groq_key_here"


def check_chromadb() -> bool:
    """Check if ChromaDB has ingested documents."""
    try:
        from rag.retriever import chromadb_has_documents
        return chromadb_has_documents()
    except Exception:
        return False


def run_auto_ingestion():
    """Run ingestion automatically (for Hugging Face Spaces or first launch)."""
    st.markdown("## OpenReturn — First-Time Setup")
    st.info(
        "Downloading and indexing IRS documents for the first time. "
        "This takes about 5-10 minutes. The app will be ready when it finishes."
    )

    progress_bar = st.progress(0, text="Starting ingestion...")
    status_text = st.empty()

    try:
        from ingestion.ingest import get_chroma_client, ingest_source
        from ingestion.irs_sources import IRS_SOURCES
        from rag.embedder import get_embeddings
        from utils.constants import CHROMA_COLLECTION_NAME

        client = get_chroma_client()
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
        embedding_fn = get_embeddings()

        total = len(IRS_SOURCES)
        for i, source in enumerate(IRS_SOURCES):
            status_text.markdown(f"**Ingesting:** {source['name']}...")
            progress_bar.progress((i + 1) / total, text=f"Document {i + 1} of {total}")
            try:
                ingest_source(collection, embedding_fn, source)
            except Exception as e:
                logging.warning(f"Skipped {source['name']}: {e}")

        progress_bar.progress(1.0, text="Ingestion complete!")
        status_text.success(
            f"Done! Indexed {collection.count()} chunks from {total} IRS documents. "
            "Reloading the app..."
        )
        st.rerun()

    except Exception as e:
        st.error(f"Ingestion failed: {e}")
        logging.error(f"Auto-ingestion error: {e}", exc_info=True)
        st.markdown(
            "You can also run ingestion manually:\n"
            "```bash\npython ingestion/ingest.py\n```"
        )


def render_groq_setup():
    """Show Groq API key setup instructions."""
    st.markdown("## OpenReturn — Setup Required")
    st.error("Groq API key not found.")
    st.markdown(
        """
### How to fix:

1. **Get a free Groq API key:**
   - Go to [console.groq.com](https://console.groq.com)
   - Sign up (free, no credit card needed)
   - Go to "API Keys" → "Create API Key"
   - Copy the key (starts with `gsk_...`)

2. **Set up your environment:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and paste your key:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

3. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

**On Hugging Face Spaces:** Go to Settings → Repository Secrets → add `GROQ_API_KEY`.
"""
    )


def main():
    """Main app router."""
    # Step 1: Check Groq API key
    if not check_groq_key():
        render_groq_setup()
        return

    # Step 2: Check ChromaDB — auto-ingest if empty
    if not check_chromadb():
        run_auto_ingestion()
        return

    # Step 3: Route to current page
    page = st.session_state.get("current_page", "landing")

    try:
        if page == "landing":
            from ui.pages.landing import render
        elif page == "interview":
            from ui.pages.interview import render
        elif page == "forms_summary":
            from ui.pages.forms_summary import render
        elif page == "guidance":
            from ui.pages.guidance import render
        elif page == "disclaimer":
            from ui.pages.disclaimer import render
        elif page == "download":
            from ui.pages.download import render
        else:
            from ui.pages.landing import render

        render()
    except Exception as e:
        st.error("Something went wrong. Please try again.")
        logging.error(f"Page render error: {e}", exc_info=True)
        if st.button("Return to Home"):
            st.session_state.current_page = "landing"
            st.rerun()


if __name__ == "__main__":
    main()
