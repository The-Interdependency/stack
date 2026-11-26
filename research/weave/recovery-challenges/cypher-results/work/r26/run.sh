#!/bin/bash
# Round 26 (Nov 26 daily): retry the two unresolved r25 jobs, one each, 2 parallel, SIGKILL cap 14400 s,
# with per-job start/end epoch stamps so a kill can be attributed to the cap vs. an outside event.
cd /workspace/cypher/work/r26
date > started.txt
xargs -P 2 -L 1 bash -c 's=$(date +%s); nice -n 5 timeout -s KILL 14400 python3 kport3.py "$0" "$1" "$2" "$3" "$4" 2>>err.log; rc=$?; e=$(date +%s); [ $rc -ne 0 ] && echo "{\"mode\":\"$0\",\"t\":$1,\"seed\":$2,\"sched\":\"$3\",\"solver\":\"$4\",\"status\":\"exit$rc\",\"start\":$s,\"end\":$e}"; echo "{\"stamp\":\"$0 $4\",\"start\":$s,\"end\":$e,\"rc\":$rc}" >> stamps.jsonl' < args.txt >> out.jsonl
echo '{"DONE":1}' >> out.jsonl
