#!/usr/bin/python
#encoding: utf-8
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import threading
import os,time,random

pool=ThreadPoolExecutor(4)   #不填则默认为cpu的个数*5


def task(n):
    print('%s:%s is running' %(threading.currentThread().getName(),os.getpid()))
    time.sleep(2)
    return n**2


def func():
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
    func()