"""Compact register van alle gepubliceerde ECLI's 2016-2026 (belasting, bestuur, straf, civiel) voor de ECLI-check."""
import json, os, re, collections
F = "/home/claude/data/feeds"
reg = collections.defaultdict(set)
other = set()
for f in os.listdir(F):
    for r in json.load(open(f"{F}/{f}")):
        m = re.match(r"ECLI:NL:([A-Z]+):(\d{4}):(\d+)$", r["ecli"])
        if m: reg[f"{m[1]}:{m[2]}"].add(int(m[3]))
        else: other.add(r["ecli"])
def b36(n):
    s = ""
    while True:
        n, r = divmod(n, 36); s = "0123456789abcdefghijklmnopqrstuvwxyz"[r] + s
        if n == 0: return s
out = {}
for k, v in reg.items():
    nums = sorted(v); prev = 0; parts = []
    for n in nums: parts.append(b36(n - prev)); prev = n
    out[k] = ",".join(parts)
json.dump({"v": out, "x": sorted(other)}, open("/home/claude/site/data/eclireg.json", "w"), separators=(",", ":"))
print(sum(len(v) for v in reg.values()), "ECLI's;", os.path.getsize("/home/claude/site/data/eclireg.json") // 1024, "KB")
