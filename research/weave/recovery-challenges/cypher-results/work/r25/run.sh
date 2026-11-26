#!/bin/bash
# Round 25 (Nov 25 daily): XCCC t=5 planted negatives (near1, near8, rand) + full planted recovery/uniqueness (pos) on seed 3 (kissat404). SIGKILL cap 7200 s, 4 parallel.
cd /workspace/cypher/work/r25
date > started.txt
xargs -P 4 -L 1 bash -c 'nice -n 5 timeout -s KILL 7200 python3 kport3.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
