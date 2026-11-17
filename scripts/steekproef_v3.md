# Opdracht: Sonnet-steekproef op Haiku-samenvattingen (schema v3, parkeren)

Je krijgt een deel-nummer N. Lijst: `/home/claude/data/steekproef/v3_parkeren_haiku.json` → sleutel "N" (bestandsnamen).
Lees eerst `/home/claude/scripts/verrijk_v3.md` (de regels waaraan de samenvatting moet voldoen).

Per bestand:
1. Lees de uitspraak met `python3 /home/claude/scripts/toon_v3.py parkeren <bestand>` (alles) en de samenvatting `/home/claude/data/uit_v3/parkeren/<bestand>`.
2. Beoordeel: (a) uitkomst/titel/kern kloppen met de beslissing; (b) wie-zei-wat niet omgedraaid; (c) rechtsregel is de winnende regel; (d) bezwaargronden en oordelen kloppen; (e) geen beleid van een andere partij doorgetrokken naar de gemeente; (f) relevant/niet-relevant juist; (g) B1 en rolnamen.
3. Fout gevonden: herstel het bestand zelf (zelfde schema, citaten letterlijk) en draai `python3 /home/claude/scripts/check_uit_v3.py parkeren <bestand>` tot FOUTEN: 0.
4. Schrijf `/home/claude/data/steekproef/uit_N.json`: lijst van {"bestand", "oordeel": "goed|klein|ernstig", "fout": "<1 zin of null>", "hersteld": true|false}. "ernstig" = uitkomst, kern of rechtsregel inhoudelijk fout.

Gebruik ALLEEN Bash, Read en Write. Nooit ToolSearch, send_later, create_trigger, berichten of andere tools.
Eindrapport in één regel: deel, aantal goed/klein/ernstig.
