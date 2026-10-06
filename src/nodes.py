from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever

from src.state import IncidentState
from src.libs.utils import get_documents
from src.llm import llm, llm_with_tools
from src.prompts.incident_prompts import (
    AGENT_SYSTEM_PROMPT,
    DOCUMENTATION_QUERY_PROMPT,
    FINAL_SYNTHESIS_PROMPT,
)
from src.libs.constants import (
    INVESTIGATING,
    NO_INCIDENT,
    INCIDENT_FOUND,
)


def documentation_validation(state: IncidentState):
    """Search technical documentation and known incidents."""

    messages = state["messages"]

    search_query_response = llm.invoke([
        ("system", DOCUMENTATION_QUERY_PROMPT),
        *messages
    ])

    search_query = search_query_response.content

    docs = get_documents()

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "section")
        ]
    )

    chunks = []

    for doc in docs:
        doc_chunks = splitter.split_text(doc.page_content)

        for chunk in doc_chunks:
            chunk.metadata["source"] = doc.metadata["source"]

        chunks.extend(doc_chunks)

    retriever = BM25Retriever.from_documents(
        documents=chunks,
        k=3
    )

    results = retriever.invoke(search_query)

    return {
        "documentation_query": search_query,
        "retrieved_docs": results
    }


def agent_node(state: IncidentState):

    response = llm_with_tools.invoke([
        ("system", AGENT_SYSTEM_PROMPT),
        *state["messages"]
    ])

    # Mientras pida tools seguimos investigando
    if response.tool_calls:
        return {
            "messages": [response],
            "investigation_status": INVESTIGATING
        }

    # Ya ha terminado de investigar
    content = response.content.strip()

    if content.startswith("NO_INCIDENT"):
        status = NO_INCIDENT

    elif content.startswith("INCIDENT_FOUND"):
        status = INCIDENT_FOUND

    else:
        status = INVESTIGATING

    return {
        "messages": [response],
        "investigation_status": status
    }


def final_synthesis(state: IncidentState):

    messages = state["messages"]
    docs = state["retrieved_docs"]

    documentation = "\n\n".join(
        f"Source: {doc.metadata}\n{doc.page_content}"
        for doc in docs
    )

    prompt = FINAL_SYNTHESIS_PROMPT.format(
        documentation=documentation
    )

    response = llm.invoke([
        ("system", prompt),
        *messages
    ])

    return {
        "messages": [response]
    }