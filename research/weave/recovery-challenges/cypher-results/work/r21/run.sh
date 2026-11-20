#!/bin/bash
# Round 21: kissat404 planted XCCC batch. SIGKILL cap 3600 s. Exit code recorded so crashes are not mislabelled.
cd /workspace/cypher/work/r21
xargs -P 4 -L 1 bash -c 'timeout -s KILL 3600 python3 kport.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
