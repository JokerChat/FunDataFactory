FROM fangchat/python:3.9-node
WORKDIR /fun
COPY . .
RUN mkdir /fun/logs \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD gunicorn -c gunicorn.py -k RestarUvicorn.RestartableUvicornWorker main:fun