#!/usr/bin/python
#encoding: utf-8
from influxdb import InfluxDBClient
from config import cfg
import redis
from config import REDIS_HOST
from config import REDIS_PORT
from config import REDIS_NUM

DB_HOST = cfg["influxdb"]["host"]
DBNAME = cfg["influxdb"]["dbname"]
USER = cfg["influxdb"]["user"]
PASSWORD = cfg["influxdb"]["password"]

influx_client = InfluxDBClient(database=DBNAME,host=DB_HOST,username=USER,password=PASSWORD)
redis_client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db=REDIS_NUM)
