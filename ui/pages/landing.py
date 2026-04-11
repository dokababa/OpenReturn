"""Landing page for OpenReturn — professional, conversion-focused design."""

import streamlit as st

from ui.components import apply_styles
from utils.constants import SUPPORTED_TAX_YEARS
from utils.session_state import navigate_to

LANDING_CSS = """
<style>
    /* === Hero Section === */
    .hero-section {
        text-align: center;
        padding: 3.5rem 2rem 2.5rem;
        background:
            linear-gradient(
                135deg,
                rgba(248,250,249,0.92) 0%,
                rgba(232,245,236,0.88) 50%,
                rgba(234,247,242,0.90) 100%
            ),
            url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&q=80') center/cover no-repeat;
        border-radius: 16px;
        margin: -1rem -1rem 1.5rem -1rem;
        border: 1px solid #d1ddd8;
    }
    .hero-app-name {
        font-size: 4rem;
        font-weight: 900;
        color: #0f2b24 !important;
        letter-spacing: -0.04em;
        margin-bottom: 0.75rem;
        line-height: 1;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(30,111,92,0.12);
        color: #166534 !important;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 16px;
        border-radius: 20px;
        margin-bottom: 1.25rem;
        letter-spacing: 0.03em;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f2b24 !important;
        line-height: 1.15;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }
    .hero-title span {
        background: linear-gradient(135deg, #1e6f5c, #2a9d8f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #4a6e64 !important;
        max-width: 540px;
        margin: 0 auto 2rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* === Trust Bar === */
    .trust-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin: 1.5rem 0 2.5rem;
        padding: 0;
    }
    .trust-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85rem;
        color: #4a6e64 !important;
        font-weight: 500;
    }
    .trust-item .t-icon {
        font-size: 1.1rem;
    }

    /* === Feature Cards === */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin: 2rem 0;
    }
    @media (max-width: 768px) {
        .features-grid {
            grid-template-columns: 1fr;
        }
    }
    .feature-card {
        background: #ffffff;
        border: 1px solid #d1ddd8;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: left;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.75rem;
    }
    .feature-card h3 {
        font-size: 1rem;
        font-weight: 700;
        color: #0f2b24 !important;
        margin: 0 0 0.4rem;
    }
    .feature-card p {
        font-size: 0.88rem;
        color: #4a6e64 !important;
        margin: 0;
        line-height: 1.5;
    }

    /* === Section Headers === */
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f2b24 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .section-subtitle {
        font-size: 1rem;
        color: #4a6e64 !important;
        text-align: center;
        margin-bottom: 2rem;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
    }

    /* === How It Works === */
    .steps-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    .step-item {
        text-align: center;
        flex: 1;
        min-width: 180px;
        max-width: 250px;
    }
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1e6f5c, #2a9d8f);
        color: white !important;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .step-item h4 {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f2b24 !important;
        margin: 0 0 0.3rem;
    }
    .step-item p {
        font-size: 0.85rem;
        color: #4a6e64 !important;
        margin: 0;
        line-height: 1.5;
    }
    .step-connector {
        display: flex;
        align-items: center;
        color: #b8dcc4 !important;
        font-size: 1.5rem;
        padding-top: 0.5rem;
    }
    @media (max-width: 768px) {
        .step-connector { display: none; }
    }

    /* === International Student Callout === */
    .intl-callout {
        background: linear-gradient(135deg, #e8f5ec, #eaf7f2);
        border: 1px solid #b8dcc4;
        border-radius: 12px;
        padding: 1.75rem 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    .intl-callout h3 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f2b24 !important;
        margin: 0 0 0.5rem;
    }
    .intl-callout p {
        font-size: 0.92rem;
        color: #1a5c32 !important;
        margin: 0;
        line-height: 1.6;
    }

    /* === Privacy Strip === */
    .privacy-strip {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        flex-wrap: wrap;
        margin: 2rem 0;
        padding: 1.25rem;
        background: #f0f5f2;
        border-radius: 12px;
        border: 1px solid #d1ddd8;
    }
    .privacy-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        color: #1a2e2a !important;
        font-weight: 500;
    }
    .privacy-item .p-icon {
        font-size: 1.2rem;
    }

    /* === Disclaimer Inline === */
    .landing-disclaimer {
        background: #fef9e7;
        border: 1px solid #f0c94b;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        text-align: center;
        font-size: 0.82rem;
        color: #6b5a00 !important;
        margin: 1.5rem auto;
        max-width: 600px;
    }
    .landing-disclaimer strong {
        color: #5a4b00 !important;
    }

    /* === Bottom CTA === */
    .bottom-cta {
        text-align: center;
        padding: 2.5rem 1rem;
        margin: 2rem 0 1rem;
        background: linear-gradient(135deg, #f0f5f2, #e8f5ec);
        border-radius: 16px;
    }
    .bottom-cta h2 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f2b24 !important;
        margin: 0 0 0.5rem;
    }
    .bottom-cta p {
        font-size: 0.95rem;
        color: #4a6e64 !important;
        margin: 0 0 1.5rem;
    }

    /* === Landing Footer === */
    .landing-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        border-top: 1px solid #d1ddd8;
        margin-top: 2rem;
    }
    .landing-footer p {
        font-size: 0.78rem;
        color: #6b8f84 !important;
        margin: 0.2rem 0;
        line-height: 1.5;
    }
    .landing-footer a {
        color: #1e6f5c !important;
        text-decoration: none;
    }
    .landing-footer a:hover {
        color: #175a4a !important;
    }
</style>
"""


def render():
    """Render the professional landing page."""
    apply_styles()
    st.markdown(LANDING_CSS, unsafe_allow_html=True)

    # ── Hero Section ──
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-app-name">OpenReturn</div>
            <div class="hero-badge">100% Free &bull; No Sign-Up Required</div>
            <div class="hero-title">
                Understand Your<br><span>US Tax Forms</span>
            </div>
            <div class="hero-subtitle">
                AI-powered guidance that tells you which IRS forms you need
                and walks you through them line by line — with citations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Primary CTA ──
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button(
            "Start My Tax Guidance",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("interview")

    # ── Trust Indicators ──
    st.markdown(
        """
        <div class="trust-bar">
            <div class="trust-item"><span class="t-icon">&#128274;</span> No data stored</div>
            <div class="trust-item"><span class="t-icon">&#128218;</span> IRS-cited guidance</div>
            <div class="trust-item"><span class="t-icon">&#9889;</span> Results in minutes</div>
            <div class="trust-item"><span class="t-icon">&#127891;</span> Built for students</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Disclaimer (compact) ──
    st.markdown(
        '<div class="landing-disclaimer">'
        "<strong>Not tax advice.</strong> OpenReturn is a free educational tool. "
        "It does not file your taxes or replace a professional."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── How It Works ──
    st.markdown(
        """
        <div class="section-title">How It Works</div>
        <div class="section-subtitle">Three steps to clarity — no account needed.</div>
        <div class="steps-container">
            <div class="step-item">
                <div class="step-number">1</div>
                <h4>Answer Questions</h4>
                <p>A short interview about your income, filing status, and situation.</p>
            </div>
            <div class="step-connector">&#8594;</div>
            <div class="step-item">
                <div class="step-number">2</div>
                <h4>Get Your Forms</h4>
                <p>We identify exactly which IRS forms apply to you and why.</p>
            </div>
            <div class="step-connector">&#8594;</div>
            <div class="step-item">
                <div class="step-number">3</div>
                <h4>Follow the Roadmap</h4>
                <p>Line-by-line guidance with IRS citations you can trust.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Features ──
    st.markdown(
        """
        <div class="section-title">What You Get</div>
        <div class="section-subtitle">Everything you need to understand your federal tax return.</div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">&#128203;</div>
                <h3>Form Identification</h3>
                <p>Know exactly which forms you need — 1040, 1040-NR, Schedule OI, 8843, and more.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128221;</div>
                <h3>Line-by-Line Guidance</h3>
                <p>Plain English explanations for every line on your forms. No more guessing.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128279;</div>
                <h3>IRS Citations</h3>
                <p>Every recommendation links back to an official IRS publication.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128196;</div>
                <h3>PDF Tax Roadmap</h3>
                <p>Download a complete filing guide you can follow at your own pace.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#127758;</div>
                <h3>International Students</h3>
                <p>Built-in support for F-1/J-1 visas, tax treaties, 1042-S, and nonresident filing.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128170;</div>
                <h3>Always Free</h3>
                <p>No paywalls, no upsells, no sign-up. Open source and community-driven.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── International Student Callout ──
    st.markdown(
        """
        <div class="intl-callout">
            <h3>&#127891; International Student or Scholar?</h3>
            <p>
                OpenReturn supports F-1 and J-1 visa holders with specialized guidance for
                Form 1040-NR, Schedule OI, Schedule NEC, Form 8843, Form 8833, and
                tax treaty benefits for 27 countries. If your university's VITA clinic
                couldn't help because you're a nonresident — we've got you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Privacy Strip ──
    st.markdown(
        """
        <div class="privacy-strip">
            <div class="privacy-item"><span class="p-icon">&#128274;</span> Zero data collection</div>
            <div class="privacy-item"><span class="p-icon">&#128683;</span> No SSNs or bank info</div>
            <div class="privacy-item"><span class="p-icon">&#128421;</span> Nothing stored on servers</div>
            <div class="privacy-item"><span class="p-icon">&#128465;</span> Session erased on close</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Bottom CTA ──
    st.markdown(
        """
        <div class="bottom-cta">
            <h2>Ready to understand your taxes?</h2>
            <p>It takes about 5 minutes. No sign-up. No cost. Just clarity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button(
            "Get Started — It's Free",
            type="primary",
            use_container_width=True,
            key="bottom_cta",
        ):
            navigate_to("interview")

    # ── Footer ──
    years_str = ", ".join(str(y) for y in SUPPORTED_TAX_YEARS)
    st.markdown(
        f"""
        <div class="landing-footer">
            <p>Federal returns only &bull; Tax Years {years_str} &bull; Powered by Groq + LangGraph</p>
            <p>Open source on <a href="https://github.com/dokababa/OpenReturn" target="_blank">GitHub</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
