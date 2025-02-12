from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.prompts import HumanMessagePromptTemplate,PromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage

template = ""

prompt_template = PromptTemplate.from_template(template)

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位人工智能助手，你的名字是{name}."),
        ("human","你好"),
        ("ai","我很好，谢谢！"),
        ("human", "{user_input}"),
        MessagesPlaceholder("msgs"),

    ])

# chat_template1 = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(
#             content =(
#                 "你是一个快乐的助手，可以润色内容，使其看起来更简单易读。"
#             )
#         ), 
#         HumanMessagePromptTemplate.from_template("{text}"),
#     ])

#Format message
# messages = chat_template.format_messages(name= "Bob", user_input= "你的名字叫什么？")
# print(messages)

result = prompt_template.invoke({"msgs":[HumanMessage(content="Hi!"),HumanMessage(content="How are you?")]})
print(result)
# messages1 = chat_template1.format_messages(text= "我不喜欢吃好吃的东西")
# print(messages1)