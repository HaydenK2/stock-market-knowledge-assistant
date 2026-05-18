### Search

from langchain_community.tools.tavily_search import TavilySearchResults


def create_web_search_tool():
    return TavilySearchResults(k=3)