FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

WORKDIR /app

COPY requirements.txt .  

RUN pip install --no-cache-dir -i https://pypi.org/simple -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["python", "app.py"]
