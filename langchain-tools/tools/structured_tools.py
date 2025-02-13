#导入装饰器的库
from langchain_core.tools import StructuredTool
import asyncio

# StructuredTool.from_function ： 可动态的切换同步和异步函数，供同步和异步调用

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def main():
    #func参数是同步函数,在同步上下文中调用时，调用
    #coroutine参数是异步函数，异步调用时使用
    calculator = StructuredTool.from_function(func=multiply,coroutine=amultiply)
    #invoke是同步调用
    print(calculator.invoke({"a":2,"b":3}))
    #ainvoke是异步调用
    print(await calculator.ainvoke({"a":2,"b":5}))

asyncio.run(main())