#!/usr/bin/python
#encoding: utf-8
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import threading
import os,time,random

pool=ThreadPoolExecutor(15)   #不填则默认为cpu的个数*5

    # start=time.time()
    # for i in range(10):
    #     obj=p.submit(task,i)
    #     l.append(obj)
    # p.shutdown()
    # print('='*30)
    # print([obj.result() for obj in l])
    # print(time.time()-start)
