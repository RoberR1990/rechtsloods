import json,subprocess,time,os
K=json.load(open('/home/claude/data/kandidaten.json'))
for i,r in enumerate(K):
    f=f"/home/claude/data/xml/{r['ecli'].replace(':','_')}.xml"
    if os.path.exists(f) and os.path.getsize(f)>500: continue
    subprocess.run(["curl","-s","-m","60","-o",f,f"https://data.rechtspraak.nl/uitspraken/content?id={r['ecli']}"])
    time.sleep(0.25)
    if i%100==0: print(i,flush=True)
print("klaar")
