from duckduckgo_search import DDGS
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information about places, routes, weather, and attractions.
    Use this tool to find real-time or specific information that you don't know."""
    try:
        results = DDGS().text(query, max_results=5)
        if results:
            return "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
        return "No results found."
    except Exception as e:
        return f"Search error: {e}"

tools = [search_web]
