from typing import Any, Dict, List, Literal, Optional, Type, Union
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

import akshare as ak

class StockSearchInput(BaseModel):
    stockid: str = Field(description="要查询信息的股票stockid")

class StockSearch(BaseTool):
    """Tool that search Stack statistic information
    """
    name: str = "stack_search"
    description: str = (
        "a search engine for getting statistic information about given stock id."
        "Useful for when you need to analysis a stock." \
        "Input shout be a stock id, like 000001"
    )
    args_schema: Type[BaseModel] = StockSearchInput


    def _run(self, stockid: str):
        stock_individual_basic_info_xq_df = ak.stock_zh_a_hist(symbol=stockid, start_date="20210901", end_date="20250803")
        return stock_individual_basic_info_xq_df
    
if __name__ == "__main__":
    s = StockSearch()
    print(s("688768"))