# Pilot goedkope modelmix: resultaten fase 0 tot 2 (15 nov 2026)

Status: **Verkenning**. Bijbehorende scope: `docs/pilot-modelmix-scope.md`. Ruwe cijfers: `lab/score_f1.json`, `lab/score_toep.json`, `lab/judge/`.
Kosten tot nu toe: **$5,89 volgens OpenRouter** (eigen telling $5,82). Dat is 54% van de €10. Het werk van de Sonnet-beoordelaars valt daarbuiten: 21 agents van elk ~110-160k tokens.

## 1. Kosten per 1.000 uitspraken (gemeten via de usage-gegevens van OpenRouter)
| | DeepSeek V4.1 Flash | Qwen3.8 Flash | Qwen3.7 Plus | Mistral Small |
|---|---|---|---|---|
| Laag 1 (labels) | $0,20–0,24 | $0,61–0,67 | $1,28–1,46 | $0,73 |
| Laag 2 (volledig) | $2,42–2,62 | $3,53–3,80 | $11,10 | $4,76 |
Ter vergelijking: Sonnet als subagent verbruikt ~22–25k tokens per uitspraak in laag 2.

## 2. Benchmark parkeren (110 uitspraken; maatstaf = gecorrigeerde Haiku-uitvoer + Sonnet)
**Labels** (gelijk aan de maatstaf, laag 2):
| | scriptcheck ok | uitkomst | onderwerp | sub | alle kernvelden |
|---|---|---|---|---|---|
| DeepSeek | 109/110 | 91% | 98% | 88% | 82% |
| Qwen3.8 Flash | 108/110 | 95% | 100% | 92% | 85% |
| Qwen3.7 Plus | 99/110 | 91% | 98% | 89% | 78% |
| Mistral Small | 19/110 | 79% | 95% | 63% | 35% |
- Mistral Small valt af: de citaten zijn niet letterlijk, ook niet na herstel.
- Qwen3.7 Plus is 4× zo duur en niet beter. Advies: niet in de mix.
- **Consensus van 3 modellen** (zoals vooraf vastgelegd): 63% eens; daarvan klopt 96% op alle kernvelden en 99% op uitkomst. **Met 2 modellen** (DeepSeek + Qwen3.8): 81% eens, 92% op alle kernvelden, 97% op uitkomst. Die 2-modellenvariant is achteraf berekend.
- Laag 1 (labels op korte invoer): DeepSeek alleen 70% op alle kernvelden, uitkomst 90%. Consensus van 3: 60% eens, daarvan 85% alle kernvelden en 96% uitkomst. Blinde toets op de 13 consensus-items met een labelverschil, geteld per veld: in laag 1 kreeg de maatstaf 7 keer gelijk, het model 1 keer en beide 2 keer. In laag 2 kreeg het model 3 keer gelijk. Geen ernstige fouten.

**Teksten** (blinde beoordeling door een Sonnet-agent: A/B willekeurig, model tegen maatstaf):
| | goed | klein | ernstig | voorkeur model / gelijk / maatstaf |
|---|---|---|---|---|
| DeepSeek, oorspronkelijke instructie (n=55) | 13% | 82% | 5% | 12 / 7 / 36 |
| Maatstaf, zelfde items | 47% | 49% | 4% | |
| **DeepSeek + aanscherping v3b** (n=30) | **27%** | **70%** | **3%*** | **13 / 4 / 13** |
| Maatstaf, zelfde 30 | 43% | 57% | 0% | |
\* Het ene "ernstige" geval was een fout van de beoordelaar: de aangehaalde ECLI staat in alinea 98. Na controle is het dus 0 van 30.
- Terugkerende kleine fouten van DeepSeek: burger standaard "bewoner", bewijslast verzonnen, "vaste lijn" zonder grond, wetsartikelen uit eigen kennis, te ruime actie_gemeente, proceskosten ontbreken in het gevolg. De aanscherping (`lab/aanscherping_v3b.md`, 8 regels) pakt die aan.
- **De drempel "≥ 65% helemaal goed" haalt ook de maatstaf zelf niet bij deze (strenge) beoordelaar** (43–60%). Dezelfde maatstaf-teksten kregen bij twee rondes 53% en 43% goed: de beoordelaar schommelt ±10 procentpunt. Absolute percentages zijn dus niet bruikbaar; de vergelijking met de maatstaf wel.

## 3. Toepassing op nieuwe domeinen (geen maatstaf)
| | eens (DeepSeek + Qwen3.8) | eens (3 modellen) | scriptcheck ok |
|---|---|---|---|
| AVG laag 2, v3b (150 hoge rechters) | 57% | — | 149/150 en 145/150 |
| BPM laag 1 (300) | 41% | 29% | 300, 293 en 300 van 300 |
- De meeste verschillen zitten in **BPM-uitkomst**: bij 92 van de 300 zijn de modellen het oneens. De blinde toets op 15 daarvan: DeepSeek 8 keer goed, Qwen 6 keer, 1 keer beide. Op BPM-uitkomst zijn beide dus onbetrouwbaar. De consensuspoort is hier nodig en stuurt veel door naar het vangnet.
- AVG: de uitkomst van DeepSeek (laag 2) wijkt bij 23% af van de bestaande Haiku-laag 1. Blinde toets op 10: DeepSeek 8 keer goed, Haiku 2 keer.
- Nieuwe domeinen hebben een concept-taxonomie (onderwerp, sub en zaaktype verschillen vaak). Dat drukt de consensus.

## 4. Wat dit betekent (Verkenning)
- **Laag 1:** DeepSeek + Qwen3.8 met consensus en vangnet is goedkoop (< $1 per 1.000) en op parkeren zonder ernstige fouten. Op BPM is de uitkomst lastig; een kwart tot de helft gaat dan naar het vangnet.
- **Laag 2:** met aanscherping v3b scoort DeepSeek in de blinde vergelijking gelijk met de maatstaf (13–13), met meer kleine fouten. Kosten ~$6 per 1.000 voor 2 modellen plus het vangnet voor 20–45%.
- Nog niet gedaan: een jurist-steekproef (10), en v3b gemeten met beide modellen op de volledige 110.

## 5. Gemaakte keuzes tijdens de pilot (vastgelegd)
- Denkbudget 4.000 tokens voor alle modellen. Max_tokens verhoogd naar 24.000 omdat de aanbieder Baidu het budget negeerde (21 afgekapte antwoorden van DeepSeek, opnieuw gedraaid).
- De runs van AVG met de oude instructie zijn afgebroken (deels in `lab/runs/f2-v3-avg-*`) ten gunste van v3b. Qwen3.7 Plus is gestopt na de benchmark.
- De beoordelaars werkten elk in een eigen map, kregen geen modelnamen te zien en hadden geen toegang tot de sleutel (`lab/judge_key_*.json`).

## 6. Bevestiging en afronding (na de besluiten van 15 nov, avond)
- **v3b op alle 110 parkeeruitspraken** (`lab/runs/f1c-*`):
  - DeepSeek: 110/110 zonder scriptfouten, uitkomst 91%, alle kernvelden 84%, $2,10 per 1.000.
  - Qwen3.8 Flash: 109/110 zonder scriptfouten, uitkomst 89%, kernvelden 79%, $3,65 per 1.000.
  - **Eens: 85 van 110 (77%)**; daarvan 92% op alle kernvelden gelijk aan de maatstaf.
- **Uitkomstverschillen binnen de consensus (5 van 85), blind getoetst:**
  - 3 keer zijn beide antwoorden aanvaardbaar (de grens tussen "alleen procedure" en "wederpartij wint").
  - 2 keer is het model te positief voor de burger: "burger wint" of "deels", terwijl het alleen om proceskosten of terugwijzing ging.
  - Dat is **2 op 85 (2,4%)**, net boven de grens van 2% voor ernstige fouten. Kandidaat voor een extra regel: wie alleen proceskosten, een dwangsom of terugwijzing krijgt, heeft uitkomst "alleen procedure".
- **AVG: 150 uitspraken in laag 2 zijn klaar** (`lab/out/avg-privacy/`, herkomst per uitspraak in `lab/out/avg-privacy_herkomst.json`):
  - 86 via consensus (DeepSeek, v3b) en 64 via het vangnet (Sonnet-subagents, 11 batches).
  - Check: 150 bestanden, **0 fouten**, 43 waarschuwingen.
  - Het vangnet kostte ~29k Sonnet-tokens per uitspraak. Het totaal is daarmee ~57% minder Sonnet-tokens dan alles via Sonnet, plus $0,96 aan OpenRouter.
  - Nog niet overgezet naar `data/uit_v3/avg-privacy`: dat is de map van de sessie `domeinen`.
- **Jurist-pakket:** Claude Doc "Rechtsloods – jurist-toets AI-samenvattingen (blind, 10 uitspraken)", https://claude.ai/artifact/5GSBF2wMWrqd2ZNiU9hG5i. Daarin 5 parkeeruitspraken A/B (blind: DeepSeek v3b tegen de bestaande uitvoer) en 5 AVG-uitspraken (4 via consensus, 1 via het vangnet). De sleutel staat in `lab/jurist_key.json`; deel die niet met de jurist.
- **Kosten totaal: $6,53 (OpenRouter)** van de €10.

## 7. Overdracht
- Draaien: `LAB_EFFORT=budget:4000 LAB_EXTRA=lab/aanscherping_v3b.md python3 -I lab/run.py v3 <slug> <model> <set> <run-id>`, voor beide modellen. Daarna de consensus bepalen (zie `lab/score_toep.py`), en de rest naar Sonnet-subagents volgens `lab/vangnet_opdracht.md`.
- Open:
  - het oordeel van de jurist
  - een uitkomstregel voor proceskosten of terugwijzing
  - BPM: de uitkomst van belastingzaken (41% eens)
  - overzetten van de AVG-uitvoer naar de sessie `domeinen`
  - **de OpenRouter-sleutel roteren** na afloop

## 8. Efficiëntieronde (15 nov, avond)
- **Uitkomstregel v3c** (`lab/aanscherping_v3c.md`, en `aanscherping_l1c.md` voor laag 1): proceskosten, dwangsom en terugwijzing = "alleen procedure"; vaste regels voor belastingzaken.
  - Parkeren, DeepSeek: uitkomst 93,6% gelijk aan de maatstaf (was 90,9%), 0 scriptfouten.
  - BPM laag 1: uitkomstverschillen tussen de twee modellen 92 → **29** van 300; eens 41% → **54%** (68% als sub niet meetelt). Kosten gelijk ($0,86 per 1.000).
- **Tweede model alleen labels** (`run.py v3lab`): Qwen leest dezelfde volledige tekst, maar geeft alleen de kernvelden terug.
  - Kosten laag 2 per 1.000: **$3,18** (DeepSeek $2,02 + Qwen-labels $1,16), was $5,75: **−45%**.
  - Eens: **80%** (was 77%); daarvan 93% op alle kernvelden en **98,9% op uitkomst** gelijk aan de maatstaf (1 verschil, en daarin is het model voorzichtiger).
- **Extra deterministische check** (`lab/extra_check.py`): ECLI's die niet in de tekst staan, artikelnummers die niet in de tekst staan, en "bewoner" zonder grond.
  - DeepSeek v3b op 100 relevante uitspraken: 1 / 1 / 2. Ter vergelijking: oude prompt 5 / 5 / 22, maatstaf 0 / 1 / 10.
  - AVG: 59 van 149 hebben "bewoner", ook bij Sonnet. Oorzaak: het schema noemt "bewoner" als voorbeeld. Dit is een schemapunt, geen modelfout.
- Kosten pilot totaal: $7,06 (stop bij $8,80).

## 9. Afmaken met de pijplijn (15–16 nov, nacht)
`lab/pijplijn.py draai|samen`: laag 2 = DeepSeek (v3c) + Qwen3.8-labels; laag 1 = DeepSeek + Qwen3.8 (l1c). Bij onenigheid gaat de uitspraak naar het vangnet.
| Domein | Laag | n | eens | vangnet | resultaat |
|---|---|---|---|---|---|
| Openbare orde | 2 (rest) | 152 | 102 (67%) | 50 (Sonnet als corrector) | `lab/out/openbare-orde/`, 0 fouten. Met de 258 die er al waren is alles uit de batches klaar (410). |
| AVG | 2 (rest) | 292 | 189 (65%) | 103 (Sonnet zelf geschreven) | `lab/out/avg-privacy/` nu **442/442**, 0 fouten |
| BPM | 1 (alles) | 2.537 | 1.194 (47%) | 1.343 → Haiku, **nog niet gedraaid** | consensusdeel staat klaar |
| Wahv (proef) | 1 | 300 | 175 (58%) | 125 → Haiku, nog niet gedraaid | zie hieronder |

- **Sonnet als corrector bespaart niets:** ~35k tokens per uitspraak, tegen ~29–33k bij zelf schrijven. De correctors herschreven veel. Voor het vervolg is "zelf schrijven" de standaard (`lab/vangnet_v3.md`).
- **Scheidsrechter (derde model, 2 van 3) uitgezet.** Wahv-proef: waar de meerderheid van de 3 modellen afwijkt van Haiku-laag 1, had de meerderheid bij de blinde toets 4 keer gelijk, Haiku 9 keer en beide 2 keer (n=15). Dat zou ~4% foute uitkomsten geven. Alles waarover de modellen het oneens zijn gaat nu naar het vangnet.
- Wahv-proef, consensus tegen Haiku-laag 1 (n=175): relevant 100%, onderwerp 92,5%, uitkomst 94,3%, zaaktype 74% (de zaaktypes van het concept-schema overlappen).
- Openbare orde, opgemerkt door de correctors: een uitkomstregel voor strafzaken ontbreekt (straf lager in hoger beroep: "deels" of "wederpartij wint"?). Kandidaat voor een v3d-regel.
- Extra check op `lab/out/avg-privacy`: 108 keer "bewoner" zonder grond (schemapunt), 5 artikelen niet letterlijk in de tekst, 1 ECLI.
- Kosten OpenRouter totaal $12,75. Stop bij $20,06.

## 10. Vangnet BPM en Wahv-proef gedraaid (16 nov)
- **BPM laag 1 compleet: 2.537/2.537** (`lab/out/bpm_l1.json` + herkomst): 1.194 via consensus (DeepSeek), 1.343 via Haiku-subagents (54 batches). Vangnet-check: 0 fouten. 15 niet relevant.
- **Wahv-proef: 300/300** (`lab/out/verkeersboetes_l1.json`): 175 via consensus, 125 via Haiku. 0 fouten.
- **Haiku-verbruik:** 20 agents, elk 3 batches van 25. Samen ~5,3M tokens, ~3,6k per uitspraak. Dat is ongeveer de helft van de oude ~7k bij één batch per agent.
- **Gemeld door het vangnet, voor de jurist of de domeinsessie:**
  - In BPM-hofzaken is het dictum vaak afgekapt of staat het in een tabel. Daar staat de uitkomst op zekerheid laag.
  - GHARL:2026:1328 noemt een "verminderde" naheffing die hoger is dan de oorspronkelijke aanslag. Mogelijk een fout in de bron.
  - GHSHE:2022:565 en 1118 zijn als niet relevant gemarkeerd (weigering van een gemachtigde, geen BPM-inhoud).
- Kosten OpenRouter blijven $12,75: het vangnet liep via Claude.

## Stand per domein (16 nov)
| Domein | Laag 1 | Laag 2 (hoge rechters + Rotterdam) | Waar |
|---|---|---|---|
| Parkeren | n.v.t. | 2.721 v3; ~1.000 v2 (bewust) | data/ (domeinen) |
| Openbare orde | 2.005 ✓ | 410/410 ✓ (152 nieuw) | lab/out/openbare-orde |
| AVG | 1.174 ✓ | 442/442 ✓ | lab/out/avg-privacy |
| BPM | 2.537/2.537 ✓ | nog niet gepland | lab/out/bpm_l1.json |
| Wahv | 475 (Haiku) + proef 300 | — | lab/out/verkeersboetes_l1.json |
Alles in `lab/out` moet nog worden overgezet door de sessie `domeinen`. Daarna: `build_verrijkt`, de site-data en de feeds.

## 11. Kosten oud tegen nieuw in API-dollars (16 nov, Verkenning)
API-prijzen (platform.claude.com, 16 nov), per miljoen tokens: Sonnet 5.5 $2 in, $10 uit, $0,10 cache-lezen; Haiku 5.5 $0,10 in, $0,50 uit, $0,01 cache-lezen.
De agents rapporteren alleen totale tokens. Ik reken daarom met een bandbreedte:
- **Laag** (90% cache-lezen, 5% cache-schrijven, 5% uitvoer): Sonnet $0,72 en Haiku $0,04 per miljoen.
- **Hoog** (geen cache, 5% uitvoer): Sonnet $2,40 en Haiku $0,12 per miljoen.

**Wat er nu is gedaan** (594 uitspraken laag 2 + 2.837 laag 1):
| | Sonnet-tokens | Haiku-tokens | OpenRouter | Totaal API-equivalent |
|---|---|---|---|---|
| Oud (alles Claude: Sonnet ~30k per uitspraak laag 2, Haiku ~7k laag 1) | 17,8M | 19,9M | – | $13,5–45 |
| Nieuw (gemeten) | 7,0M | 5,3M | $6,65* | $11,9–24 |
\* Inclusief ~$1,20 voor de scheidsrechter die later is uitgezet. Daarnaast kostte het onderzoek (benchmark, varianten) $6,09 OpenRouter plus ~5M Sonnet-tokens voor de blinde beoordelaars.

**Per 1.000 uitspraken:**
| | Oud | Nieuw |
|---|---|---|
| Laag 2 | $21–72 | $11–29 (−50 à −60%) |
| Laag 1 | $0,28–0,84 | $0,93–1,08 (**duurder**) |

**Conclusie (Verkenning):**
- De mix loont voor laag 2.
- Voor laag 1 is Haiku 5.5 zelf al zo goedkoop dat OpenRouter niets bespaart in dollars. Haiku met 3 batches per agent (~3,6k tokens per uitspraak) kost ~$0,14–0,44 per 1.000. Dat is de goedkoopste route.
- Op een abonnement verschuift het beeld. OpenRouter is dan extra geld, Claude-tokens niet tot aan de limiet. Laag 1 dus via Haiku in batches, laag 2 via de mix.

## 12. Wahv afgerond (16 nov)
- **Laag 1:** 3.969/3.969 via Haiku-subagents (3 batches per agent, 47 agents, ~11,8M Haiku-tokens, ~3,4k per uitspraak). Geen OpenRouter, conform conclusie §11. 89 niet relevant (vooral parkeren).
- **Uitkomstregels Wahv** vastgelegd (nihil = burger wint; alleen OvJ-beslissing vernietigd = alleen procedure). Daarna 158 labels opnieuw beoordeeld.
- **Laag 2:** een selectie van 150 via de mix. 94 keer waren de goedkope modellen het eens (63%), 56 gingen naar het Sonnet-vangnet. OpenRouter: ~$0,85. De 15 verschillen tussen laag 1 en laag 2 zijn met de hand afgestemd (11 in laag 1 aangepast, 4 in laag 2).
- Kosten OpenRouter totaal: $13,60.
