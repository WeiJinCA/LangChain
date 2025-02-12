from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough

chat = ChatOpenAI(model="gpt-4")
temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("我叫jack,你好")
temp_chat_history.add_ai_message("你好,我是一个聊天机器人")
temp_chat_history.add_user_message("我今天心情挺好")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我下午打篮球")
temp_chat_history.add_ai_message("你下午在做什么")
temp_chat_history.messages

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个乐于助人的助手，尽力回答所有的问题，提供的聊天历史包括与您交谈的用户的事实"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
    ]
)