"""Zet data/trends_uit/<onderwerp>.json in site/data/trends.json (behoudt _algemeen) en controleert citaten letterlijk."""
import json, re, os
D = "/home/claude/data"; S = "/home/claude/site/data/trends.json"
U = {u["ecli"]: u for u in json.load(open(f"{D}/uitspraken.json"))}
norm = lambda s: re.sub(r"\s+", " ", (s or "")).strip()
def tekst(e):
    u = U.get(e); return norm(" ".join([u.get("inhoud", "")] + [a["t"] for a in u["alineas"]])) if u else ""
T = json.load(open(S)); st = {"ok": 0, "weg": 0}
for f in sorted(os.listdir(f"{D}/trends_uit")):
    o = f[:-5]; n = json.load(open(f"{D}/trends_uit/{f}"))
    for ow in n.get("ontwikkelingen", []):
        goed = [b for b in ow.get("bronnen", []) if norm(b.get("citaat")) and norm(b["citaat"]) in tekst(b.get("ecli"))]
        st["ok"] += len(goed); st["weg"] += len(ow.get("bronnen", [])) - len(goed); ow["bronnen"] = goed
    n["ontwikkelingen"] = [ow for ow in n.get("ontwikkelingen", []) if ow["bronnen"]]
    n["kantelpunten"] = [k for k in n.get("kantelpunten", []) if k.get("ecli") in U]
    T[o] = n
json.dump(T, open(S, "w"), ensure_ascii=False, separators=(",", ":"))
print("trends", {o: len(T[o].get("ontwikkelingen", [])) for o in T if o != "_algemeen"}, st)
