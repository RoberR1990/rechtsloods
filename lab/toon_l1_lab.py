"""Toon laag-1-invoer voor een vangnetbatch: python3 -I toon_l1_lab.py <naam> <slug> <batch-id> [van] [tot]"""
import json, sys, os
L = os.path.dirname(os.path.abspath(__file__)); n, s, b = sys.argv[1:4]
V = f'{L}/runs/{n}-vangnet/D'; I = json.load(open(f'{V}/in_l1/{s}.json'))
B = [x for x in json.load(open(f'{V}/batches/l1_{s}.json')) if x['id'] == b][0]['eclis']
van = int(sys.argv[4]) if len(sys.argv) > 4 else 0; tot = int(sys.argv[5]) if len(sys.argv) > 5 else len(B)
for e in B[van:tot]:
    d = I[e]; print(f"=== {e} | {d['instantie']} | {d['datum']} | {d['procedure']} | gemeente (metadata): {d['gemeente_meta']}")
    print('INHOUDSINDICATIE:', d['inhoud']); print('KOP:', ' | '.join(f"[{a['id']}] {a['t']}" for a in d['kop']))
    print('BESLISSING:', ' '.join(f"[{a['id']}] {a['t']}" for a in d['beslissing']) or '(niet gevonden)'); print()
