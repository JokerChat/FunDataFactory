FROM python:3.9-slim
WORKDIR /fun
RUN apt update -y \
    && apt upgrade -y \
    && apt install -y git \
    && apt install -y nodejs \
    && apt install -y npm \
    && mv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && npm install apidoc@0.22 -g \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD gunicorn -c gunicorn.py -k RestarUvicorn.RestartableUvicornWorker main:fun