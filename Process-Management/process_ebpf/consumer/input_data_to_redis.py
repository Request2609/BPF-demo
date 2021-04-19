from get_data_from_db import get_info_from_db
need_delete_tb_name_list = {}
def input_data_into_redis(key, date_time, rows, interval, user_tag):
    tb_name = "thread_create_count"
    if key == "wakeuptime":
        tb_name = "proc_wakeuptime"
    elif key == "thread_create_count":
        tb_name = "thread_create_count"
    elif key == "dispatch_count":
        tb_name = "core_dispacher_times"
    elif tb_name == "runqueue_latency":
        tb_name = "queue_length"
    else :
        tb_name == "proc_wakeuptime"
    redis_key = tb_name+"@"+user_tag
    print("redis_key:",redis_key, "tb_name:",tb_name)
    need_delete_tb_name_list[tb_name] = 1
    get_info_from_db(tb_name, date_time, rows, interval, redis_key)