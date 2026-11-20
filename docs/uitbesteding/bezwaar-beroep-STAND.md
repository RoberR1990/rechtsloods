# Bezwaar en beroep (Awb): STAND (20 nov 2026)
Branch `claude/project-thread-d3rjh5` (niet live; niet in site-index). Gepauzeerd op verzoek van Robert (tokenlimiet): laag 2 en site-data niet gestart.

## Stappen
- [x] 0 Oriëntatie. Repo = snapshot van live; geen `live`-branch, geen data/feeds, geen data/dom, geen docs/uitbesteding. Feeds opnieuw opgehaald. Wel aanwezig: scripts/dom_*.py, check_l1.py, toon_l1.py, maak_in_l1.py, lab/*.
- [x] 1 Verzamelen: Open Data Rechtspraak 2016-2026, RvS + CRvB + CBb + Rb Rotterdam (bestuursrecht), selectie op titel + inhoudsindicatie (±400 tekens). **3.443 kandidaten** (CRvB 1.744, RvS 600, Rb Rotterdam 659, CBb 440). Precisie steekproef 100 (Haiku): 76 ja / 9 randje / 15 nee vóór aanscherping; nee-bronnen (dwangsom bij handhaving, proceskosten-boilerplate) eruit. Overlap: 746 kandidaten raken sociaal (636), parkeren/belasting (81+25), openbare orde (12), AVG (18).
- [x] 2 Taxonomie (6 onderwerpen, 29 subonderwerpen), uitkomstregels, besluiten: `data/dom/bezwaar-beroep/{config,taxonomie,argumenten}.json`, `bezwaar-beroep-besluiten.md`. Reviewpunt 1 zelf doorlopen (zie besluiten).
- [x] 3 Laag 1 (Haiku): 3.443 uitspraken, 138 batches, **check_l1 0 fouten**. Relevant 3.158, niet relevant 285. Zekerheid: hoog 1.555, middel 1.392, laag 211. Per onderwerp: termijn/verschoonbaar 1.086, lus 725, motivering 500, dwangsom 422, proceskosten 265, hoorplicht 160. Uitkomst: wederpartij wint 1.327, burger wint 1.051, deels 429, alleen procedure 351. Uitvoer: `data/uit_l1/bezwaar-beroep/`.
- [ ] 4 Selectie laag 2 (RvS + Rotterdam, max ±200) en reviewpunt 2
- [ ] 5 Laag 2 (Sonnet), checks, blinde steekproef
- [ ] 6 Nakijkronde uitkomstregels
- [ ] 7 Stand per onderwerp
- [ ] 8 Site-data (dom_build.py), feeds, privacy-scan, test
- [ ] 9 Overdracht

## Verbruik laag 1
46 Haiku-agents (pilot 129k tokens/25 uitspraken = 5,2k per uitspraak; golven ±230-320k per 75 = ±3,2-4,3k per uitspraak; richtwaarde 3,6k). Totaal ≈ 11-12M tokens Haiku.

## Open punten
- 285 'niet relevant' bevat ±25 tussenuitspraken waarvan het dictum ontbrak in de invoer (maak_in_l1 pakt het dictum niet bij tussenuitspraken). Volgens de regel hoort dat 'zekerheid laag' te zijn, niet laten vallen: nog herstellen (script: ECLI's met reden 'dictum/beslissing' terugzetten als relevant met onderwerp bestuurlijke-lus, zekerheid laag).
- Precisie na aanscherping niet opnieuw gemeten (aanname ±90%; laag 1 'niet relevant' = 8%).
- Proceskosten dun (265): inhoudsindicatie noemt het zelden. Uitbreiden vereist volledige-tekst-selectie.
- Extra bronnen (Awb, Besluit proceskosten, Kamerstukken, Behoorlijkheidswijzer): niet opgehaald, host geblokkeerd in de cloudomgeving.
- Overlap met Sociaal domein (±636 CRvB-zaken, WIA/bijstand-procedure): niet publiceren zonder FG-akkoord Sociaal domein, of filteren bij live zetten.

## Domeinafbeelding
Placeholder ontbreekt nog (`site/assets/dom-bezwaar-beroep.webp`, 1100x825). ChatGPT-prompt (docs/huisstijl.md): "Platte vectorillustratie, dunne donkerblauwe contourlijnen (#1F2F44), vlakken in petrol #0F5C63 en zeer licht grijsblauw #E2E6E6, één oranje accent #A84A00, witte achtergrond, 4:3, geen tekst, geen groen. Een ambtenarenbureau: een bureau met een dossiermap, een kalender met omcirkelde datum en een weegschaal; generiek Nederlands, geen herkenbare Rotterdamse bouwwerken." Daarna `python3 -I tools/herkleur_afbeeldingen.py <bestand>`.

## Let op: juiste repo
Deze PR staat in RoberR1990/rechtsloods (publieke snapshot). De site draait waarschijnlijk vanaf RoberR1990/rechtzoeker (branch `live`). Bij hervatten: werk daar verder (branch bezwaar-beroep vanaf live) en neem `scripts/bezwaar/`, `data/dom/bezwaar-beroep/` en `data/uit_l1/bezwaar-beroep/` van deze branch over.

## Volgende actie
1. Tussenuitspraken-zonder-dictum herstellen (klein script).
2. Selectie laag 2 (`scripts/dom_select`-patroon, RvS + Rb Rotterdam, ±200), kostenschatting.
3. Laag 2 met Sonnet volgens lab/vangnet_v3.md, daarna stap 6-9.
Werkplek: scripts verwachten /home/claude/{data,site,scripts}; zie memory `rechtsloods-bezwaar-beroep`. Scratch (xml, uitspraken.json) niet in repo; opnieuw te maken met `scripts/bezwaar/fetch_xml.py` + `scripts/dom_parse.py`.
