from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import AgentState
from tools.search_tool import web_search, calculate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)


def researcher_agent(state: AgentState) -> AgentState:
    """
    Takes the plan from Planner, researches each sub-question
    using tools directly, and accumulates notes into research_notes.
    """
    print("\n[Researcher] Starting research...")

    plan = state.get("plan", [])
    existing_notes = state.get("research_notes", "")
    all_notes = existing_notes
    last_response = None

    for i, question in enumerate(plan):
        print(f"[Researcher] Researching: {question}")

        # Step 1: Call the tool directly (no LLM tool-calling API)
        search_result = web_search.invoke({"query": question})

        # Step 2: Ask the LLM to summarize the tool result
        messages = [
            SystemMessage(content="""You are a thorough research assistant.
            Given a question and search results, write a clear 2-3 sentence 
            summary of the key findings. Be factual and concise."""),
            HumanMessage(content=f"""
Question: {question}

Search Results:
{search_result}

Summarize the key findings in 2-3 sentences.
            """)
        ]

        last_response = llm.invoke(messages)
        all_notes += f"\n\nQ{i+1}: {question}\nFindings: {last_response.content}"

    print("[Researcher] Research complete")

    return {
        "research_notes": all_notes,
        "messages": [last_response] if last_response else []
    }


def should_continue_research(state: AgentState) -> str:
    """
    Conditional edge function.
    Returns 'writer' if research is done, 'researcher' to loop again.
    """
    notes = state.get("research_notes", "")
    plan = state.get("plan", [])

    questions_covered = notes.count("Q")
    if questions_covered >= len(plan):
        print("[Router] Research complete → routing to Writer")
        return "writer"
    else:
        print("[Router] More research needed → looping Researcher")
        return "researcher"