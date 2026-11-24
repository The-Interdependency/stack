#!/bin/bash
# Round 24 (Nov 24 daily): XCCC t=5 truth admission on new planted seeds 2-4 (kissat404) + seed 1 with cadical195. SIGKILL cap 7200 s, 4 parallel.
cd /workspace/cypher/work/r24
date > started.txt
xargs -P 4 -L 1 bash -c 'nice -n 5 timeout -s KILL 7200 python3 kport3.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
