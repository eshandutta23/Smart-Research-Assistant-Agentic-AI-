import streamlit as st
from graph.graph_builder import research_graph

st.set_page_config(
    page_title="Smart Research Agent",
    page_icon="",
    layout="wide"
)

st.title("Smart Research Assistant")
st.caption("Multi-agent system built with LangGraph · Planner → Researcher → Writer")

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of Generative AI on banking sector"
)

col1, col2, col3 = st.columns(3)

if st.button("Run Research", type="primary") and topic:
    
    initial_state = {
        "topic": topic,
        "plan": [],
        "research_notes": "",
        "final_report": "",
        "messages": []
    }

    with st.spinner("Running agents..."):
        
        plan_shown = False
        notes_shown = False

        for step in research_graph.stream(initial_state):
            node_name = list(step.keys())[0]
            node_output = list(step.values())[0]

            if node_name == "planner" and not plan_shown:
                with col1:
                    st.subheader("Planner")
                    st.success("Plan created")
                    plan = node_output.get("plan", [])
                    for i, q in enumerate(plan, 1):
                        st.write(f"{i}. {q}")
                plan_shown = True

            elif node_name == "researcher" and not notes_shown:
                with col2:
                    st.subheader("Researcher")
                    st.success("Research complete")
                    st.text_area(
                        "Notes",
                        node_output.get("research_notes", ""),
                        height=300
                    )
                notes_shown = True

            elif node_name == "writer":
                with col3:
                    st.subheader("Writer")
                    st.success("Report ready")
                    st.markdown(node_output.get("final_report", ""))

    st.balloons()