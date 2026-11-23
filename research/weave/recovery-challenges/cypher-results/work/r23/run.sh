#!/bin/bash
# Round 23 (Nov 23 daily): XCCC t=7 seed 3 near-miss (1 and 8 flipped wire bits) + random-wire negatives. SIGKILL cap 2400 s.
cd /workspace/cypher/work/r23
date > started.txt
xargs -P 3 -L 1 bash -c 'nice -n 5 timeout -s KILL 2400 python3 kport3.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
