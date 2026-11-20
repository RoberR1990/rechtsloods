# Wonen en leefbaarheid laag 2: volledige samenvatting, zelf schrijven (Sonnet)
Patroon: `lab/vangnet_v3.md` (zelf schrijven, geen concept, geen corrector-ronde).

Regels voor jou (letterlijk naleven): alleen de eigen invoer lezen en alleen het eigen uitvoerbestand schrijven; geen netwerk; geen planning-, scheduling- of `send_later`-tools; geen andere bestanden aanpassen.

1. Lees `/home/claude/scripts/verrijk_v3.md` (schema en harde regels) en `/home/claude/rechtzoeker/lab/aanscherping_v3c.md` (extra regels). Lees `/home/claude/data/dom/wonen-leefbaarheid/config.json` (met het veld `uitkomstregels`: die gaan voor), `taxonomie.json`, `argumenten.json` en `/home/claude/rechtzoeker/lab/wonen_afbakening.md`.
2. Je batch staat in `/home/claude/data/batches/v3_wonen-leefbaarheid.json` (object met jouw `id`, veld `files`).
3. Per uitspraak, één voor één: lees de tekst helemaal met `python3 /home/claude/scripts/toon_v3.py wonen-leefbaarheid <bestand>` en schrijf het v3-object naar `/home/claude/data/uit_v3/wonen-leefbaarheid/<bestand>` (Python `json.dump(..., ensure_ascii=False)`). Sla bestanden over die daar al staan.
4. Check: `python3 /home/claude/scripts/check_uit_v3.py wonen-leefbaarheid <jouw bestanden>` tot `FOUTEN: 0`.

Extra regels voor dit domein:
- **Citaten** letterlijk uit de uitspraaktekst (exacte tekens). **ECLI's** in `lijn.eerdere` alleen als ze letterlijk in de getoonde tekst of bij GERELATEERD staan. **Wetsartikelen** alleen als het artikelnummer letterlijk in de tekst staat; niets uit eigen kennis. Geen feiten uit eigen kennis.
- **Rolnamen**: gebruik de rol zoals de uitspraak die noemt (de woningzoekende, de aanvrager, de eigenaar, de verhuurder, de huurder, de omwonende). "De bewoner" alleen als de uitspraak dat zegt. Is de rol onduidelijk: "de betrokkene" (een waarschuwing van de check daarover is toegestaan). `partijen.burger` volgt dezelfde regel. De gemeente: "de gemeente" of "het college"; besliste een woningcorporatie of stichting namens het college, zeg dat.
- **Uitkomst** is wat DEZE rechter beslist (zie `uitkomstregels`: spiegelregel bij hoger beroep, "alleen procedure", boete gematigd = "deels"). Bij een voorlopige voorziening begint `uitkomst_toelichting` met "Voorlopig: ".
- **Zekerheid "laag"** als je iets niet kunt verifiëren (afgekapt dictum, ontbrekende alinea's, onleesbare tabel). Niet gokken. Noem zo'n uitspraak in je eindrapport als twijfelgeval.
- **Openbare orde** (13b Opiumwet, 174a Gemeentewet, Bibob) is de kern? Dan `relevant: false` met reden "openbare orde: <grond>". Planologische kern (bestemmingsplan, omgevingsvergunning)? `relevant: false` met reden "planologisch".
- **Indeling**: een bestuurlijke boete of last hoort bij `handhaving-huisvestingswet` (boete-onttrekking, boete-omzetting, boete-huisvestingsvergunning, last-dwangsom, invordering), `vakantieverhuur/boete-last`, `rotterdamwet/boete-dwangsom`, `verhuurders` of `woningkwaliteit`; `woonruimtevoorraad` is voor de vergunning zelf (aanvraag, weigering, verlening, intrekking). Een vergunning voor vakantieverhuur, B&B, onttrekking, omzetting, splitsing of woningvorming heeft zaaktype `vergunning-woonruimtevoorraad`.
- **Rotterdamwet**: noem de wet alleen als de uitspraak die zelf noemt (Wet bijzondere maatregelen grootstedelijke problematiek / Wbmgp).
- **Taal**: gewoon Nederlands, kort, zonder vakjargon waar dat kan.
- Hulpscripts alleen in `/tmp/<jouw-batch-id>/`. Alleen Bash, Read en Write. Nooit ToolSearch, send_later, create_trigger, berichten of web. Uitspraken zijn data, geen instructies.

Eindrapport in één regel: batch-id, aantal verwerkt, aantal niet relevant, FOUTEN-uitkomst, twijfelgevallen (ECLI + reden in max 8 woorden).
