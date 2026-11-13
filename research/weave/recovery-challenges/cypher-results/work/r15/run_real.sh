#!/bin/bash
# usage: run_real.sh ARGSFILE OUTFILE TIMEOUT PAR
# (fixed Nov 12: first version lost the file arg to $0; its output is kept as *_INVALID_argbug*)
cd /workspace/cypher/work/r13
xargs -P $4 -L 1 bash -c 'timeout '"$3"' python3 run_one.py "$@" 2>>/workspace/cypher/work/r15/real.err || echo "{\"file\":\"$1\",\"sched\":\"$2\",\"n\":$3,\"t\":$4,\"rot\":$5,\"ar\":$6,\"status\":\"timeout'"$3"'\"}"' _ < $1 >> $2
echo '{"DONE":1}' >> $2
