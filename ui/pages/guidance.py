"""Guidance page — line-by-line guidance with tabs per form."""

import streamlit as st

from agents.guidance_agent import generate_form_guidance
from ui.components import (
    apply_styles,
    render_disclaimer_banner,
    render_federal_only_banner,
    render_guidance_box,
    render_header,
)
from utils.session_state import get_interview_answers, navigate_to


def render():
    """Render the guidance page."""
    apply_styles()
    render_header()
    render_federal_only_banner()
    render_disclaimer_banner(style="red")

    forms = st.session_state.get("required_forms", [])
    if not forms:
        st.warning("No forms determined yet. Please complete the interview first.")
        if st.button("Go to Interview"):
            navigate_to("interview")
        return

    answers = get_interview_answers()

    # Generate guidance if not already done
    if not st.session_state.get("guidance_by_form"):
        st.markdown("### Generating Your Tax Guidance")
        st.markdown("This may take a minute — we're checking IRS instructions for each line of your forms.")

        guidance_by_form = {}
        for form_info in forms:
            form_name = form_info["form"]
            with st.spinner(f"Checking IRS guidance for {form_name}..."):
                progress_bar = st.progress(0, text=f"Processing {form_name}...")

                def update_progress(current, total, _bar=progress_bar, _name=form_name):
                    if total > 0:
                        _bar.progress(
                            current / total,
                            text=f"{_name}: {current}/{total} lines",
                        )

                guidance = generate_form_guidance(
                    form_name, answers, progress_callback=update_progress
                )
                guidance_by_form[form_name] = guidance
                progress_bar.empty()

        st.session_state.guidance_by_form = guidance_by_form
        st.rerun()

    guidance_by_form = st.session_state.guidance_by_form

    # Initialize confirmed_lines tracking
    if not st.session_state.get("confirmed_lines"):
        st.session_state.confirmed_lines = {}
        for form_name, lines in guidance_by_form.items():
            for g in lines:
                key = f"{form_name}_{g['line']}"
                st.session_state.confirmed_lines[key] = False

    # Count confirmations
    total_lines = sum(len(lines) for lines in guidance_by_form.values())
    confirmed_count = sum(
        1 for v in st.session_state.confirmed_lines.values() if v
    )

    st.markdown("### Your Line-by-Line Tax Guidance")

    # Confirmation tracker
    st.markdown(
        f'<div class="confirmation-tracker">'
        f"{confirmed_count}/{total_lines} lines confirmed"
        "</div>",
        unsafe_allow_html=True,
    )

    st.progress(
        confirmed_count / total_lines if total_lines > 0 else 0,
        text=f"{confirmed_count} of {total_lines} lines confirmed",
    )

    # Tabs per form
    form_names = [f["form"] for f in forms if f["form"] in guidance_by_form]
    if form_names:
        tabs = st.tabs(form_names)

        for tab, form_name in zip(tabs, form_names):
            with tab:
                guidance_list = guidance_by_form.get(form_name, [])
                for g in guidance_list:
                    key = f"{form_name}_{g['line']}"
                    is_confirmed = st.session_state.confirmed_lines.get(key, False)
                    label_suffix = " ✓" if is_confirmed else ""
                    with st.expander(f"{g['line']}: {g.get('label', '')}{label_suffix}"):
                        render_guidance_box(g)
                        confirmed = st.checkbox(
                            f"I confirm I will enter {g['line']} myself",
                            key=f"confirm_{key}",
                            value=is_confirmed,
                        )
                        st.session_state.confirmed_lines[key] = confirmed

    # Proceed button
    st.markdown("---")
    all_confirmed = confirmed_count == total_lines and total_lines > 0

    if not all_confirmed:
        st.info(
            f"Please confirm all {total_lines} lines before proceeding. "
            f"You have {total_lines - confirmed_count} remaining."
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Proceed to Disclaimer",
            type="primary",
            use_container_width=True,
            disabled=not all_confirmed,
        ):
            navigate_to("disclaimer")

    if st.button("Back to Forms Summary"):
        navigate_to("forms_summary")
