"""Check completed replay and its historical/independent census comparisons.
Usage: python verify_evidence.py (after running both replays and timing).
"""
import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).parent

def digest(filename):
    return sha256((ROOT/filename).read_bytes()).hexdigest()

def check(condition,message):
    if not condition:
        raise AssertionError(message)

r=json.loads((ROOT/'evidence.json').read_text())
check(digest('evidence.json')==digest('evidence-replay.json'),'replay mismatch')
for name,key in [('experiment.py','implementation_sha256'),('PROTOCOL.md','protocol_sha256'),('PROTOCOL_ADDENDUM.md','addendum_sha256')]:
    check(digest(name)==r[key],f'source drift: {name}')
check(r['geometry']['cube_mismatch_count']==0,'full circle mismatch')
check(r['cryptographic_security']=='NOT_TESTED','invalid status transfer')
check(r['prime_census']['limit_inclusive']==60_000_000,'wrong census limit')
check(r['prime_census']['excluded_crossing_pairs']==1,'crossing count')
check(r['prime_census']['crossing_witnesses'][0]['primes']==[29999999,30000001],'crossing pair identity')
check(r['prime_census']['crossing_witnesses'][0]['formula_agrees'],'crossing formula')
expected=[('first_interval',152890,5646,[9239941,5797009,1355131]),('next_interval',127666,4721,[43736521,37818091,32349619])]
for label,twins,eligible,last in expected:
    p=r['prime_census'][label]
    check(p['twin_pairs']==twins and p['eligible_pairs']==eligible,f'{label} independent census counts')
    check(p['spokes']=={'original':6561,'eligible_input':243,'output':81},f'{label} observed spokes')
    check([p['upper_prime_last_new_spoke'][k] for k in ('original','eligible_input','output')]==last,f'{label} saturation points')
    check(p['direct_cube_mismatches']==0,f'{label} cube mismatch')
    rows=p['all_output_families']
    check([x['output_spoke'] for x in rows]==list(range(0,19683,243)),f'{label} wheel positions')
    check(all(len(x['family_counts'])==3 and min(x['family_counts'])>0 and sum(x['family_counts'])==x['total'] for x in rows),f'{label} family completeness')
    check(sum(x['total'] for x in rows)==eligible,f'{label} census accounting')
    check(all(x['colliding_classes']>0 for x in p['ordinal_labels'].values()),f'{label} ordinal classification')
check(next(x for x in r['prime_census']['next_interval']['all_output_families'] if x['output_spoke']==5589)['family_counts']==[10,30,23],'independent imbalance witness')
check(next(x for x in r['prime_census']['next_interval']['all_output_families'] if x['output_spoke']==11178)['family_counts']==[25,26,19],'independent brightness witness')
t=json.loads((ROOT/'timing.json').read_text())
check([x['exponent'] for x in t['rows']]==[5,7,9,11,13,15],'timing scope')
for x in t['rows']:
    check(len(x['nine_runs_ns'])==9 and x['median_ns']>0,'timing repetitions')
    check(x['classes']*3==x['objects'],'scale class count')
print('PASS: source hashes, byte-identical replay, full finite carrier, both census windows, crossing witness, all 243 families, ordinal collision scope, scaling scope, non-security status.')
print('Evidence SHA-256:',digest('evidence.json'))
