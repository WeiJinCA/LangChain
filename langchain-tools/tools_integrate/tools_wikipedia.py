from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

#使用Wikipedia工具搜索信息

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
print(tool.invoke({"query":"langchain"}))

print(f"Name:{tool.name}")
print(f"Description:{tool.description}")
print(f"Args:{tool.args}")
print(f"Return Direct:{tool.return_direct}")