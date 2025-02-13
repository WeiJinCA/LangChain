from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o",temperature=0)

actor_query = "生成周星驰的简化电影作品列表，按照最新的时间降序."

parser = XMLOutputParser(tags=["movie","actor","film","name","genre"])

prompt = PromptTemplate(
    template="回答用户的查询。\n{format_instructions}\n{query}",
    input_variables={"query"},
    partial_variables={"format_instructions":parser.get_format_instructions()},
)
#print(parser.get_format_instructions())
chain = prompt | model | parser
for s in chain.stream({"query":actor_query}):
    print(s)
