"""Interview page — multi-stage with grouped inputs per stage."""

import streamlit as st

from agents.interview_agent import (
    get_active_questions,
    get_current_stage,
    get_stage_number,
    get_total_questions,
    INTERVIEW_QUESTIONS,
)
from ui.components import apply_styles, render_disclaimer_banner, render_header
from utils.constants import INTERVIEW_STAGES
from utils.session_state import navigate_to


# Income form questions that should be shown as number-input counters on one screen
INCOME_FORM_KEYS = [
    ("has_w2", "W-2", "Wages from an employer"),
    ("has_1099_nec", "1099-NEC", "Freelance / contract income"),
    ("has_1099_misc", "1099-MISC", "Other income (rents, royalties, prizes)"),
    ("has_1099_g", "1099-G", "Unemployment compensation"),
    ("has_1099_r", "1099-R", "Retirement distributions"),
    ("has_1042s", "1042-S", "Foreign person's US source income"),
    ("has_1098t", "1098-T", "Tuition statement from your school"),
]

# These income questions are yes/no and stay as separate questions
INCOME_YESNO_KEYS = {"has_capital_gains", "has_foreign_income", "scholarship_exceeds_tuition"}


def _render_stage_select(questions: list[dict]):
    """Render select-type questions for the current stage."""
    for q in questions:
        options = q.get("options", [])
        current_val = st.session_state.get(q["state_key"])
        # Find the default index
        default_idx = 0
        if current_val and str(current_val) in options:
            default_idx = options.index(str(current_val)) + 1

        st.markdown(f"### {q['text']}")
        st.markdown(
            f'<div class="question-why">{q["why"]}</div>',
            unsafe_allow_html=True,
        )
        selected = st.selectbox(
            "Select one:",
            options=["-- Choose --"] + options,
            index=default_idx,
            key=f"sel_{q['id']}",
            label_visibility="collapsed",
        )
        if selected and selected != "-- Choose --":
            value = selected
            if q["state_key"] == "selected_tax_year":
                value = int(selected)
            st.session_state[q["state_key"]] = value


def _render_stage_yesno(questions: list[dict]):
    """Render yes/no questions as toggles."""
    for q in questions:
        current = st.session_state.get(q["state_key"])
        st.markdown(f"**{q['text']}**")
        st.markdown(
            f'<div class="question-why">{q["why"]}</div>',
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button(
                "Yes",
                key=f"yes_{q['id']}",
                use_container_width=True,
                type="primary" if current is True else "secondary",
            ):
                st.session_state[q["state_key"]] = True
                st.rerun()
        with col2:
            if st.button(
                "No",
                key=f"no_{q['id']}",
                use_container_width=True,
                type="primary" if current is False else "secondary",
            ):
                st.session_state[q["state_key"]] = False
                st.rerun()
        st.markdown("")


def _render_income_forms_screen():
    """Render the income forms screen as a single grouped counter page."""
    st.markdown("### How many of each tax form did you receive?")
    st.markdown(
        '<div class="question-why">'
        "Set each to 0 if you didn't receive that form. "
        "This helps us determine which IRS forms and schedules you need."
        "</div>",
        unsafe_allow_html=True,
    )

    # Filter out 1042-S for US citizens (it's only for foreign persons)
    is_citizen = st.session_state.get("is_us_citizen") is True
    visible_forms = [
        f for f in INCOME_FORM_KEYS
        if not (f[0] == "has_1042s" and is_citizen)
    ]

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True,
    )

    for state_key, form_name, description in visible_forms:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f'<div class="form-count-label">{form_name}</div>'
                f'<div class="form-count-why">{description}</div>',
                unsafe_allow_html=True,
            )
        with col2:
            count = st.number_input(
                form_name,
                min_value=0,
                max_value=20,
                value=1 if st.session_state.get(state_key) else 0,
                key=f"count_{state_key}",
                label_visibility="collapsed",
            )
            st.session_state[state_key] = count > 0

    st.markdown("</div>", unsafe_allow_html=True)


def _get_stage_questions(stage_key: str, session_state: dict) -> list[dict]:
    """Get active questions for a specific stage."""
    questions = []
    for q in INTERVIEW_QUESTIONS:
        if q["stage"] != stage_key:
            continue
        skip_fn = q.get("skip_if")
        if skip_fn and skip_fn(session_state):
            continue
        questions.append(q)
    return questions


def render():
    """Render the interview page, one stage at a time."""
    apply_styles()
    render_header()

    # Initialize interview_stage if not set
    if "interview_stage_idx" not in st.session_state:
        st.session_state.interview_stage_idx = 0

    stage_keys = list(INTERVIEW_STAGES.keys())
    stage_idx = st.session_state.interview_stage_idx
    total_stages = len(stage_keys)

    # If past all stages, go to forms summary
    if stage_idx >= total_stages:
        st.session_state.interview_complete = True
        navigate_to("forms_summary")
        return

    current_stage_key = stage_keys[stage_idx]
    current_stage_name = INTERVIEW_STAGES[current_stage_key]
    session_dict = dict(st.session_state)

    # Progress bar
    st.progress(
        (stage_idx + 1) / total_stages,
        text=f"Stage {stage_idx + 1} of {total_stages} -- {current_stage_name}",
    )

    render_disclaimer_banner()

    # Get questions for this stage
    stage_questions = _get_stage_questions(current_stage_key, session_dict)

    if not stage_questions:
        # Skip empty stages
        st.session_state.interview_stage_idx += 1
        st.rerun()
        return

    # Special handling for the income stage: show form counters + remaining yes/no
    if current_stage_key == "income":
        _render_income_forms_screen()

        # Remaining income yes/no questions (investments, foreign income)
        yesno_qs = [q for q in stage_questions if q["state_key"] in INCOME_YESNO_KEYS]
        if yesno_qs:
            st.markdown("---")
            _render_stage_yesno(yesno_qs)

    else:
        select_qs = [q for q in stage_questions if q["type"] == "select"]
        yesno_qs = [q for q in stage_questions if q["type"] == "yes_no"]

        if select_qs:
            _render_stage_select(select_qs)
        if yesno_qs:
            if select_qs:
                st.markdown("---")
            _render_stage_yesno(yesno_qs)

    # Navigation buttons
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if stage_idx > 0:
            if st.button("Back", use_container_width=True):
                st.session_state.interview_stage_idx -= 1
                st.rerun()

    with col2:
        # Validate required fields before allowing continue
        can_continue = True
        for q in stage_questions:
            if q["type"] == "select":
                val = st.session_state.get(q["state_key"])
                if val is None:
                    can_continue = False
                    break
            elif q["type"] == "yes_no" and q["state_key"] not in INCOME_YESNO_KEYS:
                # For non-income yes/no, require an answer
                val = st.session_state.get(q["state_key"])
                if val is None and current_stage_key != "income":
                    can_continue = False
                    break

        button_label = "Continue" if stage_idx < total_stages - 1 else "See My Forms"
        if st.button(
            button_label,
            type="primary",
            use_container_width=True,
            disabled=not can_continue,
        ):
            st.session_state.interview_stage_idx += 1
            st.rerun()

    if not can_continue:
        st.caption("Please answer all questions above to continue.")
