from typing import Any, Dict, List, Literal, Optional, Type, Union
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

import akshare as ak

class GetStockIdInput(BaseModel):
    stockname: str = Field(description="要查询股票代码的股票名称")

class GetStockId(BaseTool):
    """Tool that get stock id by given stock name
    """
    name: str = "get_stock_id"
    description: str = (
        "a search engine for getting stock id by given stock name."
        "Useful for when you need to get the id of a certain stock name." \
        "Input shout be a stock name"
    )
    args_schema: Type[BaseModel] = GetStockIdInput


    def _run(self, stockname: str):
        result = ak.stock_info_a_code_name()

        for i,line in result.iterrows():
            if line["name"] == stockname:
                return line["code"]
        return ""
    
if __name__ == "__main__":
    s = GetStockId()
    print(s("容知日新"))