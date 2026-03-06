import os

from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def search_web(query: str) -> str:
    """Searches the web for current, up-to-date information about any topic.
    Use this when you need recent news, facts, sports results, or any
    information you are not confident about.
    Input should be a specific search query string."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query, max_results=3)

        results = response.get("results", [])
        if not results:
            return "No results found."

        formatted = []
        for r in results:
            formatted.append(
                f"Title: {r['title']}\nSummary: {r['content']}\nSource: {r['url']}"
            )
        return "\n\n".join(formatted)

    except Exception as e:
        return f"Search failed: {str(e)}"
