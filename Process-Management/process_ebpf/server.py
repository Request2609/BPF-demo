#!/usr/bin/python
#encoding: utf-8
import signal
from init import init
from application.service.thread_pool import pool
from application.service.produce import connection

# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    pool.shutdown()
    connection.close()
    
# 设置相应信号处理的handler
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)


if __name__=="__main__":
    init().run(debug=True)