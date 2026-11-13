#!/bin/bash
cd /workspace/cypher/work/r13
for a in "XCC 3 7" "XCC 7 3" "XCC 5 2" "XCCC 3 7" "XCCC 5 1" "XCCC 7 3"; do
  echo "$a"
done | xargs -P 3 -L 1 bash -c 'timeout 900 python3 test_synth2.py $0 $1 $2 || echo "$0 $1 $2 timeout900"' >> /workspace/cypher/work/r15/synth.log 2>>/workspace/cypher/work/r15/synth.err
echo DONE >> /workspace/cypher/work/r15/synth.log
