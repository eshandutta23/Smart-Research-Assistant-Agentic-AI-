from langgraph.graph import StateGraph, START, END
from graph.state import AgentState
from agents.planner import planner_agent
from agents.researcher import researcher_agent, should_continue_research
from agents.writer import writer_agent


def build_graph():
    """
    Assembles the multi-agent StateGraph.
    
    Flow: START → planner → researcher → (conditional) → writer → END
                                 ↑______________↓ (loop if needed)
    """

    # 1. Initialize the graph with our shared state schema
    graph = StateGraph(AgentState)

    # 2. Add nodes — each node is a function that takes state and returns state
    graph.add_node("planner", planner_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("writer", writer_agent)

    # 3. Add edges — the fixed paths
    graph.add_edge(START, "planner")          # Always start with Planner
    graph.add_edge("planner", "researcher")   # Planner always → Researcher
    graph.add_edge("writer", END)             # Writer always → END

    # 4. Add conditional edge — the smart routing
    # After Researcher runs, call should_continue_research()
    # Its return value ("researcher" or "writer") decides the next node
    graph.add_conditional_edges(
        "researcher",
        should_continue_research,
        {
            "researcher": "researcher",   # Loop back
            "writer": "writer"            # Move forward
        }
    )

    # 5. Compile the graph (validates structure + creates runnable)
    app = graph.compile()
    return app


# Singleton — import this in main.py and app.py
research_graph = build_graph()