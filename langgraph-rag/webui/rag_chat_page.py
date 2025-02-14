import streamlit as st
#导入状态图和消息状态
from langgraph.graph import END,StateGraph,MessagesState
#导入工具节点
from langgraph.prebuilt import ToolNode,tools_condition
#导入内存保存器，持久化状态
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessageChunk,ToolMessage

from utils import PLATFORMS,get_chatllm,get_llm_models,get_kb_names,get_img_base64
from tools.naive_tag_tool import get_naive_rag_tool
import json

RAG_PAGE_INTRODUCTION = "你好，我是智能客服助手，请问有什么可以帮助您的吗？"

def get_rag_graph(platform,model,temperature,selected_kbs,KBS):
    tools = [KBS[k] for k in selected_kbs]

    tool_node = ToolNode(tools)

    def call_model(state):
        llm = get_chatllm(platform,model,temperature=temperature)
        llm_with_tools = llm.bind_tools(tools)
        return {"messages":[llm_with_tools.invoke(state["messages"])]}
        
    workflow = StateGraph(MessagesState)

    workflow.add_node("agent",call_model)
    workflow.add_edge("tools",tool_node)
    workflow.add_conditional_edges("agent",tools_condition)
    workflow.add_edge("agent","tools")

    workflow.set_entry_point("agent")

    checkpointer = MemorySaver()

    app = workflow.compile(checkpointer=checkpointer)
    #将生成的图保存到文件
    # graph_png = app.get_graph().draw_mermaid_png()
    # with open("./langgraph-rag/img/langgraph_base.png","wb") as f:
    #     f.write(graph_png)

    return app

def graph_response(graph,input):
    for event in graph.invoke(
        {"messages":input},
        config={"configurable":{"thread_id":42}},
        stream_mode="messages",
    ):
        if type(event[0]) == AIMessageChunk:
            if len(event[0].tool_calls):
                st.session_state["rage_tool_calls"].append(
                    {
                        "status":"正在查询...",
                        "knowledge_base":event[0].tool_calls[0]["name"].replace("_knowledge_base_tool",""),
                        "query":""
                    }
                )
            yield event[0].content
        elif type(event[0]) == ToolMessage:
            status_placeholder = st.empty()
            with (status_placeholder.status("正在查询...",expanded=True) as s):
                st.write("已调用`",event[0].name.replace("_knowledge_base_tool",""),"`   知识库进行查询")
                continue_save = False
                if len(st.session_state["rage_tool_calls"]):
                    if "content" not in st.session_state["rage_tool_calls"][-1].keys():
                        continue_save = True

                st.write("知识库检索加过： ")
                st.code(event[0].content,wrap_lines=True)
                s.update(label="已完成知识库检索！",expanded=False)
            
            if continue_save:
                st.session_state["rage_tool_calls"][-1]["status"] = "已完成知识库检索！"
                st.session_state["rage_tool_calls"][-1]["content"] = json.loads(event[0].content)
            else:
                st.session_state["rage_tool_calls"].append(
                    {
                        "status":"已完成知识库检索！",
                        "knowledge_base":event[0].name.replace("_knowledge_base_tool",""),
                        "query":json.loads(event[0].content)
                    }
                )

def get_rag_chat_response(platform,model,temperature,selected_kbs,KBS,input):
    app = get_rag_graph(platform,model,temperature,selected_kbs,KBS)
    return graph_response(graph=app,input=input)

def display_chat_history():

    for message in st.session_state["rage_chat_history_with_tool_call"]:
        with st.chat_message(message["role"],
                             avatar=get_img_base64("chatchat_avatar.png") if message["role"]=="assistant" else None):
            if "tool_calls" in message.keys():
                
                for tool_call in message["tool_calls"]:
                    with st.status(tool_call["status"],expanded=False):
                        st.write("已调用 `",tool_call['knowledge_base'],"` 知识库进行查询")
                        st.write("知识库检索结果： ")
            st.write(message["content"])


def clear_chat_history():
    st.session_state["rage_chat_history"] = [
        {
            "role":"assistant",
            "content":RAG_PAGE_INTRODUCTION,
        }
    ]
    st.session_state["rage_chat_history_with_tool_call"] = [
        {
            "role":"assistant",
            "content":RAG_PAGE_INTRODUCTION,
        }
    ]
    st.session_state["rage_tool_calls"] = []

    def rag_chat_page():
        kbs = get_kb_names()
        KBS = dict()
        for kb in kbs:
            KBS[f"{k}"] = get_naive_rag_tool(k)
        
        if "rage_chat_history" not in st.session_state:
            st.session_state["rage_chat_history"] = [
                {
                    "role":"assistant",
                    "content":RAG_PAGE_INTRODUCTION,
                }
            ]
        
        if "rage_chat_history_with_tool_call" not in st.session_state:
            st.session_state["rage_chat_history_with_tool_call"] = [
                {
                    "role":"assistant",
                    "content":RAG_PAGE_INTRODUCTION,
                }
            ]
        
        if "rage_tool_calls" not in st.session_state:
            st.session_state["rage_tool_calls"] = []
        
        with st.sidebar:
            selected_kbs = st.multiselect("请选择对话中可用的知识库",kbs,default=kbs)

        display_chat_history()

        with st._bottom:
            cols = st.columns([1.2,10,1])
            with cols[0].popover(":gear",use_container_width=True,help="配置模型"):
                platform = st.selectbox("选择要使用的模型加载方式",PLATFORMS)
                model = st.selectbox("选择要使用的模型",get_llm_models(platform))
                temperature = st.slider("选择Temperature",0.1,1.,0.1)
                history_len = st.slider("选择历史消息长度",1,10,5)

            input = cols[1].chat_input("请输入您的问题")
            cols[2].button(":wastebasket:",help="清除聊天记录",on_click=clear_chat_history)

        if input:
            with st.chat_message("user"):
                st.write(input)
            st.session_state["rage_chat_history"] += [
                {
                    "role":"user",
                    "content":input,
                }
            ]
            st.session_state["rage_chat_history_with_tool_call"] += [
                {
                    "role":"user",
                    "content":input,
                }
            ]
            #获取RAG聊天响应
            stream_response = get_rag_chat_response(platform,model,temperature,
                                                    st.session_state["teg_chat_history"][-history_len:],                
                                                    selected_kbs,KBS)
            
            #显示助手消息
            with st.chat_message("assistant",avatar=get_img_base64("chatchat_avatar.png")):
                response = st.write_stream(stream_response)