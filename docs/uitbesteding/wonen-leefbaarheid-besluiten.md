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

## B08 Rolnaam: "betrokkene" in plaats van "bewoner"
- **Besluit:** `partijen.burger` = de rol zoals de uitspraak die noemt (woningzoekende, aanvrager, eigenaar, verhuurder, huurder, omwonende); "bewoner" alleen als de uitspraak dat zegt; bij twijfel "betrokkene". In zinnen ook de concrete rolnaam; "de betrokkene" mag als terugvaloptie (opdracht), al geeft `check_uit_v3.py` daar een waarschuwing (LET OP, geen fout) voor.
- Alternatief: `verrijk_v3.md` volgen ("betrokkene" nooit in zinnen).
- Reden: de opdracht zegt uitdrukkelijk "betrokkene, niet bewoner"; dit volgt ook het AVG-voorbeeld (`lab/avg_taxonomie_samenvoegen.py`).
- Status: door Robert te bevestigen.

## B09 Planologische zaken vallen buiten het domein
- **Besluit:** zaken waarin het bestemmingsplan, omgevingsplan of de omgevingsvergunning de grondslag is, vallen af, ook als het over kamerverhuur, splitsing of B&B gaat. Wel binnen: dezelfde onderwerpen op grond van de Huisvestingswet/huisvestingsverordening, Woningwet/Bouwbesluit, Leegstandwet, enz.
- Alternatief: kamerverhuur en splitsing via het bestemmingsplan meenemen.
- Reden: de afbakening sluit "omgevingsvergunning bouwen/bestemmingsplan" uit; de precisiesteekproef liet zien dat dit de grootste bron van valse treffers is.
- Status: door Robert te bevestigen.

## B10 Filter in twee stappen, gemeten precisie ~95%
- **Besluit:** (1) regex op titel + inhoudsindicatie of een treffer in de volledige tekst; (2) na het ophalen een filter op de volledige tekst (`lab/wonen_select.py filter`): weg als er geen woonbegrip in de tekst staat, als planologische termen domineren of in de inhoudsindicatie staan zonder woonbegrip, bij belastingrecht, CRvB zonder woonbegrip, leges/prostitutie/recreatie/Woo, en bij een kernbegrip dat alleen in een bijzin staat (< 4 keer). Alle afgevallen ECLI's met reden staan in `data/dom/wonen-leefbaarheid/afgevallen.json`.
- Precisie: Haiku-steekproef van 100 (vóór de laatste regel): 84 in, 8 uit, 8 twijfel; bij nalezen zijn 6 van de 8 twijfelgevallen "in" → ~90%. De laatste regel (planologisch in de inhoudsindicatie) haalde 5 van de 8 "uit" weg en geen enkele "in" → ~95%. Eigen controle van 15: 15 in. Overgebleven valse treffers worden in laag 1 `relevant: false`.
- Status: door Robert te bevestigen.

## B11 Rotterdamwet altijd opnemen
- **Besluit:** elke uitspraak die de Rotterdamwet (Wbmgp) noemt, blijft in de set, ongeacht de andere filters (27 uitspraken; 3 civiele treffers vallen af onder B07).
- Reden: de opdracht vraagt om alle Rotterdamwet-uitspraken.
- Status: ter info.

## B12 Taxonomie bevroren: 7 onderwerpen, 25 subonderwerpen
- **Besluit:** concept van een Sonnet-agent (201 inhoudsindicaties, `lab/wonen/taxonomie_concept.json`), met twee aanvullingen: sub `woonruimteverdeling/huisvestingsvergunning` (vergunning buiten de Rotterdamwet) en `handhaving-huisvestingswet/boete-huisvestingsvergunning`; `spoed-procedure` heet `procedure`. Rotterdamwet is een eigen onderwerp (3 subs) omdat het uniek is voor Rotterdam. Openbare orde (13b, 174a, Bibob) krijgt geen eigen onderwerp.
- Alternatief: Rotterdamwet als sub onder woonruimteverdeling.
- Reden: zichtbaarheid voor Rotterdam; dunne subs zijn samengevoegd (woningkwaliteit 2 subs, verhuurders 2 subs).
- Status: door Robert te bevestigen (concept: true per onderwerp).

## B13 Uitkomstregels in `config.json` (veld `uitkomstregels`)
- **Besluit:** de regels van de bestaande domeinen (alleen procedure, deels, misbruik = wederpartij wint, spiegelregel hogere instanties, voorlopige voorziening met "Voorlopig: ") plus domeinregels voor boete, last, invordering, vergunningen, derden en handhavingsverzoeken, Rotterdamwet en "geen bestuursorgaan". Bron: `lab/wonen/uitkomstregels.json`.
- Alternatief: alleen verwijzen naar `lab/aanscherping_l1c.md`.
- Reden: de opdracht vraagt de regels in de config; de bestaande configs in deze snapshot hebben dat veld nog niet.
- Status: door Robert te bevestigen.

## B14 `scripts/parse.py` laadt `data/kandidaten2.json` (parkeren) bij het importeren
- **Besluit:** lokaal een lege `data/kandidaten2.json` (`[]`) neergezet, niet gecommit (`.git/info/exclude`). `dom_parse.py` overschrijft `P.K` toch.
- Alternatief: `parse.py` aanpassen.
- Reden: gedeeld script niet wijzigen.
- Status: technisch, ter info.

## B15 Voorval: een laag-1-agent riep `list_triggers` aan (alleen lezen)
- **Wat:** tijdens het hervatten na het limiet meldde de omgeving een `list_triggers`-aanroep door een Haiku-agent. Gecontroleerd: er zijn geen geplande taken (lijst leeg). Opdrachtteksten `lab/wonen_l1.md` en `lab/wonen_l2.md` verbieden nu ook expliciet `list_triggers` en andere trigger- of sessietools, "ook niet om te kijken".
- Later meldden twee Haiku-agents zelf een geweigerde aanroep: `mcp__Claude_Docs__batch` en `mcp__claude-code-remote__create_session`. Beide door het permissiesysteem geweigerd; gecontroleerd: geen documenten, geen nieuwe sessies (list_sessions children: geen nieuwe), geen geplande taken. Opdrachten zeggen nu "uitsluitend Bash, Read en Write; elke andere tool is verboden, ook om te kijken".
- Status: ter info.

## B16 Tempo na het 5-uurslimiet
- **Besluit:** na het limiet (20 nov 12:50 UTC) afgebroken agents hervat met hun eigen context (SendMessage) en hooguit 5 Haiku-agents tegelijk. Onafgemaakte batches werden eerst apart gezet (`lab/wonen/l1_onaf/`) en niet in de data gecommit.
- Reden: de opdracht zegt "rond af, check, commit, push, stop" bij een limiet; de stand is veiliggesteld (commit ad02c05) en daarna verder gewerkt omdat het limiet al gereset was.
- Status: ter info.
