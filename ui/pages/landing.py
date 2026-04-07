"""Landing page for OpenReturn."""

import streamlit as st

from ui.components import (
    apply_styles,
    render_disclaimer_banner,
    render_footer,
    render_header,
)
from utils.constants import APP_TAGLINE, PRIVACY_NOTICE, SUPPORTED_TAX_YEARS, TAX_YEAR
from utils.session_state import navigate_to


def render():
    """Render the landing page."""
    apply_styles()
    render_header()

    st.markdown(
        f'<div class="sub-header">{APP_TAGLINE}</div>',
        unsafe_allow_html=True,
    )

    render_disclaimer_banner(style="yellow")

    st.markdown("### What OpenReturn Does")
    st.markdown(
        """
- Walks you through a simple interview about your tax situation
- Tells you **exactly which IRS forms** you need
- Gives you **line-by-line guidance** for each form in plain English
- Cites every piece of guidance to an **official IRS publication**
- Generates a **downloadable PDF roadmap** you can follow while filing
"""
    )

    st.markdown("### What OpenReturn Does NOT Do")
    st.markdown(
        """
- Does **not** file your taxes for you
- Does **not** calculate your exact tax owed
- Does **not** constitute professional tax advice
- Does **not** store any of your personal financial data
- Does **not** collect SSNs, bank details, or addresses
"""
    )

    st.markdown("### Your Privacy")
    st.info(PRIVACY_NOTICE)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Start My Tax Guidance",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("interview")

    st.markdown("")

    years_str = ", ".join(str(y) for y in SUPPORTED_TAX_YEARS)
    st.markdown(
        f'<div class="footer-text">'
        f"Federal only &bull; Tax Years {years_str} &bull; Powered by Groq &bull; Free forever"
        "</div>",
        unsafe_allow_html=True,
    )
