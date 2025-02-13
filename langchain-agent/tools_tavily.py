from langchain_community.tools.tavily_search import TavilySearchResults

#使用在线搜索工具
search = TavilySearchResults(max_results=1)
print(search.invoke("今天上海天气怎么样？"))