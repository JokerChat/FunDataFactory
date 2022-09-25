# gunicorn的配置

import multiprocessing

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:8080"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/error.log"
# 代码改动, 自动重载
reload = True
# 是否以守护进程启动
daemon = False
# 请求超时配置
timeout = 30

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'