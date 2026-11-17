import json, time, sys, urllib.request
URL="https://uitspraken.rechtspraak.nl/api/zoek"
def q(term, start, size=100):
    body={"StartRow":start,"PageSize":size,"ShouldReturnHighlights":False,"ShouldCountFacets":start==0,
      "SortOrder":"UitspraakDatumDesc","SearchTerms":[{"Term":term,"Field":"AlleVelden"}],
      "Contentsoorten":[],"Rechtsgebieden":[],"Instanties":[],"DatumPublicatie":[],"DatumUitspraak":[],
      "Advanced":{"PublicatieStatus":"AlleenGepubliceerd"},"CorrelationId":"x","Proceduresoorten":[]}
    r=urllib.request.Request(URL,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(r,timeout=60))
terms=sys.argv[1:]
out={}
for t in terms:
    d=q(t,0); n=d["ResultCount"]; rows=d["Results"]; s=len(rows)
    while s<n:
        rows+=q(t,s)["Results"]; s+=100; time.sleep(0.3)
    out[t]=rows; print(t,n,len(rows),flush=True)
json.dump(out,open("/home/claude/data/harvest.json","w"))
