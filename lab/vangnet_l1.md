# Vangnet laag 1 (pijplijn): afwijkingen op scripts/verrijk_l1.md
Voer `/home/claude/scripts/verrijk_l1.md` uit voor domein `<slug>`, met deze afwijkingen:
- Lees ook `/home/claude/rechtzoeker/lab/aanscherping_l1c.md` (uitkomstregels) en volg die.
- Je batch staat in `/home/claude/rechtzoeker/lab/runs/<naam>-vangnet/D/batches/l1_<slug>.json`.
- Lezen: `python3 -I /home/claude/rechtzoeker/lab/toon_l1_lab.py <naam> <slug> <batch-id> 0 10`, enz.
- Uitvoer: `/home/claude/rechtzoeker/lab/runs/<naam>-vangnet/D/uit_l1/<slug>/<batch-id>.json`.
- Check: `python3 -I /home/claude/rechtzoeker/lab/runs/<naam>-vangnet/_check_l1.py <slug> <batch-id>` tot `FOUTEN: 0`.
- Hulpscripts alleen in `/tmp/<naam>-<batch-id>/`. Alleen Bash, Read en Write.
