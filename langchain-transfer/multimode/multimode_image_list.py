import base64
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url_1 = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
#不同的图片
image_url_2 = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"

model = ChatOpenAI(model="gpt-4o")
message = HumanMessage(
    content=[
        {"type": "text", "text": "这两张图片有什么不同？"},
        #如果因为网络原因，大模型访问不到该url,则不适用这种方式
        {"type":"image_url", "image_url":{"url": image_url_1}},
        {"type":"image_url", "image_url":{"url": image_url_2}},
    ],
)

response = model.invoke([message])
print(response.content)