#!/bin/bash
# Round 25b: pos rerun with cadical195 (kissat404 aborts on add_clause after solve, exit134).
cd /workspace/cypher/work/r25
date > started2.txt
xargs -P 4 -L 1 bash -c 'nice -n 5 timeout -s KILL 7200 python3 kport3.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\"}"' < args2.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
