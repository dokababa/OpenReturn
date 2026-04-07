"""Reusable Streamlit UI components for OpenReturn."""

import streamlit as st

from ui.styles import CUSTOM_CSS
from utils.constants import APP_NAME, DISCLAIMER_TEXT, SUPPORTED_TAX_YEARS


def apply_styles():
    """Inject custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header():
    """Render the app header."""
    st.markdown(f'<div class="main-header">{APP_NAME}</div>', unsafe_allow_html=True)


def render_disclaimer_banner(style: str = "yellow"):
    """Render a disclaimer banner."""
    css_class = "disclaimer-banner-red" if style == "red" else "disclaimer-banner"
    st.markdown(
        f'<div class="{css_class}">'
        "<strong>Not tax advice.</strong> OpenReturn provides educational guidance only. "
        "You are responsible for your own tax return."
        "</div>",
        unsafe_allow_html=True,
    )


def render_full_disclaimer():
    """Render the full disclaimer text."""
    st.markdown(
        f'<div class="disclaimer-banner-red">'
        f'<pre style="white-space: pre-wrap; font-family: inherit; margin: 0; '
        f'color: #7f1d1d; font-size: 0.9rem; line-height: 1.6;">'
        f'{DISCLAIMER_TEXT}</pre></div>',
        unsafe_allow_html=True,
    )


def render_form_card(form_info: dict):
    """Render a form card with name, reason, and badges."""
    required = form_info.get("required", True)
    badge_class = "badge-required" if required else "badge-optional"
    badge_text = "Required" if required else "Optional"
    card_class = "form-card form-card-required" if required else "form-card form-card-optional"

    irs_url = form_info.get("irs_url", "")
    link_html = f' <a href="{irs_url}" target="_blank">IRS Info</a>' if irs_url else ""

    st.markdown(
        f'<div class="{card_class}">'
        f'<strong>{form_info["form"]}</strong> '
        f'<span class="{badge_class}">{badge_text}</span>'
        f"<br>{form_info['reason']}{link_html}"
        "</div>",
        unsafe_allow_html=True,
    )


def render_guidance_box(guidance: dict):
    """Render a single line guidance box."""
    note_html = ""
    if guidance.get("important_note") and guidance["important_note"] != "null":
        note_html = f"<br><strong>Note:</strong> {guidance['important_note']}"

    st.markdown(
        f'<div class="guidance-box">'
        f'<strong>{guidance["form"]} — {guidance["line"]}</strong><br>'
        f'<em>{guidance["label"]}</em>'
        f"<br><br>"
        f'<strong>What it means:</strong> {guidance["plain_english"]}<br>'
        f'<strong>Where to find it:</strong> {guidance["where_to_find_it"]}<br>'
        f'<strong>What to enter:</strong> {guidance["what_to_enter"]}'
        f"{note_html}<br><br>"
        f'<span class="irs-citation">IRS Source: {guidance["irs_citation"]}</span>'
        "</div>",
        unsafe_allow_html=True,
    )


def render_progress_bar(current: int, total: int, label: str = ""):
    """Render a progress bar with label."""
    if total > 0:
        progress = current / total
        st.progress(progress, text=label)


def render_footer():
    """Render the app footer."""
    st.markdown(
        '<div class="footer-text">'
        f"Federal only &bull; Tax Years {', '.join(str(y) for y in SUPPORTED_TAX_YEARS)} &bull; Powered by Groq &bull; Free forever"
        "</div>",
        unsafe_allow_html=True,
    )
