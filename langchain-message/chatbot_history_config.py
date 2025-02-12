from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
#针对会话的配置
from langchain_core.runnables import ConfigurableFieldSpec

###############添加user_id和conversation_id################

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

#获得会话历史，传入会话id，返回会话历史
def get_session_history(user_id:str,conversation_id:str)->BaseChatMessageHistory:
    if (user_id,conversation_id) not in store:
        store[(user_id,conversation_id)] = ChatMessageHistory()
    return store[(user_id,conversation_id)]

#将runnable和get_session_history传入RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="The user ID",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="The conversation ID",
            default="",
            is_shared=True,
        )

    ])

#调用invoke方法，传入用户输入和能力，返回response
response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"余弦是什么意思？",
        
    },
    config={"configurable":{"conversation_id":"1","user_id":"123"}}
)
print(response)

response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"什么？",
    },
    config={"configurable":{"conversation_id":"1","user_id":"123"}}
)
print(response)

#不同的session_id, 不知道聊天历史
response = with_message_history.invoke(
    {
        "ability":"math",
        "input":"什么？",
    },
    config={"configurable":{"conversation_id":"2","user_id":"123"}}
)
print(response)