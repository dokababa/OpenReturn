"""PDF Tax Roadmap cheat sheet generator using ReportLab."""
from __future__ import annotations

import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from utils.constants import APP_NAME, APP_VERSION, DISCLAIMER_TEXT, TAX_YEAR


def _get_styles():
    """Build custom paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "AppTitle",
        parent=styles["Title"],
        fontSize=24,
        spaceAfter=6,
        textColor=colors.HexColor("#1a1a2e"),
    ))
    styles.add(ParagraphStyle(
        "DisclaimerText",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#cc0000"),
        spaceAfter=12,
        leading=10,
    ))
    styles.add(ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#2196F3"),
        spaceBefore=18,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "LineHeader",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1a1a2e"),
        fontName="Helvetica-Bold",
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "LineBody",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#333333"),
        spaceAfter=2,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        "Citation",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#666666"),
        fontName="Helvetica-Oblique",
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "FooterStyle",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#999999"),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "ProfileItem",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=4,
    ))

    return styles


def generate_cheatsheet(
    user_name: str,
    filing_status: str,
    is_resident: bool,
    required_forms: list[dict],
    guidance_by_form: dict,
    disclaimer_accepted: bool = True,
    selected_tax_year: int | None = None,
) -> bytes:
    """
    Generate a PDF tax roadmap cheat sheet.

    Returns PDF as bytes.
    """
    tax_year = selected_tax_year if selected_tax_year else TAX_YEAR
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _get_styles()
    story = []
    now = datetime.now(timezone.utc)

    # === PAGE 1: SUMMARY ===
    story.append(Paragraph(f"{APP_NAME} — Your Tax Roadmap", styles["AppTitle"]))
    story.append(Paragraph(
        f"Generated: {now.strftime('%B %d, %Y at %I:%M %p UTC')}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 8))

    # Red disclaimer banner
    disclaimer_short = (
        "NOT TAX ADVICE. This document provides educational guidance only. "
        "You are solely responsible for the accuracy of your tax return. "
        "OpenReturn bears no liability for errors, penalties, or issues with your filing."
    )
    story.append(Paragraph(disclaimer_short, styles["DisclaimerText"]))
    story.append(Spacer(1, 12))

    # Filing profile
    story.append(Paragraph("Your Filing Profile", styles["SectionHeader"]))
    filer_type = "US Resident / Citizen" if is_resident else "Nonresident Alien"
    profile_items = [
        f"<b>Tax Year:</b> {tax_year}",
        f"<b>Filing Status:</b> {filing_status}",
        f"<b>Filer Type:</b> {filer_type}",
        f"<b>Forms Needed:</b> {len(required_forms)}",
    ]
    for item in profile_items:
        story.append(Paragraph(item, styles["ProfileItem"]))

    story.append(Spacer(1, 8))

    # Forms summary table
    story.append(Paragraph("Forms You Need", styles["SectionHeader"]))
    table_data = [["Form", "Purpose", "Status"]]
    for form in required_forms:
        status = "Required" if form.get("required") else "Optional"
        table_data.append([form["form"], form["reason"], status])

    if len(table_data) > 1:
        t = Table(table_data, colWidths=[1.5 * inch, 4 * inch, 1 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2196F3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)

    # === PAGES 2+: FORM GUIDANCE ===
    for form_info in required_forms:
        form_name = form_info["form"]
        guidance_list = guidance_by_form.get(form_name, [])

        if not guidance_list:
            continue

        story.append(Spacer(1, 16))
        story.append(Paragraph(
            f"{form_name} — Line-by-Line Guidance",
            styles["SectionHeader"],
        ))

        for g in guidance_list:
            # Line header
            story.append(Paragraph(
                f"{g['form']} — {g['line']}: {g['label']}",
                styles["LineHeader"],
            ))

            # Guidance content
            body_parts = [
                f"<b>What it means:</b> {g.get('plain_english', '')}",
                f"<b>Where to find it:</b> {g.get('where_to_find_it', '')}",
                f"<b>What to enter:</b> {g.get('what_to_enter', '')}",
            ]
            if g.get("important_note") and g["important_note"] != "null":
                body_parts.append(f"<b>Note:</b> {g['important_note']}")

            for part in body_parts:
                story.append(Paragraph(part, styles["LineBody"]))

            # Citation
            story.append(Paragraph(
                f"IRS Source: {g.get('irs_citation', 'N/A')}",
                styles["Citation"],
            ))

            # Checkbox placeholder
            story.append(Paragraph(
                "[ ] I confirm I will enter this myself",
                styles["LineBody"],
            ))
            story.append(Spacer(1, 6))

    # === LAST PAGE: DISCLAIMER + ACKNOWLEDGMENT ===
    story.append(Spacer(1, 24))
    story.append(Paragraph("Disclaimer & Acknowledgment", styles["SectionHeader"]))

    # Full disclaimer
    for line in DISCLAIMER_TEXT.split("\n"):
        line = line.strip()
        if line:
            story.append(Paragraph(line, styles["DisclaimerText"]))

    story.append(Spacer(1, 16))

    # Acknowledgment — no PII, just timestamp
    if disclaimer_accepted:
        story.append(Paragraph(
            "<b>Disclaimer acknowledged before download.</b>",
            styles["ProfileItem"],
        ))
        story.append(Paragraph(
            f"<b>Generated:</b> {now.strftime('%B %d, %Y')}",
            styles["ProfileItem"],
        ))

    story.append(Spacer(1, 24))

    # Footer
    story.append(Paragraph(
        f"{APP_NAME} v{APP_VERSION} — Free Tax Education Tool — Not Tax Advice",
        styles["FooterStyle"],
    ))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.read()
