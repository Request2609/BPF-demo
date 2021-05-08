#!/usr/bin/python
#encoding: utf-8
from bcc import BPF

text_prog = """
#include <uapi/linux/ptrace.h>

BPF_HASH(start, u32);
BPF_HASH(data, u32, u64);

int trace_func_entry(){
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid ;
    u32 tgid = pid_tgid>>32 ;
    u64 ts = bpf_ktime_get_ns() ;
    start.update(&pid, &ts);
    return 0 ;
}

int trace_func_end(){
    u64* tsp,  delta ;
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid;
    u32 tgid = pid_tgid>>32 ;

    tsp = start.lookup(&pid) ;
    if (tsp == 0){
        return 0 ;
    }
    delta = bpf_ktime_get_ns()-*tsp ;
    start.delete(&pid) ;
    data.update(&pid, &delta) ;
    return 0 ;
}
"""
b = BPF(text = text_prog)

b.attach_kprobe(event="_exit", fn_name="trace_func_entry")
b.attach_kretprobe(event="_exit", fn_name="trace_func_end")

while True:
    delta = b.get_table("data")
    for k, v in delta:
        print(k.value, v.value)

