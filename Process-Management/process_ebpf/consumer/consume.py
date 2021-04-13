#!/usr/bin/python
#encoding: utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
from thread_pool import pool
from config import queue_Info
from config import cfg
from config import indicator
from plugin_factory import factroy
from plugin_factory import plugin

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
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    param = body.decode("utf-8")
    fac = factroy()
    plugin = fac.get_plugin(param)
    if indicator[param] == 1:

    elif(indicator[param]) == 2:

    elif(indicator[param] == 3):

    elif(indicator[param] == 4):
    
    else:

    

def get_message():
    # 告诉rabbitmq，用callback来接收消息
    channel.basic_consume(MQ_QUEUE_NAME,callback)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()

if __name__=="__main__":
    get_message()