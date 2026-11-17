"""Toon een uitspraak compact: python3 toon.py <bestandsnaam.json> [...]"""
import json,sys
for f in sys.argv[1:]:
    d=json.load(open('/home/claude/data/proef/in3/'+f))
    print(f"=== {f} | {d['ecli']} | {d['instantie']} | {d['datum']} | {d['procedure']} | {d['rechtsgebied']} | voorgesteld onderwerp: {d['onderwerp']}")
    print("INHOUDSINDICATIE:",d['inhoud'])
    for a in d['alineas']: print(f"[{a['id']}]{'(r.o. '+a['rov']+')' if a['rov'] else ''} {a['t']}")
    print()
