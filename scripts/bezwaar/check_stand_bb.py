import json,sys
I=json.load(open(sys.argv[1]));U=json.load(open(sys.argv[2]))
ok={}
for s,b in I['subs'].items():
    for u in b['uitspraken']:
        c={(u.get('kern') or {}).get('citaat'),(u.get('rechtsregel') or {}).get('citaat')}|{x.get('citaat') for x in (u.get('samenvatting') or [])}
        ok[u['ecli']]=c-{None}
f=0
def chk(it,pad):
    global f
    if not it.get('bronnen'): print(pad,'geen bron');f+=1
    for b in it.get('bronnen',[]):
        if b.get('citaat') not in ok.get(b.get('ecli'),()): print(pad,b.get('ecli'),'citaat niet gevonden');f+=1
for s,v in U.items():
    if s not in I['subs']: print(s,'onbekend sub');f+=1;continue
    for k in('regels','uitzonderingen','toetslijst'):
        for i,it in enumerate(v.get(k,[])): chk(it,f'{s}.{k}[{i}]')
    for k in('steunt_gemeente','steunt_parkeerder'):
        for e in v.get(k,[]):
            if e not in ok: print(s,k,e,'onbekende ecli');f+=1
print('fouten',f);sys.exit(1 if f else 0)
