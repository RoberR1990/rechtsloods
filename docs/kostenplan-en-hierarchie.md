# Kostenplan en onderwerpenhiërarchie voor nieuwe domeinen (voorstel 12 nov 2026)

## Uitgangspunt
- Tellingen = 10 jaar (2016–2026). Recente jaren domineren: 2021+ is 50–88% van elk domein (WOZ 82%). Minder jaren bespaart dus weinig.
- Huidige methode ≈ 12–14k tokens per uitspraak (25 uitspraken per agent; context stapelt op).

## Besluit Robert (12 nov 2026, 21:00)
Nachtrun laag 2 = **alleen prioriteit 1 en 2** (hoogste rechters + hoven, en Rotterdam als partij). Clusters en de rest later.

## Twee lagen — later "doe de rest" zonder herwerk
**Laag 1 — voor ALLE uitspraken (goedkoop, ~15% van een volledige samenvatting)**
Leest alleen inhoudsindicatie + beslissing (+ regex op de volledige tekst, gratis):
domein, onderwerp → sub → kenmerk (hiërarchie), zaaktype, partijen / gemeente_is_partij, procesvorm, uitkomst, wetsartikelen (regex + koppeling aan BWB-structuur), feitcodes (Wahv, regex), bezwaargronden (labels), gemeente, dubbel_van, cluster-id.
→ Hiermee werkt diep filteren al voor alles.

**Laag 2 — volledige v3-samenvatting, in prioriteitsvolgorde**
1. Hoge Raad, Raad van State, CRvB, hoven (~35% bij parkeren)
2. Rotterdam als partij
3. Eén vertegenwoordiger per cluster van (bijna) gelijke zaken (massabezwaren WOZ/Wahv)
4. Later: de rest ("doe de rest") — zelfde instructie, zelfde schema, alleen de selectie verandert.
Laag-2-velden komen erbij; laag-1-velden blijven staan. Geen herwerk.

**Plus:** batches van 6 i.p.v. 25 en alleen inhoudsindicatie + overwegingen + beslissing meesturen (procesverloop/feiten-boilerplate eruit).

Grove schatting (vóór meting): alles volledig met huidige methode ≈ 10× parkeren; met dit plan ≈ 2–2,5× parkeren, dus ~4× goedkoper. **Eerst meten** op 20 uitspraken (tokens per uitspraak, laag 1 vs laag 2) voordat de nachtrun start.

## Hiërarchie: domein → onderwerp → sub → kenmerk, plus facetten
Facetten (dwars): instantie, jaar, zaaktype, uitkomst, procesvorm, gemeente, bezwaargrond, wetsartikel (zelf hiërarchisch: wet → hoofdstuk → artikel → lid), raakt (team).

Officiële ankers per domein (onderwerpen afleiden van de structuur van de wet/het model, niet zelf verzinnen):
| Domein | Anker voor onderwerpen | Anker voor bezwaargronden |
|---|---|---|
| Parkeren | Gemeentewet 225/234, RVV 1990 + BABW, VNG-model parkeerbelastingverordening | bestaande `argumenten.json` |
| Verkeersboetes | Wahv-structuur + OM-feitcodes (Boetebase), hiërarchisch per gedraging | Wahv art. 9 (billijkheid), bewijs, kenbaarheid |
| WOZ | Wet WOZ hoofdstukken + Uitvoeringsregeling instructie waardebepaling; Waarderingskamer Vraagbaak | waardebepaling, vergelijkingsobjecten, taxatieverslag, proceskosten (art. 30a) |
| BPM | Wet BPM (o.a. art. 9, 10 afschrijving) | taxatierapport, koerslijst, proceskosten |
| Openbare orde | Gemeentewet 172–176a, Opiumwet 13b, Wet Bibob, VNG-model-APV hoofdstukken | evenredigheid, bestuurlijke rapportage, last/sluitingsduur |
| AVG/Woo | AVG-artikelen (5, 6, 12–22), Woo art. 5.1/5.2 | weigeringsgrond, zoekslag, termijn |
| Sociaal | Participatiewet / Wmo 2015 / Jeugdwet hoofdstukken | onderzoek, terugvordering, boete, maatwerk |

Let op: de Rechtspraak levert zelf een officiële wetsverwijzing mee, maar bij parkeren maar in 79 van 3.833 uitspraken (2%). We halen wetsartikelen dus zelf uit de tekst en koppelen ze aan de wettenbank-structuur.
Concept-taxonomieën blijven `"concept": true` tot een vakinhoudelijk collega ze heeft nagekeken.
