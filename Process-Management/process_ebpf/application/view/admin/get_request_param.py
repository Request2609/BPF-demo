from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for,session
from flask_marshmallow import Marshmallow
from flask import request
from application.service.thread_pool import pool
from application.service.produce import send_message
from application.service.process_param_list import process_param_map
from application.service.get_data_from_db import get_info_from_db
req_proc_view = Blueprint('admin_index', __name__, url_prefix='/admin/')
ma = Marshmallow()
time = datetime.now().isoformat()
# {'time': '2021-04-14T13:53:40.095582Z', 'glob': 'glob', 'lantency': 72, 'process_name': 'dbus-daemon'}
@req_proc_view.route("/get_req_param", methods =['GET', 'POST'])
def get_request_param():
    return render_template("/admin/proc_wakeuptime.html")

@req_proc_view.route("/wakeup_lantency")
def update_data():
    # req_list = request.form.getlist("vehicle")
    data_list = get_info_from_db("wakeuptime", 300000)
    name = []
    lan = []
    tmp_time = datetime.now().isoformat()
    for k in data_list:
        name.append(k['process_name'])
        lan.append(k['lantency'])
        tmp_time = k['time']
    time = tmp_time
    #线程池给消息队列发送指令执行插件
    # pool.submit(send_message,process_param_map(req_list))
    return jsonify({"process_name":name, "lantency":lan})
    