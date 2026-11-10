#!/usr/bin/env python3
"""Apply the single-C DP to remaining WLN1 files (m>=3 at C)."""
import json, sys, time
from pathlib import Path
sys.path[:0] = ['/workspace/cypher/work/r12']
import wln_dp as D
import wln_coupled as W

REC = set(Path('/workspace/cypher/work/v2_recovered/RECOVERED_IDS.txt').read_text().split())
OUT = Path('/workspace/cypher/work/r12/run_1c.jsonl')

def remaining():
    files = []
    for f in sorted(Path('/workspace/cypher/v2/blind/files').glob('*.bin')):
        if f.name in REC or f.stem in REC:
            continue
        data = f.read_bytes()
        if data[:4] != b'WLN1':
            continue
        files.append(f)
    return files

def main():
    min_m = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print('precomputing layouts', flush=True)
    by = D.precompute_layouts(D.candidates_1c())
    # filter m
    byf = {}
    for shape, ls in by.items():
        ls = [(c, u, v) for c, u, v in ls if len(u) >= min_m]
        if ls:
            byf[shape] = ls
            print(' shape', shape, 'layouts', len(ls), flush=True)
    files = remaining()
    print('remaining WLN1', len(files), flush=True)
    done = set()
    if OUT.exists():
        for line in OUT.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)['file'])
    n_done = 0
    with OUT.open('a') as out:
        for f in files:
            if f.name in done:
                continue
            data = f.read_bytes()
            st = W.tc.decode_lanes(data)
            wl = [list(l) for l in st.lanes]
            shape = tuple(map(len, wl))
            t0 = time.time()
            res = D.recover_file(wl, byf.get(shape, []))
            rec = {
                'file': f.name, 'shape': list(shape), 'verdict': res['verdict'],
                'msg': res['msg'], 'secs': round(time.time() - t0, 3),
                'nhits': len(res['hits']),
                'hit_status': [h['status'] + ':' + h['sched'] for h in res['hits'][:12]],
            }
            out.write(json.dumps(rec) + '\n')
            out.flush()
            n_done += 1
            if rec['verdict'] != 'none' or n_done % 10 == 0:
                print(json.dumps({k: rec[k] for k in rec if k != 'msg'}), rec.get('msg') and rec['msg'][:43], flush=True)
    print('wrote', n_done, 'new rows to', OUT, flush=True)

if __name__ == '__main__':
    main()
