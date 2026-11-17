"""Bereidt invoer voor de stand-van-het-recht-agents: per onderwerp/subonderwerp de belangrijkste uitspraken."""
import json, os, re, collections
src = open('/home/claude/scripts/build_data2.py').read().split('# --- embeddingen ---')[0].replace('from fastembed import TextEmbedding', '')
ns = {}; exec(src, ns)
docs, VER, TAX = ns['docs'], ns['VER'], ns['TAX']
cnt = collections.Counter()
for u in docs:
    full = " ".join(a["t"] for a in u["alineas"])
    for e in set(re.findall(r"ECLI:NL:[A-Z]+:\d{4}:[A-Z0-9]+", full)):
        if e != u["ecli"]: cnt[e] += 1
OUT = '/home/claude/data/stand_in'; os.makedirs(OUT, exist_ok=True)
fout = {e for e, v in VER.items() if not v.get('relevant')}
def niv(i): return 3 if ('Hoge Raad' in i or 'Raad van State' in i) else 2 if 'Gerechtshof' in i else 1
per = collections.defaultdict(list)
for u in docs:
    if u['ecli'] in fout: continue
    v = VER.get(u['ecli'])
    o, s = (v['onderwerp'], v['sub']) if v and v.get('sub') else (u['onderwerp'], ns['auto_sub'](u))
    per[(o, s)].append(u)
for o in TAX:
    blok = {}
    for s in TAX[o]['sub']:
        L = per.get((o, s), [])
        L.sort(key=lambda u: (-(niv(u['instantie']) * 10 + min(cnt[u['ecli']], 10) + (8 if u['ecli'] in VER else 0)), u['datum']), reverse=False)
        items = []
        for u in L[:22]:
            v = VER.get(u['ecli'])
            it = {"ecli": u['ecli'], "instantie": u['instantie'], "datum": u['datum'], "procedure": u['procedure'],
                  "aangehaald": cnt[u['ecli']], "inhoudsindicatie": u['inhoud'][:900]}
            if v:
                it["samenvatting"] = {"kern": v['kern'], "rechtsregel": v.get('rechtsregel'), "uitkomst": v.get('uitkomst'),
                                      "uitkomst_type": v.get('uitkomst_type'), "steunt": v.get('steunt'), "argumenten": v.get('argumenten')}
            items.append(it)
        blok[s] = {"label": TAX[o]['sub'][s], "aantal_totaal": len(L), "uitspraken": items}
    json.dump(blok, open(f"{OUT}/{o}.json", "w"), ensure_ascii=False, indent=1)
    print(o, {s: b['aantal_totaal'] for s, b in blok.items()}, os.path.getsize(f"{OUT}/{o}.json") // 1024, "KB")
# argumenten: kandidaten per argument (uit verrijkte argumenten + patroon in inhoudsindicatie)
PAT = {
 "borden-onduidelijk": r"kenbaar|bord|bebording|markering", "app-automaat-werkte-niet": r"parkeerapp|app\b|automaat|parkeermeter|storing|defect",
 "kort-stilstaan": r"onmiddellijk|in- of uitstappen|laden en lossen|laden of lossen|stilstaan", "wel-betaald-fout-zone-kenteken": r"zonecode|verkeerde zone|kenteken.*(onjuist|verkeerd)|tikfout",
 "vergunning-niet-geactiveerd": r"bezoek|niet aangemeld|aanmelding|vergunning.*niet.*(geactiveerd|gekoppeld)", "bewijs-scanauto": r"scanauto|scanfoto|bewijs|waarneming",
 "kosten-te-hoog": r"kosten|tarief|kostenraming", "overmacht-medisch": r"overmacht|medisch|noodsituatie|ziekenhuis", "gehandicaptenkaart": r"gehandicaptenparkeerkaart|invalidenparkeerkaart",
 "termijn-verschoonbaar": r"termijnoverschrijding|verschoonbaar|te laat", "te-laat-beslist": r"dwangsom|ingebrekestelling|niet tijdig", "hoorplicht-motivering": r"horen|hoorzitting|motivering",
 "gelijkheid": r"gelijkheid|gelijke gevallen", "onevenredig": r"evenredig|hardheid|coulance|billijk", "belangenafweging-verkeersbesluit": r"verkeersbesluit|belangenafweging",
 "plafond-verdeling": r"plafond|wachtlijst|schaars", "parkeernorm-onvoldoende": r"parkeernorm|parkeerbehoefte|parkeerdruk", "privaat-voorwaarden": r"algemene voorwaarden|parkeervoorwaarden|exploitant",
 "privacy-kenteken": r"privacy|persoonsgegevens|\bavg\b", "ai-bronnen": r"kunstmatige intelligentie|niet-bestaande|chatgpt|\bai\b"}
args = {}
for a, p in PAT.items():
    L = [u for u in docs if u['ecli'] not in fout and ((u['ecli'] in VER and any(x.get('arg') == a for x in VER[u['ecli']].get('argumenten') or [])) or re.search(p, u['inhoud'].lower()))]
    L.sort(key=lambda u: -(niv(u['instantie']) * 10 + min(cnt[u['ecli']], 10) + (15 if u['ecli'] in VER else 0)))
    args[a] = [{"ecli": u['ecli'], "instantie": u['instantie'], "datum": u['datum'], "onderwerp": u['onderwerp'], "aangehaald": cnt[u['ecli']], "inhoudsindicatie": u['inhoud'][:700],
                **({"argumenten": VER[u['ecli']].get('argumenten'), "kern": VER[u['ecli']]['kern']} if u['ecli'] in VER else {})} for u in L[:18]]
json.dump(args, open(f"{OUT}/argumenten.json", "w"), ensure_ascii=False, indent=1)
print('argumenten', {a: len(v) for a, v in args.items()})
