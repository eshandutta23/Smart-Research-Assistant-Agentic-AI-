from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import AgentState
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)


def planner_agent(state: AgentState) -> AgentState:
    """
    Takes the user's topic and breaks it into
    3-5 focused sub-questions for the Researcher.
    """
    print("\n[Planner] Creating research plan...")

    messages = [
        SystemMessage(content="""You are a research planning expert.
        Given a topic, output ONLY a numbered list of 3-5 specific research 
        sub-questions. No preamble. No explanation. Just the numbered list."""),
        HumanMessage(content=f"Topic to research: {state['topic']}")
    ]

    response = llm.invoke(messages)

    # Parse the numbered list into a Python list
    lines = response.content.strip().split("\n")
    plan = [
        line.split(". ", 1)[1].strip()
        for line in lines
        if line.strip() and line[0].isdigit()
    ]

    print(f"[Planner] Plan created with {len(plan)} sub-questions")

    return {
        "plan": plan,
        "messages": [response]
    }