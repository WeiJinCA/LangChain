from langchain_community.document_loaders import WebBaseLoader
#FAISS : Facebook AI Similarity Search
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

#搜索工具

#下载网站内容
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

print(retrieval.invoke("猫的特征")[0]) #搜索与“猫”最相似的5个文档

retriever_tool = create_retriever_tool(
    retrieval,
    "Wiki_search",
    "搜索维基百科"
)