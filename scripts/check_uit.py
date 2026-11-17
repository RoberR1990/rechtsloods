"""Controleer uitvoer: python3 check_uit.py <bestandsnaam.json> [...]  -> meldt fouten per bestand"""
import json,sys,os
T=json.load(open('/home/claude/data/taxonomie.json'));A=json.load(open('/home/claude/data/argumenten.json'))
fout=0
for f in sys.argv[1:]:
    p='/home/claude/data/proef/uit/'+f
    if not os.path.exists(p): print(f,"ONTBREEKT");fout+=1;continue
    try:o=json.load(open(p))
    except Exception as e: print(f,"GEEN GELDIGE JSON",e);fout+=1;continue
    if not o.get('relevant'): continue
    src={a['id']:a['t'] for a in json.load(open('/home/claude/data/proef/in3/'+f))['alineas']}
    if o.get('onderwerp') not in T or o.get('sub') not in T[o['onderwerp']]['sub']: print(f,"onbekend onderwerp/sub",o.get('onderwerp'),o.get('sub'));fout+=1
    items=[('kern',o.get('kern'))]+[('sam',s) for s in o.get('samenvatting') or []]+([('regel',o['rechtsregel'])] if o.get('rechtsregel') and o['rechtsregel'].get('zin') else [])+[('les',s) for s in o.get('lessen_voor_gemeente') or []]+[('arg',a) for a in o.get('argumenten') or [] if a.get('citaat')]
    for k,it in items:
        b=(it or {}).get('bron') or [];c=(it or {}).get('citaat','')
        if not b or b[0] not in src: print(f,k,"bron-id ontbreekt/onbekend",b);fout+=1
        elif not c or c not in src[b[0]]: print(f,k,"citaat niet letterlijk in alinea",b[0],":",c[:60]);fout+=1
    for a in o.get('argumenten') or []:
        if a.get('arg') not in A: print(f,"onbekend argument",a.get('arg'));fout+=1
    if not 3<=len(o.get('samenvatting') or [])<=6: print(f,"samenvatting moet 3-6 zinnen");fout+=1
print("FOUTEN:",fout)
