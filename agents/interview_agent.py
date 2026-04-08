"""LangGraph-powered conversational interview agent."""
from __future__ import annotations

from utils.constants import FILING_STATUSES, INTERVIEW_STAGES, SUPPORTED_TAX_YEARS


def _is_citizen_or_resident(s: dict) -> bool:
    """True if user is a US citizen OR a resident alien."""
    return s.get("is_us_citizen") is True or s.get("is_resident_alien") is True


# Each question: id, text, why, stage, state_key, question_type, options (if any),
# and skip_condition (optional callable that checks session_state to skip)
INTERVIEW_QUESTIONS = [
    # STAGE 0 — Tax Year
    {
        "id": 0,
        "text": "Which tax year are you filing for?",
        "why": "Different tax years have different rules, deduction amounts, and form versions. We'll tailor all guidance to the year you choose.",
        "stage": "tax_year",
        "state_key": "selected_tax_year",
        "type": "select",
        "options": [str(y) for y in SUPPORTED_TAX_YEARS],
    },
    # STAGE 1 — Residency
    {
        "id": 1,
        "text": "Are you a US Citizen or Green Card holder?",
        "why": "This determines which tax form you'll use as your primary return.",
        "stage": "residency",
        "state_key": "is_us_citizen",
        "type": "yes_no",
    },
    {
        "id": 2,
        "text": "Were you physically present in the US for 183 or more days this year?",
        "why": "If you're not a citizen/permanent resident, this helps determine if you file as a resident or nonresident alien.",
        "stage": "residency",
        "state_key": "is_resident_alien",
        "type": "yes_no",
        # Only ask non-citizens
        "skip_if": lambda s: s.get("is_us_citizen") is True,
    },
    {
        "id": 13,
        "text": "Are you an international student or on a visa (F-1, J-1, H-1B, OPT, etc.)?",
        "why": "Visa holders may have special tax treaty benefits and different filing requirements.",
        "stage": "residency",
        "state_key": "is_international_student",
        "type": "yes_no",
        # Only ask non-citizens — a US citizen can't be an international student
        "skip_if": lambda s: s.get("is_us_citizen") is True,
    },
    # STAGE 2 — Personal
    {
        "id": 3,
        "text": "What is your filing status?",
        "why": "Your filing status affects your tax rates and standard deduction amount.",
        "stage": "personal",
        "state_key": "filing_status",
        "type": "select",
        "options": FILING_STATUSES,
    },
    {
        "id": 4,
        "text": "Do you have any dependents (children or qualifying relatives)?",
        "why": "Dependents can qualify you for valuable tax credits and a higher standard deduction.",
        "stage": "personal",
        "state_key": "has_dependents",
        "type": "yes_no",
    },
    # STAGE 3 — Income
    # Form-count questions are handled by the interview UI as number inputs.
    # These remain as yes_no in the data model so the form agent still works.
    {
        "id": 5,
        "text": "Did you receive a W-2 from an employer this year?",
        "why": "W-2 wages are reported on the main line of your tax return.",
        "stage": "income",
        "state_key": "has_w2",
        "type": "yes_no",
    },
    {
        "id": 6,
        "text": "Did you receive a 1099-NEC for freelance or contract work?",
        "why": "Freelance income requires Schedule C and self-employment tax (Schedule SE).",
        "stage": "income",
        "state_key": "has_1099_nec",
        "type": "yes_no",
    },
    {
        "id": 7,
        "text": "Did you receive a 1099-MISC for other income?",
        "why": "Miscellaneous income like rents, royalties, or prizes gets reported differently.",
        "stage": "income",
        "state_key": "has_1099_misc",
        "type": "yes_no",
    },
    {
        "id": 8,
        "text": "Did you receive a 1099-G for unemployment compensation?",
        "why": "Unemployment benefits are taxable and must be reported on your return.",
        "stage": "income",
        "state_key": "has_1099_g",
        "type": "yes_no",
    },
    {
        "id": 9,
        "text": "Did you receive a 1099-R for retirement distributions?",
        "why": "Retirement account withdrawals may be partially or fully taxable.",
        "stage": "income",
        "state_key": "has_1099_r",
        "type": "yes_no",
    },
    {
        "id": 10,
        "text": "Did you receive a 1042-S (foreign person's US source income)?",
        "why": "This form reports income paid to nonresident aliens and affects which return you file.",
        "stage": "income",
        "state_key": "has_1042s",
        "type": "yes_no",
        # Only relevant for non-citizens / non-residents
        "skip_if": lambda s: s.get("is_us_citizen") is True and s.get("is_international_student") is not True,
    },
    {
        "id": 11,
        "text": "Did you have investment income (dividends, stock sales, or interest)?",
        "why": "Investment income may require Schedule D and affects your total taxable income.",
        "stage": "income",
        "state_key": "has_capital_gains",
        "type": "yes_no",
    },
    {
        "id": 12,
        "text": "Did you earn income in a foreign country?",
        "why": "Foreign-earned income has special reporting rules and may qualify for the Foreign Earned Income Exclusion.",
        "stage": "income",
        "state_key": "has_foreign_income",
        "type": "yes_no",
    },
    # STAGE 4 — Deductions
    {
        "id": 14,
        "text": "Do you own a home and pay mortgage interest?",
        "why": "Mortgage interest can be itemized on Schedule A if it exceeds your standard deduction.",
        "stage": "deductions",
        "state_key": "has_mortgage",
        "type": "yes_no",
    },
    {
        "id": 15,
        "text": "Did you pay student loan interest this year?",
        "why": "You can deduct up to $2,500 in student loan interest even without itemizing.",
        "stage": "deductions",
        "state_key": "has_student_loan",
        "type": "yes_no",
    },
    {
        "id": 16,
        "text": "Did you make charitable donations over $500?",
        "why": "Large charitable contributions can be itemized as deductions on Schedule A.",
        "stage": "deductions",
        "state_key": "has_charitable",
        "type": "yes_no",
    },
    {
        "id": 17,
        "text": "Did you have significant medical expenses this year?",
        "why": "Medical expenses exceeding 7.5% of your income can be deducted on Schedule A.",
        "stage": "deductions",
        "state_key": "has_medical",
        "type": "yes_no",
    },
    {
        "id": 18,
        "text": "Did you work from home as a self-employed person?",
        "why": "Self-employed home office expenses can reduce your business income on Schedule C.",
        "stage": "deductions",
        "state_key": "has_home_office",
        "type": "yes_no",
        # Only show if user has freelance income
        "skip_if": lambda s: not s.get("has_1099_nec"),
    },
    # STAGE 5 — Credits
    {
        "id": 19,
        "text": "Did you pay for childcare so you could work?",
        "why": "Childcare expenses may qualify you for the Child and Dependent Care Credit.",
        "stage": "credits",
        "state_key": "has_childcare",
        "type": "yes_no",
        # Only relevant if user has dependents
        "skip_if": lambda s: not s.get("has_dependents"),
    },
    {
        "id": 20,
        "text": "Are you or a dependent paying college tuition?",
        "why": "Education expenses can qualify for the American Opportunity or Lifetime Learning Credit.",
        "stage": "credits",
        "state_key": "has_education",
        "type": "yes_no",
    },
    {
        "id": 21,
        "text": "Did you contribute to an IRA or retirement account?",
        "why": "Retirement contributions may be tax-deductible and reduce your taxable income.",
        "stage": "credits",
        "state_key": "has_retirement_contrib",
        "type": "yes_no",
    },
]


def get_active_questions(session_state: dict) -> list[dict]:
    """Return the list of questions that apply, skipping those with met skip conditions."""
    active = []
    for q in INTERVIEW_QUESTIONS:
        skip_fn = q.get("skip_if")
        if skip_fn and skip_fn(session_state):
            continue
        active.append(q)
    return active


def get_current_question(session_state: dict) -> dict | None:
    """Get the current question based on interview_step."""
    questions = get_active_questions(session_state)
    step = session_state.get("interview_step", 0)
    if step < len(questions):
        return questions[step]
    return None


def get_total_questions(session_state: dict) -> int:
    """Get the total number of active questions."""
    return len(get_active_questions(session_state))


def get_current_stage(session_state: dict) -> str:
    """Get the stage name for the current question."""
    q = get_current_question(session_state)
    if q:
        return INTERVIEW_STAGES.get(q["stage"], q["stage"])
    return "Complete"


def get_stage_number(session_state: dict) -> int:
    """Get the current stage number (1-5)."""
    q = get_current_question(session_state)
    if q:
        stages = list(INTERVIEW_STAGES.keys())
        try:
            return stages.index(q["stage"]) + 1
        except ValueError:
            return 1
    return 5
