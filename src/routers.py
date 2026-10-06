from langgraph.graph import END

from src.state import IncidentState
from src.libs.constants import (
    PORTFOLIO_NOT_FOUND,
    LOGS_NOT_FOUND,
    NO_INCIDENT,
    INCIDENT_FOUND,
)


def route_agent(state: IncidentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    if state["investigation_status"] == NO_INCIDENT:
        return END

    if state["investigation_status"] == INCIDENT_FOUND:
        return "documentation_validation"

    raise ValueError(
        f"Unexpected investigation status: {state['investigation_status']}"
    )


def route_tools(state: IncidentState):

    if state["investigation_status"] in [
        PORTFOLIO_NOT_FOUND,
        LOGS_NOT_FOUND
    ]:
        return END

    return "agent"