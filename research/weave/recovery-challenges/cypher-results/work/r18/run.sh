#!/bin/bash
# Round 18: XCCC planted truth-admission / random-negative / full-recovery tests. SIGKILL cap 14400 s (4 h).
cd /workspace/cypher/work/r18
xargs -P 6 -L 1 bash -c 'timeout -s KILL 14400 python3 negpos4.py "$0" "$1" "$2" "$3" "$4" 2>>err.log || echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$4\",\"status\":\"killed14400\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
