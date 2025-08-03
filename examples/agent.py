import langchain_core.messages
from model import DoubaoModel

from langchain_tavily import TavilySearch
from tools.seacrhStock import StockSearch
from tools.checkStockid import GetStockId
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

memory = MemorySaver()

model = DoubaoModel()

stocksearch = StockSearch()
getstockid = GetStockId()
tools = [stocksearch, getstockid]

agent = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

try:
    while True:
        try:
            user_input = input(">>> ")
            user_input = "我想分析688768这只股票。"
            input_message = {
                    "role": "user",
                    "content": user_input
                }

            for step in agent.stream(
                {"messages": [input_message]}, config=config, stream_mode="values"
            ):
                if isinstance(step["messages"][-1], HumanMessage):
                    continue
                step["messages"][-1].pretty_print()
            
        except KeyboardInterrupt:
            # 第一次 Ctrl+C - 提示退出
            print("\n再次按 Ctrl+C 退出，或按回车继续")
            try:
                # 等待用户确认
                input()
            except KeyboardInterrupt:
                # 第二次 Ctrl+C - 退出程序
                print("\n退出程序")
                break
                
except EOFError:
    print("\n检测到文件结束符，退出程序")
