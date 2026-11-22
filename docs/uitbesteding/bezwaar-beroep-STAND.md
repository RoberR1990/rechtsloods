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

## Laag 2 (21 nov 2026)
- 200 samenvattingen (Rb Rotterdam 100 / RvS 61 / dunne onderwerpen 39) in data/uit_v3/bezwaar-beroep/; check_uit_v3: 0 fouten, 7 waarschuwingen (LET OP uitkomst vs. dictum, 6x Rb Rotterdam: termijn verschoonbaar + proceskosten, dus 'deels' verdedigbaar; 2024_6777 en 2026_2293 handmatig nalopen). 197 relevant, 3 niet relevant.
- Nog open: blinde 10%-steekproef, reparatie ~25 tussenuitspraken in laag 1, stand per onderwerp (stand_dom.py), site-data (dom_build.py) + privacyscan, netwerkverruiming (Robert).

## Vervolg 22 nov 2026 (omgeving zonder data.rechtspraak.nl)
- Stap 1 gedaan (offline): `scripts/bezwaar/herstel_tussen.py` zet 12 tussenuitspraken zonder dictum terug als relevant (bestuurlijke-lus, sub overig, zekerheid laag, uitkomst 'alleen procedure', `hersteld: true`, uitkomst_bron leeg). Niet hersteld: 2 TVL-tussenuitspraken, 1 geheimhoudingsbeslissing en 5 CRvB-zaken 'beslispassage ontbreekt' (type onbekend zonder brontekst). Onderwerp/uitkomst van de 12 zijn aannames: nalopen zodra bronteksten bereikbaar zijn; check_l1 verwacht uitkomst_bron en moet hiervoor een uitzondering op `hersteld` krijgen.
- Geblokkeerd tot netwerk 'rechtzoeker' (of data.rechtspraak.nl) beschikbaar is: blinde 10%-steekproef, precisie-steekproef proceskosten, handmatig nalopen 2024_6777 en 2026_2293, stand per onderwerp, site-data en privacyscan, overlap-markering Sociaal domein. Alle vereisen brontekst; de sessieomgeving is niet te verwisselen (sessie is door een andere sessie aangemaakt).

## Stand in het kort (22 nov 2026, op laag 2)
- `data/dom/bezwaar-beroep/stand/<onderwerp>.json` (6 bestanden, 0 citaatfouten via `scripts/bezwaar/check_stand_bb.py`; invoer via `prep_stand_bb.py`, instructie `stand_instructie_bb.md`). Gebouwd op de 197 relevante laag 2-samenvattingen (geen inhoudsindicaties), dus een steekproef: zwaar Rb Rotterdam en RvS, 2024-2026. Lijnen: vaste-lijn voor de meeste subonderwerpen, hr-lijn alleen dwangsom/hoogte-maximum, 'weinig' bij hoorzitting-verloop, overig, invulling-herstel, derdebelanghebbende, vaststelling-uitbetaling, proceskosten-beroep; motiveringsplicht losse-uitspraken.
- Aandachtspunten: veldnaam `steunt_parkeerder` = burger/belanghebbende (schema uit parkeren; hernoemen bij site-koppeling); parkeerzaken zijn bewust niet als bron gebruikt; hoorzitting-verloop (3 uitspraken) kreeg 'weinig' volgens regel; RVS:2026:6820 jaartal controleren; subonderwerpen overlappen op griffierecht.
- Nog open (alle brontekst/netwerk): blinde steekproef 10%, precisie proceskosten, nalopen 2024_6777 en 2026_2293, check_l1-uitzondering voor `hersteld`, site-data (dom_build) + privacyscan, overlap Sociaal domein markeren, wetsbronnen. Live pas na review Robert.

## Afronding open punten (22 nov 2026, netwerk data.rechtspraak.nl weer bereikbaar)
Bereikbaar: data.rechtspraak.nl, gegevensmagazijn.tweedekamer.nl (200), repository.overheid.nl (302). Niet bereikbaar: wetten.overheid.nl, tweedekamer.nl (webpagina's), officielebekendmakingen, nationaleombudsman.nl. Wetsbronnen (Awb, Besluit proceskosten, Behoorlijkheidswijzer) dus nog niet opgehaald.
- **Blinde 10%-steekproef laag 2** (20 van 200, blind eigen uitkomst bepaald, Sonnet): 13 goed, 7 klein, 0 ernstig; alle 7 hersteld, check 0 fouten. Kleine fouten: omgedraaide toelichting (RBROT:2023:10028), bezwaargrond-code, ontbrekend gevolg dwangsom (CRVB:2026:142) e.a. Eén privacyvondst (daklozenstatus in `partijen.burger`, RBROT:2024:5580) verwijderd. Regels niet bijgesteld.
- **Nalopen 2024_6777 en 2026_2293**: beide 'beroep gegrond, rechtsgevolgen in stand, griffierecht + proceskosten vergoed'. Label 'wederpartij wint' paste niet bij de regel 'deels'. Gewijzigd naar deels. Zelfde patroon was inconsistent gelabeld in RBROT:2024:11623 en 2026:1941 (burger wint): ook deels. Laag-2-patroon 'vernietigd + in stand' is nu: 11 deels, 3 burger wint (echt andere zaken: dwangsom/plan vernietigd), 0 wederpartij wint.
- **12 herstelde tussenuitspraken** gecontroleerd tegen het dictum ("stelt in de gelegenheid het gebrek te herstellen / houdt beslissing aan"): alle 12 bestuurlijke lus, nu sub toepassing-lus / lus-toegepast, zekerheid hoog, `uitkomst_bron` gevuld, `dictum_gecontroleerd: true`. Nog niet hersteld (5 CRvB 2016, TVL-aanvraag CBB:2024:670, geheimhouding CBB:2020:776) blijven bewust uit.
- **Precisie proceskosten** (40 uit 265, Haiku): 22 ja, 18 randje (alleen standaardbeslissing, geen redenering), 0 nee. Strikt 55%, ruim 100%. Uitkomstlabel 2 fout (RBROT:2024:5235 -> burger wint; CBB:2021:687 -> deels) en 2 onzeker (CBB:2021:224/696 -> deels): alle 4 aangepast. Advies: randje blijft zichtbaar maar het subonderwerp 'proceskosten' is dun; toon het met 'beperkte onderbouwing'.
- **Privacyscan** over alle 200 laag-2-bestanden (postcode, geboortedatum, BSN, straat+nummer, titel+naam, initialen, medische termen): geen adressen, geboortedata of namen. Aanwezige `[adres 1]`-vormen zijn de anonimisering van de rechtbank. Medische woorden vooral instellingen en procedure (medisch advies, arbeidsongeschiktheid, gehandicaptenparkeerkaart): geen diagnose of status herleidbaar; voor FG-inzage: CRVB:2021:2646 (ziekte bij ziekenhuismedewerker), RBROT:2024:3131 (gehandicaptenparkeerkaart), RBROT:2024:6104 (Sociaal Medische Indicatie).
- **Overlap Sociaal domein**: `overlap` zit in kandidaten.json (636 sociaal). Geen enkele laag-2-samenvatting hoort daar bij. In de site-data is `overlap` toegevoegd aan verrijkt.json en is de **volledige tekst van die 636 niet opgenomen** (config `sociaal_tekst_weren`; dom_build.py aangepast). Alleen labels blijven; tekst pas na FG-akkoord Sociaal domein.
- **Site-data** `site/data/domeinen/bezwaar-beroep/` (3.443 uitspraken, 200 laag 2, 36 MB, citaten 0 weggevallen buiten 2694 ok/herstel). **Niet in `site/data/domeinen/index.json`** gezet (dom_build zou 'live' zetten): toevoegen = live zetten, besluit van Robert.
- Nog open: wetsbronnen (netwerk), jurist-toets, live na review Robert, hernoemen veld `steunt_parkeerder` bij site-koppeling.
