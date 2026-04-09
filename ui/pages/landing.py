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

    # No paid software banner
    st.markdown(
        '<div style="background:#f0faf4;border:1px solid #86efac;border-left:4px solid #16a34a;'
        'border-radius:6px;padding:0.6rem 1rem;margin:0.5rem 0 1rem 0;font-size:0.9rem;color:#14532d;">'
        "<strong>Free for everyone, especially international students.</strong> "
        "You do not need to pay for tax filing software to understand your US tax obligations. "
        "OpenReturn covers F-1, J-1, and other visa holders — including Form 8843, "
        "treaty benefits, and 1040-NR guidance — at no cost."
        "</div>",
        unsafe_allow_html=True,
    )

    # Trust strip
    st.markdown(
        '<div style="display:flex; gap:0.5rem; margin: 1rem 0 1.5rem 0;">'
        '<div class="trust-item"><span class="trust-icon">$0</span>Always Free</div>'
        '<div class="trust-item"><span class="trust-icon">🔒</span>No Data Stored</div>'
        '<div class="trust-item"><span class="trust-icon">✓</span>No Signup Needed</div>'
        '<div class="trust-item"><span class="trust-icon">📖</span>IRS-Cited</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # Flow diagram
    st.markdown("**How it works:**")
    cols = st.columns([3, 1, 3, 1, 3, 1, 3])
    flow_steps = ["Interview", "Form ID", "Guidance", "PDF"]
    for i, step in enumerate(flow_steps):
        with cols[i * 2]:
            st.markdown(f'<div class="flow-step"><span>{step}</span></div>', unsafe_allow_html=True)
        if i < len(flow_steps) - 1:
            with cols[i * 2 + 1]:
                st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)

    st.markdown("")

    # --- PRIMARY CTA — above the fold ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Start My Tax Guidance",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("interview")

    # Disclaimer below the CTA so it doesn't block the first impression
    render_disclaimer_banner(style="yellow")

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

    # Replaces the "Does NOT Do" wall of negatives
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
