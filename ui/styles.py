"""Custom CSS styles for OpenReturn — clean, modern design."""

CUSTOM_CSS = """
<style>
    /* === Base Theme Override === */
    .stApp {
        background-color: #fafafa;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #6b7280;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* === Form Cards === */
    .form-card {
        background: #ffffff;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .form-card-required {
        border-left-color: #ef4444;
    }
    .form-card-optional {
        border-left-color: #22c55e;
    }

    /* === Guidance Box === */
    .guidance-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        line-height: 1.6;
    }
    .guidance-box strong {
        color: #111827;
    }

    .irs-citation {
        font-size: 0.8rem;
        color: #9ca3af;
        font-style: italic;
    }

    /* === Disclaimer Banners === */
    .disclaimer-banner {
        background: #fefce8;
        border: 1px solid #facc15;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        color: #713f12;
        font-size: 0.9rem;
    }
    .disclaimer-banner strong {
        color: #92400e;
    }

    .disclaimer-banner-red {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        color: #7f1d1d;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .disclaimer-banner-red strong {
        color: #991b1b;
    }

    /* === Progress / Stage Labels === */
    .progress-stage {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .question-why {
        font-size: 0.88rem;
        color: #6b7280;
        font-style: italic;
        margin-top: 0.25rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    /* === Badges === */
    .badge-required {
        background: #ef4444;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-optional {
        background: #22c55e;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* === Confirmation Tracker === */
    .confirmation-tracker {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        font-weight: 600;
        color: #166534;
    }

    /* === Footer === */
    .footer-text {
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }

    /* === Section Card (for interview groups) === */
    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-card h4 {
        margin-top: 0;
        color: #111827;
    }

    /* === Buttons === */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.15s ease;
    }
    div.stButton > button[kind="primary"] {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #2563eb;
        border-color: #2563eb;
    }

    /* === Number Inputs in Interview === */
    .form-count-label {
        font-size: 0.95rem;
        color: #374151;
        font-weight: 500;
        margin-bottom: 0.15rem;
    }
    .form-count-why {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
</style>
"""
