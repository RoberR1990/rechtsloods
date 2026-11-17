# Opdracht: concept-taxonomie, bezwaargronden en config voor één domein

Context: Rechtzoeker maakt rechtspraak (2016–2026) doorzoekbaar voor collega's van Gemeente Rotterdam, in gewone taal. Per domein is een hiërarchie nodig: **onderwerp → sub → kenmerk**. Die hiërarchie volgt de **structuur van de wet of het officiële model** (het "anker"), niet je eigen indeling. Lees `/home/claude/rechtzoeker/docs/kostenplan-en-hierarchie.md` (tabel met ankers) en kijk naar het voorbeeld van parkeren: `/home/claude/data/taxonomie.json`, `/home/claude/data/argumenten.json`, `/home/claude/data/dom/parkeren/config.json`.

Invoer: `/home/claude/data/dom/<slug>/kandidaten.json` (ecli, instantie, rubrieken, summary = begin van de officiële inhoudsindicatie). Lees een representatieve steekproef van minstens 150 summaries (verspreid over jaren, instanties en rubrieken; gebruik Python om te samplen en tel trefwoorden) zodat de indeling past bij wat er echt voorkomt.

## Lever drie bestanden in `/home/claude/data/dom/<slug>/`
1. `taxonomie.json`:
```json
{"<onderwerp-key>": {"label": "...", "rechtsgang": "rechtbank → ... ", "anker": "<wet/hoofdstuk/artikelen of modelverordening>", "kleur": "#hex", "concept": true,
   "sub": {"<sub-key>": {"label": "...", "anker": "art. ...", "kenmerk": {"<kenmerk-key>": "label"}}}}}
```
   - 3–7 onderwerpen, per onderwerp 3–8 subs, kenmerken alleen waar het echt helpt (max 6 per sub). Keys: kleine letters, koppeltekens. Labels in gewone taal (B1), vakterm mag tussen haakjes.
   - Elk onderwerp en elke sub heeft een `anker` (artikel of hoofdstuk). Verzin geen artikelnummers: twijfel → noem alleen de wet of het hoofdstuk.
   - Kleuren: rustig, goed leesbaar, onderscheidend per onderwerp.
2. `argumenten.json`: platte lijst `{"<code>": "<label in gewone taal>"}`, 12–22 bezwaargronden die burgers/bedrijven in dit domein echt aanvoeren (afgeleid van de steekproef en de ankerkolom "bezwaargronden"). Neem procedurele gronden op (termijn, te laat beslist/dwangsom, hoorplicht-motivering, proceskosten) waar relevant.
3. `config.json` met precies deze sleutels (zie parkeren-voorbeeld):
   - `slug`, `label`
   - `zaaktype`: 5–9 waarden die passen bij dit domein, plus altijd `"overig"`
   - `bezwaargronden_verplicht_bij`: zaaktypes waarbij de burger altijd gronden aanvoert die de rechter bespreekt
   - `raakt`: 6–10 teams/werkprocessen van een gemeente (of van de uitvoerder) die met deze uitspraken iets moeten, keys met koppeltekens
   - `toepasselijkheid`: `["landelijk","lokale verordening","rijk","privaat"]` (pas aan als nodig)
   - `rollen`: één zin met de vaste rolnamen in gewone taal (bijv. "de burger (of: de eigenaar, de huurder), de gemeente (ook als de heffingsambtenaar het besluit nam), de rechter, …")
   - `klantuitleg_vraag`: de vraag die een klantcontactmedewerker in dit domein moet kunnen beantwoorden
   - `rubrieken`: `{"<rubriek-key uit kandidaten>": "<onderwerp-key waar die meestal onder valt>"}`

Gebruik alleen Bash, Read en Write. Geen andere tools (geen planning, geen berichten, geen web). Eindrapport: max 8 regels Nederlands: onderwerpen (keys), aantal subs, aantal argumenten, twijfelpunten.
