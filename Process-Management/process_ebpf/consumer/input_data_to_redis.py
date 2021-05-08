from get_data_from_db import get_info_from_db
need_delete_tb_name_list = {}

def input_data_into_redis(delete_key, key, date_time, rows, interval, user_tag):
    if key == "wakeuptime":
        tb_name = "proc_wakeuptime"
    if key == "thread_create_count":
        tb_name = "thread_create_count"
    if key == "dispatch_count":
        tb_name = "core_dispacher_times"
    if key == "runqueue_latency":
        tb_name = "runqueue_lentacy"
    if key == "runqueue_length":
        tb_name = "queue_length"
    redis_key = tb_name+"@"+user_tag
    need_delete_tb_name_list[tb_name] = 1
    get_info_from_db(delete_key, tb_name, date_time, rows, interval, redis_key)          