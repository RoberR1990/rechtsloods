for y in 2016 2017 2018 2019 2020 2021 2022; do
  python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht_belastingrecht" $y-01-01 $y-12-31 data/feeds/bel$y.json
  python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht" $y-01-01 $y-12-31 data/feeds/best$y.json
  python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#strafrecht" $y-01-01 $y-12-31 data/feeds/straf$y.json
done
for y in 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026; do e=$([ $y = 2026 ] && echo 2026-11-12 || echo $y-12-31)
  python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#civielRecht" $y-01-01 $e data/feeds/civ$y.json
done
echo KLAAR
