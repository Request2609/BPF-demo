from bcc import BPF

bpf_source ="""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
int trace_go_main(struct pt_regs* ctx) {
	u64 pid = bpf_get_current_pid_tgid();
	bpf_trace_printk("hello-bpf:%d\\n", pid);
	return 0;
}
"""
bpf = BPF(text=bpf_source)

bpf.attach_uprobe(name="/home/changke/BPF-demo/Process-Management/tmp/test", sym="main.greet",fn_name="trace_go_main")

bpf.trace_print()