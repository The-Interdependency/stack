import sys,json
sys.path.insert(0,'/workspace/cypher/src')
from pathlib import Path
from fractions import Fraction
import cycle
from cycle import Profile, CycleLimits, _prepared, _native_identity, NORMAL_MAGIC
from cycle_native import load_native
from prime_schedule import plan, interleave
from numeral import _Reader

SOURCES='/workspace/cypher/src/sources'
prof_pub=Path('/workspace/cypher/src/profiles/cycle-v1.json').read_bytes()

def reverse_to_normalized(wire, profile, limits=CycleLimits()):
    reader=_Reader(wire)
    assert reader.take(4)==cycle.MAGIC
    src_id=reader.take(32); prof_id=reader.take(32); root=reader.take(32).hex()
    rc=reader.uint(); data=reader.blob(limits.round_bytes)
    assert reader.pos==len(wire)
    info={'source_identity_matches_native':src_id==_native_identity(),
          'profile_identity_matches':prof_id==profile.identity,
          'root_origin':root,'round_count':rc}
    routes,engine=_prepared(profile,limits)
    api,geometry=load_native(SOURCES)
    for i in range(len(profile.rounds)-1,-1,-1):
        spec,route=profile.rounds[i],routes[i]
        split=plan(len(data)*8,route,spec.arities,limits.numeral(),engine=engine)
        packed=interleave(data,split,inverse=True,end_order=spec.end_order)
        data=cycle.unaffix(packed,api=api,geometry=geometry,scope=profile.scope,root=root,round_id=i,spec=spec,limits=limits)
    # verify root reconstructs
    info['root_reconstructs']=api.ByteOrigin(data,profile.scope,0,geometry).message_origin==root
    return data,info

if __name__=='__main__':
    profile=Profile.read(prof_pub)
    for k in ['a01','a02','a03','a04']:
        wire=Path(f'/workspace/cypher/v1/ciphertexts/{k}.wvc').read_bytes()
        try:
            data,info=reverse_to_normalized(wire,profile)
            assert data[:4]==NORMAL_MAGIC, data[:8]
            length=int.from_bytes(data[4:12],'big')
            corpus_hash=data[12:44].hex()
            msg=data[44:44+length]
            Path(f'/workspace/cypher/work/{k}.recovered').write_bytes(msg)
            print(f'=== {k}: RECOVERED {length} bytes, corpus_sha256={corpus_hash}')
            print('   info',info)
            print('   preview', msg[:300])
        except Exception as e:
            import traceback; print(f'=== {k} FAILED:',repr(e)); traceback.print_exc()
