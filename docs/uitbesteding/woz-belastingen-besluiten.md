# WOZ en gemeentelijke belastingen: besluiten tijdens de bouw

Per besluit staan hieronder het besluit, het alternatief, de reden en de status. Alles is "door Robert te bevestigen", tenzij er iets anders bij staat.
Waar een vaste regel uit een bestaand domein geldt, gaat die voor op een eigen keuze.

## B01 Repo `rechtsloods` in plaats van `rechtzoeker`, vertrek vanaf `main`
- **Besluit:** gebouwd in `RoberR1990/rechtsloods` op branch `col/woz-belastingen`, vertrokken vanaf `main` (commit db7c004).
- Alternatief: stoppen met een BLOKKADE.
- Reden: `add_repo RoberR1990/rechtzoeker` geeft "geen toegang". `rechtsloods` is de snapshot van `live` (commit "Import Rechtsloods uit privé-werkrepo (snapshot live, 16 nov 2026)"). Er bestaat geen branch `live` of `woo-uitdiepen`. Alle scripts, opdrachtteksten en checks staan in de snapshot. De parallelle sessie voor `wonen-leefbaarheid` koos om dezelfde reden hetzelfde. Om de branch over te zetten naar `rechtzoeker` zijn alleen nieuwe bestanden nodig, plus `site/data/domeinen/index.json` en `site/feeds/`.
- Status: door Robert te bevestigen.

## B02 Voorbeelddomein: BPM (belasting) en AVG/openbare orde (laag 2) in plaats van Woo
- **Besluit:** het bestandsformaat volgt `bpm` (belastingdomein, zelfde uitkomstregels). De laag-2-werkwijze volgt `avg-privacy` en `openbare-orde`.
- Alternatief: Woo.
- Reden: Woo staat in de snapshot op "binnenkort" (alleen een telling), en `data/dom/woo/config.json` bestaat niet.
- Status: door Robert te bevestigen.

## B03 Paden `/home/claude/...` via symlinks; lege `data/kandidaten2.json`
- **Besluit:** `/home/claude/{data,scripts,site}` en `/home/claude/rechtzoeker` wijzen met symlinks naar de repo. Er staat een lege `data/kandidaten2.json` (`[]`), omdat `scripts/parse.py` dat bestand bij het importeren laadt. Het bestand wordt niet gecommit (`.git/info/exclude`).
- Alternatief: de paden in de gedeelde scripts aanpassen.
- Reden: geen wijziging aan gedeelde scripts (werkafspraak 7). Dit is dezelfde aanpak als `setup.sh`.
- Status: technisch, ter info.

## B04 Alleen Claude-subagents, geen OpenRouter-keten
- **Besluit:** laag 1 = Haiku-subagents met `scripts/verrijk_l1.md`, plus `lab/aanscherping_l1c.md`, plus `lab/woz_l1.md` (3 batches van 25 per agent, zoals `lab/wahv_l1.md`). Laag 2 = Sonnet-subagents die zelf schrijven (`lab/vangnet_v3.md`: `scripts/verrijk_v3.md`, plus `lab/aanscherping_v3c.md`, plus `lab/woz_v3.md`). De stand = Sonnet met `lab/stand_opdracht.md`.
- Alternatief: `lab/pijplijn.py` (DeepSeek/Qwen via OpenRouter).
- Reden: de opdracht staat alleen Claude toe en geen API-sleutels.
- Status: volgt uit de opdracht.

## B05 Eigen scripts `lab/woz_*.py`; gedeelde scripts ongewijzigd
- **Besluit:** verzamelen, afbakenen, selectie en nakijken gebeuren in `lab/woz_zoek.py`, `lab/woz_afbakening.py`, `lab/woz_select.py` en `lab/woz_nakijk.py`. De rest van de keten draait ongewijzigd.
- Alternatief: `woz-belastingen` toevoegen aan de vaste lijst in `scripts/dom_select.py` (daar staat al een 'woz' met alleen een regex).
- Reden: werkafspraak 7. De regex in `dom_select.py` mist zaken zonder "WOZ" in de inhoudsindicatie, zoals proceskosten en immateriële schade, en neemt rijksbelastingen mee die alleen naar de WOZ-waarde verwijzen.
- Status: door Robert te bevestigen.
