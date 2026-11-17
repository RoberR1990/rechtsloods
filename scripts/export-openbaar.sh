#!/bin/bash
# Kopieert de openbare onderdelen van de werkrepo (privé) naar een checkout van de openbare repo.
# Gebruik: scripts/export-openbaar.sh <werkrepo> <openbare-checkout>
# Daarna in de openbare checkout: git add -A && git commit && git push
set -e
SRC=$(cd "$1" && pwd); DST=$(cd "$2" && pwd)
# Wat NIET mee gaat: sessienotities, Claude-instructies, experimentruns, ruwe downloads, video-bronnen.
# Doel leegmaken (behalve .git, README, LICENSE, CONTRIBUTING) en opnieuw vullen.
find "$DST" -mindepth 1 -maxdepth 1 ! -name .git ! -name README.md ! -name LICENSE ! -name CONTRIBUTING.md -exec rm -rf {} +
(cd "$SRC" && tar cf - \
  --exclude=./.git --exclude=./CLAUDE.md \
  --exclude='./docs/sessie-*.md' --exclude=./docs/STAND.md --exclude=./docs/teams-kanaal.md \
  --exclude=./lab/runs --exclude=./data/raw --exclude=./video \
  --exclude=./README.md --exclude=./LICENSE --exclude=./CONTRIBUTING.md .) | (cd "$DST" && tar xf -)
# Data: alleen afgeleide uitvoer (data/uit_v3), de rest van data/ blijft weg.
find "$DST/data" -mindepth 1 -maxdepth 1 ! -name uit_v3 -exec rm -rf {} + 2>/dev/null || true
# Interne adressen weghalen.
sed -i -E 's#https?://192\.168\.[0-9.]+(:[0-9]+)?#het interne beheeradres#g; s#192\.168\.[0-9.]+#intern adres#g' "$DST"/docs/*.md 2>/dev/null || true
# Controle: geen privé-IP's of sleutels mee.
if grep -rInE '192\.168\.|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}' "$DST" --exclude-dir=.git --exclude-dir=data -l | head -3 | grep .; then
  echo "STOP: gevoelig patroon gevonden (bestanden hierboven)"; exit 1; fi
echo "Export klaar. Controleer met: git -C $DST status --short | head"
