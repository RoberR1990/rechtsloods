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

## B09 Uitkomstregels: BPM overgenomen, met WOZ-afwijkingen
- **Besluit:** de uitkomstregels staan in `config.json` (veld `uitkomstregels`, U1-U10; bron `lab/woz_uitkomstregels.json`). Overgenomen zijn de belastingregels van BPM uit `lab/aanscherping_l1c.md`: vernietigd = burger wint, gehandhaafd = wederpartij wint, hoger beroep van de fiscus dat slaagt = wederpartij wint, alleen kosten of immateriële schade = alleen procedure. Ook overgenomen zijn de regels uit de opdracht (misbruik = wederpartij wint, de spiegelregel en de voorlopige voorziening met "Voorlopig: "). Afwijkingen voor WOZ:
  1. **U3 Verlaging van de waarde:** BPM zegt "aanslag verminderd = deels". Voor WOZ geldt: verlaagd tot (of onder) wat de burger vroeg = "burger wint", verlaagd maar hoger dan wat de burger vroeg = "deels". Is de gevraagde waarde onbekend, dan "deels" met zekerheid "middel". Reden: bij WOZ is de waarde zelf het geschil, en "wie krijgt wat hij vroeg, wint".
  2. **U4 Vernietiging zonder gevolg voor de waarde:** het beroep is gegrond om de hoorplicht, art. 40 Wet WOZ of de motivering, maar de waarde blijft ("rechtsgevolgen in stand"). Dan geldt "alleen procedure". Dat komt in WOZ-zaken veel voor.
  3. **U5 Kostenzaken:** "alleen procedure" (zoals BPM), maar de toelichting begint met "Kosten: " en zegt wie het kostenpunt won. Reden: anders is de business case (proceskosten, no-cure-no-pay) niet te volgen in de uitkomstverdeling.
  4. **U9 Conclusie AG:** "alleen procedure", plus de markering `soort_document: "conclusie AG"` (advies), ook in laag 1.
  5. **U10 Cassatie met verwijzing:** cassatie van de burger slaagt = "burger wint", die van de heffingsambtenaar slaagt = "wederpartij wint", met zekerheid "middel".
- Alternatief: BPM-regels ongewijzigd.
- Reden: zie per punt.
- Status: door Robert te bevestigen.

## B10 Taxonomie: 5 onderwerpen, 22 subonderwerpen (concept)
- **Besluit:** de taxonomie volgt de Sonnet-agent (`lab/woz_taxonomie_opdracht.md`, steekproef van 226 inhoudsindicaties plus trefwoordtellingen over 9.653 zaken): `waardebepaling` (5), `niet-woningen` (4), `object-beschikking-ozb` (3), `procedure` (5), `proceskosten-gemachtigden` (5). Ik heb alle ankerartikelen nagelopen: ze staan letterlijk in de uitspraken (bijv. art. 17 Wet WOZ 8.092×, art. 40 Wet WOZ 5.901×, art. 30a Wet WOZ 1.630×). Erfpacht en herziening (art. 29) zijn te dun voor een eigen sub en staan als kenmerk elders.
- Alternatief: ±30 subs met eigen subs voor erfpacht, herziening en belanghebbende.
- Reden: elke sub moet in de data herkenbaar voorkomen. Dunne subs leveren in de stand alleen "te weinig" op.
- Status: door Robert te bevestigen. `concept: true` blijft staan tot een vakinhoudelijk collega de taxonomie heeft nagekeken.

## B11 "betrokkene" en "bewoner"
- **Besluit:** in `partijen.burger` (laag 1 en 2) komt wat de uitspraak zegt (eigenaar, huurder, bedrijf, gemachtigde-bureau). Is dat onduidelijk, dan "betrokkene". "Bewoner" alleen als de uitspraak dat woord gebruikt. In lopende zinnen staan de rolnamen uit `config.rollen` ("de eigenaar", "de gemeente").
- Alternatief: overal "betrokkene".
- Reden: de kwaliteitsregel uit de opdracht. `check_uit_v3.py` waarschuwt bij "betrokkene" in zinnen (jargonlijst van `verrijk_v3.md`), daarom gebruik ik het alleen in het partijveld.
- Status: door Robert te bevestigen.
