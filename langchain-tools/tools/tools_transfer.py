#导入装饰器的库
from langchain_core.tools import tool
from pydantic import BaseModel,Field

#定义输入参数的模式
class CalculatorInput(BaseModel):
    a: int=Field(description="First number")
    b: int=Field(description="Second number")

#return_direct:如果为True，则返回值将直接返回，而不是作为字典返回
@tool("multiplication-tool",args_schema=CalculatorInput,return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

#让我们检查与该工具的关联性
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)

print(multiply.invoke({"a":2,"b":3}))