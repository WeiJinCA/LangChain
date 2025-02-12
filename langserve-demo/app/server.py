from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langserve import add_routes
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(
    title="Langchain Server",
    description="使用Langchain的Runable接口的简单API服务器",
    version="0.1.0",
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(
    app, 
    ChatOpenAI(model="gpt-3.5-turbo"),
    path="/openai",
)

parser = StrOutputParser()
add_routes(
    app,
    ChatOpenAI(model="gpt-3.5-turbo") | parser, 
    path="/openai_str_parser",
)

prompt = ChatPromptTemplate.from_template("告诉我一个关于{topic}的故事.")
add_routes(
    app,
    prompt | ChatOpenAI(model="gpt-4"), 
    path="/openai_ext",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
