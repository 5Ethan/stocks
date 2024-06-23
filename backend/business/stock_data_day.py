import baostock as bs
import pandas as pd

from common.stock_trading_day import get_trading_day


def identify_market(stock_code):
    """
    识别股票编码所属市场类型
    """
    if stock_code.startswith("60") or stock_code.startswith("68"):
        return "sh." + stock_code
    elif stock_code.startswith("00") or stock_code.startswith("30"):
        return "sz." + stock_code
    elif stock_code.startswith("83") or stock_code.startswith("87"):
        return "bj." + stock_code
    return None


def fetch_stock_data_day(stock_code, start_day, end_day):
    """
    按天获取股票交易数据
    """
    full_stock_code = identify_market(stock_code)
    if not full_stock_code:
        print("Invalid stock code format.")
        return

    lg = bs.login()

    if lg.error_code != "0":
        print("login respond error_code:" + lg.error_code)
        print("login respond error_msg:" + lg.error_msg)
        print("Login failed")
        return

    rs = bs.query_history_k_data_plus(
        full_stock_code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
        start_date=start_day,
        end_date=end_day,
        frequency="d",
        adjustflag="3",
    )

    if rs.error_code != "0":
        print("Query failed")
        bs.logout()
        return

    data_list = []
    while (rs.error_code == "0") & rs.next():
        data_list.append(rs.get_row_data())

    result = pd.DataFrame(data_list, columns=rs.fields)

    bs.logout()
    return result


def get_stock_data_list(stock_code, count=7):
    """
    获取股票最近`count`天的交易数据
    """
    day_list = get_trading_day(count)
    formatted_day_list = [item.strftime("%Y-%m-%d") for item in day_list]

    print(f"formatted_day_list={formatted_day_list}")
    print(f"{formatted_day_list[0]}")
    print(f"{formatted_day_list[-1]}")

    dfs = fetch_stock_data_day(
        stock_code, start_day=formatted_day_list[0], end_day=formatted_day_list[-1]
    )

    print(f"{dfs}")

    return dfs
