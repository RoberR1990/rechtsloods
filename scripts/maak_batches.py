"""Batches maken. Laag 1: python3 maak_batches.py l1 <slug> <grootte>
Laag 2: python3 maak_batches.py v3 <slug> <grootte> [prio-max]   (sonnet voor prio 1, haiku voor rest; parkeren: hoge instanties sonnet)
Bestaande batches blijven behouden (alleen nieuwe ecli's worden toegevoegd)."""
import json,sys,os,re
laag,s,n=sys.argv[1],sys.argv[2],int(sys.argv[3]);D='/home/claude/data'
HOOG=re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')
U=json.load(open(f'{D}/uitspraken.json' if s=='parkeren' else f'{D}/dom/{s}/uitspraken.json'))
for u in U:
    if 'prio' not in u: u['prio']=1 if (HOOG.search(u['instantie']) or ':PHR:' in u['ecli']) else 3
p=f'{D}/batches/{laag}_{s}.json';B=json.load(open(p)) if os.path.exists(p) else []
key='eclis' if laag=='l1' else 'files'
al={x for b in B for x in b[key]}
if laag=='v3':
    pm=int(sys.argv[4]) if len(sys.argv)>4 else 3
    rel=None
    if s!='parkeren' and os.path.exists(f'{D}/uit_l1/{s}'):  # alleen relevante uit laag 1
        rel={o['ecli'] for f in os.listdir(f'{D}/uit_l1/{s}') for o in json.load(open(f'{D}/uit_l1/{s}/{f}')) if o.get('relevant') is not False}
    if s=='parkeren':
        V={json.load(open(f'{D}/uit/{f}')).get('ecli'):json.load(open(f'{D}/uit/{f}')).get('relevant') for f in os.listdir(f'{D}/uit')}
        U=[u for u in U if V.get(u['ecli']) is not False]
    U=[u for u in U if u['prio']<=pm and (rel is None or u['ecli'] in rel)]
seen=set();U2=[]
for u in sorted(U,key=lambda u:(u['prio'],u['datum']),reverse=False):
    if u['ecli'] in seen: continue
    seen.add(u['ecli']);U2.append(u)
U2.sort(key=lambda u:(u['prio'],-int(u['datum'][:4] or 0)))
nieuw=[u for u in U2 if (u['ecli'] if laag=='l1' else u['ecli'].replace(':','_')+'.json') not in al]
for m in ([1,3] if laag=='v3' else [None]):
    grp=[u for u in nieuw if m is None or (u['prio']==1)==(m==1)]
    for i in range(0,len(grp),n):
        c=grp[i:i+n];bid=f"{laag}-{s}-{len(B)+1:04d}"
        b={'id':bid,key:[u['ecli'] if laag=='l1' else u['ecli'].replace(':','_')+'.json' for u in c]}
        if laag=='v3': b['model']='sonnet' if m==1 else 'haiku'
        B.append(b)
json.dump(B,open(p,'w'),indent=0);print(p,len(B),'batches,',sum(len(b[key]) for b in B),'items')
