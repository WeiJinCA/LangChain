from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o",temperature=0)


joke_query = "Tell me a joke about."

parser = JsonOutputParser()
prompt = PromptTemplate(
    template="回答用户的查询。\n{format_instructions}\n{query}",
    input_variables={"query"},
    partial_variables={"format_instructions":parser.get_format_instructions()},
)

chain = prompt | model | parser
response = chain.invoke({"query":joke_query})
print(response)