"""Line-by-line guidance engine using RAG + Groq."""
from __future__ import annotations

import json
import logging
import os
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag.retriever import IRSRetriever
from utils.tax_logic import get_form_lines

load_dotenv()
logger = logging.getLogger(__name__)

GUIDANCE_PROMPT = """You are a tax education assistant. You help people UNDERSTAND how to fill their own tax forms.
You do NOT fill forms — you educate so people can fill forms themselves.
Always cite the specific IRS publication and page number.
Use plain simple English. Never use unexplained jargon.

IMPORTANT: The user is filing for TAX YEAR {tax_year}. All guidance must be specific to
the {tax_year} tax year rules, thresholds, and form versions. If a rule changed between
years, mention the {tax_year}-specific amount.

For identification fields (name, SSN, address, bank info, signature, EIN):
- Tell the user EXACTLY what to write and WHERE to find it on their documents
- For SSN: "Copy your 9-digit Social Security number from your Social Security card"
- For bank info: "Find your routing number (9 digits) on the bottom-left of a check"
- For address: "Write your current mailing address where the IRS can reach you"
- For signature: "Sign your name in ink and write today's date"
- Be specific and helpful — the user fills these in on the paper/e-file form themselves

User's tax situation:
{user_situation}

IRS Instructions retrieved for {form_name}, {line_number}:
{retrieved_context}

Respond in this exact JSON format only (no markdown, no code fences):
{{
    "plain_english": "1-2 sentence explanation of what this line/field means",
    "what_to_enter": "exactly what info goes here — be specific about format and source",
    "where_to_find_it": "which personal document to look at (SSA card, check, W-2, etc.)",
    "irs_citation": "e.g. Form 1040 Instructions, Page 28",
    "important_note": "any warnings or null if none"
}}"""


def get_smart_llm():
    """Get the full-size Groq LLM for guidance generation."""
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0,
    )


def get_fast_llm():
    """Get the smaller Groq LLM for simpler tasks."""
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0,
    )


def format_user_situation(answers: dict) -> str:
    """Format the user's tax situation as a readable string."""
    parts = []
    tax_year = answers.get("selected_tax_year", 2025)
    parts.append(f"Filing for Tax Year {tax_year}")
    if answers.get("is_resident"):
        parts.append("US resident/citizen")
    else:
        parts.append("Nonresident alien")
    if answers.get("filing_status"):
        parts.append(f"Filing status: {answers['filing_status']}")
    if answers.get("has_w2"):
        parts.append("Has W-2 wage income")
    if answers.get("has_1099_nec"):
        parts.append("Has freelance/self-employment income (1099-NEC)")
    if answers.get("has_capital_gains"):
        parts.append("Has investment/capital gains income")
    if answers.get("is_international_student"):
        parts.append("International student")
    if answers.get("has_mortgage"):
        parts.append("Pays mortgage interest")
    if answers.get("has_dependents"):
        parts.append("Has dependents")
    return "; ".join(parts) if parts else "Standard taxpayer"


def generate_line_guidance(
    form_name: str,
    line: str,
    label: str,
    user_situation: str,
    retriever: IRSRetriever,
    llm=None,
) -> dict:
    """
    Generate guidance for a single form line using RAG + Groq.

    Returns a guidance dict with plain_english, what_to_enter, etc.
    """
    if llm is None:
        llm = get_smart_llm()

    # Get RAG context
    context = retriever.get_guidance_context(form_name, f"{line} {label}")

    if not context:
        context = f"No specific IRS instructions found for {form_name} {line}. Use general knowledge of {form_name} instructions."

    # Extract tax year from user_situation string or default to 2025
    tax_year = 2025
    if "Tax Year" in user_situation:
        try:
            tax_year = int(user_situation.split("Tax Year ")[1][:4])
        except (ValueError, IndexError):
            pass

    prompt = GUIDANCE_PROMPT.format(
        tax_year=tax_year,
        user_situation=user_situation,
        form_name=form_name,
        line_number=f"{line} — {label}",
        retrieved_context=context,
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            content = response.content.strip()

            # Strip markdown code fences if present
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

            parsed = json.loads(content)

            return {
                "form": form_name,
                "line": line,
                "label": label,
                "plain_english": parsed.get("plain_english", ""),
                "what_to_enter": parsed.get("what_to_enter", ""),
                "where_to_find_it": parsed.get("where_to_find_it", ""),
                "irs_citation": parsed.get("irs_citation", ""),
                "important_note": parsed.get("important_note"),
                "confirmed": False,
            }
        except json.JSONDecodeError:
            logger.warning(
                f"JSON parse error for {form_name} {line}, attempt {attempt + 1}"
            )
            if attempt < max_retries - 1:
                time.sleep(1)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate" in error_str.lower():
                wait = 2 ** (attempt + 1)
                logger.warning(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                logger.error(f"Error generating guidance for {form_name} {line}: {e}")
                break

    # Fallback if all retries fail
    return {
        "form": form_name,
        "line": line,
        "label": label,
        "plain_english": f"Enter the value for {label}.",
        "what_to_enter": f"Refer to your tax documents for {label}.",
        "where_to_find_it": f"See the {form_name} instructions for {line}.",
        "irs_citation": f"{form_name} Instructions",
        "important_note": "We couldn't generate detailed guidance — please refer to the IRS instructions directly.",
        "confirmed": False,
    }


def generate_form_guidance(
    form_name: str, answers: dict, progress_callback=None
) -> list[dict]:
    """
    Generate guidance for all lines of a form.

    Args:
        form_name: The IRS form name (e.g., "Form 1040").
        answers: User interview answers.
        progress_callback: Optional callable(current, total) for progress updates.

    Returns:
        List of guidance dicts for each line.
    """
    lines = get_form_lines(form_name)
    if not lines:
        return []

    retriever = IRSRetriever()
    llm = get_smart_llm()
    user_situation = format_user_situation(answers)

    guidance_list = []
    for i, line_def in enumerate(lines):
        if progress_callback:
            progress_callback(i, len(lines))

        guidance = generate_line_guidance(
            form_name=form_name,
            line=line_def["line"],
            label=line_def["label"],
            user_situation=user_situation,
            retriever=retriever,
            llm=llm,
        )
        guidance_list.append(guidance)

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    if progress_callback:
        progress_callback(len(lines), len(lines))

    return guidance_list
