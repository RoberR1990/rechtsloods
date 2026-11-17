"""Volgende batches: python3 volgende.py <v3|l1> <slug> <n> [model]  -> print batch-id's en markeer als lopend (verloopt na 45 min).
python3 volgende.py stand  -> voortgang van alle batchbestanden."""
import json,os,sys,time
D='/home/claude/data';L=f'{D}/batches/lopend.json'
lop=json.load(open(L)) if os.path.exists(L) else {}
now=time.time();lop={k:v for k,v in lop.items() if now-v<2700}
def klaar(laag,s,b):
    if laag=='l1':
        p=f'{D}/uit_l1/{s}/{b["id"]}.json'
        if not os.path.exists(p): return False
        try: return len(json.load(open(p)))>=len(b['eclis'])-1
        except Exception: return False
    return all(os.path.exists(f'{D}/uit_v3/{s}/{f}') for f in b['files'])
if sys.argv[1]=='stand':
    for f in sorted(os.listdir(f'{D}/batches')):
        if not (f.startswith('v3_') or f.startswith('l1_')): continue
        laag,s=f[:2],f[3:-5];B=json.load(open(f'{D}/batches/{f}'))
        k=sum(klaar(laag,s,b) for b in B);print(f'{laag} {s}: {k}/{len(B)} batches klaar, lopend {sum(1 for b in B if b["id"] in lop)}')
    sys.exit()
laag,s,n=sys.argv[1],sys.argv[2],int(sys.argv[3]);m=sys.argv[4] if len(sys.argv)>4 else None
B=json.load(open(f'{D}/batches/{laag}_{s}.json'));out=[]
for b in B:
    if len(out)>=n: break
    if b['id'] in lop or (m and b.get('model')!=m) or klaar(laag,s,b): continue
    out.append(b['id']);lop[b['id']]=now
json.dump(lop,open(L,'w'));print(' '.join(out))
