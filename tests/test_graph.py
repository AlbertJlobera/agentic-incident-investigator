from langchain_core.messages import HumanMessage

from src.graph import graph
from src.libs.constants import (
    INVESTIGATING,
    INCIDENT_FOUND,
    NO_INCIDENT,
    PORTFOLIO_NOT_FOUND,
    LOGS_NOT_FOUND,
)


def run_investigation(portfolio_id: str):
    return graph.invoke({
        "messages": [
            HumanMessage(
                content=f"Investigate possible incidents for portfolio {portfolio_id}"
            )
        ],
        "investigation_status": INVESTIGATING,
        "documentation_query": "",
        "retrieved_docs": [],
    })

def test_incident_found():
    result = run_investigation("PORT-483")

    assert result["investigation_status"] == INCIDENT_FOUND


def test_no_incident():
    result = run_investigation("PORT-221")

    assert result["investigation_status"] == NO_INCIDENT


def test_portfolio_not_found():
    result = run_investigation("PORT-999")

    assert result["investigation_status"] == PORTFOLIO_NOT_FOUND


def test_logs_not_found():
    result = run_investigation("PORT-555")

    assert result["investigation_status"] == LOGS_NOT_FOUND