import os
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "langchain.db")

db = SQLDatabase.from_uri("sqlite:///{db_path}")
toolkit = SQLDatabaseToolkit(db=db,llm=ChatOpenAI(temperature=0))
print(toolkit.get_tools())

agent_executor = create_sql_agent(
    llm=ChatOpenAI(temperature=0,model="gpt-4"),
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

result = agent_executor.invoke({"describe the full_llm_cache table"})
print(result)
