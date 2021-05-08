#!/usr/bin/python
#encoding:utf-8

from init_db import influx_client
from db_modules import read_wakeuptime_from_db,read_thread_create_count_from_db, redis_lset,read_sched_count_from_db,read_queue_lantency_from_db, read_queue_length_from_db, delete_a_key

def get_info_from_db(delete_key, tb_name, date_time, rows, interval, redis_key):#分页查询
    no_data_count = 100  #要是100次没有获取到数据，就退出
    page = 1
    flag = 0
    if delete_key:
        print("删除redis list key", redis_key)
        delete_a_key(redis_key)
    while no_data_count > 0:
        if tb_name == "proc_wakeuptime":
            res = read_wakeuptime_from_db(influx_client, tb_name, date_time, rows, page) 
            for key in zip(res):
                # print(key[0])
                flag = 1
                input_wakeuptime_into_redis(key[0], redis_key)
        if tb_name == "thread_create_count":
            res = read_thread_create_count_from_db(influx_client, tb_name, date_time, rows, page)
            for key in zip(res):
                flag = 1
                input_thread_create_count_into_redis(key[0], redis_key)
        if tb_name == "core_dispacher_times":
            res = read_sched_count_from_db(influx_client, tb_name, date_time, rows, page)
            for key in zip(res):
                flag = 1 
                # print(key[0])
                input_sched_count_into_redis(key[0], redis_key)
        if tb_name == "runqueue_lentacy":
            res = read_queue_lantency_from_db(influx_client, tb_name, date_time, rows, page)
            for key in zip(res):
                flag = 1
                # print(key[0])
                input_queue_lantency_into_redis(key[0], redis_key)
        if tb_name == "queue_length":
            res = read_queue_length_from_db(influx_client, tb_name, date_time, rows, page)
            for key in zip(res):
                flag = 1
                # print(key[0])
                input_queue_length_into_redis(key[0], redis_key)
        if flag == 0:
            sleep(1)
            no_data_count -= 1
        if flag == 1:
            page+=1
            flag = 0   
        if rows == -1:
            break 
        sleep(interval)

def input_sched_count_into_redis(data, key):
    print(data)
    for k in data:
        _0 = "cpu_0_"+str(k["cpu_0"])
        _1 = "cpu_1_"+str(k["cpu_1"])
        _2 = "cpu_2_"+str(k["cpu_2"])
        _3 = "cpu_3_"+str(k["cpu_3"])
        redis_lset(key, _0)
        redis_lset(key, _1)
        redis_lset(key, _2)
        redis_lset(key, _3)
        print("name:",key, _0, _1, _2, _3)

def input_queue_lantency_into_redis(data, key):
    print(data)
    for k in data:
        _0 = "cpu_0_"+str(k["cpu_0"])
        _1 = "cpu_1_"+str(k["cpu_1"])
        _2 = "cpu_2_"+str(k["cpu_2"])
        _3 = "cpu_3_"+str(k["cpu_3"])
        redis_lset(key, _0)
        redis_lset(key, _1)
        redis_lset(key, _2)
        redis_lset(key, _3)
        print("name:",key, _0, _1, _2, _3)

def input_thread_create_count_into_redis(data, key):
    print(data)
    for k in data:
        print(k)
        tmp =""
        tmp = k["process_name"]+"_"+str(k["count"])
        redis_lset(key, tmp)

def input_queue_length_into_redis(data, key):
    print(data)
    for k in data:
        _0 = "cpu_0_"+str(k["cpu_0"])
        _1 = "cpu_1_"+str(k["cpu_1"])
        _2 = "cpu_2_"+str(k["cpu_2"])
        _3 = "cpu_3_"+str(k["cpu_3"])
        redis_lset(key, _0)
        redis_lset(key, _1)
        redis_lset(key, _2)
        redis_lset(key, _3)
        print("name:",key, _0, _1, _2, _3)
#type data is list
def input_wakeuptime_into_redis(data, key):
    print(data)
    for k in data:
        print(k)
        tmp = ""
        tmp = k["process_name"]+"_"+str(k["lantency"])
        redis_lset(key, tmp)
