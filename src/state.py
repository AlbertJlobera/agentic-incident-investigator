from typing import Literal

from langgraph.graph import MessagesState
from langchain_core.documents import Document




class IncidentState(MessagesState):
    documentation_query: str
    retrieved_docs: list[Document]
    investigation_status: Literal[
    "INVESTIGATING",
    "PORTFOLIO_NOT_FOUND",
    "LOGS_NOT_FOUND",
    "NO_INCIDENT",
    "INCIDENT_FOUND"
]