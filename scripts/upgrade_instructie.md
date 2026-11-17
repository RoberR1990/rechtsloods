# Opdracht: kwaliteitsronde op bestaande samenvattingen (v2)

Een jurist heeft deze samenvattingen gereviewd. Belangrijkste kritiek:
(a) een bron-citaat bestaat wel, maar ondersteunt de zin niet altijd;
(b) de herkomst van een rechtsregel ontbreekt (eigen oordeel van deze rechter, of toepassing van een lijn van de Hoge Raad of Raad van State);
(c) de uitkomst moet onderscheiden tussen inhoud, procedure en voorlopige voorziening (spoed);
(d) "lessen" zijn een AI-suggestie, geen oordeel van de rechter.

Je krijgt een lijst bestanden. Voor elk bestand:
- Invoer (de uitspraak): `/home/claude/data/proef/in/<naam>` met `alineas` [{id, rov, t}].
- Huidige samenvatting: `/home/claude/data/proef/uit/<naam>`.
Lees BEIDE volledig. Sla bestanden met `"relevant": false` over (laat ze ongemoeid).

Werk het uit-bestand bij (zelfde pad, Write-tool), alle bestaande velden behouden plus:

1. **Dekkingscontrole per zin** (kern, samenvatting, rechtsregel, lessen): lees de bron-alinea. Ondersteunt die alinea de bewering echt? Zo niet: kies een betere alinea en een nieuw letterlijk citaat (5-20 woorden, exact gekopieerd), of herschrijf de zin zodat hij klopt. Voeg aan elk zin-object `"dekking": "ok"` toe nadat je het gecontroleerd hebt.
2. `"uitkomst_type"`: `"inhoud"` | `"procedure"` (niet-ontvankelijk, termijnen, kosten/dwangsom zonder inhoudelijk oordeel) | `"voorlopige voorziening"` | `"anders"`.
3. `"uitkomst_toelichting"`: max 15 woorden, gewone taal, bijv. "Naheffing blijft staan; gemeente betaalt wel dwangsom wegens te laat beslissen."
4. In `rechtsregel`: voeg `"herkomst"` toe: `"eigen oordeel"` of `"toepassing lijn <ECLI>"` (alleen als de tekst die ECLI zelf noemt) of `"wettekst <artikel>"`. Als de regel alleen voor dit specifieke geval geldt en te algemeen is geformuleerd: maak hem specifieker of zet rechtsregel op null.
5. `"wetsartikelen"`: lijst van genoemde kernartikelen in korte vorm, bijv. ["art. 234 Gemeentewet", "art. 225 Gemeentewet", "art. 7:10 Awb", "art. 4:17 Awb", "art. 24 RVV 1990", "art. 9 Wahv"]. Max 5, alleen wat echt in de tekst staat.
6. `"argumenten"`: welke bezwaargronden uit `/home/claude/data/argumenten.json` worden in deze zaak beoordeeld (sleutels, 0-3), elk met wie op dat punt gelijk kreeg: `[{"arg": "app-automaat-werkte-niet", "oordeel": "verworpen" | "gehonoreerd" | "niet beoordeeld", "bron": [id], "citaat": "..."}]`.
7. `"steunt"`: `"gemeente"` | `"parkeerder"` | `"gemengd"`: aan wiens kant zou een gemeente-jurist deze uitspraak in een volgende zaak gebruiken?

Harde regels: elk citaat letterlijk uit de bron-alinea; geen persoonsnamen; gewone taal (B1). Schrijf geldige JSON.
Rapporteer aan het eind alleen: aantal bijgewerkt, aantal zinnen herzien wegens slechte dekking (met ECLI), twijfelgevallen in max 1 regel elk.
