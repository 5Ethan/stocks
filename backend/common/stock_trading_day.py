import pandas_market_calendars as mcal
import datetime

def get_last_trading_day():
    """
    获取最近的一个交易日日期
    """
    return get_trading_day(1)[0].strftime("%Y-%m-%d")

def get_trading_day(count=7):
    """
    获取最近的 `count` 个交易日
    """
    if count < 1 or count > 30:
        count = 10

    cn_cal = mcal.get_calendar("XSHG")
    today = datetime.datetime.now()
    start_date = (today - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    schedule = cn_cal.schedule(start_date=start_date, end_date=end_date)
    
    trading_days = schedule.index.tolist()

    if len(trading_days) >= count:
        return trading_days[-count:]
    else:
        return trading_days
