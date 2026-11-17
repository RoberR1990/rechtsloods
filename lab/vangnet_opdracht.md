# Vangnet AVG (pilot modelmix): afwijkingen op scripts/verrijk_v3.md
Voer `/home/claude/scripts/verrijk_v3.md` uit voor domein `avg-privacy`, met deze afwijkingen:
- Je batch staat in `/home/claude/rechtzoeker/lab/runs/f2c-vangnet-avg/batches.json` (object met jouw `id`, veld `files`), NIET in data/batches.
- Uitvoer naar `/home/claude/rechtzoeker/lab/runs/f2c-vangnet-avg/D/uit_v3/avg-privacy/<bestand>`, NIET naar data/uit_v3.
- Check: `python3 -I /home/claude/rechtzoeker/lab/runs/f2c-vangnet-avg/_check_uit_v3.py avg-privacy <jouw bestanden>` tot `FOUTEN: 0`.
- Lezen: `python3 /home/claude/scripts/toon_v3.py avg-privacy <bestand>`; domeinbestanden in `/home/claude/data/dom/avg-privacy/`.
- Hulpscripts alleen in `/tmp/<jouw-batch-id>/`. Schrijf niets anders in de repo.
