#!/bin/bash
# Round 22 (pre-reset Nov 23): XCCC planted negatives + t=5 truth admission. SIGKILL cap 4200 s, exit codes recorded.
cd /workspace/cypher/work/r22
xargs -P 4 -L 1 bash -c 'nice -n 5 timeout -s KILL 4200 python3 kport.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
