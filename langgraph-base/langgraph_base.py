from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
#导入内存保存器，持久化状态
from langgraph.checkpoint.memory import MemorySaver
#导入状态图和消息状态
from langgraph.graph import END,StateGraph,MessagesState
#导入工具节点
from langgraph.prebuilt import ToolNode

#定义工具函数，用于代理调用外部工具
@tool
def search(query:str):
    """模拟一个搜索工具"""
    if "上海" in query.lower() or "shanghai" in query.lower():
        return "现在30度,有雾"
    return "现在35度,阳光明媚"

#将工具添加到工具节点中
tools = [search]
#创建工具节点
tool_node = ToolNode(tools=tools)

model = ChatOpenAI(model="gpt-4o",temperature=0).bind_tools(tools)

#定义状态图
def should_continue(state:MessagesState)->Literal["tools",END]:
    messages = state['messages']
    last_message = messages[-1]
    #LLM调用了工具，则转到tools节点
    if last_message.tool_calls:
        return "tools"
    return END #否则停止回复用户

#1.定义调用模型的函数
def call_model(state:MessagesState):
    messages = state['messages']
    #调用模型
    response = model.invoke(messages)
    #返回列表，因为这将被添加到现有列表中
    return {"messages":[response]}

#2.用状态初始化状态图，定义一个新的状态图
workflow = StateGraph(MessagesState)
#3.定义图节点， 定义我们将循环的两个节点
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)

#4.定义入口点和图边
workflow.set_entry_point("agent")

#添加条件边
workflow.add_conditional_edges("agent",should_continue)

#添加从tools到agent的普通边
workflow.add_edge("tools","agent")

#初始化内存，以便在状态图中持久化状态
checkpointer = MemorySaver()

#5. 编译图为可运行的langchain对象
app = workflow.compile(checkpointer)

#6.执行图
final_state = app.invoke({"messages":[HumanMessage(content = "上海的天气怎么样？")]},
    config={"configurable":{"thread_id":42}}
    )

#从final_state中提取最后一条消息的内容
result = final_state['messages'][-1].content
print(result)

final_state = app.invoke({"messages":[HumanMessage(content = "我问的哪个城市？")]},
    config={"configurable":{"thread_id":42}} #更改不同的id,测试持久化状态
    )
result = final_state['messages'][-1].content
print(result)

#将生成的图保存到文件
graph_png = app.get_graph().draw_mermaid_png()
with open("./langgraph-base/langgraph_base.png","wb") as f:
    f.write(graph_png)