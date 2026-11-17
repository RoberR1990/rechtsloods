"""Bouwt de datalaag voor het prototype: metadata, auto-indeling, gelijkenis, ketens, tekstbestanden."""
import json, re, os, collections
import numpy as np
from fastembed import TextEmbedding

D = "/home/claude/data"
OUT = "/home/claude/site/data"
os.makedirs(OUT, exist_ok=True)
U = [u for u in json.load(open(f"{D}/uitspraken.json")) if u["onderwerp"]]
# dubbele ECLI's (zelfde uitspraak in twee lijsten) samenvoegen
seen, docs = set(), []
for u in U:
    if u["ecli"] in seen: continue
    seen.add(u["ecli"]); docs.append(u)
TAX = json.load(open(f"{D}/taxonomie.json"))

RULES = {
 "parkeerbelasting": [
  ("naheffingskosten", r"hoogte (van )?de (naheffings)?kosten|kosten (zijn )?te hoog|kostenraming|art(ikel|\.)? ?234|kostenvergoeding naheffing|tarief(bepaling|tabel)|onverbindend"),
  ("invordering", r"invordering|aanmaning|dwangbevel|kwijtschelding"),
  ("begrip-parkeren", r"onmiddellijk|in- of uitstappen|in- en uitstappen|laden en lossen|laden of lossen|stilstaan|sprake van parkeren"),
  ("betalen", r"parkeerapp|app\b|automaat|parkeermeter|zonecode|gebiedscode|betaal|kenteken (verkeerd|onjuist)|storing|defect"),
  ("bewijs-scanauto", r"scanauto|scanfoto|foto|handhaver|bewijs|controleur|waarneming"),
  ("vergunning-in-betaalgebied", r"vergunning|ontheffing|bezoekers"),
  ("kenbaarheid", r"kenbaar|bord|bebording|markering|duidelijk"),
  ("belastingplicht", r"kentekenhouder|houder van het|huurder|lease|belastingplichtig"),
  ("evenredigheid", r"evenredig|coulance|hardheid|billijk"),
  ("procedure", r"niet-ontvankelijk|termijnoverschrijding|te laat|redelijke termijn|kunstmatige intelligentie|\bai\b|ontvankelijk|beroepstermijn|bezwaartermijn|dwangsom"),
 ],
 "parkeerverbod": [
  ("gehandicaptenplaats", r"gehandicapt|invalid"),
  ("wegslepen", r"wegslepen|weggesleept|verwijder|bestuursdwang|takel"),
  ("laadplek", r"laadpaal|opladen|elektrisch|deelauto|doelgroep"),
  ("maximale-duur", r"blauwe zone|parkeerschijf|maximale parkeerduur|parkeerduur"),
  ("verkeersbesluit", r"verkeersbesluit|aanwijzingsbesluit|aanwijzen|opheffen van|verkeersmaatregel"),
  ("wahv-boete", r"wahv|sanctie|inleidende beschikking|kantonrechter|gedraging|rvv"),
 ],
 "vergunningen": [
  ("gehandicaptenkaart", r"gehandicaptenparkeerkaart|invalidenparkeerkaart|medisch|keuring|loopafstand"),
  ("plafond-wachtlijst", r"plafond|wachtlijst|maximum aantal|schaars"),
  ("bezoekersregeling", r"bezoek"),
  ("bedrijfsvergunning", r"bedrijfs|zorg|mantelzorg|beroeps|ondernem"),
  ("ontheffing", r"ontheffing"),
  ("bewonersvergunning", r"bewoner|vergunning"),
 ],
}

def auto_sub(u):
    head = (u["inhoud"] + " " + " ".join(a["t"] for a in u["alineas"][:60])).lower()
    inh = u["inhoud"].lower()
    for key, pat in RULES[u["onderwerp"]]:
        if re.search(pat, inh): return key
    for key, pat in RULES[u["onderwerp"]]:
        if re.search(pat, head): return key
    return RULES[u["onderwerp"]][-1][0]

def niveau(i):
    if "Hoge Raad" in i or "Parket" in i: return "Hoge Raad"
    if "Raad van State" in i: return "Raad van State"
    if "Gerechtshof" in i: return "Gerechtshof"
    if "Centrale Raad" in i or "College van Beroep" in i: return "Bijzonder college"
    return "Rechtbank"

def uitkomst(u):
    s = (u["beslissing"] + " " + u["inhoud"]).lower()
    if "niet-ontvankelijk" in s and "gegrond" not in s: return "niet-ontvankelijk"
    if re.search(r"(?<!on)gegrond", s) and "ongegrond" not in s: return "gegrond"
    if "ongegrond" in s and not re.search(r"(?<!on)gegrond", s): return "ongegrond"
    if re.search(r"vernietigt", s): return "gegrond"
    if re.search(r"bevestigt", s): return "ongegrond"
    if "gegrond" in s: return "deels"
    return "onbekend"

# --- embeddingen ---
model = TextEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
def emb_text(u):
    body = " ".join(a["t"] for a in u["alineas"] if not a["kop"])[:1500]
    return (u["inhoud"] + " " + body)[:2000]
E = np.array(list(model.embed([emb_text(u) for u in docs])))
E /= np.linalg.norm(E, axis=1, keepdims=True)
S = E @ E.T
np.fill_diagonal(S, -1)

idx = {u["ecli"]: i for i, u in enumerate(docs)}
# ketens: relaties naar en van andere uitspraken in de set
later = collections.defaultdict(list)
for u in docs:
    for r in u["relaties"]:
        if r["aanleg"] == "eerdereAanleg" and r["ecli"]:
            later[r["ecli"]].append({"ecli": u["ecli"], "gevolg": r["gevolg"], "niveau": niveau(u["instantie"])})

meta, teksten = [], {}
for i, u in enumerate(docs):
    nb = [docs[j]["ecli"] for j in np.argsort(-S[i])[:6]]
    rel = [{"ecli": r["ecli"], "richting": "eerder" if r["aanleg"] == "eerdereAanleg" else "later",
            "type": r["type"], "gevolg": r["gevolg"]} for r in u["relaties"] if r["ecli"]]
    for l in later.get(u["ecli"], []):
        if not any(x["ecli"] == l["ecli"] for x in rel):
            rel.append({"ecli": l["ecli"], "richting": "later", "type": "hogerBeroep", "gevolg": l["gevolg"]})
    meta.append({"e": u["ecli"], "i": u["instantie"], "n": niveau(u["instantie"]), "d": u["datum"],
                 "p": u["procedure"], "o": u["onderwerp"], "s": auto_sub(u), "g": u["gemeente"],
                 "u": uitkomst(u), "h": u["inhoud"][:700], "r": rel, "v": nb, "z": u["zaaknr"],
                 "t": u["tekens"]})
    teksten[u["ecli"]] = [[a["rov"], a["t"], 1 if a["kop"] else 0] for a in u["alineas"]]

json.dump(meta, open(f"{OUT}/meta.json", "w"), ensure_ascii=False, separators=(",", ":"))
# tekst in 4 delen, geladen op aanvraag
keys = list(teksten)
for k in range(4):
    part = {e: teksten[e] for e in keys[k::4]}
    json.dump(part, open(f"{OUT}/tekst{k}.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump({e: k for k in range(4) for e in keys[k::4]}, open(f"{OUT}/tekstindex.json", "w"), separators=(",", ":"))
# embeddingen gekwantiseerd voor "vergelijkbaar met" in de browser (niet nodig: buren al berekend)
print(len(meta), "uitspraken")
print(collections.Counter((m["o"], m["s"]) for m in meta).most_common(40))
print(collections.Counter(m["u"] for m in meta))
print(sum(1 for m in meta if m["r"]), "met relaties")
for f in os.listdir(OUT): print(f, os.path.getsize(f"{OUT}/{f}") // 1024, "KB")
