"""python3 volgende_prio.py <n> [model] -> volgende batch-id's uit data/batches/prioriteit.json (helft-selectie 14 nov)."""
import json,os,sys,time
D='/home/claude/data';L=f'{D}/batches/lopend.json'
lop=json.load(open(L)) if os.path.exists(L) else {};now=time.time();lop={k:v for k,v in lop.items() if now-v<2700}
B={b['id']:b for b in json.load(open(f'{D}/batches/v3_parkeren.json'))}
n=int(sys.argv[1]);m=sys.argv[2] if len(sys.argv)>2 else None;out=[]
for i in json.load(open(f'{D}/batches/prioriteit.json')):
    b=B[i]
    if len(out)>=n:break
    if i in lop or (m and b['model']!=m) or all(os.path.exists(f'{D}/uit_v3/parkeren/{x}') for x in b['files']):continue
    out.append(i);lop[i]=now
json.dump(lop,open(L,'w'));print(' '.join(out))
