#导入装饰器的库
from langchain_core.tools import tool

#加async,为异步函数
@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

#让我们检查与该工具的关联性
print(multiply.name)
print(multiply.description)
print(multiply.args)