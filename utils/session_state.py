"""Session state management for OpenReturn."""

import streamlit as st


DEFAULT_SESSION_STATE = {
    "current_page": "landing",
    "interview_step": 0,
    "interview_stage_idx": 0,
    "interview_complete": False,
    "selected_tax_year": None,
    "is_us_citizen": None,
    "is_resident_alien": None,
    "filing_status": None,
    "has_dependents": False,
    "visa_type": None,
    "home_country": None,
    "years_in_us_as_student": None,
    "has_itin": None,
    "has_w2": False,
    "has_1099_nec": False,
    "has_1099_misc": False,
    "has_1099_g": False,
    "has_1099_r": False,
    "has_1042s": False,
    "has_dividends": False,
    "has_capital_gains": False,
    "has_interest": False,
    "has_foreign_income": False,
    "is_international_student": False,
    "has_1098t": False,
    "scholarship_exceeds_tuition": False,
    "has_mortgage": False,
    "has_student_loan": False,
    "has_charitable": False,
    "has_medical": False,
    "has_home_office": False,
    "has_childcare": False,
    "has_education": False,
    "has_retirement_contrib": False,
    "required_forms": [],
    "guidance_by_form": {},
    "confirmed_lines": {},
    "disclaimer_accepted": False,
    "generation_timestamp": None,
}


def init_session_state():
    """Initialize all session state variables with defaults."""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    """Reset all session state to defaults."""
    for key, value in DEFAULT_SESSION_STATE.items():
        st.session_state[key] = value


def navigate_to(page: str):
    """Navigate to a specific page."""
    st.session_state.current_page = page
    st.rerun()


def get_selected_tax_year() -> int:
    """Get the user's selected tax year, falling back to the default."""
    from utils.constants import TAX_YEAR

    year = st.session_state.get("selected_tax_year")
    if year is None:
        return TAX_YEAR
    return int(year)


def get_interview_answers() -> dict:
    """Collect all interview answers from session state into a dict."""
    return {
        "selected_tax_year": get_selected_tax_year(),
        "is_us_citizen": st.session_state.is_us_citizen,
        "is_resident_alien": st.session_state.is_resident_alien,
        "is_resident": (
            st.session_state.is_us_citizen or st.session_state.is_resident_alien
        ),
        "filing_status": st.session_state.filing_status,
        "has_dependents": st.session_state.has_dependents,
        "visa_type": st.session_state.visa_type,
        "home_country": st.session_state.home_country,
        "years_in_us_as_student": st.session_state.years_in_us_as_student,
        "has_itin": st.session_state.has_itin,
        "is_f_or_j_visa": st.session_state.get("visa_type") in ("F-1", "J-1", "OPT (post-F-1)"),
        "has_w2": st.session_state.has_w2,
        "has_1099_nec": st.session_state.has_1099_nec,
        "has_freelance": st.session_state.has_1099_nec,
        "has_1099_misc": st.session_state.has_1099_misc,
        "has_1099_g": st.session_state.has_1099_g,
        "has_1099_r": st.session_state.has_1099_r,
        "has_1042s": st.session_state.has_1042s,
        "has_dividends": st.session_state.has_dividends,
        "has_capital_gains": st.session_state.has_capital_gains,
        "has_stock_sales": st.session_state.has_capital_gains,
        "has_interest": st.session_state.has_interest,
        "has_foreign_income": st.session_state.has_foreign_income,
        "is_international_student": st.session_state.is_international_student,
        "has_1098t": st.session_state.has_1098t,
        "scholarship_exceeds_tuition": st.session_state.scholarship_exceeds_tuition,
        "has_mortgage": st.session_state.has_mortgage,
        "has_student_loan": st.session_state.has_student_loan,
        "has_large_donations": st.session_state.has_charitable,
        "has_charitable": st.session_state.has_charitable,
        "has_large_medical": st.session_state.has_medical,
        "has_medical": st.session_state.has_medical,
        "has_home_office": st.session_state.has_home_office,
        "has_childcare": st.session_state.has_childcare,
        "has_education": st.session_state.has_education,
        "has_tuition": st.session_state.has_education,
        "has_retirement_contrib": st.session_state.has_retirement_contrib,
    }
