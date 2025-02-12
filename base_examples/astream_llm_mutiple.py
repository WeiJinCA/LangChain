from langchain_openai import ChatOpenAI
import asyncio

async def task1():
    model = ChatOpenAI(model="gpt-4")
    chunks = []
    async for chunk in model.astream("天空是什么颜色？"):
        chunks.append(chunk)
        if(len(chunks) == 2):
            print(chunks[1]) 
        print(chunk.content, end="|",flush=True)

async def task2():
    model = ChatOpenAI(model="gpt-4")
    chunks = []
    async for chunk in model.astream("讲个笑话？"):
        chunks.append(chunk)
        if(len(chunks) == 2):
            print(chunks[1]) 
        print(chunk.content, end="|",flush=True)

async def main():
    #同步调用，用await
    # await task1()
    # await task2()
    #异步调用
     await asyncio.gather(task1(), task2())
#异步调用
asyncio.run(main())