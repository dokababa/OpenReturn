"""Download page — generate and download the PDF tax roadmap."""

import streamlit as st

from pdf.cheatsheet_generator import generate_cheatsheet
from ui.components import apply_styles, render_disclaimer_banner, render_federal_only_banner, render_header
from utils.constants import (
    IRS_8843_URL,
    IRS_FREE_FILE_URL,
    IRS_ITIN_URL,
    IRS_VITA_URL,
    IRS_WHERE_TO_FILE_URL,
    TAX_YEAR,
)
from utils.session_state import get_interview_answers, get_selected_tax_year, navigate_to


def render():
    """Render the download page."""
    apply_styles()
    render_header()
    render_federal_only_banner()
    render_disclaimer_banner(style="red")

    answers = get_interview_answers()
    forms = st.session_state.get("required_forms", [])
    guidance = st.session_state.get("guidance_by_form", {})
    selected_year = get_selected_tax_year()

    if not forms or not guidance:
        st.warning("Missing guidance data. Please complete the full flow first.")
        if st.button("Start Over"):
            navigate_to("landing")
        return

    st.markdown(f"### Your Tax Year {selected_year} Roadmap is Ready!")
    st.balloons()

    # Generate PDF
    with st.spinner("Generating your PDF..."):
        pdf_bytes = generate_cheatsheet(
            user_name="Taxpayer",  # No PII collected — generic label
            filing_status=st.session_state.get("filing_status", "Single"),
            is_resident=answers.get("is_resident", True),
            required_forms=forms,
            guidance_by_form=guidance,
            disclaimer_accepted=st.session_state.get("disclaimer_accepted", True),
            selected_tax_year=selected_year,
        )

    # Download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label=f"Download Tax Year {selected_year} Roadmap (PDF)",
            data=pdf_bytes,
            file_name=f"OpenReturn_Tax_Roadmap_{selected_year}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    st.markdown("---")

    # Next steps
    st.markdown("### Next Steps")
    st.markdown(
        f"""
- [ ] Gather all your tax documents (W-2s, 1099s, etc.)
- [ ] Download blank forms from [IRS.gov](https://www.irs.gov/forms-instructions)
- [ ] Follow your roadmap line by line for each form
- [ ] Double-check all numbers against your source documents
- [ ] Sign and date your return
- [ ] File by the deadline: **June 15, {selected_year + 1}** for international filers, or **April 15, {selected_year + 1}** for everyone else
"""
    )

    st.markdown("### Free Filing Resources")
    st.markdown(
        f"""
- **IRS Free File:** File online for free if your income is under $84,000 — [{IRS_FREE_FILE_URL}]({IRS_FREE_FILE_URL})
- **VITA Free Tax Prep:** In-person help for qualifying taxpayers — [{IRS_VITA_URL}]({IRS_VITA_URL})
- **Where to Mail Your Return:** [{IRS_WHERE_TO_FILE_URL}]({IRS_WHERE_TO_FILE_URL})
"""
    )

    # ITIN guide for international students
    if answers.get("is_international_student") or answers.get("is_f_or_j_visa"):
        st.markdown("### International Student Resources")
        with st.expander("Do you have an SSN or ITIN?"):
            st.markdown(
                f"""
You need either a **Social Security Number (SSN)** or an **Individual Taxpayer Identification
Number (ITIN)** to file a US tax return.

**If you work on campus or have OPT/CPT authorization:** You should have an SSN from your employer.

**If you have no US income (zero-income filer):** You still need to file Form 8843, but you
may not need an SSN or ITIN — Form 8843 can be filed without one in some cases.
Check the Form 8843 instructions for details.

**If you have US income but no SSN:** You need to apply for an ITIN using **Form W-7**.
- Download Form W-7: [{IRS_ITIN_URL}]({IRS_ITIN_URL})
- Submit Form W-7 with your tax return and required identity documents
- Processing typically takes 7-11 weeks
- Many university international student offices (ISO/DSO) can help you with this process

**Form 8843 reminder:** Every F-1 and J-1 visa holder must file Form 8843 each year,
even with zero income. The deadline is the same as your tax return.
- Form 8843 info: [{IRS_8843_URL}]({IRS_8843_URL})
"""
            )

    st.markdown("---")

    st.success(
        "Thank you for using OpenReturn! Remember — this is educational guidance only. "
        "If your tax situation is complex, consider consulting a tax professional."
    )

    if st.button("Start Over"):
        from utils.session_state import reset_session_state

        reset_session_state()
        navigate_to("landing")
