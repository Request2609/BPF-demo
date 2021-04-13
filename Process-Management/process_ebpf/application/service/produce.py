#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
import json

from config import MQ_HOST
from config import MQ_PASSWORD
from config import MQ_PORT
from config import MQ_QUEUE_NAME
from config import MQ_USER
from config import MQ_V_HOST

credentials = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)  # mq用户名和密码
# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST,MQ_PORT,MQ_V_HOST, credentials = credentials))
channel=connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建
result = channel.queue_declare(MQ_QUEUE_NAME)

for i in range(10):
    message=json.dumps({'OrderId':"1000%s"%i})
# 向队列插入数值 routing_key是队列名
    channel.basic_publish(exchange = '',routing_key = MQ_QUEUE_NAME,body = message)
    print(message)
connection.close()