FROM python:3.9-slim as builder
WORKDIR /fun
RUN apt update -y \
    && apt upgrade -y \
    && apt install -y tzdata \
    && apt install -y wget \
    && apt install -y tar \
    && apt install -y xz-utils \
    && wget https://nodejs.org/download/release/v14.16.1/node-v14.16.1-linux-x64.tar.xz \
    && tar -xvJf node-v14.16.1-linux-x64.tar.xz \
    && mv node-v14.16.1-linux-x64 node-v14.16.1

FROM python:3.9-slim
WORKDIR /fun
COPY . .
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY --from=builder /fun/node-v14.16.1 /usr/local/nodejs
COPY ./ssh_config /etc/ssh/
ENV PATH=/usr/local/nodejs/bin:$PATH
RUN apt update -y \
    && apt upgrade -y \
    && apt install -y git \
    && ln -s /usr/local/nodejs/bin/node /usr/bin/node \
    && ln -s /usr/local/nodejs/bin/npm /usr/bin/npm \
    && npm install apidoc@0.22 -g \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD gunicorn -c gunicorn.py -k RestarUvicorn.RestartableUvicornWorker main:fun