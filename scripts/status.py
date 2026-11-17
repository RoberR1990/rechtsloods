import json,os
B=json.load(open('/home/claude/data/batches/batches.json'))
uit=set(os.listdir('/home/claude/data/proef/uit'))
done=[b['id'] for b in B if all(f in uit for f in b['files'])]
part=[b['id'] for b in B if any(f in uit for f in b['files']) and b['id'] not in done]
print('klaar',len(done),'deels',part,'| bestanden',sum(1 for b in B for f in b['files'] if f in uit),'/',sum(len(b['files']) for b in B))
