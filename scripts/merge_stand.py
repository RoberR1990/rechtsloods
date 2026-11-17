"""Voegt stand-van-het-recht en standaardlijnen samen en valideert elk citaat tegen de bron."""
import json, os, re
D = "/home/claude/data"
U = {u["ecli"]: u for u in json.load(open(f"{D}/uitspraken.json"))}
V = {v["ecli"]: v for v in json.load(open("/home/claude/site/data/verrijkt.json"))}
norm = lambda s: re.sub(r"\s+", " ", (s or "")).strip()
def bronteksten(e):
    t = [U[e]["inhoud"]] if e in U else []
    if e in U: t += [a["t"] for a in U[e]["alineas"]]
    v = V.get(e)
    if v and v.get("relevant"):
        for it in [v.get("kern"), v.get("rechtsregel")] + (v.get("argumenten") or []):
            if it and it.get("citaat"): t.append(it["citaat"])
    return norm(" ".join(t))
stats = {"ok": 0, "weg": 0}
def check_bronnen(br):
    goed = []
    for b in br or []:
        e = b.get("ecli"); c = norm(b.get("citaat"))
        if e in U and (not c or c in bronteksten(e)):
            goed.append({"ecli": e, "citaat": b.get("citaat", "")}); stats["ok"] += 1
        else: stats["weg"] += 1
    return goed
def schoon_lijst(L):
    out = []
    for r in L or []:
        br = check_bronnen(r.get("bronnen"))
        if br: out.append({"zin": r["zin"], "bronnen": br})
    return out
stand = {}
for o in ["parkeerbelasting", "parkeerverbod", "vergunningen", "parkeernormen", "garages-privaat", "handhaving-privacy"]:
    p = f"{D}/stand_uit/{o}.json"
    if not os.path.exists(p): print("ontbreekt", o); continue
    S = json.load(open(p)); stand[o] = {}
    for k, s in S.items():
        s["regels"] = schoon_lijst(s.get("regels")); s["uitzonderingen"] = schoon_lijst(s.get("uitzonderingen")); s["toetslijst"] = schoon_lijst(s.get("toetslijst"))
        s["steunt_gemeente"] = [e for e in s.get("steunt_gemeente", []) if e in U]; s["steunt_parkeerder"] = [e for e in s.get("steunt_parkeerder", []) if e in U]
        if not s["regels"] and s.get("lijn") != "weinig": s["lijn"] = "weinig"
        stand[o][k] = s
lijnen = {}
for f in ["lijnen_1.json", "lijnen_2.json"]:
    p = f"{D}/stand_uit/{f}"
    if not os.path.exists(p): print("ontbreekt", f); continue
    for a, l in json.load(open(p)).items():
        l["bronnen"] = check_bronnen(l.get("bronnen")); l["uitzonderingen"] = schoon_lijst(l.get("uitzonderingen"))
        if not l["bronnen"]: l["lijn"] = "weinig"; l.pop("bouwsteen", None)
        lijnen[a] = l
json.dump(stand, open("/home/claude/site/data/stand.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(lijnen, open("/home/claude/site/data/lijnen.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("bronnen geldig", stats, "| onderwerpen", {o: len(s) for o, s in stand.items()}, "| lijnen", len(lijnen))
