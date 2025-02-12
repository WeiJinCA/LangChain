from langchain_openai import ChatOpenAI
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


model = ChatOpenAI(model="gpt-4")

chain = (model | JsonOutputParser())

async def async_stream():
    async for text in chain.astream(
        "以json格式输出法国、西班牙和日本的国家及其人口列表。"
        '使用一个带有“countries”外部键的字典，其中包含国家列表'
        "每个国家都应该有键“name”和“population”。"
    ):
        print(text,flush=True)

#异步调用
asyncio.run(async_stream())