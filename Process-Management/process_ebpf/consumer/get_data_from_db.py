#!/usr/bin/python
#encoding:utf-8

from init_db import influx_client
from db_modules import read_wakeuptime_from_db,read_thread_create_count_from_db, redis_lset

def get_info_from_db(tb_name, date_time, rows, interval, redis_key):#分页查询
    page = 1
    flag = 0
    while True:
        if tb_name == "proc_wakeuptime":
            res = read_wakeuptime_from_db(influx_client, tb_name, date_time, rows, page) 
            for key in zip(res) :
                flag = 1
                input_wakeuptime_into_redis(key[0], redis_key)
        if tb_name == "thread_create_count":
            res = read_thread_create_count_from_db(influx_client, tb_name, date_time, rows, page)
            for key in zip(res) :
                flag = 1
                input_thread_create_count_into_redis(key[0], redis_key)
        if flag == 1:
            page+=1
            flag = 0   
        if rows == -1:
            break 
        sleep(interval)

def input_thread_create_count_into_redis(data, key):
    for k in data:
        tmp =""
        tmp = k["process_name"]+"_"+str(k["count"])
        redis_lset(key, tmp)

#type data is list
def input_wakeuptime_into_redis(data, key):
    for k in data:
        tmp = ""
        tmp = k["process_name"]+"_"+str(k["lantency"])
        print(tmp)
        redis_lset(key, tmp)