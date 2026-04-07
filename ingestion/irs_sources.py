"""Master list of IRS publication URLs for ingestion.

We ingest three tax years for richer RAG context:
- 2025 (current filing year) — latest docs at /pub/irs-pdf/
- 2024 (prior year) — archived at /pub/irs-prior/
- 2023 (two years prior) — archived at /pub/irs-prior/

The /pub/irs-pdf/ URLs always point to the most current revision.
Prior-year documents use /pub/irs-prior/ with the same filenames.
"""

# --- Document definitions (shared across years) ---
_DOCUMENT_DEFS = [
    {
        "name": "Publication 17 - Your Federal Income Tax",
        "filename": "p17.pdf",
        "forms": ["1040"],
    },
    {
        "name": "Form 1040 Instructions",
        "filename": "i1040gi.pdf",
        "forms": ["1040"],
    },
    {
        "name": "Form 1040-NR Instructions",
        "filename": "i1040nr.pdf",
        "forms": ["1040-NR"],
    },
    {
        "name": "Schedule C Instructions",
        "filename": "i1040sc.pdf",
        "forms": ["Schedule C"],
    },
    {
        "name": "Schedule A Instructions",
        "filename": "i1040sca.pdf",
        "forms": ["Schedule A"],
    },
    {
        "name": "Schedule D Instructions",
        "filename": "i1040sd.pdf",
        "forms": ["Schedule D"],
    },
    {
        "name": "Schedule SE Instructions",
        "filename": "i1040sse.pdf",
        "forms": ["Schedule SE"],
    },
    {
        "name": "Publication 519 - US Tax Guide for Aliens",
        "filename": "p519.pdf",
        "forms": ["1040-NR"],
    },
    {
        "name": "Publication 901 - US Tax Treaties",
        "filename": "p901.pdf",
        "forms": ["1040-NR", "8833"],
    },
    {
        "name": "Form 8833 Instructions",
        "filename": "i8833.pdf",
        "forms": ["8833"],
    },
    {
        "name": "Publication 505 - Tax Withholding and Estimated Tax",
        "filename": "p505.pdf",
        "forms": ["1040", "1040-NR"],
    },
    {
        "name": "Form 1099-NEC Instructions",
        "filename": "i1099nec.pdf",
        "forms": ["Schedule C"],
    },
]


def _build_sources() -> list[dict]:
    """Build the full IRS_SOURCES list across all three years."""
    sources = []

    for doc in _DOCUMENT_DEFS:
        # 2025 — current year (latest at /pub/irs-pdf/)
        sources.append({
            "name": f"{doc['name']} (2025)",
            "url": f"https://www.irs.gov/pub/irs-pdf/{doc['filename']}",
            "year": 2025,
            "forms": doc["forms"],
        })

        # 2024 — prior year (archived at /pub/irs-prior/)
        sources.append({
            "name": f"{doc['name']} (2024)",
            "url": f"https://www.irs.gov/pub/irs-prior/{doc['filename']}",
            "year": 2024,
            "forms": doc["forms"],
        })

        # 2023 — two years prior (archived at /pub/irs-prior/)
        sources.append({
            "name": f"{doc['name']} (2023)",
            "url": f"https://www.irs.gov/pub/irs-prior/{doc['filename']}",
            "year": 2023,
            "forms": doc["forms"],
        })

    return sources


IRS_SOURCES = _build_sources()
