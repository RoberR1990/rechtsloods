"""Invoer voor trend-agents: cijfers per jaar en niveau, hoogste-rechter-uitspraken, stand van het recht."""
import json, os, collections
D = "/home/claude/data"; OUT = f"{D}/trends_in"; os.makedirs(OUT, exist_ok=True)
M = json.load(open("/home/claude/site/data/meta.json"))
TAX = json.load(open(f"{D}/taxonomie.json"))
STAND = json.load(open("/home/claude/site/data/stand.json"))
V = {}
for f in os.listdir(f"{D}/proef/uit"):
    v = json.load(open(f"{D}/proef/uit/{f}"))
    if v.get("relevant"): V[v["ecli"]] = v
U = {u["ecli"]: u for u in json.load(open(f"{D}/uitspraken.json"))}
def onderwerp(m):
    v = V.get(m["e"]); return v["onderwerp"] if v and v.get("onderwerp") in TAX else m["o"]
for o in TAX:
    L = [m for m in M if onderwerp(m) == o or o in (m.get("x") or [])]
    per_jaar = {}
    for y in range(2016, 2027):
        J = [m for m in L if m["d"].startswith(str(y))]
        uit = collections.Counter((V[m["e"]]["uitkomst"] if m["e"] in V else "auto:" + m["u"]) for m in J)
        per_jaar[y] = {"totaal": len(J), "per_niveau": dict(collections.Counter(m["n"] for m in J)), "uitkomsten": dict(uit),
                       "per_sub": dict(collections.Counter((V[m["e"]]["sub"] if m["e"] in V else m["s"]) for m in J))}
    top = []
    for m in sorted(L, key=lambda m: m["d"]):
        if m["n"] in ("Hoge Raad", "Raad van State") or m["c"] >= 5:
            v = V.get(m["e"])
            top.append({"ecli": m["e"], "instantie": m["i"], "datum": m["d"], "aangehaald": m["c"], "status": m["st"],
                        "inhoudsindicatie": U[m["e"]]["inhoud"][:500],
                        **({"titel": v["titel"], "kern": v["kern"], "rechtsregel": v.get("rechtsregel"), "uitkomst": v["uitkomst"]} if v else {})})
    recent = [{"ecli": m["e"], "instantie": m["i"], "datum": m["d"], "titel": V[m["e"]]["titel"], "kern": V[m["e"]]["kern"]["zin"]}
              for m in sorted(L, key=lambda m: m["d"], reverse=True) if m["e"] in V and m["d"] >= "2025-06-01"][:30]
    json.dump({"onderwerp": o, "label": TAX[o]["label"], "rechtsgang": TAX[o]["rechtsgang"], "subonderwerpen": TAX[o]["sub"],
               "per_jaar": per_jaar, "hoogste_en_vaak_aangehaald": top, "recent_samengevat": recent,
               "stand_van_het_recht": {k: {x: s.get(x) for x in ["lijn", "kern", "lijn_uitleg", "hiaten"]} for k, s in STAND.get(o, {}).items()}},
              open(f"{OUT}/{o}.json", "w"), ensure_ascii=False, indent=1)
    print(o, len(L), "top", len(top), "recent", len(recent), os.path.getsize(f"{OUT}/{o}.json") // 1024, "KB")
