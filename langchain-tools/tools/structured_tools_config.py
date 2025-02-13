#导入装饰器的库
from langchain_core.tools import StructuredTool
import asyncio
from pydantic import BaseModel,Field
# StructuredTool.from_function ： 可动态的切换同步和异步函数，供同步和异步调用


#定义输入参数的模式
class CalculatorInput(BaseModel):
    a: int=Field(description="First number")
    b: int=Field(description="Second number")

def multiply(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

async def async_addition(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def main():
    #func参数是同步函数,在同步上下文中调用时，调用
    #coroutine参数是异步函数，异步调用时使用
    calculator = StructuredTool.from_function(
        func=multiply,
        name="Calculator",
        description="Multiply two numbers.",
        args_schema=CalculatorInput,
        return_direct=True,
        #coroutine=async_addition
        )
    
    #invoke是同步调用
    print(calculator.invoke({"a":2,"b":3}))
    print(calculator.name)
    print(calculator.description)
    print(calculator.args)

asyncio.run(main())