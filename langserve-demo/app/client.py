from langchain.schema.runnable import RunnableMap
from langchain_core.prompts import ChatPromptTemplate
from langserve import RemoteRunnable

#方法一：使用RemoteRunnable调用langserve的API

openai = RemoteRunnable("http://localhost:8000/openai")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个喜欢写故事的助手"),
        ("user","写一个故事，主题是{topic}")
    ]
)

chain = prompt | RunnableMap({
    "openai": openai
})
print("同步调用")
response = chain.invoke({"topic":"爱情"})
print(response)


# openai_str_parser = RemoteRunnable("http://localhost:8000/openai_str_parser/")
# chain_str_parser = prompt | RunnableMap({
#     "openai": openai_str_parser
# })
# print("测试StrOutputParser")
# response_str_parser = chain_str_parser.invoke({"topic":"爱情"})
# print(response_str_parser)

# print("流式调用/stream结果")
# for chunk in chain.stream({"topic":"爱情"}):
#     print(chunk,end="",flush=True)
#     print(chunk["openai"].content,end="",flush=True)