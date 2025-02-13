from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o",temperature=0)

#定义期望的数据结构
class Joke(BaseModel):
    setup: str = Field(description="设置笑话的问题")
    punchline: str = Field(description="解决笑话的回答")

joke_query = "Tell me a joke about."

parser = JsonOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
    template="回答用户的查询。\n{format_instructions}\n{query}",
    input_variables={"query"},
    partial_variables={"format_instructions":parser.get_format_instructions()},
)

chain = prompt | model | parser
response = chain.invoke({"query":joke_query})
print(response)