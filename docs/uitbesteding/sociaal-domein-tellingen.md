# Sociaal domein: tellingen stap 1 (Open Data Rechtspraak, uitspraakdatum 2016-01-01 t/m 2026-11-20)

Bron: `data/feeds/{best,civ}<jaar>.json` (bestuursrecht en civiel recht, alleen gepubliceerde uitspraken met document). Selectie: `scripts/sociaal_select.py`. Volledige cijfers: `data/dom/sociaal-domein/tellingen.json`.

**Let op:** rechtspraak.nl publiceert maar een deel van alle uitspraken. Vooral rechtbankuitspraken in het sociale domein worden weinig gepubliceerd, terwijl de CRvB veel publiceert. Deze aantallen zijn dus wat **publiek** staat, niet hoeveel zaken er zijn.

- Kandidaten na afbakening: **16499**. Dubbele publicaties (zelfde instantie, datum en zaaknummer): **0**.
- Hoge instanties (CRvB, RvS, HR/PHR, hoven): **11010**. Uit civiel recht: **134**.
- Massazaken (≥ 3 bijna gelijke inhoudsindicaties, geen dubbele publicatie): **806** uitspraken. Die worden gemarkeerd, niet verwijderd (`cluster` in `dom_build`).
- Overlap met bestaande domeinen (gemarkeerd in veld `overlap`, niet verwijderd): {'parkeren': 6, 'avg-privacy': 12, 'openbare-orde': 5}.
- Hoogste rechter: **CRvB** voor Participatiewet, Wmo, Jeugdwet, Bbz, IOAW/IOAZ en Tozo (10789 uitspraken). Voor **schuldhulpverlening (Wgs)** is dat de **Raad van State** (73 van de 109 RvS-uitspraken). De Hoge Raad komt alleen voor bij civiele zaken over verhaal en contractering (18 uitspraken + 14 conclusies).

## Per instantie en jaar
| instantie | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | totaal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CRvB | 1746 | 1452 | 1362 | 1237 | 974 | 934 | 770 | 714 | 620 | 581 | 399 | 10789 |
| RvS | 15 | 17 | 17 | 12 | 9 | 5 | 5 | 4 | 11 | 6 | 8 | 109 |
| HR / PHR | 6 | 2 | 2 | 1 | 3 | 2 | 5 | 5 | 3 | 0 | 3 | 32 |
| Hoven | 4 | 8 | 11 | 5 | 12 | 4 | 7 | 6 | 8 | 5 | 6 | 76 |
| Rb Rotterdam | 39 | 31 | 45 | 46 | 39 | 68 | 60 | 65 | 75 | 113 | 118 | 699 |
| Overige rechtbanken | 267 | 282 | 267 | 229 | 504 | 590 | 608 | 504 | 546 | 504 | 489 | 4790 |
| Overig | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 4 |
| **totaal** | 2077 | 1793 | 1705 | 1531 | 1541 | 1604 | 1455 | 1298 | 1263 | 1209 | 1023 | **16499** |

## Per rubriek en instantie (een uitspraak kan in meer rubrieken vallen)
| rubriek | CRvB | RvS | HR / PHR | Hoven | Rb Rotterdam | Overige rechtbanken | Overig |
|---|---:|---:|---:|---:|---:|---:|---:|
| bijstand | 9191 | 20 | 17 | 44 | 520 | 3147 | 3 |
| wmo | 1512 | 13 | 7 | 20 | 138 | 1352 | 1 |
| jeugdwet | 87 | 3 | 0 | 11 | 31 | 296 | 0 |
| schuldhulp | 0 | 73 | 8 | 4 | 17 | 43 | 0 |

## Precisie van het filter
| meting | n | relevant | precisie |
|---|---:|---:|---:|
| Steekproef 1, willekeurig (vóór bijstelling) | 100 | 95 | 95% |
| Steekproef 1, rechtbank/civiel-selectie (vóór bijstelling) | 60 | 59 | 98% |
| Steekproef 1 na bijstelling (zelfde 200, in-sample) | 155 geselecteerd | 154 | 99,4% |
| Steekproef 2, nieuw en onafhankelijk (na bijstelling) | 60 | 59 | 98,3% |
| Net-niet-zaken (uitgesloten door filter) | 40 | 2 betwistbaar relevant | dekking ±95% |
| Eigen controle (15 uit steekproef 1) | 15 | eens met Haiku 15/15 | — |

Beoordeling door een Haiku-subagent op kop en inhoudsindicatie (`lab/sociaal_precisie_opdracht.md`, `lab/sociaal_precisie.py`). De steekproeven zelf bevatten inhoudsindicaties en staan daarom niet in de repo (B3).

## Rotterdam als partij (schatting uit 1.260 volledige teksten)
- Rechtbank Rotterdam: 397 van 698 (57%), want de rechtbank bedient ook Dordrecht/Drechtsteden, Capelle, Schiedam en andere gemeenten. Geschat ±398 in de populatie.
- CRvB: 67 van 392 (17%). Geschat ±1.840 in de populatie.
- Overige instanties: 0 van 149.
- Totaal geschat: **±2.240** uitspraken met Rotterdam als partij. Herkenning: `rotterdam_partij` in `config.json`.

## "Bijlagen:"-bug in `scripts/maak_in_v3.py`
In de 1.260 opgehaalde teksten hebben er 161 een bijlage-kop. In 37 daarvan laat `maak_in_v3.py` tekst weg na die kop. Dat is steeds het wettelijk kader **na** de beslissing, dus het weglaten is daar bedoeld. In geen enkele tekst valt beoordeling of dictum weg (`lab/sociaal_bijlagen_check.py`: `GERAAKT: 0`). Eén eerdere melding was vals alarm: het woord "beslissing" stond in een wetsartikel. De steekproef dekt 7,6% van de kandidaten. Bij stap 3 draait de controle opnieuw op alle teksten (`lab/sociaal_bijlagen_check.py`).
