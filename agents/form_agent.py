"""Form determination agent — decides which IRS forms the user needs."""


def determine_forms(answers: dict) -> list[dict]:
    """
    Determine which IRS forms the user needs based on interview answers.

    Args:
        answers: Dict of interview answers from session state.

    Returns:
        List of form dicts with form name, reason, url, and required flag.
    """
    forms = []

    # Base form — 1040 vs 1040-NR
    if answers.get("is_resident"):
        forms.append({
            "form": "Form 1040",
            "reason": "Your primary federal tax return as a US resident or citizen",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040",
            "required": True,
        })
    else:
        forms.append({
            "form": "Form 1040-NR",
            "reason": "Federal tax return for nonresident aliens",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-1040-nr",
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

    # Form 8833 for treaty benefits
    if answers.get("is_international_student"):
        forms.append({
            "form": "Form 8833",
            "reason": "Claim tax treaty benefits with your home country",
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

    # Form 8863 for education credits
    if answers.get("has_tuition") or answers.get("has_education"):
        forms.append({
            "form": "Form 8863",
            "reason": "Claim education credits (American Opportunity or Lifetime Learning)",
            "irs_url": "https://www.irs.gov/forms-pubs/about-form-8863",
            "required": True,
        })

    return forms
