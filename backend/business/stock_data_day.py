import baostock as bs
import pandas as pd
import os

from common.stock_data_enum import Data_Type
from common.stock_trading_day import get_last_trading_day, get_trading_day

from config import g_data_dir


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


def data_file_day(stock_code, day):
    """
    股票日数据存储路径。如果路径不存在，则创建路径。
    """
    directory_path = os.path.join(g_data_dir, "datas", "day", stock_code)
    file_path = os.path.join(directory_path, f"{day}.csv")

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    return file_path


def fetch_stock_data_day(stock_code, day):
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
        start_date=day,
        end_date=day,
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

    file_name = data_file_day(stock_code, day)
    result.to_csv(file_name, index=False)

    bs.logout()


def get_stock_data(stock_code, type=Data_Type.DAY, day=None):
    """
    获取指定日期的股票数据，如果文件存在则读取数据，否则获取数据并存储到文件
    """
    if Data_Type.DAY == type:
        if day is None:
            day = get_last_trading_day()

        file_path = data_file_day(stock_code, day)

        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Fetching data.")
            fetch_stock_data_day(stock_code, day)

        return pd.read_csv(file_path)


def get_stock_data_list(stock_code, count=7):
    """
    获取股票最近`count`天的交易数据
    """
    day_list = get_trading_day(count)

    dfs = []
    for day in day_list:
        df = get_stock_data(stock_code, day=day.strftime("%Y-%m-%d"))
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True).sort_values(by='date', ascending=True)

