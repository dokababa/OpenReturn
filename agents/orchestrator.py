"""LangGraph orchestrator connecting all agents."""
from __future__ import annotations

import logging
from typing import Any

from langgraph.graph import END, START, StateGraph

from agents.form_agent import determine_forms
from agents.guidance_agent import generate_form_guidance

logger = logging.getLogger(__name__)


def interview_node(state: dict) -> dict:
    """Process interview answers from session state."""
    answers = state.get("answers", {})
    state["answers"] = answers
    state["interview_complete"] = True
    return state


def form_determination_node(state: dict) -> dict:
    """Determine which forms the user needs."""
    answers = state.get("answers", {})
    forms = determine_forms(answers)
    state["required_forms"] = forms
    return state


def guidance_node(state: dict) -> dict:
    """Generate line-by-line guidance for all required forms."""
    forms = state.get("required_forms", [])
    answers = state.get("answers", {})
    progress_callback = state.get("progress_callback")

    guidance_by_form = {}
    for form_info in forms:
        form_name = form_info["form"]
        logger.info(f"Generating guidance for {form_name}...")
        guidance = generate_form_guidance(
            form_name, answers, progress_callback=progress_callback
        )
        guidance_by_form[form_name] = guidance

    state["guidance_by_form"] = guidance_by_form
    return state


def should_generate_guidance(state: dict) -> str:
    """Decide whether to proceed to guidance generation."""
    if state.get("required_forms"):
        return "generate"
    return "end"


def run_full_pipeline(
    answers: dict, progress_callback=None
) -> dict[str, Any]:
    """
    Run the complete tax guidance pipeline.

    This builds a LangGraph workflow: interview → form_determination → guidance.
    The interview node is a pass-through since answers come from the Streamlit UI.

    Args:
        answers: User interview answers dict.
        progress_callback: Optional callback for progress updates.

    Returns:
        Dict with required_forms and guidance_by_form.
    """
    # Build the graph fresh each run
    workflow = StateGraph(dict)

    workflow.add_node("interview", interview_node)
    workflow.add_node("form_determination", form_determination_node)
    workflow.add_node("guidance", guidance_node)

    workflow.add_edge(START, "interview")
    workflow.add_edge("interview", "form_determination")
    workflow.add_conditional_edges(
        "form_determination",
        should_generate_guidance,
        {
            "generate": "guidance",
            "end": END,
        },
    )
    workflow.add_edge("guidance", END)

    graph = workflow.compile()

    initial_state = {
        "answers": answers,
        "progress_callback": progress_callback,
    }

    result = graph.invoke(initial_state)

    return {
        "required_forms": result.get("required_forms", []),
        "guidance_by_form": result.get("guidance_by_form", {}),
    }
