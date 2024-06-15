
from common.data_convert import convert_to_echarts_multi_line_format
from business.stock_data_day import get_stock_data_list

if __name__ == "__main__":
    data = get_stock_data_list("603628")

    print(convert_to_echarts_multi_line_format(data))

    