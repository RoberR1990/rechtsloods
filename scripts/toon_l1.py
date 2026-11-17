"""Toon laag-1-invoer voor een batch: python3 toon_l1.py <slug> <batch-id> [van] [tot]"""
import json,sys
s,b=sys.argv[1],sys.argv[2];I=json.load(open(f'/home/claude/data/in_l1/{s}.json'))
B=[x for x in json.load(open(f'/home/claude/data/batches/l1_{s}.json')) if x['id']==b][0]['eclis']
van=int(sys.argv[3]) if len(sys.argv)>3 else 0;tot=int(sys.argv[4]) if len(sys.argv)>4 else len(B)
for e in B[van:tot]:
    d=I[e];print(f"=== {e} | {d['instantie']} | {d['datum']} | {d['procedure']} | gemeente (metadata): {d['gemeente_meta']}")
    print('INHOUDSINDICATIE:',d['inhoud'])
    print('KOP:',' | '.join(f"[{a['id']}] {a['t']}" for a in d['kop']))
    print('BESLISSING:',' '.join(f"[{a['id']}] {a['t']}" for a in d['beslissing']) or '(niet gevonden)')
    print()
