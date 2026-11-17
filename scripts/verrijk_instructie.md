# Opdracht: verrijk parkeeruitspraken (proefset)

Je krijgt een map met uitspraken als JSON (`/home/claude/data/proef/in/*.json`). Elk bestand bevat metadata en `alineas`: een lijst met `{id, rov, t}` (id = alineanummer in dit bestand, rov = rechtsoverwegingsnummer van de rechter of null, t = tekst).

Verwerk ALLEEN de bestanden die in jouw opdracht staan. Schrijf per uitspraak één bestand naar `/home/claude/data/proef/uit/<zelfde bestandsnaam>` met exact dit JSON-schema:

```json
{
  "ecli": "...",
  "relevant": true,
  "onderwerp": "parkeerbelasting | parkeerverbod | vergunningen",
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

## Harde regels
1. **Elke zin heeft minimaal één bron-id.** Een zin die je niet aan een alinea kunt koppelen, schrijf je niet.
2. **`citaat` is letterlijk** gekopieerd uit de tekst van de eerste bron-alinea (exacte tekens, geen aanpassing). Dit wordt automatisch gecontroleerd.
3. Samenvatting: 3 tot 6 zinnen. Volgorde: wat gebeurde er → wat vond de burger → wat vond de gemeente → oordeel rechter → gevolg.
4. Gewone taal: geen "belanghebbende", "verweerder", "heffingsambtenaar" → zeg "de parkeerder", "de gemeente". Geen Latijn. Bedragen en data wel noemen.
5. Lessen voor gemeente: 0 tot 2, alleen als de uitspraak echt iets zegt over hoe een gemeente het beter of juist goed doet (borden, bewijs, communicatie, beleid). Geen algemeenheden.
6. Als de uitspraak niet over parkeren gaat (valse treffer): `"relevant": false` en laat de rest null/leeg.
7. Persoonsnamen nooit overnemen; uitspraken zijn al geanonimiseerd, houd dat zo.
8. `taxonomie.json` staat in `/home/claude/data/taxonomie.json`. Gebruik alleen sleutels die daar staan.

Lees elk invoerbestand volledig (Read-tool) voordat je schrijft. Schrijf met de Write-tool. Rapporteer aan het eind alleen: aantal verwerkt, aantal niet relevant, en eventuele twijfelgevallen (ECLI + 1 regel).
