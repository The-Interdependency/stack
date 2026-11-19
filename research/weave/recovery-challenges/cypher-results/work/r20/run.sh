#!/bin/bash
# Round 20: XCCC truth-admission solver portfolio (planted only). SIGKILL cap 7200 s (2 h). Control: XCC t=7 seed 1 (CaDiCaL SAT in seconds in r17).
cd /workspace/cypher/work/r20
xargs -P 7 -L 1 bash -c 'timeout -s KILL 7200 python3 portfolio.py "$0" "$1" "$2" "$3" "$4" "$5" 2>>err.log || echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$4\",\"solver\":\"$5\",\"status\":\"killed7200\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
