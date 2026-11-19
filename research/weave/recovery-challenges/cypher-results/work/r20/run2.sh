#!/bin/bash
# Round 20b: kissat404 + cryptosat on XCCC truth t=7 seed 4. SIGKILL cap 7200 s. Records exit code so crashes are not logged as timeouts.
cd /workspace/cypher/work/r20
xargs -P 2 -L 1 bash -c 'timeout -s KILL 7200 python3 portfolio2.py "$0" "$1" "$2" "$3" "$4" "$5" 2>>err2.log; rc=$?; [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$4\",\"solver\":\"$5\",\"status\":\"exit$rc\"}"' < args2.txt >> out2.jsonl
echo '{"DONE":1}' >> out2.jsonl
