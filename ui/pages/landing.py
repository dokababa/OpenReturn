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

    # Primary CTA above the fold
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Start My Tax Guidance",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("interview")

    st.divider()

    # International student callout
    with st.expander("Are you an international student? Read this first."):
        st.markdown(
            """
**OpenReturn is built with international students in mind.** Here's what you should know before filing:

- **You likely file Form 1040-NR**, not the standard Form 1040 — different rules apply
- **Form 8843 is required every year** for F-1 and J-1 visa holders, even if you had zero income
- **Your scholarship may be partially taxable** — the portion covering living expenses (not tuition) is generally taxable
- **Your country may have a tax treaty** with the US that reduces or eliminates tax on your scholarship or wages — the interview will check this
- **Deadline:** International students have until **June 15** to file (not April 15)
- **No SSN?** You may need to apply for an ITIN (Form W-7) — we'll guide you at the end

OpenReturn will walk you through all of this step by step, free of charge.
"""
        )

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

    with st.expander("Important Limits to Know"):
        st.markdown(
            """
- Does **not** file your taxes for you — you submit the return yourself
- Does **not** calculate your exact tax owed — use IRS Free File or a tax professional for that
- Does **not** constitute professional tax or legal advice
- Does **not** store any of your personal financial data
- Does **not** collect SSNs, bank details, or addresses
- **Federal only** — state and local tax filing is not covered
"""
        )

    st.markdown("### Your Privacy")
    st.info(PRIVACY_NOTICE)

    st.markdown("")

    years_str = ", ".join(str(y) for y in SUPPORTED_TAX_YEARS)
    st.markdown(
        f'<div class="footer-text">'
        f"Federal only &bull; Tax Years {years_str} &bull; Powered by Groq &bull; Free forever"
        "</div>",
        unsafe_allow_html=True,
    )
