from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults 

llm = ChatOpenAI(model="gpt-4")
#搜索工具
tools = [TavilySearchResults(max_results=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一位得力的助手"),
        ("placeholder","{chat_history}"),
        ("human","{input}"),
        ("placeholder","{agent_scratchpad}"),
    ]
)
agent = create_tool_calling_agent(llm,tools,prompt)
executor = AgentExecutor(agent=agent,tools=tools)
response = executor.invoke({"input":"谁指导了2023的电影《奥本海默》，他多少岁了？"})
print(response)