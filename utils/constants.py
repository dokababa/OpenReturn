"""Application-wide constants for OpenReturn."""

APP_NAME = "OpenReturn"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Understand your US taxes. Free. Clear. Cited."
TAX_YEAR = 2025  # Default / most recent
SUPPORTED_TAX_YEARS = [2025, 2024, 2023]

# LLM models
SMART_MODEL = "llama-3.3-70b-versatile"
FAST_MODEL = "llama-3.1-8b-instant"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ChromaDB
CHROMA_COLLECTION_NAME = "irs_documents"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Interview stages
INTERVIEW_STAGES = {
    "tax_year": "Tax Year",
    "residency": "Residency Status",
    "personal": "Personal Information",
    "income": "Income Sources",
    "deductions": "Deductions",
    "credits": "Credits & Contributions",
}

# Filing statuses
FILING_STATUSES = [
    "Single",
    "Married Filing Jointly",
    "Married Filing Separately",
    "Head of Household",
]

# Disclaimer
DISCLAIMER_TEXT = """IMPORTANT DISCLAIMER — PLEASE READ CAREFULLY

OpenReturn provides tax EDUCATION and GUIDANCE only. It is NOT a tax preparation \
service and does NOT constitute professional tax, legal, or financial advice.

OpenReturn does not prepare, calculate, or file tax returns. It does not act as a \
tax practitioner under IRS Circular 230. No fee is charged. This is a free \
educational tool — not a tax preparation service.

The guidance provided by OpenReturn:
• Is based on publicly available IRS publications and form instructions
• Is intended to help you understand your tax forms, not to prepare them for you
• May not account for every unique aspect of your tax situation
• Should not be relied upon as a substitute for professional tax advice

By using OpenReturn and downloading your Tax Roadmap, you acknowledge that:
• YOU are solely responsible for the accuracy of your tax return
• YOU will independently verify all information against your source documents
• OpenReturn bears NO liability for any errors, penalties, or issues with your filing
• This guidance is for educational purposes only

Free tax help: IRS Free File (irs.gov/freefile) • VITA (irs.gov/vita)"""

# Privacy notice
PRIVACY_NOTICE = """OpenReturn does not store, log, or transmit your personal \
information. Everything stays in your browser and is deleted when you close this tab.

We never collect:
• Social Security numbers
• Bank account or routing numbers
• Full legal names or addresses
• Exact income amounts

You only share general categories (filing status, income types, yes/no answers). \
You fill in your actual sensitive details yourself on the real IRS forms — \
we never see or touch that data."""

# Data policy (for Terms of Service)
DATA_POLICY = """Data Collection: OpenReturn collects no personal identifying \
information. We do not store SSNs, income data, bank information, or any \
financial details. All session data is temporary and exists only in your \
browser memory during your session. No database. No logs of user answers. \
No analytics that capture user inputs."""

# IRS links
IRS_FREE_FILE_URL = "https://www.irs.gov/filing/free-file-do-your-federal-taxes-for-free"
IRS_VITA_URL = "https://www.irs.gov/individuals/free-tax-return-preparation-for-qualifying-taxpayers"
IRS_WHERE_TO_FILE_URL = "https://www.irs.gov/filing/where-to-file-paper-tax-returns-with-or-without-a-payment"
