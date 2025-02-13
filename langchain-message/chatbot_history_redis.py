from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

model = ChatOpenAI(model="gpt-4")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are an assistant who's good at {ability}.Respond in 20 words or less."),
        MessagesPlaceholder(variable_name="history"),
        ("human","{input}"),
    ]
)

runnable = prompt | model
#用于存储用户的聊天历史
store = {}

REDIS_URL = "redis://localhost:6379/0"

#获得会话历史，传入会话id，返回会话历史
def get_session_history(session_id:str)->RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id,url=REDIS_URL)

#将runnable和get_session_history传入RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",)

#调用invoke方法，传入用户输入和能力，返回response
response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"余弦是什么意思？",
        
    },
    config={"configurable":{"session_id":"abc123"}}
)
print(response)

response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"什么？",
    },
    config={"configurable":{"session_id":"abc123"}}
)
print(response)

#不同的session_id, 不知道聊天历史
response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"什么？",
    },
    config={"configurable":{"session_id":"def123"}}
)
print(response)