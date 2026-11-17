#!/usr/bin/env python3
"""Maakt site/data/zoekindex.json: lichte index van alle live rechtsgebieden voor 'zoeken over alles' op Home.
Draai opnieuw na elke data-update (build_verrijkt / dom_build). Gebruik: python3 -I scripts/maak_zoekindex.py"""
import json, os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
idx = json.load(open(f'{S}/data/domeinen/index.json', encoding='utf-8'))
uit = {}
for d in idx:
    if d.get('status') == 'binnenkort':
        continue
    pad = f"{S}/{d.get('pad', 'data/')}".replace('//', '/')
    meta = json.load(open(pad + 'meta.json', encoding='utf-8'))
    verr = json.load(open(pad + 'verrijkt.json', encoding='utf-8'))
    fout = {v['ecli'] for v in verr if not v.get('relevant')}
    rows = []
    for m in meta:
        if m['e'] in fout:
            continue
        h = (m.get('h') or '').strip()
        if len(h) > 240:
            h = h[:237].rsplit(' ', 1)[0] + '…'
        rows.append(
                    {'e': m['e'], 'i': m['i'], 'n': m['n'], 'd': m['d'], 'h': h, 'st': m.get('st'), 'c': m.get('c', 0)})
    uit[d['slug']] = rows
    print(d['slug'], len(rows))
json.dump(uit, open(f'{S}/data/zoekindex.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('bytes', os.path.getsize(f'{S}/data/zoekindex.json'))
