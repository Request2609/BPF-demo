#! /usr/bin/python3
# -*- coding:utf-8 -*-
from config import DatabaseType
from influxdb import InfluxDBClient
from config import cfg
from application.db_module.init_db import redis_client
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

def read_from_db(client, tb_name, time, rows):
    if rows == -1:
        query_str = "select process_name, lantency from "+tb_name+" where time >='"+time+"'"
    else:
        query_str = "select process_name, lantency from "+tb_name+" where time >='"+time+"'  "+"limit "+str(rows)
    res_list = client.query(query_str)
    return res_list

def redis_lset(key, value):
    for val in value:
        redis_client.lpush(key,value)
    
def redis_lget(key, count):
    res_list = []
    for i in range count:
        res_list.append(redis_client.blpop(key))
    return res_list