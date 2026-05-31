### Search
from langchain_tavily import TavilySearch

def create_web_search_tool():
    return TavilySearch(k=3)