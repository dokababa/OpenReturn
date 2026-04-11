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
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

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

# Visa types shown in the interview — covers all common nonimmigrant categories
VISA_TYPES = [
    "F-1",           # Student
    "F-2",           # F-1 dependent
    "J-1",           # Exchange visitor (student/scholar/researcher)
    "J-2",           # J-1 dependent
    "OPT (post-F-1)",  # Optional Practical Training
    "M-1",           # Vocational student
    "H-1B",          # Specialty occupation worker
    "H-4",           # H-1B dependent
    "L-1",           # Intracompany transferee
    "L-2",           # L-1 dependent
    "O-1",           # Extraordinary ability
    "TN",            # USMCA professional (Canada/Mexico)
    "E-1",           # Treaty trader
    "E-2",           # Treaty investor
    "E-3",           # Australian specialty worker
    "R-1",           # Religious worker
    "B-1/B-2",       # Visitor (business/tourist)
    "Other",
]

# Legacy alias used in interview_agent
STUDENT_VISA_TYPES = VISA_TYPES

# Countries with US tax treaties relevant to students.
# benefit: None means no treaty — users from those countries get no exemption.
# Educational reference only — verify against IRS Publication 901.
TREATY_COUNTRIES = {
    "China (PRC)": {
        "article": "Article 20",
        "benefit": (
            "Students from China may exclude up to $5,000 of wages/compensation per year "
            "from US tax. Scholarship and fellowship income for study is also generally exempt."
        ),
    },
    "India": {
        "article": "Article 21",
        "benefit": (
            "Students from India may exclude certain scholarship, fellowship, and stipend "
            "income received for education or training from US tax."
        ),
    },
    "South Korea": {
        "article": "Article 21",
        "benefit": (
            "Students from South Korea may exclude income received for maintenance, study, "
            "or training from US tax for up to 5 years."
        ),
    },
    "Philippines": {
        "article": "Article 22",
        "benefit": (
            "Students from the Philippines may exclude payments received for maintenance, "
            "education, or training from US tax for a reasonable period."
        ),
    },
    "Pakistan": {
        "article": "Article XV",
        "benefit": (
            "Students from Pakistan may exclude grants, scholarships, and stipends received "
            "from outside the US for maintenance and education."
        ),
    },
    "Indonesia": {
        "article": "Article 19",
        "benefit": (
            "Students from Indonesia may exclude income received for maintenance and education "
            "from US tax for a limited period while studying."
        ),
    },
    "Thailand": {
        "article": "Article 22",
        "benefit": (
            "Students from Thailand may exclude payments received for maintenance, "
            "education, or training from US tax for a reasonable period."
        ),
    },
    "Morocco": {
        "article": "Article 18",
        "benefit": "Students from Morocco may exclude income received for maintenance and education from US tax.",
    },
    "Romania": {
        "article": "Article 20",
        "benefit": "Students from Romania may exclude amounts received from abroad for maintenance, education, or training.",
    },
    "Hungary": {
        "article": "Article 17",
        "benefit": "Students from Hungary may exclude payments received for maintenance, study, or training for a limited period.",
    },
    "Canada": {
        "article": "Article XX",
        "benefit": (
            "Students from Canada may exclude scholarship, fellowship, and bursary income "
            "from US tax. Review IRS Pub 901 Article XX for full details."
        ),
    },
    "UK": {
        "article": "Article 20",
        "benefit": "Students from the UK may exclude payments for maintenance and education from US tax for a limited period.",
    },
    "Germany": {
        "article": "Article 20",
        "benefit": "Students from Germany may exclude payments for maintenance and education from US tax while studying.",
    },
    "France": {
        "article": "Article 21",
        "benefit": "Students from France may exclude payments for maintenance and education from US tax for a limited period.",
    },
    "Japan": {
        "article": "Article 20",
        "benefit": "Students from Japan may exclude payments for maintenance, study, or training from US tax for a limited period.",
    },
    "Netherlands": {
        "article": "Article 22",
        "benefit": "Students from the Netherlands may exclude payments for maintenance and education from US tax.",
    },
    "Sweden": {
        "article": "Article 22",
        "benefit": "Students from Sweden may exclude payments for maintenance and education from US tax for up to 5 years.",
    },
    "Norway": {
        "article": "Article 16",
        "benefit": "Students from Norway may exclude payments for maintenance and education from US tax for a limited period.",
    },
    "Mexico": {
        "article": "Article 21",
        "benefit": "Students from Mexico may exclude scholarship and fellowship income from US tax while studying.",
    },
    "Bangladesh": {"article": "No treaty", "benefit": None},
    "Nepal": {"article": "No treaty", "benefit": None},
    "Nigeria": {"article": "No treaty", "benefit": None},
    "Ghana": {"article": "No treaty", "benefit": None},
    "Kenya": {"article": "No treaty", "benefit": None},
    "Brazil": {"article": "No treaty", "benefit": None},
    "Colombia": {"article": "No treaty", "benefit": None},
    "Other": {
        "article": "Check IRS Pub 901",
        "benefit": (
            "The US has tax treaties with many countries. Check IRS Publication 901 "
            "to see if your country has a treaty and what student benefits apply."
        ),
    },
}

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
IRS_ITIN_URL = "https://www.irs.gov/individuals/individual-taxpayer-identification-number"
IRS_8843_URL = "https://www.irs.gov/forms-pubs/about-form-8843"
IRS_PUB_519_URL = "https://www.irs.gov/pub/irs-pdf/p519.pdf"
