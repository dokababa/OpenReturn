"""Tax logic helpers for OpenReturn."""
from __future__ import annotations

from utils.constants import TAX_YEAR

# Standard deduction amounts by year
STANDARD_DEDUCTIONS_BY_YEAR = {
    2025: {
        "Single": 15000,
        "Married Filing Jointly": 30000,
        "Married Filing Separately": 15000,
        "Head of Household": 22500,
    },
    2024: {
        "Single": 14600,
        "Married Filing Jointly": 29200,
        "Married Filing Separately": 14600,
        "Head of Household": 21900,
    },
    2023: {
        "Single": 13850,
        "Married Filing Jointly": 27700,
        "Married Filing Separately": 13850,
        "Head of Household": 20800,
    },
}

# Default (latest year) — used when no year is specified
STANDARD_DEDUCTIONS = STANDARD_DEDUCTIONS_BY_YEAR[TAX_YEAR]

# Tax brackets (single) by year
TAX_BRACKETS_SINGLE_BY_YEAR = {
    2025: [
        (11925, 0.10),
        (48475, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250525, 0.32),
        (626350, 0.35),
        (float("inf"), 0.37),
    ],
    2024: [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float("inf"), 0.37),
    ],
    2023: [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
        (231250, 0.32),
        (578125, 0.35),
        (float("inf"), 0.37),
    ],
}

TAX_BRACKETS_SINGLE = TAX_BRACKETS_SINGLE_BY_YEAR[TAX_YEAR]

# Form line definitions — which lines need guidance for each form
FORM_LINES = {
    "Form 1040": [
        # Top of form — identification fields
        {"line": "Header — Name", "label": "Your full legal name and spouse's name (if filing jointly)"},
        {"line": "Header — SSN", "label": "Your Social Security number"},
        {"line": "Header — Address", "label": "Your current mailing address"},
        {"line": "Header — Filing Status", "label": "Check the box for your filing status"},
        {"line": "Header — Digital Assets", "label": "Digital assets question (cryptocurrency)"},
        {"line": "Header — Dependents", "label": "Dependent names, SSNs, and relationship"},
        # Income lines
        {"line": "Line 1a", "label": "Wages, salaries, tips (W-2 Box 1)"},
        {"line": "Line 1z", "label": "Total from adding lines 1a through 1h"},
        {"line": "Line 2a", "label": "Tax-exempt interest"},
        {"line": "Line 2b", "label": "Taxable interest"},
        {"line": "Line 3a", "label": "Qualified dividends"},
        {"line": "Line 3b", "label": "Ordinary dividends"},
        {"line": "Line 4a", "label": "IRA distributions"},
        {"line": "Line 4b", "label": "Taxable IRA distributions"},
        {"line": "Line 5a", "label": "Pensions and annuities"},
        {"line": "Line 5b", "label": "Taxable pensions and annuities"},
        {"line": "Line 7", "label": "Capital gain or loss (from Schedule D)"},
        {"line": "Line 8", "label": "Other income (Schedule 1, line 10)"},
        {"line": "Line 9", "label": "Total income"},
        {"line": "Line 10", "label": "Adjustments to income (Schedule 1, line 26)"},
        {"line": "Line 11", "label": "Adjusted gross income"},
        {"line": "Line 12", "label": "Standard deduction or itemized deductions"},
        {"line": "Line 13", "label": "Qualified business income deduction"},
        {"line": "Line 14", "label": "Total deductions"},
        {"line": "Line 15", "label": "Taxable income"},
        {"line": "Line 16", "label": "Tax"},
        {"line": "Line 24", "label": "Total tax"},
        {"line": "Line 25a", "label": "Federal income tax withheld from W-2s"},
        {"line": "Line 33", "label": "Total payments"},
        {"line": "Line 34", "label": "Overpayment (refund)"},
        {"line": "Line 35a", "label": "Refund — direct deposit: bank routing number"},
        {"line": "Line 35b", "label": "Refund — direct deposit: account type (checking/savings)"},
        {"line": "Line 35c", "label": "Refund — direct deposit: account number"},
        {"line": "Line 37", "label": "Amount you owe"},
        # Signature
        {"line": "Sign Here — Signature", "label": "Your signature and date"},
        {"line": "Sign Here — Occupation", "label": "Your occupation"},
        {"line": "Sign Here — Phone", "label": "Your daytime phone number"},
    ],
    "Form 1040-NR": [
        # Top of form — identification fields
        {"line": "Header — Name", "label": "Your full legal name"},
        {"line": "Header — SSN or ITIN", "label": "Your SSN or Individual Taxpayer Identification Number (ITIN)"},
        {"line": "Header — Address", "label": "Your current US or foreign mailing address"},
        {"line": "Header — Country", "label": "Country of citizenship and country of residence"},
        {"line": "Header — Filing Status", "label": "Check the box for your filing status"},
        {"line": "Header — Dependents", "label": "Dependent names, SSNs/ITINs, and relationship"},
        # Income lines
        {"line": "Line 1a", "label": "Wages, salaries, tips (W-2 Box 1)"},
        {"line": "Line 1b", "label": "Scholarship/fellowship grants"},
        {"line": "Line 2a", "label": "Tax-exempt interest"},
        {"line": "Line 2b", "label": "Taxable interest"},
        {"line": "Line 3a", "label": "Qualified dividends"},
        {"line": "Line 3b", "label": "Ordinary dividends"},
        {"line": "Line 7", "label": "Capital gain or loss"},
        {"line": "Line 8", "label": "Other income"},
        {"line": "Line 9", "label": "Total income"},
        {"line": "Line 10", "label": "Adjustments to income"},
        {"line": "Line 11", "label": "Adjusted gross income"},
        {"line": "Line 12", "label": "Itemized deductions"},
        {"line": "Line 14", "label": "Total deductions"},
        {"line": "Line 15", "label": "Taxable income"},
        {"line": "Line 16", "label": "Tax"},
        {"line": "Line 24", "label": "Total tax"},
        {"line": "Line 25a", "label": "Federal income tax withheld"},
        {"line": "Line 33", "label": "Total payments"},
        {"line": "Line 34", "label": "Overpayment"},
        {"line": "Line 35a", "label": "Refund — direct deposit: bank routing number"},
        {"line": "Line 35b", "label": "Refund — direct deposit: account type (checking/savings)"},
        {"line": "Line 35c", "label": "Refund — direct deposit: account number"},
        {"line": "Line 37", "label": "Amount you owe"},
        # Signature
        {"line": "Sign Here — Signature", "label": "Your signature and date"},
        {"line": "Sign Here — Occupation", "label": "Your occupation"},
    ],
    "Schedule C": [
        # Header
        {"line": "Header — Name", "label": "Name of proprietor (your name)"},
        {"line": "Header — SSN", "label": "Social Security number of proprietor"},
        {"line": "Header — Business Name", "label": "Principal business or profession name"},
        {"line": "Header — EIN", "label": "Employer ID number (EIN) if you have one"},
        {"line": "Header — Business Address", "label": "Business address (if different from home)"},
        {"line": "Header — Accounting Method", "label": "Accounting method (cash, accrual, or other)"},
        # Income/expense lines
        {"line": "Line 1", "label": "Gross receipts or sales"},
        {"line": "Line 4", "label": "Cost of goods sold"},
        {"line": "Line 7", "label": "Gross income"},
        {"line": "Line 8", "label": "Advertising expenses"},
        {"line": "Line 10", "label": "Car and truck expenses"},
        {"line": "Line 11", "label": "Commissions and fees"},
        {"line": "Line 17", "label": "Legal and professional services"},
        {"line": "Line 18", "label": "Office expense"},
        {"line": "Line 22", "label": "Supplies"},
        {"line": "Line 24a", "label": "Travel expenses"},
        {"line": "Line 25", "label": "Utilities"},
        {"line": "Line 28", "label": "Total expenses"},
        {"line": "Line 29", "label": "Tentative profit or loss"},
        {"line": "Line 30", "label": "Home office deduction (Form 8829)"},
        {"line": "Line 31", "label": "Net profit or loss"},
    ],
    "Schedule A": [
        {"line": "Header — Name", "label": "Name(s) shown on Form 1040"},
        {"line": "Header — SSN", "label": "Your Social Security number"},
        {"line": "Line 1", "label": "Medical and dental expenses"},
        {"line": "Line 4", "label": "Medical deduction (amount exceeding 7.5% of AGI)"},
        {"line": "Line 5a", "label": "State and local income taxes or sales taxes"},
        {"line": "Line 5b", "label": "State and local personal property taxes"},
        {"line": "Line 5c", "label": "State and local real estate taxes"},
        {"line": "Line 5d", "label": "Total state and local taxes (max $10,000)"},
        {"line": "Line 8a", "label": "Home mortgage interest (Form 1098)"},
        {"line": "Line 10", "label": "Investment interest"},
        {"line": "Line 11", "label": "Gifts to charity by cash or check"},
        {"line": "Line 12", "label": "Gifts to charity other than cash or check"},
        {"line": "Line 14", "label": "Total charitable contributions"},
        {"line": "Line 17", "label": "Total itemized deductions"},
    ],
    "Schedule D": [
        {"line": "Header — Name", "label": "Name(s) shown on return"},
        {"line": "Header — SSN", "label": "Your Social Security number"},
        {"line": "Line 1a", "label": "Short-term transactions from 1099-B (basis reported)"},
        {"line": "Line 7", "label": "Net short-term capital gain or loss"},
        {"line": "Line 8a", "label": "Long-term transactions from 1099-B (basis reported)"},
        {"line": "Line 15", "label": "Net long-term capital gain or loss"},
        {"line": "Line 16", "label": "Combine short-term and long-term"},
        {"line": "Line 21", "label": "Net capital gain or loss to report on Form 1040"},
    ],
    "Schedule SE": [
        {"line": "Header — Name", "label": "Name of person with self-employment income"},
        {"line": "Header — SSN", "label": "Social Security number of person above"},
        {"line": "Line 2", "label": "Net earnings from self-employment (from Schedule C)"},
        {"line": "Line 3", "label": "92.35% of line 2"},
        {"line": "Line 4", "label": "Social Security tax limit check"},
        {"line": "Line 10", "label": "Multiply line 3 by 92.35%"},
        {"line": "Line 11", "label": "Social Security tax"},
        {"line": "Line 12", "label": "Deductible part of self-employment tax"},
    ],
    "Form 8833": [
        {"line": "Line 1", "label": "Treaty country"},
        {"line": "Line 2", "label": "Article(s) of the treaty"},
        {"line": "Line 3", "label": "IRS Code provision overruled or modified"},
        {"line": "Line 4", "label": "Nature and amount of income"},
        {"line": "Line 5", "label": "Explanation of treaty-based position"},
    ],
    "Form 2441": [
        {"line": "Line 1", "label": "Care provider information"},
        {"line": "Line 2", "label": "Qualifying person(s)"},
        {"line": "Line 3", "label": "Qualified expenses (max $3,000/$6,000)"},
        {"line": "Line 4", "label": "Earned income"},
        {"line": "Line 9", "label": "Credit percentage"},
        {"line": "Line 11", "label": "Credit amount"},
    ],
    "Form 8863": [
        {"line": "Line 1", "label": "American Opportunity Credit — adjusted qualified expenses"},
        {"line": "Line 2", "label": "Subtract $2,000 from line 1"},
        {"line": "Line 3", "label": "Multiply line 2 by 25%"},
        {"line": "Line 4", "label": "Add $2,000 and line 3 (max $2,500)"},
        {"line": "Line 19", "label": "Lifetime Learning Credit — adjusted qualified expenses"},
        {"line": "Line 20", "label": "Multiply line 19 by 20% (max $2,000)"},
    ],
    "Form 8843": [
        # Part I — all exempt individuals
        {"line": "Part I — Line 1", "label": "US visa type (e.g. F-1, J-1)"},
        {"line": "Part I — Line 2", "label": "Number of days you were present in the US in the current and two prior years"},
        {"line": "Part I — Line 3", "label": "Number of days claimed as exempt from the Substantial Presence Test"},
        {"line": "Part I — Line 4", "label": "Name and address of your US educational institution or employer"},
        # Part II — students (F or J visa)
        {"line": "Part II — Line 5a", "label": "Name and address of your school in the US"},
        {"line": "Part II — Line 5b", "label": "Name and address of your academic director or department head"},
        {"line": "Part II — Line 5c", "label": "Type of US visa and date you entered the US on that visa"},
        {"line": "Part II — Line 5d", "label": "Current nonimmigrant status and date your status was acquired"},
        {"line": "Part II — Line 5e", "label": "Visa and date of any change in visa or immigration status"},
        {"line": "Part II — Line 6", "label": "Were you previously exempt? List each previous exempt year and the category claimed"},
        # Signature
        {"line": "Signature", "label": "Your signature, date, and current mailing address"},
    ],
}


def get_standard_deduction(filing_status: str, tax_year: int | None = None) -> int:
    """Get the standard deduction for a filing status and year."""
    if tax_year is None:
        tax_year = TAX_YEAR
    year_deductions = STANDARD_DEDUCTIONS_BY_YEAR.get(tax_year, STANDARD_DEDUCTIONS)
    return year_deductions.get(filing_status, 15000)


def get_form_lines(form_name: str) -> list[dict]:
    """Get the line definitions for a given form."""
    return FORM_LINES.get(form_name, [])


def get_filing_deadline(is_international: bool = False, tax_year: int | None = None) -> str:
    """Get the applicable filing deadline for the given tax year."""
    year = tax_year if tax_year is not None else TAX_YEAR
    if is_international:
        return f"June 15, {year + 1}"
    return f"April 15, {year + 1}"


def get_current_deadline_note(tax_year: int | None = None) -> str:
    """Get a note about the filing deadline for the given tax year."""
    year = tax_year if tax_year is not None else TAX_YEAR
    return (
        f"Tax Year {year} — Regular deadline: April 15, {year + 1}. "
        f"International filers (F-1, J-1, etc.): June 15, {year + 1}."
    )
