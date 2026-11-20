# Sociaal domein: besluiten (door Robert te bevestigen)

Elk besluit: wat ik heb gekozen, het alternatief, waarom, en de status "door Robert te bevestigen". Vaste regels uit bestaande domeinen gaan voor eigen inzicht.

## B1. Werkrepo: `rechtsloods` in plaats van `rechtzoeker`
- **Besluit:** gewerkt in `RoberR1990/rechtsloods`, de enige repo die aan deze sessie hangt.
- **Alternatief:** werken in `RoberR1990/rechtzoeker` (privé), zoals de opdracht zegt.
- **Reden:** `rechtzoeker` is voor deze sessie niet bereikbaar (add_repo: "you don't have access"). `list_repos` toont alleen `rechtsloods`.
- **Status:** door Robert te bevestigen.

## B2. Vertrekpunt `main` in plaats van `live`
- **Besluit:** branch `col/sociaal-domein` vertrekt vanaf `main` (db7c004).
- **Alternatief:** vertrekken vanaf `live`.
- **Reden:** `rechtsloods` heeft geen `live`. `main` is "snapshot live, 16 nov 2026" plus drie huisstijlcommits.
- **Status:** door Robert te bevestigen.

## B3. Geen domeininhoud per uitspraak in deze (openbare) repo: BLOKKADE na stap 2
- **Besluit:** stap 0–2 volledig uitgevoerd. Dat zijn afbakening, tellingen, filter, precisiemeting, taxonomie, uitkomstregels en config. Ook de tooling voor stap 3–8 staat klaar. Stap 3–8 heb ik **niet** uitgevoerd: labels, samenvattingen, citaten, stand en site-data.
- **Alternatief:** alles bouwen en op `col/sociaal-domein` in `rechtsloods` zetten.
- **Reden:** `rechtsloods` is **openbaar** (`list_repos`: visibility public) en is de geschoonde export van de werkrepo (`scripts/export-openbaar.sh` laat `data/` behalve `uit_v3` bewust weg). Een branch in een openbare repo is voor iedereen leesbaar. Daarmee zou het domein gepubliceerd zijn. De opdracht zegt hard: "Niet publiceren zonder FG-akkoord" en "blijft altijd op je eigen branch". Die regel gaat uit van een privé-repo. Stap 3 en verder leveren per uitspraak inhoud op (labels, samenvattingen, citaten). Die wil ik vóór FG-akkoord niet openbaar maken.
- **Wat wél in de repo staat:** scripts, config, taxonomie, besluiten, tellingen en een ECLI-lijst met metadata. Dat zijn instantie, datum, wetscode uit het zaaknummer en prioriteit. Al deze gegevens staan ook openbaar in Open Data Rechtspraak. Inhoudsindicaties en uitspraakteksten staan niet in de repo.
- **Status:** door Robert te bevestigen. Oplossing: start een sessie met `rechtzoeker` gekoppeld, haal deze branch binnen (`git fetch https://github.com/RoberR1990/rechtsloods col/sociaal-domein`) en hervat bij "Volgende actie" in de STAND.

## B4. Slug `sociaal-domein` naast bestaande `sociaal` in index.json
- **Besluit:** nieuwe slug `sociaal-domein` zoals de opdracht zegt. De bestaande regel `sociaal` (status binnenkort, n=12792) in `site/data/domeinen/index.json` laat ik ongemoeid.
- **Alternatief:** de bestaande slug `sociaal` hergebruiken.
- **Reden:** de opdracht noemt de slug expliciet. De live-index mag ik buiten mijn branch niet aanpassen. Het samenvoegen van beide regels is een besluit bij het live zetten.
- **Status:** door Robert te bevestigen.
