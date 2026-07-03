# graph.py

from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from agents import (
    parser_agent,
    validator_agent,
    summary_agent,
)

from utils import read_pdf


# ==========================================================
# LangGraph State
# ==========================================================


class GraphState(TypedDict):
    report: str
    extracted_json: Dict[str, Any]
    validation: str
    summary: str
# ==========================================================
# Workflow Nodes
# ==========================================================

def parser_node(state: GraphState):

    result = parser_agent(state["report"])

    state["extracted_json"] = result

    return state


def validator_node(state: GraphState):

    result = validator_agent(
        report=state["report"],
        extracted_json=state["extracted_json"],
    )

    state["validation"] = result

    return state


def summary_node(state: GraphState):

    result = summary_agent(
        report=state["report"],
        extracted_json=state["extracted_json"],
    )

    state["summary"] = result

    return state


# ==========================================================
# Build Graph
# ==========================================================

workflow = StateGraph(GraphState)

workflow.add_node("parser", parser_node)
workflow.add_node("validator", validator_node)
workflow.add_node("summary", summary_node)

workflow.set_entry_point("parser")

workflow.add_edge("parser", "validator")
workflow.add_edge("validator", "summary")
workflow.add_edge("summary", END)

graph = workflow.compile()


# ==========================================================
# Main Function
# ==========================================================

def process_report(pdf_path: str):

    report = read_pdf(pdf_path)

    state = GraphState(
        report=report,
        extracted_json={},
        validation="",
        summary=""
    )

    result = graph.invoke(state)

    return {
        "json": result["extracted_json"],
        "validation": result["validation"],
        "summary": result["summary"],
    }
