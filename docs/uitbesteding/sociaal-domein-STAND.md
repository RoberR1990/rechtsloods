# STAND sociaal domein (slug `sociaal-domein`)

**Niet publiceren zonder FG-akkoord.** Branch: `col/sociaal-domein` (repo `RoberR1990/rechtsloods`, zie besluit B1).

## BLOKKADE
**BLOKKADE: stap 3–8 niet uitgevoerd.**
- **Oorzaak:** de doelrepo `RoberR1990/rechtzoeker` (privé) is voor deze sessie niet bereikbaar. `add_repo` gaf "you don't have access" en `list_repos` toont alleen `rechtsloods`. De enige schrijfbare repo, `RoberR1990/rechtsloods`, is **openbaar**. Labels, samenvattingen, citaten, stand en site-data per uitspraak zouden daar vóór FG-akkoord gepubliceerd worden. Dat botst met de harde privacyregel (B3).
- **Geprobeerd:**
  - `add_repo` voor `rechtzoeker`, met `push`-toegang;
  - `list_repos`.
- **Wel gedaan, zonder publicatierisico:**
  - stap 0–2 volledig;
  - alle tooling voor stap 3–8 klaargezet en getest: 1.260 teksten geparsed, selectie op proeflabels, sitetest op een bestaand domein;
  - proef laag 1 (25) en laag 2 (2) om opdrachten en checks te valideren. Die uitvoer is verwijderd, niet gecommit.
- **Oplossing:** sessie met `rechtzoeker` gekoppeld, deze branch binnenhalen, verder bij "Volgende actie".

## Volgende actie (in `rechtzoeker`, na het binnenhalen van deze branch)
1. `bash scripts/sociaal_feeds.sh && python3 -I scripts/sociaal_select.py`: verwacht 16.499 kandidaten, `FOUTEN: 0`.
2. `python3 -I scripts/sociaal_prep.py links && python3 -I scripts/sociaal_prep.py fetch 6 && python3 -I scripts/sociaal_prep.py parse && python3 -I scripts/sociaal_prep.py in`.
3. `python3 -I lab/sociaal_bijlagen_check.py`: verwacht `GERAAKT: 0`. Zo niet, melden in de overdracht.
4. Laag 1: Haiku-agents met `lab/sociaal_l1_opdracht.md`, 3 batches per agent, op volgorde van `data/batches/l1_sociaal-domein.json`. Per batch `check_l1.py`: 0 fouten. Daarna `python3 -I lab/sociaal_l1_nacontrole.py lijst` en de herzienbatches (`-hz-`) draaien.
5. `python3 -I lab/selecteer_sociaal_l2.py`, daarna laag 2 met `lab/sociaal_v3_opdracht.md` (Sonnet, 1 batch van 6 per agent).
6. `python3 -I lab/sociaal_steekproef.py trek 10`, beoordelaars met `lab/sociaal_steekproef_opdracht.md`, dan `score`. Herstel alles wat "ernstig" is.
7. `python3 -I lab/sociaal_nakijk_uitkomst.py lijst`, Sonnet-agent beoordeelt de lijst, dan `toepas`, en de checks opnieuw.
8. `python3 scripts/dom_build.py sociaal-domein --geen-embed`, dan `lab/stand_dom.py prep|samen sociaal-domein` met `lab/stand_opdracht.md`, dan `python3 -I lab/sociaal_site_na.py`. Daarna `scripts/maak_feeds.py` (de feed komt alleen mee als status ≠ binnenkort; alleen op de eigen branch) en `node lab/sociaal_sitetest.js sociaal-domein`.

## Stappen
- [x] 0 Oriëntatie
- [x] 1 Verzamelen en afbakenen: 16.499 kandidaten (CRvB 10.789; Rb Rotterdam 699; overige rechtbanken 4.790; RvS 109; hoven 76; HR/PHR 32; civiel 134). Precisie 98,3% (onafhankelijke steekproef van 60). Check `sociaal_select.py --check`: 0 fouten. Zie `sociaal-domein-tellingen.md`.
- [x] 2 Taxonomie en uitkomstregels bevriezen: 8 onderwerpen, 29 subonderwerpen, 25 argumenten, 9 zaaktypen, 10 uitkomstregels, 6 privacyregels. Check `lab/sociaal_taxonomie.py check`: 0 fouten. Label "eerste versie", `concept: true`.
- [ ] 3 Laag 1 (labels): BLOKKADE. Tooling klaar, proef van 25: 0 fouten
- [ ] 4 Selectie laag 2
- [ ] 5 Laag 2
- [ ] 6 Nakijkronde uitkomstregels
- [ ] 7 De stand in het kort
- [ ] 8 Site-data en feeds
- [x] 9 Overdracht: `sociaal-domein-overdracht.md`

## Stap 0: bevindingen
1. Doelrepo `RoberR1990/rechtzoeker` is voor deze sessie niet bereikbaar. Alleen `RoberR1990/rechtsloods` hangt eraan. Die repo is **openbaar**: het is de export van de werkrepo via `scripts/export-openbaar.sh` (B1, B3).
2. Er bestaan geen branches `live` of `woo-uitdiepen`. `main` is de "snapshot live, 16 nov 2026" plus 3 huisstijlcommits (B2).
3. Ontbreekt hier: `docs/STAND.md`, `data/dom/<slug>/` (configs staan wel als kopie in `site/data/domeinen/<slug>/`), `data/raw`, `data/feeds` en het domein Woo (in `index.json` alleen als "binnenkort").
4. `site/data/domeinen/index.json` heeft al een regel `sociaal` (binnenkort, n=12792, telling op inhoudsindicatie). De opdracht vraagt slug `sociaal-domein` (B4).
5. De keten loopt als volgt: `dom_select` (feeds → kandidaten) → `dom_fetch` (XML) → `dom_parse` (uitspraken, prio, rotterdam) → `maak_in_l1` / `maak_in_v3` → agents (`verrijk_l1.md`, `verrijk_v3.md`, `lab/aanscherping_*c.md`) → `check_l1` / `check_uit_v3` / `lab/extra_check.py` → `dom_build` → `lab/stand_dom.py` → `maak_feeds`.
6. De scripts in `scripts/` gebruiken `/home/claude/data` (symlinks uit `setup.sh`). De scripts in `lab/` werken repo-relatief. `lab/vangnet_*.md` verwijzen naar `/home/claude/rechtzoeker/...`.
7. Het schema is v3 (`docs/schema_v3.md`), met datacontract `docs/datacontract.md`. Config-velden: slug, label, zaaktype, bezwaargronden_verplicht_bij, raakt, toepasselijkheid, rollen, klantuitleg_vraag en rubrieken.
8. Uitkomstregels in de repo: `lab/aanscherping_l1c.md` / `v3c.md` (alleen procedure, deels, belastingzaken). De regels voor misbruik, spiegel en voorlopige voorziening staan alleen in de opdracht. Ik neem ze daaruit over.
9. De bron data.rechtspraak.nl is bereikbaar. wetten.overheid.nl wordt geblokkeerd door het netwerkbeleid; voor stap 0–2 is dat niet nodig.
10. CRvB-titels dragen een wetscode in het zaaknummer (PW, WWB, WMO15, BBZ, IOAW, ...). Dat is een sterk filter voor de hoogste instantie.
11. Rechtbanktitels hebben geen wetscode. Voor rechtbanken filter ik op de inhoudsindicatie.
12. `scripts/maak_in_v3.py` ("Bijlagen:"-bug): de impact kan pas gemeten worden met volledige teksten (zie stap 1, steekproef).
13. Het tokenverbruik per stap staat hieronder. Richtwaarden: laag 1 ~3,6k per uitspraak, laag 2 ~25–30k, stand ~100k per agent.
14. De privacyregel "blijft op eigen branch" gaat uit van een privé-repo. Hier is de repo openbaar. Daarom zet ik geen inhoud per uitspraak in de repo (B3).
15. Bestaande domeinen om overlap mee te markeren: parkeren (`site/data/meta.json`), avg-privacy, openbare-orde, verkeersboetes en bpm (`site/data/domeinen/*/meta.json`).

## Verbruik (schatting → werkelijk)
| stap | schatting | werkelijk |
|---|---|---|
| 0 | eigen context | — |
| proef | — | Haiku laag 1: 158,6k / 25 uitspraken. Sonnet laag 2: 109,7k / 2 uitspraken. Alle checks 0 fouten |
| 2 | eigen context ±30k | eigen context (150 inhoudsindicaties gelezen, ±25k) |
| 1 | Haiku-precisie: 2 agents, ±200k | 1 agent op 200 uitspraken: 145k tokens. 1 agent op 60 (onafhankelijk): 85k tokens. Feeds: 22 downloads, ±440k feedregels |

## Laatste commit
6568a3b (plus deze STAND-update)
