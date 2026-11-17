# Lab: pilot goedkope modelmix
Scope en besluiten: `docs/pilot-modelmix-scope.md`.
- `run.py` — draait `scripts/verrijk_v3.md` / `verrijk_l1.md` via OpenRouter, checkt met de bestaande checkscripts (in een sandbox `runs/<run>/D`), 1 herstelronde, kosten uit usage, budgetstop $8,80 over `ledger.jsonl`.
- `score.py` — vergelijkt met de maatstaf (`data/uit_v3/parkeren`, niet-relevant uit `data/uit`) en berekent consensus.
- `sets/` — benchmarkset (75 Haiku-steekproef gecorrigeerd, 25 hoge rechters Sonnet, 10 niet-relevant).
- Sleutel: `/home/claude/.secrets/openrouter_key` (buiten de repo).
