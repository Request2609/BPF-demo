#!/usr/bin/python
#encoding: utf-8
from influxdb import InfluxDBClient
import redis
from config import cfg

DBNAME = cfg["influxdb"]["dbname"]
USER = cfg["influxdb"]["user"]
PASSWORD = cfg["influxdb"]["password"]
REDIS_HOST = cfg["redis-cli"]["host"]
REDIS_PORT = cfg["redis-cli"]["port"]
REDIS_NUM = cfg["redis-cli"]["db_num"]

influx_client = InfluxDBClient(database=DBNAME,host='localhost',username=USER,password=PASSWORD)
redis_client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db=REDIS_NUM)
# TODO: 接入其他数据库
# mysql_client
# es_client
# prometheus_client
