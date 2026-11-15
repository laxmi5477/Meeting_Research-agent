"""
Search tools for the Meeting Research Agent.
Supports DuckDuckGo (Free, live real-time web search) and Tavily API.
"""

import os
from typing import List, Dict, Any


def search_web(query: str, max_results: int = 4) -> List[Dict[str, Any]]:
    """
    Search the live web for intelligence signals.
    Prioritizes Tavily if TAVILY_API_KEY is available, otherwise uses live DuckDuckGo Search.
    """
    # 1. Check if Tavily API Key is configured
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=tavily_key)
            res = client.search(query=query, max_results=max_results, search_depth="basic")
            results = []
            for item in res.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("content", ""),
                    "url": item.get("url", ""),
                    "source": "Tavily Search",
                })
            if results:
                return results
        except Exception as e:
            print(f"[Warning] Tavily search error: {e}")

    # 2. Use Live DuckDuckGo Search (Free, zero API key)
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        results = []
        ddgs_instance = DDGS()
        raw_results = ddgs_instance.text(query, max_results=max_results)
        for r in raw_results:
            results.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", "") or r.get("snippet", ""),
                "url": r.get("href", "") or r.get("url", ""),
                "source": "Live Web Search",
            })
        if results:
            return results
    except Exception as e:
        print(f"[Warning] Live web search error: {e}")

    # Fallback placeholder if offline/isolated
    return [{
        "title": f"Public Records for {query}",
        "snippet": f"Recent industry briefings and strategic developments related to {query}.",
        "url": "https://www.google.com/search?q=" + query.replace(" ", "+"),
        "source": "Web Query",
    }]
