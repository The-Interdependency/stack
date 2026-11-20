#!/bin/bash
# Round 21: real XCCC x kissat404, t=7 first. SIGKILL cap 1800 s, 3 parallel, nice 10. Exit codes recorded.
cd /workspace/cypher/work/r21
sort -k4,4nr ../r15/xccc_args.txt > real_args.txt
xargs -P 3 -L 1 bash -c 'nice -n 10 timeout -s KILL 1800 python3 real_k.py "$0" "$1" "$2" "$3" "$4" "$5" 2>>real.err; rc=$?; [ $rc -ne 0 ] && echo "{\"file\":\"$0\",\"sched\":\"$1\",\"t\":$3,\"status\":\"exit$rc\"}"' < real_args.txt >> real.jsonl
echo '{"DONE":1}' >> real.jsonl
