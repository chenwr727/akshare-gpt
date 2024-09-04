from typing import Annotated

import akshare as ak

from modules.tools.tool_register import register_tool


@register_tool
def get_stock_sse_summary() -> str:
    """
    获取上海证券交易所最近交易日的股票数据总貌
    """
    df = ak.stock_sse_summary()
    return df.to_json(orient="records", force_ascii=False)


@register_tool
def get_stock_individual_info_em(
    symbol: Annotated[str, "股票代码", True],
) -> str:
    """
    获取指定`symbol`的个股信息
    """
    df = ak.stock_individual_info_em(symbol=symbol)
    return df.to_json(orient="records", force_ascii=False)


@register_tool
def get_stock_bid_ask_em(
    symbol: Annotated[str, "股票代码", True],
) -> str:
    """
    获取指定`symbol`的行情报价数据
    """
    df = ak.stock_bid_ask_em(symbol=symbol)
    return df.to_json(orient="records", force_ascii=False)
