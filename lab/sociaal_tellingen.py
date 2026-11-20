"""Schrijft docs/uitbesteding/sociaal-domein-tellingen.md uit data/dom/sociaal-domein/{kandidaten,tellingen}.json.
  python3 -I lab/sociaal_tellingen.py"""
import json, collections, re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f'{R}/data/dom/sociaal-domein/tellingen.json')); K = json.load(open(f'{R}/data/dom/sociaal-domein/kandidaten.json'))
V = json.load(open(f'{R}/data/feeds/kandidaten_sociaal-domein.json'))
def grp(i):
    if i == 'Centrale Raad van Beroep': return 'CRvB'
    if i == 'Raad van State': return 'RvS'
    if i in ('Hoge Raad', 'Parket bij de Hoge Raad'): return 'HR / PHR'
    if i.startswith('Gerechtshof'): return 'Hoven'
    if i == 'Rechtbank Rotterdam': return 'Rb Rotterdam'
    if i.startswith('Rechtbank'): return 'Overige rechtbanken'
    return 'Overig'
G = ['CRvB', 'RvS', 'HR / PHR', 'Hoven', 'Rb Rotterdam', 'Overige rechtbanken', 'Overig']; J = list(range(2016, 2027))
c = collections.Counter((grp(k['instantie']), k['jaar']) for k in K)
rows = ['| instantie | ' + ' | '.join(str(j) for j in J) + ' | totaal |', '|---|' + '---:|' * (len(J) + 1)]
for g in G:
    if sum(c[(g, j)] for j in J): rows.append(f'| {g} | ' + ' | '.join(str(c[(g, j)]) for j in J) + f' | {sum(c[(g, j)] for j in J)} |')
rows.append('| **totaal** | ' + ' | '.join(str(sum(c[(g, j)] for g in G)) for j in J) + f' | **{len(K)}** |')
rub = collections.Counter((r, grp(k['instantie'])) for k in K for r in k['rubrieken'])
rows2 = ['| rubriek | ' + ' | '.join(G) + ' |', '|---|' + '---:|' * len(G)]
for r in ['bijstand', 'wmo', 'jeugdwet', 'schuldhulp']: rows2.append(f'| {r} | ' + ' | '.join(str(rub[(r, g)]) for g in G) + ' |')
cl = collections.Counter(re.sub(r'\W+', ' ', v['summary'].lower())[:200] for v in V if len(v['summary']) > 40)
massa = sum(n for s, n in cl.items() if n >= 3); inst = collections.Counter(k['instantie'] for k in K)
open(f'{R}/docs/uitbesteding/sociaal-domein-tellingen.md', 'w').write(f"""# Sociaal domein: tellingen stap 1 (Open Data Rechtspraak, uitspraakdatum 2016-01-01 t/m 2026-11-20)

Bron: `data/feeds/{{best,civ}}<jaar>.json` (bestuursrecht en civiel recht, alleen gepubliceerde uitspraken met document). Selectie: `scripts/sociaal_select.py`. Volledige cijfers: `data/dom/sociaal-domein/tellingen.json`.

**Let op:** rechtspraak.nl publiceert maar een deel van alle uitspraken. Vooral rechtbankuitspraken in het sociale domein worden weinig gepubliceerd, terwijl de CRvB veel publiceert. Deze aantallen zijn dus wat **publiek** staat, niet hoeveel zaken er zijn.

- Kandidaten na afbakening: **{len(K)}**. Dubbele publicaties (zelfde instantie, datum en zaaknummer): **{T['dubbel_verwijderd']}**.
- Hoge instanties (CRvB, RvS, HR/PHR, hoven): **{T['hoog']}**. Uit civiel recht: **{T['per_bron'].get('civ', 0)}**.
- Massazaken (≥ 3 bijna gelijke inhoudsindicaties, geen dubbele publicatie): **{massa}** uitspraken. Die worden gemarkeerd, niet verwijderd (`cluster` in `dom_build`).
- Overlap met bestaande domeinen (gemarkeerd in veld `overlap`, niet verwijderd): {T['overlap']}.
- Hoogste rechter: **CRvB** voor Participatiewet, Wmo, Jeugdwet, Bbz, IOAW/IOAZ en Tozo ({inst['Centrale Raad van Beroep']} uitspraken). Voor **schuldhulpverlening (Wgs)** is dat de **Raad van State** ({sum(1 for k in K if k['instantie'] == 'Raad van State' and 'schuldhulp' in k['rubrieken'])} van de {inst['Raad van State']} RvS-uitspraken). De Hoge Raad komt alleen voor bij civiele zaken over verhaal en contractering ({inst['Hoge Raad']} uitspraken + {inst['Parket bij de Hoge Raad']} conclusies).

## Per instantie en jaar
{chr(10).join(rows)}

## Per rubriek en instantie (een uitspraak kan in meer rubrieken vallen)
{chr(10).join(rows2)}

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
""")
print('\n'.join(rows)); print('massa', massa)
