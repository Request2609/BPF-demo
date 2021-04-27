
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return str(days)+":"+str(hours)+":"+str(minutes)+":"+str(seconds)
# start_time = datetime.datetime.now()
# sleep(1) #可以改成需要计算时间的目标程序
# end_time = datetime.datetime.now()
# print("时间：", convert_timedelta(end_time-start_time))
