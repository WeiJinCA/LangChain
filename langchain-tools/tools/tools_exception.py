#导入装饰器的库
from langchain_core.tools import StructuredTool
#导入异常处理的库
from langchain_core.tools import ToolException

# StructuredTool.from_function ： 可动态的切换同步和异步函数，供同步和异步调用

def get_weather(city: str) -> int:
    """Multiply two numbers."""
    raise ToolException(f"Error: {city} not found") #f-string:字符串格式化，插值法

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    #默认情况下，如果函数抛出ToolException，则将ToolException的message作为响应
    #如果设置为True,则将ToolException的message作为响应;False则抛出ToolException
    handle_tool_error = True,
    #handle_tool_error = "没有找到该城市", #也可以直接设置自定义的错误消息
    )

response = get_weather_tool.invoke({"city":"foobar"})
print(response)