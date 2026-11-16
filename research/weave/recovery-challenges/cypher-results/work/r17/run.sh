#!/bin/bash
# Round 17: planted negative + truth-admission tests for the XCC SAT encoding. SIGKILL cap 900 s.
cd /workspace/cypher/work/r17
xargs -P 6 -L 1 bash -c 'timeout -s KILL 900 python3 negpos.py "$0" "$1" "$2" 880 2>>err.log || echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"status\":\"killed900\"}"' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
