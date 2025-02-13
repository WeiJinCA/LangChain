from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel,Field

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)

class WikiInputs(BaseModel):
    query: str=Field(description="Query to look up in Wikipedia,should be 3 or less words")

tool = WikipediaQueryRun(
    name="wiki-tool",
    description="Query Wikipedia for information.",
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    return_direct=True #设置为False时，工具可能会返回更复杂的响应对象，包含更多的元数据或结构化信息
    )
print(tool.invoke({"query":"langchain"}))

print(f"Name:{tool.name}")
print(f"Description:{tool.description}")
print(f"Args:{tool.args}")
print(f"Return Direct:{tool.return_direct}")