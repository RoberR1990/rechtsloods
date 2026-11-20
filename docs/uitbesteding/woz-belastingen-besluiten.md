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

## B06 Afbakening: inhoudsindicatie plus volledige tekst
- **Besluit:** de kandidaten komen uit de feeds `bestuursrecht_belastingrecht` 2016-2026 (47.364 uitspraken). Er zijn twee bakken (`lab/woz_zoek.py`). De eerste bak (8.892) heeft een WOZ-term in de titel of inhoudsindicatie; dat is dezelfde regex als de verkenning. De tweede bak (2.227, "breed") heeft geen WOZ-term, maar wel een WOZ-achtig begrip (waardepeildatum, taxatieverslag, heffingsambtenaar, proceskosten, immateriële schade, gemachtigde, ...) en geen marker van een andere belasting. Daarna beslist de volledige tekst (`lab/woz_afbakening.py`). Een uitspraak gaat erin als er een WOZ-term in de tekst staat, er een gemeentelijk orgaan in voorkomt en het geen rijkszaak is ("inspecteur" en geen heffingsambtenaar of college in de kop). Voor de brede bak zijn ≥ 2 WOZ-termen nodig. Bij een andere-belastingmarker in de kop zijn ≥ 3 WOZ-termen nodig. Resultaat: 9.653 (8.756 regex + 898 breed − 1 dubbel).
- Alternatief: alleen de regex op de inhoudsindicatie (8.892), zoals de verkenning.
- Reden: zaken over proceskosten, immateriële schade en gemachtigden noemen "WOZ" vaak niet in de inhoudsindicatie (bijv. HR "No cure no pay staat niet in de weg aan ... immateriële schade"). Juist die zaken zijn de kern van de business case. Rijkszaken die alleen naar de WOZ-waarde verwijzen (IB, erfbelasting, verhuurderheffing) vallen eruit.
- Precisie (steekproef van 100, Haiku, 15 zelf nagelopen plus de 5 twijfelgevallen op de volledige tekst): 98%. In 40 afgevallen pool-uitspraken zat geen relevante zaak binnen de scope. De resterende valse treffers (o.a. vennootschapsbelasting, rioolheffing) markeert laag 1 als `relevant: false`.
- Status: door Robert te bevestigen.

## B07 Caribisch Nederland en Curaçao buiten de scope
- **Besluit:** de onroerendezaakbelasting van Curaçao en de vastgoedbelasting van Bonaire (OGEAC, OGHACMB) horen niet bij het domein.
- Alternatief: opnemen als "waardegeschil".
- Reden: de Wet WOZ en de Gemeentewet gelden daar niet, en de wederpartij is de inspecteur. Haiku zette er 2 op relevant; dat heb ik zelf gecorrigeerd.
- Status: door Robert te bevestigen.

## B08 BPM-zaken over de "Wet herwaardering proceskostenvergoeding WOZ en bpm" buiten de scope
- **Besluit:** uitspraken over proceskosten in een BPM-zaak (bijv. HR 26 september 2025, ECLI:NL:HR:2025:1378) horen niet bij dit domein, ook als ze dezelfde wet toepassen.
- Alternatief: opnemen als bron voor de proceskosten in WOZ-zaken.
- Reden: BPM is een eigen domein (scope-afspraak). Ik noem het als beperking in de overdracht: de HR-lijn over deze wet loopt deels via BPM-zaken.
- Status: door Robert te bevestigen.
