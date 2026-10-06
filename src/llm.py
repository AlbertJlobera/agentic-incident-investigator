from langchain_openai import ChatOpenAI

from src.tools import tools


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)