# Overdracht domein Sociaal domein (`sociaal-domein`)

> **Niet publiceren zonder FG-akkoord.**
> **BLOKKADE** na stap 2: stap 3–8 zijn niet uitgevoerd. De doelrepo `rechtzoeker` (privé) is voor deze sessie niet bereikbaar. De enige beschikbare repo, `rechtsloods`, is openbaar. Domeininhoud per uitspraak (labels, samenvattingen, citaten, stand) zou daarmee vóór FG-akkoord gepubliceerd zijn. Zie besluit B3.

## Status
- Branch: `col/sociaal-domein` in `RoberR1990/rechtsloods`, vanaf `main` (db7c004). Laatste commit: zie `git log -1 col/sociaal-domein`. De commit-hash staat ook in de STAND.
- Klaar en gecontroleerd:
  - stap 0 oriëntatie;
  - stap 1 afbakening en tellingen;
  - stap 2 taxonomie, uitkomstregels en config (label "eerste versie");
  - tooling voor stap 3–8, getest op 1.260 teksten en een proef van 25 + 2 uitspraken. De uitvoer daarvan is niet bewaard.
- Open: stap 3–9 uitvoeren in de privé-werkrepo. Elke stap staat met het exacte commando in `sociaal-domein-STAND.md` onder "Volgende actie".
- Hervatten in `rechtzoeker`:
  ```
  git fetch https://github.com/RoberR1990/rechtsloods col/sociaal-domein && git checkout -b col/sociaal-domein FETCH_HEAD
  ```
  of cherry-pick de commits op `live`. Daarna hervatten bij "Volgende actie".

## Besluiten (alle "door Robert te bevestigen"; details in `sociaal-domein-besluiten.md`)
| # | besluit | te bevestigen |
|---|---|---|
| B1 | Gewerkt in `rechtsloods`; `rechtzoeker` niet bereikbaar | ja |
| B2 | Vertrek vanaf `main` (geen `live` in deze repo) | ja |
| B3 | Geen inhoud per uitspraak in de openbare repo: BLOKKADE na stap 2 | ja |
| B4 | Nieuwe slug `sociaal-domein`; bestaande regel `sociaal` (binnenkort) ongemoeid | ja |
| B5 | CRvB geselecteerd op wetscode in het zaaknummer | ja |
| B6 | IOAW/IOAZ, Bbz, Tozo, Tonk en WWIK binnen scope (rubriek bijstand) | ja |
| B7 | AIO (SVB) buiten scope; eigen bijdrage Wmo (CAK) binnen scope | ja |
| B8 | Uitgesloten: vreemdelingenzaken, Caribisch deel, leerlingenvervoer, Wsw, Wsnp, kinderbescherming, huurzaken | ja |
| B9 | Civiel recht alleen bij contractering/tarieven/aanbesteding of verhaal | ja |
| B10 | Hoogste rechter: CRvB; voor Wgs de RvS; HR alleen civiel | ja |
| B11 | Rotterdam-herkenning met eigen regex (`config.rotterdam_partij`) | ja |
| B12 | Filter vastgezet na precisie 98,3%; geen dubbele publicaties; massazaken gemarkeerd | ja |
| B13 | Taxonomie 8 onderwerpen / 29 subonderwerpen, concept | ja |
| B14 | Uitkomstregels: algemene regels plus domeinregels (verlaagd = deels; 8:72 lid 3 = alleen procedure) | ja |
| B15 | Extra configvelden: uitkomstregels, privacy, rotterdam_partij, hoogste_rechter | ja |
| B16 | "betrokkene" toegestaan in samenvattingen | ja |
| B17 | Selectie laag 2 met quota (Rotterdam max 200 enz.) | ja |
| B18 | Proef van 25 + 2 uitspraken, uitvoer niet bewaard | ja |

## Resultaat
| stap | aantal | controle |
|---|---|---|
| 0 Oriëntatie | 15 bevindingen | — |
| 1 Verzamelen en afbakenen | 16.499 kandidaten uit ±440.000 feedregels (bestuursrecht + civiel, 2016–2026) | `sociaal_select.py --check`: 0 fouten. Precisie 98,3% (onafhankelijke steekproef van 60), 95% vóór bijstelling (100 willekeurig). Eigen controle 15/15 eens |
| 2 Taxonomie en uitkomstregels | 8 onderwerpen, 29 subonderwerpen, 25 argumenten, 9 zaaktypen, 10 uitkomstregels, 6 privacyregels | `sociaal_taxonomie.py check`: 0 fouten |
| 3 Laag 1 | niet uitgevoerd (BLOKKADE). Proef: 1 batch van 25, 25 relevant, 1 zekerheid laag (dictum ontbreekt, tussenuitspraak), uitvoer verwijderd | `check_l1.py`: 0 fouten (zelf nagedraaid) |
| 4 Selectie laag 2 | script klaar, getest op proeflabels (450, quota werken, idempotent) | — |
| 5 Laag 2 | niet uitgevoerd (BLOKKADE). Proef: 2 uitspraken (Rb Rotterdam bijstand, CRvB Wmo met Rotterdam als partij), uitvoer verwijderd | `check_uit_v3` 0, `extra_check` 0, `sociaal_privacy_check` 0 (zelf nagedraaid) |
| 6 Nakijkronde uitkomst | script klaar (`lab/sociaal_nakijk_uitkomst.py`) | — |
| 7 Stand | `lab/stand_dom.py` werkt generiek; niet uitgevoerd | — |
| 8 Site-data | niet uitgevoerd; `lab/sociaal_site_na.py` en `lab/sociaal_sitetest.js` klaar (sitetest op openbare-orde: OK) | — |

Per instantie: CRvB 10.789 · Rb Rotterdam 699 · overige rechtbanken 4.790 · RvS 109 · hoven 76 · HR/PHR 32 · overig 4. Per rubriek: bijstand 12.942 · Wmo 3.043 · Jeugdwet 428 · schuldhulp 145. Geschat ±2.240 met Rotterdam als partij. Zie `sociaal-domein-tellingen.md`.

## Twijfelgevallen voor de jurist (afbakening; inhoudelijke twijfels volgen pas uit stap 3–5)
1. `ECLI:NL:CRVB:2025:1248`: eigen bijdrage Wmo, beslissing van het CAK. Hoort het CAK binnen scope (B7)?
2. `ECLI:NL:CRVB:2021:2938`: AIO-aanvulling, uitgevoerd door de SVB. Bewust uitgesloten (B7), maar het is wel Participatiewet.
3. `ECLI:NL:RBNHO:2021:12310`: verwijsindex onder de Jeugdwet, met AVG. Valt dit onder "verwijzing" in de Jeugdwet?
4. `ECLI:NL:RBDHA:2020:3839`: vovo over de weigering van WW, waarbij "betrokkene kan bijstand aanvragen". Geselecteerd, maar eigenlijk een UWV-zaak.
5. `ECLI:NL:RBROT:2017:1492`: verrekening van een Wajong-nabetaling met bijstand. Is dat bijstand of UWV?
6. `ECLI:NL:RBROT:2022:5692`: civiele huurzaak waarin een gemeentelijk schuldhulpbesluit meespeelt. Uitgesloten (B8).
7. `ECLI:NL:GHDHA:2017:137`: bijstandsverhaal bij het hof, alleen over een termijnvraag. Na bijstelling opgenomen (B9).
8. `ECLI:NL:RBZWB:2023:5999` en `ECLI:NL:RBZWB:2022:3274`: de inhoudsindicatie is alleen "WMO". Dat kan pas laag 1 bevestigen.
9. `ECLI:NL:CRVB:2017:3054`: gehandicaptenparkeerkaart onder CRvB-code WMO15. Overlapt met parkeren. Hoort dit bij Wmo?
10. `ECLI:NL:GHSHE:2022:2392`: naheffing parkeren door een jeugdzorgverlener. Uitgesloten, want het is een parkeerzaak (B8 / uitsluiting parkeerbelasting).

## Privacy-aandachtspunten
- **In de repo staan bewust niet:** uitspraakteksten, inhoudsindicaties, labels, samenvattingen en citaten (B3). Wel een ECLI-lijst met instantie, datum, zaaknummer, wetscode, prioriteit en overlap. Die gegevens staan ook openbaar in Open Data Rechtspraak.
- **Regels voor stap 3–5** (`config.privacy`, `lab/aanscherping_sociaal.md`), die deze details weglaten:
  - namen, adressen, geboortedata, BSN, rekeningnummers en kentekens;
  - namen en leeftijden van kinderen;
  - precieze diagnoses;
  - land of plaats van bezit, werkgever en school;
  - bedragen die niet nodig zijn voor het oordeel.

  Citaten gaan over de rechtsregel, niet over persoonlijke of medische details.
- **Automatische check:** `lab/sociaal_privacy_check.py` op plaatshouders (`[eiser]`), geboortedata, leeftijden van kinderen, diagnosetermen (lijst), landen, postcodes, IBAN, BSN-achtige nummers en "mr. X". Getest op voorbeeldobjecten: 4/4 gevonden. De ziekte ALS staat er bewust niet in, omdat "als" anders overal treft.
- **Resterend risico:**
  - herleidbaarheid via combinaties: kleine gemeente plus specifiek bedrag plus jaar;
  - diagnoses buiten de woordenlijst;
  - beschrijvende omschrijvingen ("een ernstige psychische aandoening");
  - de koppeling Rotterdam × zaak. De uitspraken zelf zijn openbaar en gepseudonimiseerd, maar de bundeling en uitleg door de gemeente is precies waar de FG naar moet kijken.
- **Steekproef:** stap 5 laat elke "ernstig"-beoordeling ook op privacy toetsen (`lab/sociaal_steekproef_opdracht.md`).

## Bekende beperkingen
- **Publicatie is onvolledig:** rechtspraak.nl publiceert maar een deel. Vooral rechtbankzaken in het sociale domein ontbreken grotendeels (Rb Rotterdam: 39–118 per jaar). Het aantal gepubliceerde CRvB-uitspraken daalt (1.746 in 2016, 581 in 2025). Aantallen zeggen dus niets over het werkelijke aantal zaken of over winkansen.
- **Selectie op kop en inhoudsindicatie:** zaken met een lege of summiere inhoudsindicatie ("WMO", "TOZO", "-") worden alleen via de CRvB-code of het trefwoord gevonden. De dekking van uitgesloten net-niet-zaken is ±95%.
- **Rotterdam-schatting:** komt uit een steekproef van 1.260 teksten (57% bij Rb Rotterdam, 17% bij CRvB). Het echte aantal volgt pas na het ophalen van alle teksten (stap 3).
- **Ontbrekend dictum:** 57 van 1.239 geparste teksten (4,6%) hebben geen herkenbare beslissingssectie. Haiku kan die ten onrechte "niet relevant" noemen. `lab/sociaal_l1_nacontrole.py` maakt daar herzienbatches van.
- **"Bijlagen:"-bug in `maak_in_v3.py`:** raakt dit domein in de steekproef niet (0 van 1.260). Opnieuw controleren op alle teksten.
- **Bestaande fouten op `main` (niet van dit domein), gevonden met de sitetest:**
  - avg-privacy toont `_bevroren` als onderwerp. De site maakt van elke taxonomiesleutel een onderwerp.
  - `site/assets/dom-bpm.webp` en `dom-verkeersboetes.webp` ontbreken (404).
- **Tegelafbeelding ontbreekt:** sociaal-domein heeft nog geen `site/assets/dom-sociaal-domein.webp`. Die is nodig in stap 8 (huisstijl: `tools/herkleur_afbeeldingen.py`, `tools/check_huisstijl.py`).
- **Geblokkeerd in deze omgeving:** wetten.overheid.nl. Dat was voor stap 0–2 niet nodig.
- **Taxonomie is een concept:** nog niet vakinhoudelijk nagekeken.

## Verbruik
| stap | agents | tokens (gemeten) |
|---|---|---|
| 1 precisie | 2 × Haiku | 145k (200 uitspraken) + 85k (60 uitspraken) |
| 2 taxonomie | — | eigen context (150 inhoudsindicaties gelezen) |
| proef laag 1 | 1 × Haiku | 158.615 (25 uitspraken, 1 batch ≈ 6,3k per uitspraak; met 3 batches per agent verwacht ±4k) |
| proef laag 2 | 1 × Sonnet | 109.731 (2 uitspraken ≈ 55k per uitspraak incl. opstart; bij 6 per batch verwacht ±27–30k) |
| **schatting rest** | | laag 1: 16.499 × ±3,6k ≈ 59M Haiku (±220 agents van 3 × 25). Laag 2: 450 × ±27k ≈ 12M Sonnet (75 batches van 6). Steekproef: 45 × ±15k ≈ 0,7M. Stand: ±8 agents × 100k ≈ 0,8M |

## Volgende stappen
1. Robert: bevestig B1–B18, vooral B3 (werkrepo) en B7/B8 (scope). Leg de taxonomie voor aan een collega van Werk en Inkomen, Wmo en Jeugd.
2. Start een sessie met `rechtzoeker` gekoppeld, haal deze branch binnen en volg de "Volgende actie" in de STAND. Die begint met:
   ```
   bash scripts/sociaal_feeds.sh
   python3 -I scripts/sociaal_select.py
   python3 -I scripts/sociaal_prep.py links
   python3 -I scripts/sociaal_prep.py fetch 6
   python3 -I scripts/sociaal_prep.py parse
   python3 -I scripts/sociaal_prep.py in
   ```
   Daarna laag 1 met `lab/sociaal_l1_opdracht.md` (3 batches per Haiku-agent).
3. Vóór publicatie:
   - FG-akkoord;
   - tegelafbeelding;
   - `lab/sociaal_site_na.py` (status in-opbouw);
   - samenvoegen met de bestaande regel `sociaal` in `index.json` (B4).
