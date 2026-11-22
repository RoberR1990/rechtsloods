"""Herstel tussenuitspraken zonder dictum in laag 1: niet-relevant -> relevant, bestuurlijke-lus, zekerheid laag.
Uitkomst niet vast te stellen zonder brontekst: uitkomst 'alleen procedure', uitkomst_bron None, hersteld=True.
Uitsluiten: TVL-aanvraag, geheimhouding. Gebruik: python3 herstel_tussen.py [datadir]"""
import json,glob,sys
D=sys.argv[1] if len(sys.argv)>1 else 'data/uit_l1/bezwaar-beroep'
n=0
for f in sorted(glob.glob(D+'/b*.json')):
    ch=False
    # herlees en herstel
    L2=json.load(open(f))
    for o in L2:
        r=(o.get('reden') or '').lower()
        if o.get('relevant') is False and r.startswith('tussenuitspraak') and 'tvl' not in r:
            o.pop('reden');o.update({'relevant':True,'onderwerp':'bestuurlijke-lus','sub':'overig','kenmerk':None,'zaaktype':'bestuurlijke-lus','partijen':{'burger':None,'wederpartij':None,'gemeente_is_partij':False},'procesvorm':'beroep','uitkomst':'alleen procedure','uitkomst_bron':None,'bezwaargronden':[],'gemeente':None,'zekerheid':'laag','hersteld':True});n+=1;ch=True
    if ch: json.dump(L2,open(f,"w"),ensure_ascii=False,indent=1)
print('hersteld',n)
