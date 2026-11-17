#!/bin/bash
# Zet de werkomgeving klaar. Scripts verwachten /home/claude/data en /home/claude/site.
set -e
R=$(cd "$(dirname "$0")" && pwd)
cd "$R/data/raw"
[ -f ../uitspraken.json ] || gunzip -c uitspraken.json.gz > ../uitspraken.json
mkdir -p ../feeds && for f in feeds_*.tgz; do tar xzf "$f" -C ..; done
mkdir -p ../proef && ln -sfn ../uit ../proef/uit
python3 "$R/scripts/maak_in3.py"
ln -sfn "$R/data" /home/claude/data
python3 "$R/scripts/maak_in_v3.py" parkeren
ln -sfn "$R/data" /home/claude/data
ln -sfn "$R/site" /home/claude/site
ln -sfn "$R/scripts" /home/claude/scripts
echo "Klaar. Server: cd /home/claude/site && nohup python3 -m http.server 8765 &"
