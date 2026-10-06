from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from src.state import IncidentState
from src.tools import tools
from src.nodes import (
    agent_node,
    documentation_validation,
    final_synthesis,
)
from src.routers import route_agent, route_tools


builder = StateGraph(IncidentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_node("documentation_validation", documentation_validation)
builder.add_node("final_synthesis", final_synthesis)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route_agent
)

builder.add_conditional_edges(
    "tools",
    route_tools
)

builder.add_edge(
    "documentation_validation",
    "final_synthesis"
)

builder.add_edge(
    "final_synthesis",
    END
)

graph = builder.compile()