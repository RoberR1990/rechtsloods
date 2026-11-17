for y in 2016 2017 2018 2019 2020 2021; do python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#civielRecht" $y-01-01 $y-12-31 data/feeds/civ$y.json; done; echo KLAAR
