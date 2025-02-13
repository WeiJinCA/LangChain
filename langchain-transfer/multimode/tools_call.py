from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def weather_tool(weather: Literal["晴朗的","多云的","多雨的","下雪的"]) -> None:
    """Describe the weather."""
    pass

model = ChatOpenAI(model="gpt-4o")
model_with_tools = model.bind_tools([weather_tool])
image_url_1 = "https://images.nationalgeographic.org/image/upload/t_edhub_resource_key_image/v1638886301/EducationHub/photos/lightning-bolts.jpg"
image_url_2 = "https://www.tovima.com/wp-content/uploads/2024/10/24/KON1385-scaled.jpg"

message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述两张图中的天气"},
        #如果因为网络原因，大模型访问不到该url,则不适用这种方式
        {"type":"image_url", "image_url":{"url": image_url_1}},
        {"type":"image_url", "image_url":{"url": image_url_2}},
    ],
)

response = model_with_tools.invoke([message])
print(response.tool_calls)