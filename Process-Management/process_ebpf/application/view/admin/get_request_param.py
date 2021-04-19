from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for,session,make_response
from flask_marshmallow import Marshmallow
from flask import request
from application.service.thread_pool import pool
from application.service.produce import send_message
from application.service.process_param_list import process_param_map
from application.service.get_data_from_db import get_info_from_db, read_from_redis
from datetime import datetime
from application.service.random import get_random
from time import sleep
req_proc_view = Blueprint('admin_index', __name__, url_prefix='/admin/')
ma = Marshmallow()
time = datetime.now().isoformat()
msg = {}
def print_hello(tb_name, date_time, rows):
    print(tb_name, date_time, rows)
    while True:
        sleep(1)
        print("hello world")

# {'time': '2021-04-14T13:53:40.095582Z', 'glob': 'glob', 'lantency': 72, 'process_name': 'dbus-daemon'}
# {"indicator": ["thread_create_count", "wakeuptime", "dispatch_count", "runqueue_latency"],
# "time":"", time之后的指标数据 
# "rows":,  #一次分页获取多少行
# "interval":,  前端多长时间获取一次
# "cookie_value":  用户的标识，避免同一个用户进行重复操作
# }

@req_proc_view.route("/get_req_param", methods =['GET', 'POST'])
def get_request_param():
    msg["user_tag"] = request.remote_addr 
    tmp_list = request.form.getlist("vehicle")
    msg["indicator"] = tmp_list
    print("获取时间信息")
    date = request.form.get("date")
    time = request.form.get("time")
    if date == None or time == None:
        return "time is None"
    date_time = date+" "+time
    return
    msg["time"] = date_time
    msg["rows"] = 10
    msg["interval"] = 5 #刷新的时间
    msg["exec_time_length"]
    # pool.submit(send_message, msg)
    return render_template("/admin/proc_wakeuptime.html")      
          
@req_proc_view.route("/wakeup_lantency")
def update_wakeuptime_data():
    name = []
    lan = []
    redis_key = "wakeup_time"
    res_list = read_from_redis(redis_key, 10)
    for k in res_list:
        value = k[1].decode("utf-8")
        index = value.rfind("_")
        proc_name = value[:index-1]
        lantency = int(value[index+1:])
        name.append(proc_name)
        lan.append(round(lantency/1000*1.0,4))
    return jsonify({"process_name":name, "lantency":lan})

@req_proc_view.route("/thread_count_data")
def update_thread_count_data():
    name = []
    count = []
    user_tag = request.remote_addr
    redis_key = "thread_create_count@"+user_tag
    res_list = read_from_redis(redis_key, 10)
    for k in res_list:
        value = k[1].decode("utf-8")
        index = value.rfind("_")
        proc_name = value[:index-1]
        thread_coount = value[index+1:]
        name.append(proc_name)
        count.append(thread_coount)
    return jsonify({"process_name":name, "count": count})