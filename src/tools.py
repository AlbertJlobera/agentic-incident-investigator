
from typing import Annotated

from src.libs.utils import get_json, get_logs
from src.libs.constants import (
    PORTFOLIO_NOT_FOUND,
    LOGS_NOT_FOUND,
)

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage


@tool
def get_portfolio_executions(
    portfolio_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
):
    """Get recent executions for a portfolio."""

    doc = get_json()

    executions = [
        e for e in doc
        if e.get("portfolio_id") == portfolio_id
    ]

    if not executions:
        return Command(
            update={
                "investigation_status": PORTFOLIO_NOT_FOUND,
                "messages": [
                    ToolMessage(
                        content=f"No executions found for portfolio {portfolio_id}.",
                        tool_call_id=tool_call_id
                    )
                ]
            }
        )

    return executions



@tool
def get_execution_logs(
    execution_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
):
    """Get logs for a specific execution."""

    logs = get_logs()

    filtered_logs = []
    capturando = False

    for log in logs:

        if log == f"[{execution_id}]":
            capturando = True
            continue

        if capturando and log.startswith("[RUN-"):
            break

        if capturando:
            filtered_logs.append(log)

    if not filtered_logs:
        return Command(
            update={
                "investigation_status": LOGS_NOT_FOUND,

                "messages": [
                    ToolMessage(
                        content="No logs found for this execution.",
                        tool_call_id=tool_call_id
                    )
                ]
            }
        )

    return filtered_logs

tools = [
    get_portfolio_executions,
    get_execution_logs,
]
