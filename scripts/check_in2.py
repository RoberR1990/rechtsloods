import json,glob,os,re
IN="/home/claude/data/proef/in2/"; OUT="/home/claude/data/proef/uit/"
tax=json.load(open("/home/claude/data/taxonomie.json")); args=json.load(open("/home/claude/data/argumenten.json"))
names="ECLI_NL_RVS_2016_164 ECLI_NL_RVS_2016_1740 ECLI_NL_RVS_2016_327 ECLI_NL_RVS_2017_1746 ECLI_NL_RVS_2017_2451 ECLI_NL_RVS_2017_464 ECLI_NL_RVS_2018_1331 ECLI_NL_RVS_2018_2360 ECLI_NL_RVS_2018_2674 ECLI_NL_RVS_2018_3562".split()
bad=0
def chk(label,o,al):
    global bad
    if not o: return
    b=o["bron"]; c=o["citaat"]
    if not b: print(label,"geen bron"); bad+=1; return
    for i in b:
        if i not in al: print(label,"onbekend id",i); bad+=1
    if c not in al.get(b[0],""): print(label,"CITAAT FOUT",b,c[:60]); bad+=1
    n=len(c.split())
    if not 5<=n<=20: print(label,"woorden",n,c[:50]); bad+=1
for n in names:
    d=json.load(open(IN+n+".json")); al={a["id"]:a["t"] for a in d["alineas"]}
    o=json.load(open(OUT+n+".json"))
    assert o["onderwerp"] in tax and o["sub"] in tax[o["onderwerp"]]["sub"], n
    if o["sub2"]: assert o["sub2"] in tax[o["onderwerp"]]["sub"] or any(o["sub2"] in t["sub"] for t in tax.values()), n
    chk(n+" kern",o["kern"],al)
    for i,z in enumerate(o["samenvatting"]): chk(n+" sam%d"%i,z,al)
    assert 3<=len(o["samenvatting"])<=6,n
    chk(n+" rr",o["rechtsregel"],al)
    for i,z in enumerate(o["lessen_voor_gemeente"]): chk(n+" les%d"%i,z,al)
    for a in o["argumenten"]:
        assert a["arg"] in args,n; chk(n+" arg",a,al)
    assert len(o["titel"].split())<=10,(n,len(o["titel"].split()))
    assert len(o["uitkomst_toelichting"].split())<=15,(n,len(o["uitkomst_toelichting"].split()))
    assert o["ecli"]==d["ecli"]
print("klaar, fouten:",bad)
