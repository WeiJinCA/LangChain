#pip install streamlit==1.39.0
# pip install toml
#Python 3.12.4
import streamlit as st
import tempfile
import os
#会话内存存储
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import TextLoader
#OpenAIEmbeddings将文本转换为向量
from langchain_openai import OpenAIEmbeddings
#Chroma内存向量数据库
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import AgentExecutor,create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_openai import ChatOpenAI

# Title and description
st.set_page_config(page_title="文档问答", layout="wide")
st.title("文档问答")

uploaded_files = st.sidebar.file_uploader(
    label="Upload a document(.txt)",
    type=["txt"],#"pdf"
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info("Please upload a TXT document to start the conversation.")
    st.stop()

#实现检索器
@st.cache_resource(ttl="1h")
def configure_retriever(uploaded_files):
    #读取上传文档，并写入临时目录
    docs = []
    temp_dir = tempfile.TemporaryDirectory(dir="/tmp")
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir.name, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        #使用TextLoader加载文本
        loader = TextLoader(file_path,encoding="utf-8")
        docs.extend(loader.load())

    #进行文档分割
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    splits = splitter.split_documents(docs)
    print(f"splits: {splits}")
    if not splits:
        raise ValueError("Splits is empty. Please check the input documents.")
    
    #使用OpenAIEmbeddings将文本转换为向量
    embeddings = OpenAIEmbeddings()
    # try:
    #     embed_results = embeddings.embed_documents(splits)
    #     print(f"Generated embeddings: {embed_results}")
    # except Exception as e:
    #     print(f"Error generating embeddings: {e}")
    #     raise

    # splits = [s for s in splits if s.strip()]
    # if not splits:
    #     raise ValueError("Filtered splits are empty. Please check the input data.")

    vectordb = Chroma.from_documents(splits, embeddings)

    #创建文档检索器
    retriever = vectordb.as_retriever()

    return retriever

#配置检索器
retriever = configure_retriever(uploaded_files)

#如果session_state中没有消息或用户点击了清空聊天记录按钮，则创建一个新的session_state
if "messages" not in st.session_state or st.sidebar.button("清空聊天记录"):
    st.session_state["messages"] = [{"role":"assistant","content": "您好！我是文档问答助手。"}]

#加载历史消息
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

#创建检索工具
from langchain.tools.retriever import create_retriever_tool
tool = create_retriever_tool(
    retriever,
    "文档检索",
    "用于检索用户提出的问题，并基于检索到的文档内容进行回复。",
    )
tools = [tool]

#创建聊天消息历史记录
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs,
    return_messages=True,
    memory_key="chat_history",
    output_key="output"
)

#指令模版
instructions = """您是一个设计用于查询文档来回答问题的代理。
您可以使用文档检索工具，并基于检索内容来回答问题
您可能不查询文档就知道答案，但是您仍然应该查询文档来获得答案
如果您从文档中找不到任何信息用于回答问题，则只需返回“抱歉，这个问题我不知道”作为答案
"""

#基础提示模版
base_prompt_template = """
{instructions}

Tools:
{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes  
Action: the action to take, should be one of [{tool_names}]  
Action Input: {input}  
Observation: the result of the action  
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No  
Final Answer: [your response here]  
```

Begin!

Previous conversation history:  
{chat_history}  

New input: {input}
{agent_scratchpad}"""

#创建基础提示模版
base_prompt = PromptTemplate.from_template(base_prompt_template)

#创建部分填充的提示模版
prompt = base_prompt.partial(instructions=instructions)

#创建llm
llm = ChatOpenAI()

#创建react agent
agent = create_react_agent(
    llm,
    tools,
    prompt,
)

#创建agent执行器
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors="没有从知识库检索到相似内容"
)

#创建聊天输入框
user_query = st.chat_input(placeholder="请开始提问吧！")

#如果有用户输入的查询
if user_query:
    #将消息添加到历史记录中
    st.session_state.messages.append({"role":"user","content":user_query})
    #显示用户消息
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        #创建Streamlit回调处理程序
        st_cb = StreamlitCallbackHandler(st.container())
        #agent执行过程日志回调显示在Streamlit Container中（如思考，选择工具，执行查询，观察结果等）
        config = {"callback_handler":[st_cb]}
        #执行agent
        response = executor.invoke({"input":user_query},config=config)
        #添加消息助手到message_state
        st.session_state.messages.append({"role":"assistant","content":response["output"]})
        #显示助手响应
        st.write(response["output"])