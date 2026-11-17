# Samenvattingsschema v3 (besluit 12 nov 2026, na persona-review)

Bron: 6 persona-reviews in `data/review/` (jurist, bezwaarbehandelaar, beleidsmaker, productmanager, 2 nieuwkomers). Gemiddeld cijfer v2: 5,5/10. Kernkritiek: "lessen" zijn geen lessen, "steunt/uitkomst" klopt niet als de gemeente geen partij is, rechtsregels te ruim, jargon, bezwaargronden vaak leeg.

## Harde regels (gelden voor elk veld)
- Elke inhoudelijke zin: `{zin, bron:[alinea-id], citaat}`; citaat letterlijk uit de eerste bron-alinea (script controleert).
- Taal B1. Vaste rolnamen: **de burger** (of: de parkeerder / de aanvrager), **de gemeente**, **de rechter**, **de exploitant**, **de officier van justitie**. Vakwoord alleen met uitleg tussen haakjes de eerste keer.
- Niets invullen wat niet in de uitspraak staat. Leeg = `null` of `[]`, met `reden_leeg` waar gevraagd.
- `zekerheid` omlaag als de rechter "aannemelijk", "voorshands" of "in dit geval" oordeelt.

## Velden
| veld | wat | nieuw/gewijzigd |
|---|---|---|
| ecli, relevant, onderwerp, sub | zoals v2; sub moet echt passen, anders `sub:"overig"` | — |
| zaaktype | `naheffing` · `wahv-boete` · `vergunning` · `verkeersbesluit` · `omgevingsrecht` · `privaat` · `woo-avg` · `overig` | nieuw |
| partijen | `{burger:"bewoner/bedrijf/gemachtigde-bureau", wederpartij:"gemeente X / officier van justitie / minister / exploitant", gemeente_is_partij:bool}` | nieuw |
| procesvorm | `beroep` · `hoger beroep` · `cassatie` · `cassatie belang der wet` · `voorlopige voorziening` · `kort geding` · `verzet` | nieuw |
| intro | 2 zinnen B1: wat voor zaak, wie tegen wie, bij welke rechter | nieuw |
| titel, kern | zoals v2; titel mag niet sterker zijn dan de beslissing | — |
| samenvatting | 3–6 zinnen | — |
| uitkomst | `burger wint` · `wederpartij wint` · `deels` · `alleen procedure` | vaste waarden |
| gevolg_betrokkene | 1 zin; verplicht bij cassatie belang der wet ("voor de betrokkene verandert niets") | nieuw |
| steunt | `gemeente` · `burger` · `gemengd`, **alleen als gemeente_is_partij**, anders `null` | gewijzigd |
| bezwaargronden | `[{arg (code uit argumenten.json), burger_zegt, oordeel: gehonoreerd/verworpen/niet beoordeeld, waarom, bruikbare_zin:{citaat,bron}}]` — **nooit leeg** bij zaaktype naheffing/wahv-boete | vervangt `argumenten` |
| rechtsregel | `{zin, type: regel/feitelijk_oordeel, reikwijdte, uitzondering, herkomst: wet/vaste lijn HR-RvS/oordeel rechter/lokale verordening, bron, citaat}` — alleen als de rechter de regel zelf formuleert | gewijzigd |
| bewijs | `{bewijslast_bij, bewijsmiddelen:[], wat_gaf_doorslag}` | nieuw |
| toepasselijkheid | `landelijk` · `lokale verordening (gemeente)` · `rijk` · `privaat` | nieuw |
| lijn | `{soort: bevestigt/nieuw/wijkt af/onbekend, eerdere:[ECLI]}` | vervangt kale `verwijst_naar` |
| wetsartikelen | altijd vullen als genoemd (incl. verordening + artikel) | strenger |
| actie_gemeente | `[{actie (gebiedende wijs), raakt (enum hieronder), bron, citaat}]` of `[]` met `reden_leeg` | vervangt `lessen_voor_gemeente` |
| raakt | subset van: `bezwaar` · `klantcontact` · `bebording-verkeersbesluit` · `verordening-beleid` · `tarief-naheffing` · `vergunningen` · `scanauto-handhaving` · `betaalapp` · `privacy-woo` · `communicatie` | nieuw |
| klantuitleg | max 3 zinnen, u-vorm, B1, geen vakwoorden: wat betekent dit voor een burger, en wanneer is een naheffing/boete wel/niet terecht | nieuw |
| gemeente | uit tekst of metadata; `null` + reden als geanonimiseerd | strenger |
| dubbel_van | ECLI als dezelfde zaak eerder gepubliceerd is | nieuw |
| zekerheid | hoog/middel/laag | — |

## Uitvoering (advies)
- HR, RvS, CRvB, hoven: Sonnet. Rechtbanken: Haiku **plus** automatische checks (zie `check_uit_v3` te bouwen) **plus** 5% steekproef door Sonnet.
- Kleine batches (5–8 uitspraken per agent): kosten lopen in de huidige aanpak ~3× op doordat context zich opstapelt (≈14k tokens per uitspraak bij 25 per agent, terwijl een uitspraak ≈4k tokens is).
- Automatische checks: enum-waarden, `steunt=null` als `gemeente_is_partij=false`, bezwaargronden niet leeg bij naheffing/wahv, citaten letterlijk, `uitkomst` consistent met `beslissing`-tekst (gegrond/ongegrond).
