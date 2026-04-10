"""Form determination agent — decides which IRS forms the user needs."""

from utils.constants import TREATY_COUNTRIES


def determine_forms(answers: dict) -> list[dict]:
    """
    Determine which IRS forms the user needs based on interview answers.

    Args:
        answers: Dict of interview answers from session state.

    Returns:
        List of form dicts with form name, reason, url, and required flag.
    """
    forms = []
    is_f_or_j = answers.get("is_f_or_j_visa", False)
    is_intl = answers.get("is_international_student", False)
    home_country = answers.get("home_country")

    # F-1/J-1 students are exempt from Substantial Presence Test for first 5 years,
    # so they almost always file 1040-NR as nonresident aliens.
    years_in_us = answers.get("years_in_us_as_student", "")
    is_long_term_student = years_in_us == "5 or more years"
    files_as_nonresident = not answers.get("is_resident") or (is_f_or_j and not is_long_term_student)

    # Base form — 1040 vs 1040-NR
    if not files_as_nonresident:
        forms.append({
            "form": "Form 1040",
            "reason": "Your primary federal tax return as a US resident or citizen",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040",
            "required": True,
        })
    else:
        forms.append({
            "form": "Form 1040-NR",
            "reason": "Federal tax return for nonresident aliens — required for F-1/J-1 students in their first 5 years",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })
        # Schedule OI — required attachment to 1040-NR
        forms.append({
            "form": "Schedule OI (Form 1040-NR)",
            "reason": (
                "Other Information — required attachment to Form 1040-NR. Reports your "
                "visa status, days present in the US, and tax treaty claims."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })

    # Schedule NEC — income not effectively connected with a US trade or business
    # (e.g. scholarship income, 1042-S income for nonresidents)
    if files_as_nonresident and (
        answers.get("has_1042s")
        or answers.get("scholarship_exceeds_tuition")
        or answers.get("has_capital_gains")
    ):
        forms.append({
            "form": "Schedule NEC (Form 1040-NR)",
            "reason": (
                "Tax on Income Not Effectively Connected With a US Trade or Business — "
                "reports scholarship/fellowship income, 1042-S income, dividends, and "
                "certain capital gains taxed at a flat 30% (or lower treaty rate)."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
            "required": True,
        })

    # Form 8843 — REQUIRED for all F-1, J-1, and certain other visa holders,
    # even with zero income. Most commonly missed form by students.
    if is_f_or_j or (is_intl and answers.get("visa_type") in ("H-4", "Other")):
        forms.append({
            "form": "Form 8843",
            "reason": (
                "Required for ALL F-1 and J-1 visa holders every year — even with zero income. "
                "This declares your exempt status from the Substantial Presence Test."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-8843",
            "required": True,
        })

    # Schedule C + SE for self-employment
    if answers.get("has_1099_nec") or answers.get("has_freelance"):
        forms.append({
            "form": "Schedule C",
            "reason": "Report freelance/self-employment profit or loss",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-c-form-1040",
            "required": True,
        })
        forms.append({
            "form": "Schedule SE",
            "reason": "Calculate self-employment tax (Social Security + Medicare)",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-se-form-1040",
            "required": True,
        })

    # Schedule A for itemized deductions
    if (
        answers.get("has_mortgage")
        or answers.get("has_large_medical")
        or answers.get("has_large_donations")
    ):
        forms.append({
            "form": "Schedule A",
            "reason": "Itemize deductions if they exceed your standard deduction",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-a-form-1040",
            "required": False,
        })

    # Schedule D for capital gains
    if answers.get("has_stock_sales") or answers.get("has_capital_gains"):
        forms.append({
            "form": "Schedule D",
            "reason": "Report capital gains and losses from investments",
            "irs_url": "https://www.irs.gov/forms-pubs/about-schedule-d-form-1040",
            "required": True,
        })

    # Form 8833 — treaty-based position disclosure.
    # Only recommend if the user's home country actually has a treaty with student benefits.
    treaty_info = TREATY_COUNTRIES.get(home_country or "", {})
    has_real_treaty = treaty_info.get("benefit") is not None and treaty_info.get("article") != "No treaty"
    if is_intl and has_real_treaty:
        forms.append({
            "form": "Form 8833",
            "reason": (
                f"{home_country} has a US tax treaty ({treaty_info['article']}) "
                "that may reduce or eliminate tax on your scholarship/fellowship income. "
                "Use Form 8833 to claim this benefit."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-8833",
            "required": False,
        })
    elif is_intl and not has_real_treaty and home_country:
        forms.append({
            "form": "Form 8833",
            "reason": (
                "If your home country has a tax treaty with the US, use Form 8833 to claim "
                "treaty benefits. Check IRS Publication 901 to verify your country's treaty status."
            ),
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-8833",
            "required": False,
        })

    # Form 2441 for childcare
    if answers.get("has_childcare"):
        forms.append({
            "form": "Form 2441",
            "reason": "Claim the Child and Dependent Care Credit",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-2441",
            "required": True,
        })

    # Form 8863 for education credits (residents only —
    # nonresident aliens on 1040-NR generally cannot claim AOTC)
    if answers.get("has_tuition") or answers.get("has_education") or answers.get("has_1098t"):
        if not files_as_nonresident:
            forms.append({
                "form": "Form 8863",
                "reason": "Claim education credits — American Opportunity Credit (up to $2,500) or Lifetime Learning Credit",
                "irs_url": "https://www.irs.gov/forms-pubs/about-form-8863",
                "required": True,
            })

    return forms
