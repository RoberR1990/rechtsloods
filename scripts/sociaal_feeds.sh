#!/bin/bash
# Zoekfeeds voor sociaal-domein (stap 1): bestuursrecht en civiel recht per jaar, 2016 t/m einddatum, 6 tegelijk.
# Gebruik: bash scripts/sociaal_feeds.sh [einddatum 2026]   (bestaande bestanden worden overgeslagen door scripts/feed.py)
cd "$(dirname "$0")/.." && mkdir -p data/feeds
EIND=${1:-2026-11-20}
run(){ s=$1; k=$2; y=$3; e=$([ $y = 2026 ] && echo $EIND || echo $y-12-31); python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#$s" $y-01-01 $e data/feeds/$k$y.json; }
export -f run; export EIND
for y in $(seq 2016 2026); do echo "bestuursrecht best $y"; echo "civielRecht civ $y"; done | xargs -P 6 -L 1 bash -c 'run $0 $1 $2'
echo KLAAR
