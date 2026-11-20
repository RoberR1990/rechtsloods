# STAND sociaal domein (slug `sociaal-domein`)

**Niet publiceren zonder FG-akkoord.** Branch: `col/sociaal-domein` (repo `RoberR1990/rechtsloods`, zie besluit B1).

## Volgende actie
Stap 3 voorbereiden (tooling klaarzetten), daarna BLOKKADE (zie onder).

## Stappen
- [x] 0 Oriëntatie
- [x] 1 Verzamelen en afbakenen: 16.499 kandidaten (CRvB 10.789; Rb Rotterdam 699; overige rechtbanken 4.790; RvS 109; hoven 76; HR/PHR 32; civiel 134). Precisie 98,3% (onafhankelijke steekproef van 60). Check `sociaal_select.py --check`: 0 fouten. Zie `sociaal-domein-tellingen.md`.
- [x] 2 Taxonomie en uitkomstregels bevriezen: 8 onderwerpen, 29 subonderwerpen, 25 argumenten, 9 zaaktypen, 10 uitkomstregels, 6 privacyregels. Check `lab/sociaal_taxonomie.py check`: 0 fouten. Label "eerste versie", `concept: true`.
- [ ] 3 Laag 1 (labels)
- [ ] 4 Selectie laag 2
- [ ] 5 Laag 2
- [ ] 6 Nakijkronde uitkomstregels
- [ ] 7 De stand in het kort
- [ ] 8 Site-data en feeds
- [ ] 9 Overdracht

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
| 2 | eigen context ±30k | eigen context (150 inhoudsindicaties gelezen, ±25k) |
| 1 | Haiku-precisie: 2 agents, ±200k | 1 agent op 200 uitspraken: 145k tokens. 1 agent op 60 (onafhankelijk): 85k tokens. Feeds: 22 downloads, ±440k feedregels |

## Laatste commit
(volgt)
