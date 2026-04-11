"""Form determination agent — decides which IRS forms the user needs."""

from utils.constants import TREATY_COUNTRIES


# Visa types exempt from Substantial Presence Test (SPT) under IRC §7701(b)(5)
# These individuals do NOT count days toward the 183-day test for a limited period.
SPT_EXEMPT_VISA_TYPES = {"F-1", "F-2", "J-1", "J-2", "M-1", "M-2", "Q-1", "Q-2", "OPT (post-F-1)"}

# Visa types subject to normal SPT — if they meet 183-day test, they're residents
SPT_NORMAL_VISA_TYPES = {"H-1B", "H-4", "L-1", "L-2", "O-1", "O-2", "TN", "E-1", "E-2", "E-3", "R-1"}

# F-1/J-1/OPT holders exempt from FICA for their first 5 years
FICA_EXEMPT_VISA_TYPES = {"F-1", "J-1", "OPT (post-F-1)", "M-1"}


def _files_as_nonresident(answers: dict) -> bool:
    """
    Determine if the user should file as a nonresident alien.

    Rules:
    - US citizens and green card holders → always resident (file 1040)
    - F-1/J-1/M-1/Q-1 visa holders → SPT-exempt for first 5 years → nonresident
    - F-1/J-1 with 5+ years → subject to normal SPT
    - H-1B/L-1/O-1/TN/E-type → normal SPT: resident if 183+ days, else nonresident
    - No visa, not citizen, not resident alien → nonresident
    """
    # US citizens and green card holders always file as residents
    if answers.get("is_us_citizen"):
        return False

    visa_type = answers.get("visa_type", "")
    is_intl = answers.get("is_international_student", False)

    # SPT-exempt visa types (F-1, J-1, M-1, Q-1, OPT)
    if visa_type in SPT_EXEMPT_VISA_TYPES:
        years_in_us = answers.get("years_in_us_as_student", "")
        is_long_term = years_in_us == "5 or more years"
        if not is_long_term:
            # Still within exemption period → nonresident regardless of days
            return True
        # 5+ years → falls through to normal SPT check below

    # For all other cases, use the resident alien determination
    # (based on the 183-day SPT question in the interview)
    is_resident = answers.get("is_resident_alien", False)
    return not is_resident


def determine_forms(answers: dict) -> list[dict]:
    """
    Determine which IRS forms the user needs based on interview answers.

    Covers: US citizens, green card holders, resident aliens, nonresident aliens,
    F-1, J-1, M-1, Q-1 (SPT-exempt), H-1B, H-4, L-1, L-2, O-1, TN, E-type,
    OPT, and other visa categories.

    Args:
        answers: Dict of interview answers from session state.

    Returns:
        List of form dicts with form name, reason, url, and required flag.
    """
    forms = []
    visa_type = answers.get("visa_type", "")
    is_intl = answers.get("is_international_student", False)
    is_citizen = answers.get("is_us_citizen", False)
    home_country = answers.get("home_country")

    files_nonresident = _files_as_nonresident(answers)

    # ────────────────────────────────────────
    # 1. PRIMARY RETURN: 1040 vs 1040-NR
    # ────────────────────────────────────────
    if not files_nonresident:
        forms.append({
            "form": "Form 1040",
            "reason": "Your primary federal tax return as a US citizen or resident alien.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040",
            "required": True,
        })
    else:
        forms.append({
            "form": "Form 1040-NR",
            "reason": "Federal tax return for nonresident aliens. Required when you do not meet the Substantial Presence Test or are exempt from it.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })
        # Schedule OI is ALWAYS required with 1040-NR
        forms.append({
            "form": "Schedule OI (Form 1040-NR)",
            "reason": (
                "Other Information — required attachment to Form 1040-NR. Reports your "
                "visa status, country of citizenship, days in the US, and treaty claims."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })

    # ────────────────────────────────────────
    # 2. SCHEDULE NEC (nonresident income not effectively connected)
    # ────────────────────────────────────────
    # Income like scholarships, 1042-S, dividends, interest, and certain capital gains
    # for nonresidents is taxed at flat 30% (or treaty rate) on Schedule NEC.
    if files_nonresident and (
        answers.get("has_1042s")
        or answers.get("scholarship_exceeds_tuition")
        or answers.get("has_capital_gains")
        or answers.get("has_dividends")
        or answers.get("has_interest")
    ):
        forms.append({
            "form": "Schedule NEC (Form 1040-NR)",
            "reason": (
                "Tax on Income Not Effectively Connected With a US Trade or Business — "
                "reports 1042-S income, taxable scholarships, dividends, interest, and "
                "certain capital gains at a flat 30% rate (or lower treaty rate)."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })

    # ────────────────────────────────────────
    # 3. FORM 8843 — SPT exemption statement
    # ────────────────────────────────────────
    # Required for ALL individuals claiming exempt status from the Substantial
    # Presence Test: F-1, F-2, J-1, J-2, M-1, M-2, Q-1, Q-2 visa holders,
    # even with ZERO income. This is the most commonly missed form.
    if visa_type in SPT_EXEMPT_VISA_TYPES:
        years_in_us = answers.get("years_in_us_as_student", "")
        is_long_term = years_in_us == "5 or more years"
        if not is_long_term:
            forms.append({
                "form": "Form 8843",
                "reason": (
                    f"Required for ALL {visa_type} visa holders claiming exempt status from the "
                    "Substantial Presence Test — you must file this every year, even with zero income."
                ),
                "irs_url": "https://www.irs.gov/forms-pubs/about-form-8843",
                "required": True,
            })

    # ────────────────────────────────────────
    # 4. FORM 8833 — Treaty-based position
    # ────────────────────────────────────────
    # Only if the user's country actually has a treaty with relevant student benefits.
    if is_intl and home_country:
        treaty_info = TREATY_COUNTRIES.get(home_country, {})
        has_real_treaty = (
            treaty_info.get("benefit") is not None
            and treaty_info.get("article") != "No treaty"
        )
        if has_real_treaty:
            forms.append({
                "form": "Form 8833",
                "reason": (
                    f"{home_country} has a US tax treaty ({treaty_info['article']}) "
                    "that may reduce or eliminate tax on your scholarship, fellowship, or "
                    "wage income. File Form 8833 to claim this benefit."
                ),
                "irs_url": "https://www.irs.gov/forms-pubs/about-form-8833",
                "required": False,
            })
        elif treaty_info.get("article") == "No treaty":
            pass  # No treaty — don't suggest 8833
        else:
            # "Other" country or unknown — suggest checking
            forms.append({
                "form": "Form 8833",
                "reason": (
                    "If your home country has a tax treaty with the US, use Form 8833 to claim "
                    "treaty benefits. Check IRS Publication 901 to verify."
                ),
                "irs_url": "https://www.irs.gov/forms-pubs/about-form-8833",
                "required": False,
            })

    # ────────────────────────────────────────
    # 5. SCHEDULE C + SE (self-employment)
    # ────────────────────────────────────────
    if answers.get("has_1099_nec") or answers.get("has_freelance"):
        forms.append({
            "form": "Schedule C",
            "reason": "Report freelance or self-employment profit or loss.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-c-form-1040",
            "required": True,
        })
        # F-1/J-1/OPT students are FICA-exempt for first 5 years — no Schedule SE
        years_in_us = answers.get("years_in_us_as_student", "")
        is_fica_exempt = (
            visa_type in FICA_EXEMPT_VISA_TYPES
            and years_in_us != "5 or more years"
        )
        if not is_fica_exempt:
            forms.append({
                "form": "Schedule SE",
                "reason": "Calculate self-employment tax (Social Security + Medicare) on freelance income.",
                "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-se-form-1040",
                "required": True,
            })

    # ────────────────────────────────────────
    # 6. SCHEDULE D (capital gains)
    # ────────────────────────────────────────
    if answers.get("has_stock_sales") or answers.get("has_capital_gains"):
        if not files_nonresident:
            # Residents report on Schedule D
            forms.append({
                "form": "Schedule D",
                "reason": "Report capital gains and losses from investment sales.",
                "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-d-form-1040",
                "required": True,
            })
        # Nonresidents: capital gains from stocks generally NOT taxed unless
        # present 183+ days. If taxable, reported on Schedule NEC (already added above).

    # ────────────────────────────────────────
    # 7. SCHEDULE A (itemized deductions)
    # ────────────────────────────────────────
    if (
        answers.get("has_mortgage")
        or answers.get("has_large_medical")
        or answers.get("has_large_donations")
    ):
        forms.append({
            "form": "Schedule A",
            "reason": "Itemize deductions if they exceed your standard deduction (mortgage interest, medical expenses, charitable gifts).",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-a-form-1040",
            "required": False,
        })

    # ────────────────────────────────────────
    # 8. FORM 8863 (education credits — residents only)
    # ────────────────────────────────────────
    # Nonresident aliens on 1040-NR CANNOT claim AOTC or LLC.
    if not files_nonresident and (
        answers.get("has_tuition")
        or answers.get("has_education")
        or answers.get("has_1098t")
    ):
        forms.append({
            "form": "Form 8863",
            "reason": "Claim education credits — American Opportunity Credit (up to $2,500) or Lifetime Learning Credit.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-8863",
            "required": True,
        })

    # ────────────────────────────────────────
    # 9. FORM 2441 (childcare credit)
    # ────────────────────────────────────────
    if answers.get("has_childcare"):
        forms.append({
            "form": "Form 2441",
            "reason": "Claim the Child and Dependent Care Credit for work-related childcare expenses.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-2441",
            "required": True,
        })

    # ────────────────────────────────────────
    # 10. FORM W-7 (ITIN application)
    # ────────────────────────────────────────
    if not is_citizen and is_intl and answers.get("has_itin") is False:
        forms.append({
            "form": "Form W-7",
            "reason": (
                "You need an SSN or ITIN to file a tax return. Since you indicated you don't "
                "have one, apply for an ITIN using Form W-7. Submit it with your tax return."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-w-7",
            "required": True,
        })

    # ────────────────────────────────────────
    # 11. FOREIGN EARNED INCOME (residents with foreign income)
    # ────────────────────────────────────────
    if not files_nonresident and answers.get("has_foreign_income"):
        forms.append({
            "form": "Form 2555",
            "reason": "Claim the Foreign Earned Income Exclusion or Foreign Housing Exclusion for income earned abroad.",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-2555",
            "required": False,
        })

    return forms
