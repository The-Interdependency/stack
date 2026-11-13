#!/bin/bash
# usage: run_real_kill.sh ARGSFILE OUTFILE TIMEOUT PAR
# Like r15/run_real.sh but uses SIGKILL: SIGTERM did not stop CaDiCaL inside Python in Round 15
cd /workspace/cypher/work/r13
xargs -P $4 -L 1 bash -c 'timeout -s KILL '"$3"' python3 run_one.py "$@" 2>>/workspace/cypher/work/r16/real.err || echo "{\"file\":\"$1\",\"sched\":\"$2\",\"n\":$3,\"t\":$4,\"rot\":$5,\"ar\":$6,\"status\":\"killed'"$3"'\"}"' _ < $1 >> $2
echo '{"DONE":1}' >> $2
