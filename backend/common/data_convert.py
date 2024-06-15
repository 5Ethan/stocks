data_day_columns_to_skip = {
    "date",
    "code",
    "adjustflag",
    "tradestatus",
    "isST",
}

def convert_to_echarts_multi_line_format(df):
    echarts_data = {"xAxis": df["date"].tolist(), "series": []}

    def convert_units(column):
        if column == "volume" or column == "amount":
            df[column] = df[column] / 1000000

    columns_to_include = (column for column in df.columns if column not in data_day_columns_to_skip)
    
    for column in columns_to_include:
        convert_units(column)
        series_data = {"name": column, "type": "line", "data": df[column].tolist()}
        echarts_data["series"].append(series_data)

    return echarts_data
