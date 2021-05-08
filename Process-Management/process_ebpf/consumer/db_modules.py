#! /usr/bin/python3
# -*- coding:utf-8 -*-
from config import DatabaseType
from influxdb import InfluxDBClient
from config import cfg
from init_db import redis_client

def write2db(datatype, data, client, dbtype):
    """
    :param datatype: 数据类型
    :param data: 数`据
    :param client: 数据库client
    :param dbtype: 数据库类型
    """
    if dbtype == DatabaseType.INFLUXDB.value:
        tmp = [{"measurement": None, "tags": {}, "fields": {}, }]
        tmp[0]["measurement"] = datatype["measurement"]
        for x in datatype['tags']:
            tmp[0]["tags"][x] = getattr(data, x)
        for y in datatype['fields']:
            tmp[0]["fields"][y] = getattr(data, y)
        client.write_points(tmp)
    elif dbtype == DatabaseType.ES.value:
        pass
    elif dbtype == DatabaseType.MYSQL.value:
        pass
    elif dbtype == DatabaseType.PROMETHEUS.value:
        pass

def read_wakeuptime_from_db(influx_client, tb_name, time, rows, page):
    # print("表信息:",tb_name, time, rows, page)
    if rows == -1:
        query_str = "select process_name, lantency from "+tb_name+" where time >='"+time+"'"
    else:
        offset = (page-1)*rows
        query_str = "select process_name, lantency from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)+" offset "+str(offset)
    res_list = influx_client.query(query_str)
    return res_list

def read_thread_create_count_from_db(influx_client, tb_name, time, rows, page):
    # print("表信息:",tb_name, time, rows, page)
    if rows == -1:
        query_str = "select process_name, count from "+tb_name+" where time >='"+time+"'"
    else:
        offset = (page-1)*rows
        query_str = "select process_name, count from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)+" offset "+str(offset)
    res_list = influx_client.query(query_str)
    return res_list

def read_sched_count_from_db(influx_client, tb_name, time, rows, page):
    if rows == -1:
        query_str = "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'"
    else:
        offset = (page-1)* rows
        query_str =  "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)+" offset "+str(offset)
    res_list = influx_client.query(query_str)
    return res_list

def read_queue_lantency_from_db(influx_client, tb_name, time, rows, page):
    if rows == -1:
        query_str = "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'"
    else:
        offset = (page-1)* rows
        query_str =  "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)+" offset "+str(offset)
    res_list = influx_client.query(query_str)
    return res_list

def read_queue_length_from_db(influx_client, tb_name, time, rows, page):
    # print("表信息:",tb_name, time, rows, page)
    if rows == -1:
        query_str = "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'"
    else:
        offset = (page-1)* rows
        query_str =  "select cpu_0, cpu_1, cpu_2, cpu_3 from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)+" offset "+str(offset)
    res_list = influx_client.query(query_str)
    return res_list

def delete_tb_data(query_str):
    client.query(query_str)

def redis_lset(key, value):
    for val in value:
        redis_client.lpush(key,value)

def delete_a_key(redis_key):
    return redis_client.delete(redis_key)
