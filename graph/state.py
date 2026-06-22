from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # The user's original research topic
    topic: str

    # Planner fills this: list of sub-questions to research
    plan: List[str]

    # Researcher fills this: notes gathered for each sub-question
    research_notes: str

    # Writer fills this: the final synthesized report
    final_report: str

    # Message history for multi-turn LLM calls (auto-appended by add_messages)
    messages: Annotated[list, add_messages]