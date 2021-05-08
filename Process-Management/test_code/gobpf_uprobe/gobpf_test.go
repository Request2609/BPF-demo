package main

import (
	"os"
	"github.com/iovisor/gobpf/bcc"
)

const bpfProgram = `
#include <uapi/linux/ptrace.h>

BPF_PERF_OUTPUT(trace);

int hack(struct pt_regs *ctx) {
    char text[] = "You are hacked!";
    // read string address
    u64 addr = 0;
    u64* sp = (u64*)ctx->sp;
    bpf_probe_read(&addr, sizeof(addr), sp + 1);
    // overwrite string content
    bpf_probe_write_user((u64*)addr, text, sizeof(text));
    return 0;
}

// This function will be registered to be called everytime
// main.computeE is called.
inline int computeECalled(struct pt_regs *ctx) {
  // The input argument is stored in ax.
  long val = ctx->ax;
  trace.perf_submit(ctx, &val, sizeof(val));
  return 0;
}

`


const (
	bpfFuncName = "hack"
)

func main() {
	bpfModule := bcc.NewModule(bpfProgram, []string{})
	uprobeFD, err := bpfModule.LoadUprobe(bpfFuncName)
	if err != nil {
		panic(err)
	}

	hackedBinary := os.Args[1]
	hackedFuncName := os.Args[2]
	err = bpfModule.AttachUprobe(hackedBinary, hackedFuncName, uprobeFD, -1)
	if err != nil {
		panic(err)
	}

	select {}
}
