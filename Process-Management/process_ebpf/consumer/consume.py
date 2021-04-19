#!/usr/bin/python
#encoding: utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
from thread_pool import pool
from plugin_factory import factroy,plugin
from config import read_config,queue_Info,indicator
from filter import fileter_indicator 
from db_modules import delete_tb_data
from input_data_to_redis import need_delete_tb_name_list, input_data_into_redis

import signal
import json
cfg = read_config()

MQ_HOST = cfg["rabbitmq"]["host"]
MQ_PORT = cfg["rabbitmq"]["port"]
MQ_USER = cfg["rabbitmq"]["user"]
MQ_PASSWORD = cfg["rabbitmq"]["password"]
MQ_QUEUE_NAME = cfg["rabbitmq"]["mq_name"]
MQ_V_HOST = cfg["rabbitmq"]["v_host"]
INTERVAL_DAY = cfg["clear_data"]["interval_day"]
CHECK_INTERVAL = cfg["clear_data"]["check_interval"]
credentials = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host = MQ_HOST, port =MQ_PORT, virtual_host = MQ_V_HOST,credentials = credentials))
channel = connection.channel()

# 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
channel.queue_declare(queue = MQ_QUEUE_NAME, durable = False)
def call_plugin(obj):
    print(type(obj))
    obj.start_func()
# {"indicator": ["thread_create_count", "wakeuptime", "dispatch_count", "runqueue_latency"],
# "time":"", time之后的指标数据 
# "rows":,  #一次分页获取多少行
# "interval":,  前端多长时间获取一次
# "user_tag":  用户的标识，避免同一个用户进行重复操作
# }
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    param = body.decode("utf-8")
    param_map=json.loads(param)
    user_tag = param_map["user_tag"]
    indicator_list = fileter_indicator(param_map["indicator"], user_tag)
    date_time = param_map["time"]    
    interval = param_map["interval"]
    rows = param_map["rows"]
    fac = factroy()
    for key in indicator_list:
        # plugin = fac.get_plugin(indicator[key].value)
        # pool.submit(plugin.start_func)
        pool.submit(input_data_into_redis, key, date_time, rows, interval, user_tag)

#清理数据
def clear_data():
    while True:
        tmp_map = need_delete_tb_name_list
        for tb_name in need_delete_tb_name_list:
            day_ago = (datetime.datetime.now() - datetime.timedelta(days = INTERVAL_DAY))
            date_time = day_ago.strftime("%Y-%m-%d %H:%M:%S")
            query_str = "delete from "+tb_name+"  where time<'"+date_time+"'"
            delete_tb_data(tb_name, query_str)
        sleep(CHECK_INTERVAL*60)

# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    connection.close()
    
def get_message():
    # pool.submit(clear_data)#启动清理数据线程
    # 告诉rabbitmq，用callback来接收消息
    channel.basic_consume(MQ_QUEUE_NAME,callback)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()

if __name__=="__main__":
    print("consumer start")
    # 设置相应信号处理的handler
    signal.signal(signal.SIGINT, my_handler)
    signal.signal(signal.SIGHUP, my_handler)
    signal.signal(signal.SIGTERM, my_handler)

    get_message()