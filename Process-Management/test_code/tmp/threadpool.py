#!/usr/bin/python
#encoding: utf-8
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import threading
import os,time,random
import signal

# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    pool.shutdown()

# 设置相应信号处理的handler
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)

def task(n):
    print('%s:%s is running' %(threading.currentThread().getName(),os.getpid()))
    time.sleep(2)
    return n**2
def func(p):
    l=[]
    start=time.time()
    for i in range(10):
        obj=p.submit(task,i)
        l.append(obj)
    p.shutdown()
    print('='*30)
    print([obj.result() for obj in l])
    print(time.time()-start)

if __name__ == '__main__':
    pool=ThreadPoolExecutor()   #不填则默认为cpu的个数*5
    func(pool)
