import base64
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
model = ChatOpenAI(model="gpt-4o")
message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述图片中的logo所代表的公司"},
        #如果因为网络原因，大模型访问不到该url,则不适用这种方式
        {"type":"image_url", "image_url":{"url": image_url}},
    ],
)

response = model.invoke([message])
print(response.content)