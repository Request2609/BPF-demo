#!/usr/bin/python
#
# bashreadline  Print entered bash commands from all running shells.
#               For Linux, uses BCC, eBPF. Embedded C.
#
# This works by tracing the readline() function using a uretprobe (uprobes).
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 28-Jan-2016    Brendan Gregg   Created this.
# 12-Feb-2016    Allan McAleavy migrated to BPF_PERF_OUTPUT

from __future__ import print_function
from bcc import BPF
from time import strftime
import ctypes as ct

# load BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>

struct str_t {
    u64 pid;
    char str[80];
    u64 arg ;
};

BPF_PERF_OUTPUT(events);

int printret(struct pt_regs *ctx) {
    struct str_t data  = {};
    u32 pid;
    if (!PT_REGS_RC(ctx))
        return 0;
    pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    bpf_probe_read(&data.str, sizeof(data.str), (void *)PT_REGS_RC(ctx));
    events.perf_submit(ctx,&data,sizeof(data));

    return 0;
};

// This function will be registered to be called everytime
// main.computeE is called.
inline int test_func_trace(struct pt_regs *ctx) {
    struct str_t data  = {};
  // The input argument is stored in ax.
    u32 pid;
    if (!PT_REGS_RC(ctx))
        return 0;
    pid = bpf_get_current_pid_tgid();
    data.pid = pid ;
    data.arg = ctx->ax;
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""
STR_DATA = 80

class Data(ct.Structure):
    _fields_ = [
        ("pid", ct.c_ulonglong),
        ("str", ct.c_char * STR_DATA),
        ("arg", ct.c_ulonglong)
    ]

b = BPF(text=bpf_text)
b.attach_uretprobe(name="./test", sym="test_func", fn_name="test_func_trace")

# header
print("%-9s %-6s %s" % ("TIME", "PID", "COMMAND"))

def print_event(cpu, data, size):
    event = ct.cast(data, ct.POINTER(Data)).contents
    print("%-6d %-6d" % (event.arg, event.pid))

b["events"].open_perf_buffer(print_event)
while 1:
    b.kprobe_poll()