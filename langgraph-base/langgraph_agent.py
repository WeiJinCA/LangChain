from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
import asyncio
from langgraph.prebuilt import create_react_agent

#创建TavilySearchResults工具
tools = [TavilySearchResults(max_results=1)]

#从Langchain Hub加载模版
prompt = hub.pull("wfh/react-agent-executor")
prompt.pretty_print()

#选择驱动代理的LLM,使OpenAI的GPT-4o模型驱动代理
llm = ChatOpenAI(model="gpt-4o")
#创建一个react代理执行器，
agent_executor = create_react_agent(llm,tools,messages_modifier=prompt)

#调用代理执行器，
#agent_executor.invoke({"messages":[{"user":"谁是美国公开赛的胜利者？"}]})

import operator
from typing import Annotated,List,Tuple,TypedDict

#定义一个TypedDict类的PlanExecute,用于存储输入，计划，过去的步骤和响应(工作流参数)
class PlanExecute(TypedDict):
    input:str
    plan:List[str]
    past_steps:Annotated[List[Tuple],operator.add]
    response:str

from pydantic import BaseModel,Field
#定义一个Plan模型类，用于描述未来要执行的计划
class Plan(BaseModel):
    steps:List[str]=Field(
        description="需要执行的不同步骤，应该按顺序排列")
    
#创建一个计划生成的提示模版
from langchain_core.prompts import ChatPromptTemplate
planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """对于给定目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，如果正确执行将得到正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。"""),
         ("placeholder","{message}")
    ],
)
#使用指定的模版，创建一个生成器，使用chatGPT-4o模型
planner = planner_prompt | ChatOpenAI(
    model="gpt-4o",temperature=0).with_structured_output(Plan)

#调用计划生成器，
#planner.invoke({"messages":[{"user":"现任澳网冠军的家乡是哪里？"}]})

from typing import Union
class Response(BaseModel):
    response:str

#定义一个行为模型，用于描述要执行的行为，集成BaseModel
class Act(BaseModel):
    action:Union[Plan,Response] = Field(
        description="要执行的行为。如果要回应用户,使用Response。如果需要进一步使用工具获取答案,使用Plan。")
    
replanner_prompt = ChatPromptTemplate.from_template(
    """
    对于给定目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，如果正确执行将得到正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。
    
    你的目标是：
    {input}

    你的原计划是：
    {plan}

    你目前已完成的步骤是：
    {past_steps}
    
    响应的更新你的计划。如果不需要更多步骤并且可以返回给用户，那么就这样回应。如果需要，填写计划。只添加仍需要完成的步骤。不要返回已完成的步骤作为计划的一部分
    """
)

replanner = replanner_prompt | ChatOpenAI(
    model="gpt-4o",temperature=0).with_structured_output(Act)

from typing import Literal
#定义一个异步住函数
async def main():
    async def plan_step(state:PlanExecute):
        plan = await planner.ainvoke({"messages":[{"user":state["input"]}]})
        return {"plan":plan.steps}
    
    async def execute_step(state:PlanExecute):
        plan = state["plan"]
        plan_str = "\n".join(f"{i+1}. {step}" for i,step in enumerate(plan))
        task = plan[0]
        task_formated = f"""对于以下计划：
        {plan_str}\n\n你的任务是执行第{1}步，{task}。"""

        agent_response = await agent_executor.ainvoke(
            {"messages":[{"role":"user","content":task_formated}]}
        )
        return {"past_steps":state["past_steps"]+[(task,agent_response["messages"][-1].content)]}
    
    async def replan_step(state:PlanExecute):
        output = await replanner.ainvoke(state)
        if isinstance(output.action,Response):
            return {"response":output.action.response}
        else:
            return {"plan":output.action.steps}
        
    def should_end(state:PlanExecute)->Literal["agent","__end__"]:
        if "response" in state and state["response"]:
            return "__end__"
        else:
            return "agent"

    from langgraph.graph import StateGraph,START
    workflow = StateGraph(PlanExecute)
    workflow.add_node("planner",plan_step)
    workflow.add_node("agent",execute_step)
    workflow.add_node("replan",replan_step)
    workflow.add_edge(START,"planner")
    workflow.add_edge("planner","agent")
    workflow.add_edge("agent","replan")
    workflow.add_conditional_edges("replan",should_end)

    app = workflow.compile()

    graph_png = app.get_graph().draw_mermaid_png()
    with open("./langgraph-base/agent_workflow.png","wb") as f:
        f.write(graph_png)

    config = {"recursion_limit":50}

    inputs = {"input":"2024年巴黎奥运会100米自由泳决赛冠军的家乡是哪里？请用中文回答"}

    async for event in app.astream(inputs,config=config):
        for k,v in event.items():
            if k != "__end__":
                print(v)

asyncio.run(main())