# Wonen en leefbaarheid: besluiten tijdens de bouw

Elk besluit: **besluit**, alternatief, reden, status. Alles is "door Robert te bevestigen" tenzij anders vermeld.

## B01 Repo: `rechtsloods` in plaats van `rechtzoeker`
- **Besluit:** gebouwd in `RoberR1990/rechtsloods`, branch `col/wonen-leefbaarheid`, vertrokken vanaf `main`.
- Alternatief: stoppen met BLOKKADE omdat `rechtzoeker` niet bereikbaar is.
- Reden: deze sessie heeft alleen toegang tot `rechtsloods` (`add_repo rechtzoeker` geweigerd: geen toegang). `rechtsloods` is de openbare snapshot van `live` (commit "Import Rechtsloods uit privé-werkrepo (snapshot live, 16 nov 2026)"); er is geen branch `live` of `woo-uitdiepen`, `main` is dus het dichtstbijzijnde vertrekpunt. Alle scripts, opdrachtteksten en checks staan erin. De branch is over te zetten naar `rechtzoeker` (alleen nieuwe bestanden plus `site/data/domeinen/index.json`).
- Status: door Robert te bevestigen.

## B02 Voorbeelddomein: openbare-orde en avg-privacy in plaats van Woo
- **Besluit:** werkwijze en bestandsformaat volgen `openbare-orde` en `avg-privacy` (laag 1 + laag 2 + stand, live).
- Alternatief: Woo, zoals de opdracht noemt.
- Reden: Woo staat in deze snapshot op "binnenkort" (alleen een telling); `data/dom/woo/config.json` bestaat hier niet. Openbare orde en AVG zijn op dezelfde manier gebouwd.
- Status: door Robert te bevestigen.

## B03 Paden `/home/claude/...` via symlinks
- **Besluit:** `/home/claude/{data,scripts,site}` en `/home/claude/rechtzoeker` wijzen met symlinks naar de repo; de gedeelde scripts blijven ongewijzigd.
- Alternatief: paden in de scripts aanpassen.
- Reden: dezelfde aanpak als `setup.sh`; geen wijziging aan gedeelde scripts nodig.
- Status: technisch, ter info.

## B04 Geen OpenRouter-keten (`lab/pijplijn.py`)
- **Besluit:** laag 1 = Haiku-subagents met `scripts/verrijk_l1.md`, laag 2 = Sonnet-subagents die zelf schrijven met `scripts/verrijk_v3.md` + `lab/aanscherping_v3c.md` (zoals `lab/vangnet_v3.md`), stand = Sonnet met `lab/stand_opdracht.md`.
- Alternatief: `lab/pijplijn.py draai` (DeepSeek/Qwen via OpenRouter).
- Reden: de opdracht staat alleen Claude toe en geen API-sleutels.
- Status: volgt uit de opdracht.

## B05 Domeinspecifieke scripts in `lab/wonen_*.py`
- **Besluit:** verzamelen, filteren, selectie en nakijken in eigen scripts (`lab/wonen_zoek.py`, `lab/wonen_select.py`, ...), naar het voorbeeld van `scripts/dom_select.py` en `lab/selecteer_avg_c.py`.
- Alternatief: het nieuwe domein toevoegen aan de vaste lijst `DOM` in `scripts/dom_select.py`.
- Reden: gedeelde scripts niet wijzigen (werkafspraak 7). De rest van de keten (`dom_fetch`, `dom_parse`, `maak_in_l1`, `maak_in_v3`, checks, `dom_build`, `stand_dom`) wordt ongewijzigd gebruikt.
- Status: door Robert te bevestigen.

## B06 Bronnen: open-data-feeds plus de volledige-tekstzoeker van rechtspraak.nl
- **Besluit:** kandidaten = (a) bestuursrecht-feeds 2016-2026 van Open Data Rechtspraak (titel + inhoudsindicatie), gefilterd met een regex, plus (b) treffers uit de publieke zoekdienst van uitspraken.rechtspraak.nl (volledige tekst) voor kernbegrippen zoals de Rotterdamwet (`lab/wonen_zoek.py`, zelfde dienst als `scripts/harvest.py`).
- Alternatief: alleen de feeds (zoals bij andere domeinen).
- Reden: Rotterdamwet en huisvestingsverordening staan vaak alleen in de tekst, niet in de inhoudsindicatie. De opdracht vraagt om alle Rotterdamwet-uitspraken.
- Status: door Robert te bevestigen.

## B07 Alleen bestuursrecht
- **Besluit:** alleen uitspraken met rechtsgebied bestuursrecht (inclusief Raad van State en CRvB); civiele en strafzaken vallen af.
- Alternatief: ook civiele zaken waarin de gemeente partij is.
- Reden: de afbakening is bestuursrechtelijk (gemeente als bestuursorgaan); huurgeschillen en civiele zaken zonder gemeente vallen buiten de scope.
- Status: door Robert te bevestigen.
