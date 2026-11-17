import json,subprocess,time,os,sys
K=json.load(open('/home/claude/data/kandidaten2.json'))
w,n=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(K):
    if i%n!=w: continue
    f=f"/home/claude/data/xml/{r['ecli'].replace(':','_')}.xml"
    if os.path.exists(f) and os.path.getsize(f)>500: continue
    subprocess.run(["curl","-s","-m","60","-o",f,f"https://data.rechtspraak.nl/uitspraken/content?id={r['ecli']}"])
    time.sleep(0.2)
print("klaar",w)
