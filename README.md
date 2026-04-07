---
title: OpenReturn
emoji: 📋
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# OpenReturn — Free AI-Powered US Federal Tax Guidance

OpenReturn is a free, open-source web application that helps anyone understand how to fill their US federal tax forms. It walks you through a conversational interview, determines which IRS forms you need, and provides plain-English line-by-line guidance — all cited directly to official IRS publications.

**OpenReturn does NOT file your taxes.** It educates you so you can file them yourself, with confidence.

👉 **[Try OpenReturn Live](https://huggingface.co/spaces/dokababa/OpenReturn)**

## Philosophy

- **Free forever** — no subscriptions, no credit card, no upsells
- **Educational, not advisory** — every piece of guidance cites an IRS source
- **Privacy-first** — no personal financial data is stored
- **Federal only** — US federal taxes, no state

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Frontend | Streamlit | Free |
| LLM | Groq API (Llama 3.3 70B) | Free tier |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Free (local) |
| Vector DB | ChromaDB | Free (local) |
| Orchestration | LangGraph + LangChain | Free |
| PDF Generation | ReportLab | Free |
| Hosting | Hugging Face Spaces | Free |

## Local Setup

### Prerequisites
- Python 3.10+
- Free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/dokababa/openreturn.git
cd openreturn

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Groq API key

# Run ingestion pipeline (downloads IRS docs — 5-10 minutes)
python ingestion/ingest.py

# Start the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

> **Filing for Tax Year 2025.** Regular deadline: April 15, 2026. International filers (F-1, J-1, etc.): June 15, 2026.

## How It Works

### 1. Interview
A guided, binary decision tree asks about your tax situation — residency, income sources, deductions, and credits. Each question explains why it's being asked.

### 2. Form Determination
Based on your answers, the app determines exactly which IRS forms you need (1040, 1040-NR, Schedule C, Schedule D, etc.) and explains why.

### 3. RAG-Powered Guidance
For each form line, the app:
1. Queries ChromaDB for relevant IRS instruction chunks
2. Sends the context + your situation to Groq (Llama 3.3 70B)
3. Returns plain-English guidance with IRS citations

### 4. PDF Roadmap
A downloadable PDF summarizing your filing profile, every form line with guidance, and a full disclaimer.

## How RAG Works in This Project

OpenReturn ingests IRS documents from **three tax years** (2025, 2024, and 2023) to give the RAG engine richer context. Regulations rarely change drastically year-to-year, so prior-year instructions help fill gaps when the current year's document is ambiguous or when a concept is better explained in an older edition.

1. **Ingestion** (`ingestion/ingest.py`): Downloads IRS PDFs for tax years 2023–2025, extracts text, splits into 800-token chunks with 150-token overlap, embeds with sentence-transformers, and stores in ChromaDB with metadata (source, page, year, forms). Current-year (2025) docs come from `/pub/irs-pdf/`; prior years come from `/pub/irs-prior/`.

2. **Retrieval** (`rag/retriever.py`): For each form line, queries ChromaDB with the line description. Returns the top 3 most relevant IRS instruction chunks — these may come from any of the three ingested years, with the most semantically relevant content surfacing first.

3. **Generation** (`agents/guidance_agent.py`): Sends the retrieved context + user situation to Groq's Llama 3.3 70B. The model generates structured guidance with IRS citations, always noting which publication and year the guidance is drawn from.

## Privacy & Data Security

OpenReturn is designed with a **zero sensitive data** architecture:

**What we ask (categories only):**
- Filing status (single, married, etc.)
- Income types (W-2, 1099-NEC, etc.) — yes/no only
- Deduction and credit categories — yes/no only
- Visa type for international filers

**What we NEVER collect:**
- Social Security numbers
- Bank account or routing numbers
- Full legal names or addresses
- Exact income amounts
- Employer details

All session data lives only in browser memory via Streamlit session state. When you close the tab, everything is gone. There is no backend database, no server-side logging of user answers, and no analytics that capture form inputs. The PDF roadmap contains only guidance text — never your sensitive personal details. You fill those in yourself on the real IRS forms.

## Legal Positioning

OpenReturn is a **free educational tool**. It does not prepare, calculate, or file tax returns. It does not charge a fee. It does not act as a tax practitioner under IRS Circular 230.

- Individual tax return preparers need licensing only when they charge a fee — OpenReturn is free
- Software that assists taxpayers in completing their own returns is explicitly legal
- OpenReturn does not represent anyone before the IRS
- State-level preparer regulations (CA, MD, NY, OR, etc.) apply to paid preparers — not free educational tools

This is not tax advice. This is not a tax preparation service. This is a tool that helps you **understand** your taxes using publicly available IRS documents.

## Disclaimer

OpenReturn provides tax EDUCATION and GUIDANCE only. It is NOT a tax preparation service and does NOT constitute professional tax, legal, or financial advice. You are solely responsible for the accuracy of your tax return.

Free tax help: [IRS Free File](https://www.irs.gov/filing/free-file-do-your-federal-taxes-for-free) | [VITA](https://www.irs.gov/individuals/free-tax-return-preparation-for-qualifying-taxpayers)

## License

MIT License — see LICENSE file for details.
