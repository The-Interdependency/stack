#!/bin/bash
cd /workspace/cypher/work/r13
timeout 600 python3 run_one.py "$@" 2>>/workspace/cypher/work/r14/err.log || echo "{\"file\":\"$1\",\"sched\":\"$2\",\"n\":$3,\"t\":$4,\"rot\":$5,\"ar\":$6,\"status\":\"timeout600\"}"
