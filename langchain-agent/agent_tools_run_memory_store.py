from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader

#FAISS : Facebook AI Similarity Search
#pip install faiss-cpu
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

####创建工具
loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    #chunk_size:RecursiveCharacterTextSplitter指定每个文档块的最大长度
    #chunk_overlap:每个文档之间的重叠字符数
    chunk_size=1000, chunk_overlap = 200
    ).split_documents(docs)

#将文档转换为向量，并存储
vector = FAISS.from_documents(documents,OpenAIEmbeddings())
retrieval = vector.as_retriever() #将向量存储库转换为检索器，用于相似度搜索

#print(retrieval.invoke("猫的特征")[0]) #搜索与“猫”最相似的5个文档

retriever_tool = create_retriever_tool(
    retrieval,
    "Wiki_search",
    "搜索维基百科"
)

#大模型调用
model = ChatOpenAI(model="gpt-4")
search = TavilySearchResults(max_results=1)
#两种工具供选择调用
tools = [search,retriever_tool]

from langchain import hub
#pulling a pre-defined prompt or template from the LangChain Hub, which is a repository of shared prompts, tools, or chains hosted by LangChain.
#官方提示词仓库,获取提示词模版
prompt = hub.pull("hwchase17/openai-functions-agent")
#print(prompt.messages)

#调用工具是agent驱动的
from langchain.agents import create_tool_calling_agent
agent = create_tool_calling_agent(model,tools,prompt)

from langchain.agents import AgentExecutor
#verbose=True : 输出调试信息,打印日志
agent_executor = AgentExecutor(agent=agent,tools=tools) #,verbose=True

##精确到session_id, 以便记忆聊天内容
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
#不同的session_id调用不同的agent,会话隔离
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    )

#调用agent
response = agent_with_chat_history.invoke(
    {"input":"你好,我的名字是Jack"},
    config={"configurable":{"session_id":"123"}}
)
print(response)

response = agent_with_chat_history.invoke(
    {"input":"我的名字叫什么？"},
    config={"configurable":{"session_id":"123"}}
)
print(response)

response = agent_with_chat_history.invoke(
    {"input":"我的名字叫什么？"},
    config={"configurable":{"session_id":"234"}}
)
print(response)