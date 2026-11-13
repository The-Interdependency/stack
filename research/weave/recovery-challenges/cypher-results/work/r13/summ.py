import json,sys; from collections import Counter
r=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
print(len(r), Counter((x['sched'],x['status']) for x in r))
for x in r:
  if x['status'] not in('none','timeout'): print(x['file'],x['sched'],x['t'],x['rot'],x['ar'],x['status'],(x.get('msg') or '')[:50])
