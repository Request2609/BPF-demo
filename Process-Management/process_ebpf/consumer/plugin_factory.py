from proc_wakeuptime import gen_wakeup_time
from process_sched_count import gen_dispatch_count
from thread_create_count import gen_count_clone
from runqueue_latency import gen_queue_lentacy
from core4_runqueue_length import gen_runqueue_length

class plugin:
    def __init__(self):
        self.indicator_type = None
        self.func = None
    def get_indicator_type(self):
        return self.indicator_type
    def start_func(self):
        self.func(self.indicator_type)

class runqueue_length(plugin):
    def __init__(self, indicator_type, func):
        self.indicator_type = indicator_type 
        self.func = func
class thread_create_count(plugin):
    def __init__(self, indicator_type, func):
        self.indicator_type = indicator_type 
        self.func = func
class wakeuptime(plugin):
    def __init__(self, indicator_type, func):
        self.indicator_type = indicator_type 
        self.func = func
class dispatch_count(plugin):
    def __init__(self, indicator_type, func):
        self.indicator_type = indicator_type 
        self.func = func

class runqueue_latency(plugin):
    def __init__(self, indicator_type, func):
        self.indicator_type = indicator_type 
        self.func = func

class factroy:
    def get_plugin(self, indicator_type):
        if indicator_type == 1:
            return runqueue_length(1, gen_runqueue_length)
        if indicator_type == 2:
            return thread_create_count(2, gen_count_clone)
        if indicator_type == 3:
            return wakeuptime(3, gen_wakeup_time)
        if indicator_type == 4:
            return dispatch_count(4, gen_dispatch_count)
        if indicator_type == 5:
            return runqueue_latency(5, gen_queue_lentacy)

if __name__ == '__main__':
    fac = factroy()
    tmp = fac.get_plugin(1)
    tmp.start_func()