#!/usr/bin/python
#encoding: utf-8
from bcc import BPF
from time import sleep
import threading
from collections import Counter
from datetime import datetime
from init_db import influx_client
from db_modules import write2db

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct data_t {
    u64 mmap_area_size ;       //匿名映射区的可用内存大小
    u64 task_size ;            //size of task vm space
    u64 total_vm  ;            //进程目前的实际使用虚拟内存情况
    char comm[TASK_COMM_LEN];   //进程名称
};


BPF_HASH(task_struct_data, u32, struct data_t, 1024);

int get_task_struct_info(struct pt_regs *ctx) {
    struct data_t*data ;
    struct data_t zero = {};
    u32 pid = bpf_get_current_pid_tgid();
    struct task_struct *p = (struct task_struct *) bpf_get_current_task();
    u64 ts;
    data = task_struct_data.lookup_or_init(&pid, &zero);
    data->mmap_area_size = p->mm->mmap_base;
    data->task_size = p->mm->task_size ;
    data->total_vm = p->mm->total_vm ;
    bpf_get_current_comm(&(data->comm), sizeof(data->comm));
    return 0;
}
"""
class lmp_data_cpu_core_4(object):
    def __init__(self, time, glob, mmap_size, stack_size, total_vm, proc_name):
        self.time = time
        self.glob = glob
        self.mmap_size = mmap_size
        self.stack_size = stack_size
        self.total_vm = total_vm 
        self.proc_name = proc_name 

data_struct = {"measurement": 'process_mem_info',
               "time": [],
               "tags": ['glob', ],
               "fields": ['mmap_size', 'stack_size', 'total_vm', 'proc_name']}


b = BPF(text=bpf_text)
b.attach_kprobe(event="schedule", fn_name="get_task_struct_info")
while True:
    tmp = b.get_table("task_struct_data")
    for k, v in tmp.items():
        test_data = lmp_data(datetime.now().isoformat(), 'glob', v.mmap_area_size/1024/1024/1024,v.task_size/1024/1024/1024,v.total_vm/1024,v.comm.decode("utf-8"))
        write2db(data_struct, test_data, influx_client, DatabaseType.INFLUXDB.value)
        print(k.value, v.mmap_area_size/1024/1024/1024, v.task_size/1024/1024/1024, v.total_vm/1024, v.comm.decode("utf-8"))
    sleep(1)
    tmp.clear()

    