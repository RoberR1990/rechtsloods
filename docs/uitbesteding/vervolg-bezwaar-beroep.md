# Startprompt: Bezwaar en beroep afronden (Rechtsloods)

Doel: domein Bezwaar en beroep (Awb-procedures) afmaken en reviewklaar maken in RoberR1990/rechtsloods. Scope: dwangsom bij niet tijdig beslissen, bezwaartermijn en verschoonbare termijnoverschrijding, hoorplicht, motivering, proceskostenvergoeding/forfait, bestuurlijke lus. Werk autonoom, kies omkeerbare keuzes zelf (aanbevolen optie, vastleggen in docs/uitbesteding/bezwaar-beroep-besluiten.md), bundel vragen aan Robert in één bericht. Live zetten, FG/privacy en extra kosten blijven Roberts beslissing. Nederlands, beknopt. Geen Workflow-tool zonder expliciete opt-in.

## Stand (22 nov 2026)
- Branch `claude/project-thread-d3rjh5` in RoberR1990/rechtsloods, laatste commit 1afd2c4 (daarna deze file). Draft PR #1. Niet live; main is snapshot. De site draait waarschijnlijk uit RoberR1990/rechtzoeker (branch live): vaststellen voor je iets overbrengt.
- Laag 1 klaar: 3.443 kandidaten (RvS, CRvB, CBb, Rb Rotterdam 2016-2026; 6 Awb-thema's), data/uit_l1/bezwaar-beroep/, 0 checkfouten.
- Laag 2 klaar: 200 samenvattingen (Rb Rotterdam 100, RvS 61, dunne onderwerpen 39) in data/uit_v3/bezwaar-beroep/; check_uit_v3: 0 fouten, 7 LET OP-waarschuwingen (uitkomst vs. dictum; 2024_6777 en 2026_2293 handmatig nalopen, de rest is verdedigbaar). 197 relevant, 3 niet relevant.
- Afbeelding site/assets/dom-bezwaar-beroep.webp staat (Roberts illustratie, 1100x825).
- Docs: docs/uitbesteding/bezwaar-beroep-STAND.md en -besluiten.md (besluiten 1-15). Kopie in /mnt/project-files/rechtsloods-bezwaar-beroep/.

## Nog te doen (volgorde)
1. Tussenuitspraken (~25) zonder dictum in laag 1 staan als niet relevant; moeten relevant/zekerheid laag zijn: herstellen.
2. Blinde 10%-steekproef op laag 2, regels bijstellen indien nodig.
3. Precisie na aanscherping select.py opnieuw steekproeven (proceskosten dun: 265).
4. Stand in het kort per onderwerp (stand_dom.py), site-data (dom_build.py), privacyscan (geen namen, adressen, geboortedata, medische details).
5. Overlap met Sociaal domein (~636 CRvB-zaken): alleen laag 1, geen laag 2, gemarkeerd bij publicatie.
6. Overdrachtsnotitie + STAND bijwerken, PR #1 in sync houden, één reviewbericht aan Robert.

## Werkplek
- Scripts verwachten /home/claude/{data,site,scripts}: maak symlinks naar een datamap en de repo. lab/extra_check.py verwacht data/in_v3 in de repo (symlink).
- Alleen data.rechtspraak.nl is bereikbaar vanuit de cloudomgeving; gebruik curl (urllib faalt via de proxy).
- Ruwe feeds/XML (110 MB) staan niet in git. Opnieuw ophalen: `python3 scripts/bezwaar/feeds.py` (idempotent, output <werkmap>/feeds/<k><jaar>.json), daarna scripts/bezwaar/select.py, fetch_xml.py (parallel XML). Selectie laag 2: selecteer_l2.py.
- Subagents: Haiku laag 1 (~5,2k tokens/uitspraak), Sonnet laag 2 (~25k/uitspraak), golven van max 10, 0 fouten voor je doorgaat, alleen Bash/Read/Write. Instructies: scripts/bezwaar/verrijk_l1_bezwaar.md en verrijk_v3_bezwaar.md.
- Alleen pushen naar de eigen branch; PR-body begint met attributieregels en eindigt met sessielink; geen modelnamen in commits/code.

## Open vraag voor Robert (bundelen)
Netwerk van omgeving 'rechtzoeker' verruimen voor wetten.overheid.nl (Awb, Besluit proceskosten bestuursrecht), Kamerstukken (Wet dwangsom, Wet bestuurlijke lus), Ombudsman/Behoorlijkheidswijzer. Zonder dit werkt het domein, maar zonder wetsbronnen. Daarnaast: live zetten pas na zijn review.
