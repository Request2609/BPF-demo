from datetime import datetime
import time

#获取前external秒的时间
def get_time(external):
    # print(type(datetime.now().isoformat()))
    # print(datetime.now().isoformat())
    t=time.localtime(time.time() - external)
    return t
    # print(time.strftime("%Y-%m-%d %H:%M:%S", t))