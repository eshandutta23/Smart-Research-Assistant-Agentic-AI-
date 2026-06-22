from graph.graph_builder import research_graph


def run_research(topic: str):
    print(f"\n{'='*60}")
    print(f"Starting research on: {topic}")
    print('='*60)

    # Initial state — only topic is set; everything else starts empty
    initial_state = {
        "topic": topic,
        "plan": [],
        "research_notes": "",
        "final_report": "",
        "messages": []
    }

    # .stream() gives you real-time updates as each node completes
    # Use .invoke() for a single final result
    final_state = None
    for step in research_graph.stream(initial_state):
        node_name = list(step.keys())[0]
        print(f"\n--- Node completed: {node_name} ---")
        final_state = step

    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)

    # Get the last state value
    last_node = list(final_state.values())[0]
    print(last_node.get("final_report", "No report generated"))


if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research(topic)