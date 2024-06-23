
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

EXPOSE 8888

ENV DATA_ROOT_DIR=${DATA_ROOT_DIR:-$(pwd)}

VOLUME ["${DATA_ROOT_DIR}:/root"]

# Run app.py when the container launches
CMD ["python", "app.py"]
