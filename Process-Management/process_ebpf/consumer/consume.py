#!/usr/bin/python
#encoding: utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
from thread_pool import pool
from plugin_factory import factroy
from plugin_factory import plugin
from config import read_config
from config import queue_Info
from config import indicator
import signal
import json
cfg = read_config()

MQ_HOST = cfg["rabbitmq"]["host"]
MQ_PORT = cfg["rabbitmq"]["port"]
MQ_USER = cfg["rabbitmq"]["user"]
MQ_PASSWORD = cfg["rabbitmq"]["password"]
MQ_QUEUE_NAME = cfg["rabbitmq"]["mq_name"]
MQ_V_HOST = cfg["rabbitmq"]["v_host"]


credentials = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host = MQ_HOST, port =MQ_PORT, virtual_host = MQ_V_HOST,credentials = credentials))
channel = connection.channel()

# 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
channel.queue_declare(queue = MQ_QUEUE_NAME, durable = False)
def call_plugin(obj):
    print(type(obj))
    obj.start_func()

# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    print("消费者开始获取消息")
    #{"indicator": ["thread_create_count", "wakeuptime", "dispatch_count", "runqueue_latency"]}
    ch.basic_ack(delivery_tag = method.delivery_tag)
    param = body.decode("utf-8")
    param_map=json.loads(param)
    print(param_map)
    indicator_list = param_map["indicator"]    
    fac = factroy()
    for key in indicator_list:     
        print(indicator[key].value)
        plugin = fac.get_plugin(indicator[key].value)
        pool.submit(plugin.start_func)
# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    connection.close()
    
def get_message():
    # 告诉rabbitmq，用callback来接收消息
    channel.basic_consume(MQ_QUEUE_NAME,callback)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()

if __name__=="__main__":

    # 设置相应信号处理的handler
    signal.signal(signal.SIGINT, my_handler)
    signal.signal(signal.SIGHUP, my_handler)
    signal.signal(signal.SIGTERM, my_handler)

    get_message()