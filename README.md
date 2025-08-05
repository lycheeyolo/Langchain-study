# 记录学习LangChain

+ ## 2025-08-05
    学习主要内容：LangGraph: 将自动执行的“工作流”以链的形式构成所谓的“图”，完成设计的任务。

    - LangGraph的主要部分是三个：State，Node，Edge。其中
        * Node节点：是需要执行的任务，也就是函数。函数的参数是State。
        * Edge边：用来判断当前节点完成后，接下来执行哪一个节点的函数。
        * State状态：在整个Graph中，所有节点的入参，也是出参。用来记录整个任务执行过程中的中间状态。

        *注意：LangGraph可以理解成一种工作流，并不以LLM为基础。

    - 通过LangGraph构建一个最简单的chatbot:
        * 实例化大模型model；
        * 构建State类，继承自typing.TypeDict,实际上就是一个字典对象；类内定义属性，也就是需要在Node之间保存记录的属性，类型是Annotation[实际类， 每次操作这个属性需要执行的函数]；
        * 构建Node函数，每一个Node都是一个函数，函数的参数是state，类型是上面定义的State类。函数返回键值对，对应state的属性，state会按照属性对应的需要执行的函数将函数返回值返回给state；
        * 创建一个构建图的实例，方式如下：
        ```python
        graph_builder = GraphBuilder()
        ```
        * 为图添加节点和边，注意，图的首届点是START, 尾节点是END。最后通过complie函数生成图graph。代码如下：
        ```python
        graph_builder.add_node("nodename", node)
        graph_builder.add_edge(START, "nodename")
        graph_builder.add_edge("nodename", END)
        graph = graph_builder.complie()
        ```
        * 可以通过invoke或者streaming执行图。



+ ## 2025-08-03

    第一天，学习langchain简介，主要精力放在了怎么通过langchain调用豆包模型。由于langchain官方似乎没有提供封装好的豆包类，所以需要借助langchain_openai包，通过传入豆包url形式调用模型；

    - 学习了langchain创建chain的方式，了解了langchain对一些基础类重写了管道操作符“|”，可以通过管道的形式构建chain。然后通过invoke函数运行构建的chain；
    - 实例化一个model（区别于chain）后，也是通过invoke函数，传入问题或者messages是西安调用模型；
    - 构建一个agent，可以借助官方封装好的tool, 也可以自己构建tool。下面两种自定义tool的方式比较推荐：
        * 通过注解@tool实现
        ```python 
        from langchain_core.tools import tool


        @tool
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b

        from typing import Annotated, List


        @tool
        def multiply_by_max(
            a: Annotated[int, "scale factor"],
            b: Annotated[List[int], "list of ints over which to take maximum"],
        ) -> int:
            """Multiply a by the maximum of b."""
            return a * max(b)
        from pydantic import BaseModel, Field


        class CalculatorInput(BaseModel):
            a: int = Field(description="first number")
            b: int = Field(description="second number")


        @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b
        ```
        * 通过构建子类实现
        ```python
        from typing import Optional

        from langchain_core.callbacks import (
            AsyncCallbackManagerForToolRun,
            CallbackManagerForToolRun,
        )
        from langchain_core.tools import BaseTool
        from langchain_core.tools.base import ArgsSchema
        from pydantic import BaseModel, Field


        class CalculatorInput(BaseModel):
            a: int = Field(description="first number")
            b: int = Field(description="second number")


        # Note: It's important that every field has type hints. BaseTool is a
        # Pydantic class and not having type hints can lead to unexpected behavior.
        class CustomCalculatorTool(BaseTool):
            name: str = "Calculator"
            description: str = "useful for when you need to answer questions about math"
            args_schema: Optional[ArgsSchema] = CalculatorInput
            return_direct: bool = True

            def _run(
                self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> int:
                """Use the tool."""
                return a * b

            async def _arun(
                self,
                a: int,
                b: int,
                run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
            ) -> int:
                """Use the tool asynchronously."""
                # If the calculation is cheap, you can just delegate to the sync implementation
                # as shown below.
                # If the sync calculation is expensive, you should delete the entire _arun method.
                # LangChain will automatically provide a better implementation that will
                # kick off the task in a thread to make sure it doesn't block other async code.
                return self._run(a, b, run_manager=run_manager.get_sync())
        ```
    + 构建agent的时候，一定要实例化工具，把实例化对象以列表形式传入create_react_agent中，得到一个agent对象。通过下面方式执行agent获取结果：
    ```python
    for step in agent.stream(
        {"messages": [input_message]}, config=config, stream_mode="values"
    ):
        pass
    ```