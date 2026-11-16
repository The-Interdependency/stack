import sys, json
sys.path[:0] = ['/workspace/cypher/work/r10']
import wln_coupled as W
j = json.load(open('/workspace/cypher/work/r17/SOURCE_REPLAY_VECTORS.978951d.json'))
for v in j['vectors']:
    if v['family'] != 'transport': continue
    p = v['parameters']
    wire = W.tc.run(bytes.fromhex(v['input_hex']), list(v['schedule']), p)
    print(json.dumps({'schedule': ''.join(v['schedule']), 'forward_matches_vector': wire.hex() == v['wire_hex'], 'wire_len': len(wire)}))
