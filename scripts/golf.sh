#!/bin/bash
# golf.sh <parkeren_sonnet> <parkeren_haiku> <domein_v3> <l1>  -> volgende batch-id's
cd /home/claude/rechtzoeker
echo "S $(python3 scripts/volgende.py v3 parkeren $1 sonnet)"
echo "H $(python3 scripts/volgende.py v3 parkeren $2 haiku)"
for kind in v3 l1; do
  [ $kind = v3 ] && n=$3 || n=$4; out=""
  for s in openbare-orde avg-privacy verkeersboetes woz bpm; do
    [ -f /home/claude/data/batches/${kind}_$s.json ] || continue
    [ $n -le 0 ] && break
    for m in sonnet haiku; do
      [ $kind = l1 ] && m=""
      ids=$(python3 scripts/volgende.py $kind $s $n $m); c=$(echo $ids | wc -w); n=$((n-c))
      for i in $ids; do out="$out $i:${m:-haiku}"; done
      [ $kind = l1 ] && break
      [ $n -le 0 ] && break
    done
  done
  echo "$kind$out"
done
