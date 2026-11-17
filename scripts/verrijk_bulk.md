# Opdracht: verrijk parkeeruitspraken (proefset)

Je krijgt een map met uitspraken als JSON (`/home/claude/data/proef/in/*.json`). Elk bestand bevat metadata en `alineas`: een lijst met `{id, rov, t}` (id = alineanummer in dit bestand, rov = rechtsoverwegingsnummer van de rechter of null, t = tekst).

Verwerk ALLEEN de bestanden die in jouw opdracht staan. Schrijf per uitspraak één bestand naar `/home/claude/data/proef/uit/<zelfde bestandsnaam>` met exact dit JSON-schema:

```json
{
  "ecli": "...",
  "relevant": true,
  "onderwerp": "parkeerbelasting | parkeerverbod | vergunningen | parkeernormen | garages-privaat | handhaving-privacy",
  "sub": "<één sleutel uit taxonomie.json binnen dat onderwerp>",
  "sub2": "<optioneel tweede sleutel of null>",
  "gemeente": "<gemeente die partij is, of null als onbekend/geanonimiseerd>",
  "uitkomst": "gelijk burger | gelijk gemeente | deels | niet-ontvankelijk | anders",
  "titel": "<pakkende kop in gewone taal, max 10 woorden, geen jargon>",
  "kern": {"zin": "<1 zin: wat besliste de rechter en waarom>", "bron": [<alinea-id>], "citaat": "<letterlijk stukje van 5-20 woorden uit die alinea>"},
  "samenvatting": [
    {"zin": "<zin in gewone taal (B1)>", "bron": [<alinea-id>, ...], "citaat": "<letterlijk 5-20 woorden uit de eerste bron-alinea>"}
  ],
  "rechtsregel": {"zin": "<de algemene regel die je uit deze uitspraak kunt halen, of null>", "bron": [<id>], "citaat": "..."},
  "lessen_voor_gemeente": [{"zin": "<praktische les voor een parkeerafdeling>", "bron": [<id>], "citaat": "..."}],
  "verwijst_naar": ["<ECLI's die in de tekst worden aangehaald als vaste lijn, max 5>"],
  "zekerheid": "hoog | middel | laag"
}
```

## Extra velden (v2), verplicht
Voeg aan elk zin-object `"dekking": "ok"` toe nadat je hebt gecontroleerd dat de bron-alinea de bewering echt draagt (niet alleen dat het citaat bestaat). Formuleer `lessen_voor_gemeente` als wat de rechter zei of woog, niet als advies.
Voeg ook deze velden toe 

1. **Dekkingscontrole per zin** (kern, samenvatting, rechtsregel, lessen): lees de bron-alinea. Ondersteunt die alinea de bewering echt? Zo niet: kies een betere alinea en een nieuw letterlijk citaat (5-20 woorden, exact gekopieerd), of herschrijf de zin zodat hij klopt. Voeg aan elk zin-object `"dekking": "ok"` toe nadat je het gecontroleerd hebt.
2. `"uitkomst_type"`: `"inhoud"` | `"procedure"` (niet-ontvankelijk, termijnen, kosten/dwangsom zonder inhoudelijk oordeel) | `"voorlopige voorziening"` | `"anders"`.
3. `"uitkomst_toelichting"`: max 15 woorden, gewone taal, bijv. "Naheffing blijft staan; gemeente betaalt wel dwangsom wegens te laat beslissen."
4. In `rechtsregel`: voeg `"herkomst"` toe: `"eigen oordeel"` of `"toepassing lijn <ECLI>"` (alleen als de tekst die ECLI zelf noemt) of `"wettekst <artikel>"`. Als de regel alleen voor dit specifieke geval geldt en te algemeen is geformuleerd: maak hem specifieker of zet rechtsregel op null.
5. `"wetsartikelen"`: lijst van genoemde kernartikelen in korte vorm, bijv. ["art. 234 Gemeentewet", "art. 225 Gemeentewet", "art. 7:10 Awb", "art. 4:17 Awb", "art. 24 RVV 1990", "art. 9 Wahv"]. Max 5, alleen wat echt in de tekst staat.
6. `"argumenten"`: welke bezwaargronden uit `/home/claude/data/argumenten.json` worden in deze zaak beoordeeld (sleutels, 0-3), elk met wie op dat punt gelijk kreeg: `[{"arg": "app-automaat-werkte-niet", "oordeel": "verworpen" | "gehonoreerd" | "niet beoordeeld", "bron": [id], "citaat": "..."}]`.
7. `"steunt"`: `"gemeente"` | `"parkeerder"` | `"gemengd"`: aan wiens kant zou een gemeente-jurist deze uitspraak in een volgende zaak gebruiken?


## Harde regels
1. **Elke zin heeft minimaal één bron-id.** Een zin die je niet aan een alinea kunt koppelen, schrijf je niet.
2. **`citaat` is letterlijk** gekopieerd uit de tekst van de eerste bron-alinea (exacte tekens, geen aanpassing). Dit wordt automatisch gecontroleerd.
3. Samenvatting: 3 tot 6 zinnen. Volgorde: wat gebeurde er → wat vond de burger → wat vond de gemeente → oordeel rechter → gevolg.
4. Gewone taal: geen "belanghebbende", "verweerder", "heffingsambtenaar" → zeg "de parkeerder", "de gemeente", of bij bouwplannen en civiele zaken wie het echt is ("omwonenden", "de projectontwikkelaar", "de garage-exploitant", "de VvE"). Bij `steunt` betekent "parkeerder" dan: de burger/wederpartij van de gemeente of exploitant. Geen Latijn. Bedragen en data wel noemen.
5. Lessen voor gemeente: 0 tot 2, alleen als de uitspraak echt iets zegt over hoe een gemeente het beter of juist goed doet (borden, bewijs, communicatie, beleid). Geen algemeenheden.
6. Als de uitspraak niet over parkeren gaat (valse treffer): `"relevant": false` en laat de rest null/leeg.
7. Persoonsnamen nooit overnemen; uitspraken zijn al geanonimiseerd, houd dat zo.
8. `taxonomie.json` staat in `/home/claude/data/taxonomie.json`. Gebruik alleen sleutels die daar staan.

## Werkwijze (bulk)
- Invoer staat in `/home/claude/data/proef/in3/`. Lees uitspraken met `python3 /home/claude/scripts/toon.py <bestand1> <bestand2> ...` (2-4 tegelijk) en lees ALLES wat het toont.
- Schrijf per uitspraak één bestand naar `/home/claude/data/proef/uit/<zelfde naam>` (Write-tool of een Python-script dat json.dump gebruikt, ensure_ascii=False).
- Draai aan het eind `python3 /home/claude/scripts/check_uit.py <al jouw bestanden>` en herstel tot FOUTEN: 0.
- Gebruik geen /tmp/show.py of andere gedeelde namen; maak eventuele hulpscripts in een eigen map /tmp/<jouw-batch-id>/. Rapporteer aan het eind alleen in één regel: batch-id, aantal verwerkt, aantal niet relevant, FOUTEN-uitkomst van de check.

## Batch en bijzondere documenten
- Je bestandenlijst staat in `/home/claude/data/batches/batches.json`: het object met jouw batch-id, veld `files`. Sla bestanden over die al in `/home/claude/data/proef/uit/` staan.
- Bestanden `ECLI_NL_PHR_*` zijn conclusies van de Advocaat-Generaal (advies aan de Hoge Raad, geen uitspraak): vat het advies samen; `uitkomst` en `uitkomst_type` = "anders". Lees lange stukken één voor één.
- Gebruik ALLEEN Bash, Read en Write. Geen andere tools (geen geplande taken, geen berichten, geen web).
- Schrijf je rapport in het Nederlands.
