#获取图片的base64编码，然后传递给模型
import base64
#使用httpx库获取图片的二进制数据
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
#将图片的二进制数据转换为base64编码
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
model = ChatOpenAI(model="gpt-4o")
message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述图片中的logo所代表的公司"},
        #用本地网络访问图片，然后将图片的base64编码传递给模型
        {"type":"image_url", "image_url":{"url": f"data:image/png;base64,{image_data}"}},
    ],
)

response = model.invoke([message])
print(response.content)