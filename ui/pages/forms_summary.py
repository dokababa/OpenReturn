"""Forms summary page — shows which IRS forms the user needs."""

import streamlit as st

from agents.form_agent import determine_forms
from ui.components import (
    apply_styles,
    render_disclaimer_banner,
    render_form_card,
    render_header,
)
from utils.session_state import get_interview_answers, get_selected_tax_year, navigate_to


def render():
    """Render the forms summary page."""
    apply_styles()
    render_header()
    render_disclaimer_banner()

    answers = get_interview_answers()
    forms = determine_forms(answers)
    st.session_state.required_forms = forms

    selected_year = get_selected_tax_year()
    st.markdown(f"### Here are the forms you need for Tax Year {selected_year}:")
    st.markdown(
        f"Based on your answers, you'll need **{len(forms)} form(s)** "
        f"for your {selected_year} federal tax return."
    )

    required_forms = [f for f in forms if f.get("required")]
    optional_forms = [f for f in forms if not f.get("required")]

    if required_forms:
        st.markdown("**Required Forms:**")
        for form in required_forms:
            render_form_card(form)

    if optional_forms:
        st.markdown("")
        st.markdown("**Optional Forms (may benefit you):**")
        for form in optional_forms:
            render_form_card(form)

    st.markdown("")
    st.info(
        "Next, we'll generate **line-by-line guidance** for each form. "
        "This uses AI to explain what each line means and what you should enter, "
        "with citations to official IRS instructions."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Get Line-by-Line Guidance",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("guidance")

    st.markdown("---")
    if st.button("Back to Interview"):
        # Go back to the last interview stage
        from utils.constants import INTERVIEW_STAGES
        total_stages = len(INTERVIEW_STAGES)
        st.session_state.interview_stage_idx = max(0, total_stages - 1)
        st.session_state.interview_complete = False
        navigate_to("interview")
