# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 16:11 
# @Author : junjie
# @File : runserver.py

import uvicorn

if __name__ == '__main__':
    uvicorn.run(app="main:fun", host="0.0.0.0", port=8080, reload=True, access_log=True)
