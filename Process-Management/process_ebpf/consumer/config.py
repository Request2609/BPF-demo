#!/usr/bin/python3
# -*- coding:utf-8 -*-

import yaml
import os
from enum import IntEnum
from enum import Enum, unique


current_path = os.path.abspath(".")
yaml_path = os.path.join(current_path, "config.yaml")

#指标的枚举
@unique
class indicator(Enum):
    runqueue_length = 1
    thread_create_count = 2
    wakeuptime = 3
    dispatch_count = 4
    runqueue_latency = 5

#数据库类型
class DatabaseType(IntEnum):
    INFLUXDB = 1
    ES = 2
    MYSQL = 3
    PROMETHEUS = 4

#队列名称
class queue_Info(Enum):
    mq_name = "proc_info_param"


def read_config():
    with open(yaml_path,'r') as stream:
        cfg =yaml.load(stream,Loader=yaml.FullLoader)
    return cfg

cfg = read_config()
