```shell
pip install pandas

pip install baostock -i https://pypi.org/simple

pip install pandas_market_calendars
```

```shell
## 获取当前安装环境的项目依赖
pip freeze

pip freeze > requirements.txt

## 只获取当前根目录下的项目依赖
pip install pipreqs

pipreqs . --force
```

```shell
pip install fastapi uvicorn

uvicorn main:app

uvicorn main:app --reload
```

```shell
python main.py
```