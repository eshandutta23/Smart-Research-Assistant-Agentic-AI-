Built a multi-agent AI system from scratch last weekend using LangGraph.

Here's what it does:

→ You give it any research topic
→ A Planner agent breaks it into focused sub-questions
→ A Researcher agent investigates each one using tools
→ A Writer agent synthesizes everything into a structured report

All three agents share a typed StateGraph each one reads the previous agent's output and adds to it. The Researcher has a conditional edge that loops it back if research is incomplete, then routes forward to the Writer when done.

Key concepts I implemented:
• StateGraph with TypedDict shared state
• Conditional edges for dynamic agent routing
• Tool binding and direct tool invocation
• add_messages reducer for automatic conversation memory
• Real-time node streaming with .stream()
• Streamlit UI showing all 3 agents running live

Stack: LangGraph 1.2 · LangChain · Groq (Llama 3.3 70B) · Python · Streamlit
