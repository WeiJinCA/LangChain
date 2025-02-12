from langchain_openai import ChatOpenAI
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的故事")
model = ChatOpenAI(model="gpt-4")
output_parser = StrOutputParser()
chain = prompt | model | output_parser

async def async_stream():
    async for chunk in chain.astream({"topic":"鹦鹉"}):
        print(chunk, end="|",flush=True)

#异步调用
asyncio.run(async_stream())