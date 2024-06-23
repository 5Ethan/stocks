from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from database.mysql import execute_query,execute_insert,execute_delete
from common.data_convert import convert_to_echarts_multi_line_format
from business.stock_data_day import get_stock_data_list
from config import PORT
from pydantic import BaseModel

app = FastAPI()


class StockInfo(BaseModel):
    stock_code: int
    stock_name: str


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
    query = "SELECT stock_code,stock_name FROM info_stock;"
    result = await execute_query(query)
    return result


@app.post("/api/stocks")
async def add_stock(stock: StockInfo):
    table = 'info_stock'
    data = {
        'stock_code': stock.stock_code,
        'stock_name': stock.stock_name,
    }
    return await execute_insert(table, data)


@app.delete("/api/stocks/{stock_code}")
async def delete_stock(stock_code: str):
    table = 'info_stock'
    condition = f'stock_code = {stock_code}'  
    return await execute_delete(table, condition)



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
