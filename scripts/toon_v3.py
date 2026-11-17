"""Toon ingekorte invoer: python3 toon_v3.py <slug> <bestand.json> [...]"""
import json,sys
s=sys.argv[1]
for f in sys.argv[2:]:
    d=json.load(open(f'/home/claude/data/in_v3/{s}/{f}'))
    print(f"=== {f} | {d['ecli']} | {d['instantie']} | {d['datum']} | {d['procedure']} | {d['rechtsgebied']} | gemeente (metadata, kan fout zijn): {d.get('gemeente')}")
    print("INHOUDSINDICATIE:",d['inhoud'])
    rel=[r['ecli'] for r in d.get('relaties') or [] if r.get('ecli')]
    if rel: print("GERELATEERD (metadata):",', '.join(rel))
    for a in d['alineas']: print(f"[{a['id']}]{'(r.o. '+a['rov']+')' if a.get('rov') else ''} {a['t']}")
    print()
