from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4")

#chunk 数据块
chunks = []

#流式传输，用户大模型返回内容较多的情况，优化用户体验
for chunk in model.stream("天空是什么颜色？"):
    chunks.append(chunk)
    print(chunk.content, end="|",flush=True)