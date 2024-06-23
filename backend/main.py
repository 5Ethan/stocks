from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from common.data_convert import convert_to_echarts_multi_line_format
from business.stock_data_day import get_stock_data_list
from config import PORT, g_stock_info_list
from pydantic import BaseModel

app = FastAPI()


class StockInfo(BaseModel):
    code: str
    name: str


@app.get("/")
async def read_root():
    return FileResponse("html/index.html")


@app.get("/page/stock_show")
async def read_stock_show():
    return FileResponse("html/stock_show.html")


@app.get("/page/stock_list")
async def read_stock_list():
    return FileResponse("html/stock_list.html")


@app.get("/api/stocks")
async def get_stocks():
    return g_stock_info_list


@app.post("/api/stocks")
async def add_stock(stock: StockInfo):
    for existing_stock in g_stock_info_list:
        if existing_stock["code"] == stock.code:
            continue
        g_stock_info_list.append(stock.model_dump())
    return {"b_code": 200, "data": stock}


@app.delete("/api/stocks/{stock_code}")
async def delete_stock(stock_code: str):
    for stock in g_stock_info_list:
        if stock["code"] == stock_code:
            g_stock_info_list.remove(stock)

    return {"b_code": 200, "data": stock}


# http://localhost:8888/api/stock/data/603628
@app.get("/api/stock/data/{stock_code}")
async def stock_data_day(stock_code: str):
    data = get_stock_data_list(stock_code)
    return {"b_code": 200, "data": data}


# http://localhost:8888/api/stock/echarts/line/603628
@app.get("/api/stock/echarts/line/{stock_code}")
async def stock_data_day_echart(stock_code: str, last_day_count: int = 14):
    data = get_stock_data_list(stock_code, last_day_count)
    data_dict = convert_to_echarts_multi_line_format(data)
    return JSONResponse(content={"b_code": 200, "data": data_dict})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
