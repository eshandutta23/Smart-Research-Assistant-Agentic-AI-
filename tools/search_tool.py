from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Simulates a web search. In production, replace with
    Tavily, SerpAPI, or DuckDuckGo integration.
    """
    # Placeholder — replace with: from tavily import TavilyClient
    return f"""
    [Search results for: "{query}"]
    
    Result 1: Key finding about {query} — this is a simulated result.
    Relevant facts: Generative AI adoption grew 300% in 2024. 
    Major players: OpenAI, Google DeepMind, Anthropic, Meta AI.
    
    Result 2: Industry analysis shows {query} is transforming enterprise workflows,
    with RAG (Retrieval-Augmented Generation) being the top deployment pattern.
    
    Note: Replace this with real Tavily search:
    pip install tavily-python
    client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    return client.search(query)['results']
    """


@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Export as a list — this is what you pass to the LLM
tools = [web_search, calculate]