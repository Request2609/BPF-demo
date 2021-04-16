from application.service.get_compare_time import get_time
from application.db_module.init_db import influx_client
from application.db_module.db_modules import redis_lset, redis_lget, read_from_db
def get_info_from_db(tb_name, external):
    t = get_time(external)
    ls = []
    if tb_name == "wakeuptime":
        res = read_from_db(influx_client,"proc_wakeuptime", t, 10)
        for key in zip(res) :
            return key[0]
    return ls
#type data is list
def input_wakeuptime_into_redis(data):
    for k in data:
        tmp = ""
        tmp = k["process_name"]+"_"+str(k["lantency"])
        redis_lset("wakeup_time", tmp)

def read_wakeuptime_from_redis(key, count):
    res_list = redis_lget(key, count)
    