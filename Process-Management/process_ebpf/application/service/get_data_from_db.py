#!/usr/bin/python
#encoding:utf-8
from application.service.get_compare_time import get_time
from application.db_module.init_db import influx_client
from application.db_module.db_modules import redis_lset, redis_lget, read_from_db

def get_info_from_db(tb_name, date_time, rows):#分页查询
    if tb_name == "proc_wakeuptime":
        page = 1
        flag = 0
        while True:
            res = read_from_db(influx_client,"proc_wakeuptime", date_time, rows, page)
            for key in zip(res) :
                flag = 1
                input_wakeuptime_into_redis(key[0])
            if flag == 1:
                page+=1
                flag = 0   
            if rows == -1:
                break 
            sleep(1)
    return 1

#type data is list
def input_wakeuptime_into_redis(data):
    for k in data:
        tmp = ""
        tmp = k["process_name"]+"_"+str(k["lantency"])
        redis_lset("wakeup_time", tmp)

def read_from_redis(key, count):
    return redis_lget(key, count)