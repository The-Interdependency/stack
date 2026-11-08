#!/usr/bin/env python3
import sys, json, zipfile
from pathlib import Path
from collections import Counter
sys.path.insert(0, '/workspace/cypher/src')
sys.path.insert(0, '/workspace/cypher/v2')
from stages import split, join, inter, whole
from stages.api import Streams, PublicContext
import matrix

KNOWN = 'my human needs my help'
OUT = Path('/workspace/cypher/work/v2_recovered'); OUT.mkdir(exist_ok=True, parents=True)
ZIP = zipfile.ZipFile('/workspace/cypher/v2/blind-pack.zip')
MODS = {'X': split, 'J': join, 'I': inter, 'W': whole}

def bits(data): return tuple((b>>s)&1 for b in data for s in range(7,-1,-1))
def packed(v):
    if len(v)%8: raise ValueError('align')
    return bytes(sum(v[i+k]<<(7-k) for k in range(8)) for i in range(0,len(v),8))

def decode_lanes(data):
    if data[:4]!=b'WLN1' or len(data)<6: raise ValueError
    count=int.from_bytes(data[4:6],'big'); pos=6; lanes=[]
    if not 1<=count<=7: raise ValueError
    for _ in range(count):
        size=int.from_bytes(data[pos:pos+4],'big'); pos+=4
        width=(size+7)//8
        raw=bits(data[pos:pos+width]); pos+=width
        if any(raw[size:]): raise ValueError
        lanes.append(raw[:size])
    if pos!=len(data): raise ValueError
    return Streams(tuple(lanes))

def initial_lengths(size,count):
    q,r=divmod(size,count); return tuple(q+(i<r) for i in range(count))

def build_contexts(size, schedule, initial_lanes, thread_count, lane_rotation, inter_arity):
    lengths=initial_lengths(size, initial_lanes)
    result=[]
    for op in schedule:
        params={}
        if op=='X':
            if len(lengths)!=1: raise ValueError
            owners=split.cyclic_route(size, thread_count)
            params['split']=(thread_count, owners)
            lengths=tuple(owners.count(i) for i in range(thread_count))
        elif op=='J':
            if len(lengths)<3: raise ValueError
            r=lane_rotation%len(lengths)
            order=tuple(range(r,len(lengths)))+tuple(range(r))
            params['join']=(lengths, order)
            lengths=(sum(lengths),)
        elif op=='I':
            params['inter']=tuple(inter.balanced_schedule(n,(inter_arity,)) for n in lengths)
        elif op=='W':
            if len(lengths)!=1: raise ValueError
        else:
            raise ValueError('C unsupported')
        result.append(PublicContext(None, parameters=params))
    return result, lengths

def run_inverse(state, schedule, contexts, size, initial_lanes, final_lengths):
    if tuple(map(len,state.lanes))!=final_lengths: raise ValueError
    for op,ctx in reversed(list(zip(schedule,contexts))):
        state=MODS[op].inverse(state,ctx)
    if tuple(map(len,state.lanes))!=initial_lengths(size,initial_lanes): raise ValueError
    return packed(tuple(b for lane in state.lanes for b in lane))

# C-free accepted transport schedules
acc,_=matrix.transport_schedules()
SCHEDS=[(tuple(s),n) for s,n in acc if 'C' not in s]

def crack(data):
    state=decode_lanes(data)
    size=sum(map(len,state.lanes))
    for sched,initial in SCHEDS:
        tcs=[3,5,7] if 'X' in sched else [0]
        lrs=range(7) if 'J' in sched else [0]
        ias=[3,5,7] if 'I' in sched else [0]
        for tc in tcs:
            for lr in lrs:
                for ia in ias:
                    try:
                        ctxs,final=build_contexts(size,sched,initial,tc,lr,ia)
                        out=run_inverse(state,sched,ctxs,size,initial,final)
                    except Exception:
                        continue
                    try: t=out.decode('utf-8')
                    except: continue
                    if KNOWN in t:
                        return t, {'schedule':list(sched),'initial_lanes':initial,'thread_count':tc,'lane_rotation':lr,'inter_arity':ia}
    return None,None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    names=[n for n in ZIP.namelist() if n.endswith('.bin')]
    new=0; meth=Counter()
    for n in names:
        bid=Path(n).name
        if bid in rec: continue
        data=ZIP.read(n)
        if data[:4]!=b'WLN1': continue
        t,info=crack(data)
        if t:
            (OUT/(bid[:-4]+'.txt')).write_text(t if t.endswith('\n') else t+'\n')
            new+=1; meth['/'.join(info['schedule'])]+=1
    ids=sorted(p.stem+'.bin' for p in OUT.glob('*.txt') if p.name!='RECOVERED_IDS.txt')
    (OUT/'RECOVERED_IDS.txt').write_text('\n'.join(ids)+'\n')
    print('new transport', new, 'total', len(ids))
    print(meth.most_common(20))

if __name__=='__main__':
    main()
