"""Custom CSS styles for OpenReturn — green/teal tax-friendly theme."""

CUSTOM_CSS = """
<style>
    /* === Force light base + explicit text colors everywhere === */
    .stApp {
        background-color: #f8faf9 !important;
        color: #1a2e2a !important;
    }
    .stApp p, .stApp li, .stApp span, .stApp label, .stApp div {
        color: #1a2e2a !important;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: #0f2b24 !important;
    }
    .stApp strong, .stApp b {
        color: #0f2b24 !important;
    }
    .stApp a {
        color: #1e6f5c !important;
    }

    /* === Header === */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f2b24 !important;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #4a6e64 !important;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* === Form Cards === */
    .form-card {
        background: #ffffff !important;
        border-left: 4px solid #1e6f5c;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        color: #1a2e2a !important;
    }
    .form-card strong {
        color: #0f2b24 !important;
    }
    .form-card-required {
        border-left-color: #dc3545;
    }
    .form-card-optional {
        border-left-color: #28a745;
    }

    /* === Guidance Box === */
    .guidance-box {
        background: #ffffff !important;
        border: 1px solid #d1ddd8;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        line-height: 1.6;
        color: #1a2e2a !important;
    }
    .guidance-box strong {
        color: #0f2b24 !important;
    }
    .guidance-box em {
        color: #3a5a50 !important;
    }

    .irs-citation {
        font-size: 0.8rem;
        color: #6b8f84 !important;
        font-style: italic;
    }

    /* === Disclaimer Banners === */
    .disclaimer-banner {
        background: #fef9e7 !important;
        border: 1px solid #f0c94b;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        color: #6b5a00 !important;
        font-size: 0.9rem;
    }
    .disclaimer-banner strong {
        color: #5a4b00 !important;
    }

    .disclaimer-banner-red {
        background: #fdf0f0 !important;
        border: 2px solid #dc3545;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        color: #6e1a1a !important;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .disclaimer-banner-red strong {
        color: #5a1010 !important;
    }
    .disclaimer-banner-red pre {
        color: #6e1a1a !important;
    }

    /* === Progress / Stage Labels === */
    .progress-stage {
        font-size: 0.85rem;
        color: #6b8f84 !important;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .question-why {
        font-size: 0.88rem;
        color: #4a6e64 !important;
        font-style: italic;
        margin-top: 0.25rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    /* === Badges === */
    .badge-required {
        background: #dc3545;
        color: white !important;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-optional {
        background: #28a745;
        color: white !important;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* === Confirmation Tracker === */
    .confirmation-tracker {
        background: #e8f5ec !important;
        border: 1px solid #b8dcc4;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        font-weight: 600;
        color: #1a5c32 !important;
    }

    /* === Footer === */
    .footer-text {
        font-size: 0.8rem;
        color: #6b8f84 !important;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #d1ddd8;
    }

    /* === Section Card (for interview groups) === */
    .section-card {
        background: #ffffff !important;
        border: 1px solid #d1ddd8;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        color: #1a2e2a !important;
    }
    .section-card h4 {
        margin-top: 0;
        color: #0f2b24 !important;
    }

    /* === Buttons === */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.15s ease;
        color: #1a2e2a !important;
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #1e6f5c !important;
        border-color: #1e6f5c !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: #175a4a !important;
        border-color: #175a4a !important;
        color: #ffffff !important;
    }

    /* === Number Inputs in Interview === */
    .form-count-label {
        font-size: 0.95rem;
        color: #1a2e2a !important;
        font-weight: 500;
        margin-bottom: 0.15rem;
    }
    .form-count-why {
        font-size: 0.8rem;
        color: #6b8f84 !important;
        margin-bottom: 0.5rem;
    }

    /* === Streamlit overrides for inputs/selects === */
    .stSelectbox label, .stNumberInput label, .stCheckbox label {
        color: #1a2e2a !important;
    }
    .stMarkdown, .stMarkdown p {
        color: #1a2e2a !important;
    }

    /* === Info/Warning/Success boxes === */
    .stAlert > div {
        color: #1a2e2a !important;
    }

    /* === Federal-only persistent banner === */
    .federal-banner {
        background: #e8f4fd !important;
        border: 1px solid #90caf9;
        border-left: 4px solid #1976d2;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0 1rem 0;
        color: #0d3c61 !important;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .federal-banner strong {
        color: #0a2e4a !important;
    }
</style>
"""
