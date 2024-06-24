import math
import pandas as pd


data_day_columns_to_skip = {
    "date",
    "code",
    "adjustflag",
    "tradestatus",
    "isST",
}

def convert_to_echarts_multi_line_format(df):
    df=df.map(format_df_value)

    echarts_data = {"xAxis": df["date"].tolist(), "series": []}

    columns_to_include = (column for column in df.columns if column not in data_day_columns_to_skip)
    
    for column in columns_to_include:
        series_data = {"name": column, "type": "line", "data": df[column].tolist()}
        echarts_data["series"].append(series_data)

    return echarts_data

def format_df_value(value):
    if pd.isna(value) or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return value

    try:
        value = float(value)
    except ValueError:
        return value
    
    formatted_value = f"{value:.2f}"
    parts = formatted_value.split('.')
    if len(parts[0]) > 2:
        parts[0] = parts[0][-2:]
    return ".".join(parts)