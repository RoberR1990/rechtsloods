# Opdracht: "Snel op de hoogte" — trends en ontwikkelingen per onderwerp

Doelgroep: een collega die nieuw is bij de afdeling Parkeren van een grote gemeente (beleidsmaker, productmanager, bezwaarbehandelaar) en snel op vlieghoogte moet komen: wat speelt er, wat is veranderd in tien jaar, op welk niveau (Hoge Raad/Raad van State, hoven, rechtbanken), en wat komt eraan. Gewone taal (B1), concreet, geen jargon zonder uitleg. Geen opsommingen van losse zaken: zoek patronen en verschuivingen.

Invoer: `/home/claude/data/trends_in/<onderwerp>.json` met `per_jaar` (aantallen, uitkomsten — "auto:gegrond" etc. zijn automatisch afgeleid, de andere uit samenvattingen —, per niveau en per subonderwerp), `hoogste_en_vaak_aangehaald` (uitspraken van Hoge Raad/Raad van State en vaak aangehaalde, met inhoudsindicatie en soms een samenvatting), `recent_samengevat` en `stand_van_het_recht` per subonderwerp.

Schrijf `/home/claude/data/trends_uit/<onderwerp>.json`:
```json
{
 "kort": "<3 zinnen: waar gaat dit onderwerp over en wat moet een nieuwkomer als eerste weten>",
 "ontwikkelingen": [{"titel": "<max 8 woorden>", "zin": "<2-3 zinnen: de trend of verschuiving, met jaartallen>", "bronnen": [{"ecli": "...", "citaat": "<letterlijk 5-25 woorden>"}]}],
 "kantelpunten": [{"datum": "JJJJ-MM-DD", "ecli": "...", "label": "<max 10 woorden: wat veranderde hierdoor>"}],
 "niveaus": {"top": "<1-2 zinnen: wat de hoogste rechter bepaalt>", "hoven": "<1-2 zinnen>", "rechtbanken": "<1-2 zinnen: waar het volume zit en wat daar speelt>"},
 "nu": ["<wat speelt nu (2025-2026), 1 zin elk, max 4>"],
 "komt": ["<wat komt eraan of is onzeker: open vragen, conclusies A-G, prejudiciële vragen, wetswijzigingen die in de uitspraken genoemd worden; max 3; alleen als de invoer dat ondersteunt>"],
 "cijfers": "<1-2 zinnen over volume en uitkomsten, met de kanttekening dat publicatie selectief is en sterk is gestegen>"
}
```

## Harde regels
1. 3-5 ontwikkelingen, 3-7 kantelpunten. Elke ontwikkeling minimaal 1 bron met een citaat dat LETTERLIJK voorkomt in de `inhoudsindicatie` van die ECLI, of in `kern.citaat` / `rechtsregel.citaat`. Exact kopiëren; dit wordt gecontroleerd.
2. Kantelpunten: alleen uitspraken uit de invoer (bij voorkeur Hoge Raad/Raad van State of vaak aangehaald), met de echte datum uit de invoer.
3. Cijfers: interpreteer voorzichtig. Meer uitspraken kan komen door meer publiceren (rechtspraak.nl publiceerde in 2024 63.700 en in 2025 71.300 uitspraken). Geen percentages "kans op winst".
4. Niets verzinnen buiten de invoer. Geen persoonsnamen.
5. Controleer citaten met een klein script in een eigen map /tmp/<onderwerp>_tr/. Schrijf geldige JSON (ensure_ascii=False).

Rapporteer alleen: onderwerp, aantal ontwikkelingen en kantelpunten, FOUTEN van je citaatcheck.
