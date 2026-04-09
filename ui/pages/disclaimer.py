"""Disclaimer and acknowledgment page."""

from datetime import datetime, timezone

import streamlit as st

from ui.components import apply_styles, render_federal_only_banner, render_full_disclaimer, render_header
from utils.constants import PRIVACY_NOTICE
from utils.session_state import navigate_to


def render():
    """Render the disclaimer page."""
    apply_styles()
    render_header()
    render_federal_only_banner()

    st.markdown("### Before You Download Your Tax Roadmap")
    st.markdown(
        "Please read the following disclaimer carefully and acknowledge that you understand."
    )

    render_full_disclaimer()

    st.markdown("---")

    # Privacy notice
    st.markdown("### Your Privacy")
    st.info(PRIVACY_NOTICE)

    st.markdown("---")

    # Acknowledgment — no name or PII collected
    accepted = st.checkbox(
        "I have read and understand the disclaimer above. I acknowledge that OpenReturn "
        "provides educational guidance only, and I am solely responsible for my tax return.",
        key="disclaimer_checkbox",
    )

    today = datetime.now(timezone.utc).strftime("%B %d, %Y")
    st.markdown(f"**Date:** {today}")

    st.session_state.disclaimer_accepted = accepted

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Generate My Tax Roadmap",
            type="primary",
            use_container_width=True,
            disabled=not accepted,
        ):
            st.session_state.generation_timestamp = datetime.now(
                timezone.utc
            ).isoformat()
            navigate_to("download")

    if not accepted:
        st.info("Please accept the disclaimer to proceed.")

    if st.button("Back to Guidance"):
        navigate_to("guidance")
