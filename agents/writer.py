from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import AgentState
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0.3   # Slightly higher for more natural writing
)


def writer_agent(state: AgentState) -> AgentState:
    """
    Takes all research notes and synthesizes them
    into a structured, readable final report.
    """
    print("\n[Writer] Synthesizing final report...")

    messages = [
        SystemMessage(content="""You are an expert report writer.
        Given a research topic and detailed notes, write a clear, 
        well-structured report with:
        - An executive summary (2-3 sentences)
        - Key findings (bullet points)  
        - Conclusion
        Use professional but accessible language."""),
        HumanMessage(content=f"""
Topic: {state['topic']}

Research Notes:
{state['research_notes']}

Write the final report now.
        """)
    ]

    response = llm.invoke(messages)

    print("[Writer] Report complete")

    return {
        "final_report": response.content,
        "messages": [response]
    }