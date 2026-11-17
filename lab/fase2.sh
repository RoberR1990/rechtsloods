#!/bin/bash
# Fase 2 (toepassing), voorbereidend: alle 3 mix-modellen draaien, zodat elke mixkeuze (2 of 3 modellen) daarna kan worden gescoord.
cd "$(dirname "$0")/.."
export LAB_EFFORT=budget:4000
for m in deepseek/deepseek-v4.1-flash qwen/qwen3.8-flash qwen/qwen3.7-plus; do
  n=$(basename $m)
  python3 -I lab/run.py v3 avg-privacy $m lab/sets/toep_avg_v3.json f2-v3-avg-$n --par 8 > lab/logs/f2-v3-avg-$n.log 2>&1 &
  python3 -I lab/run.py l1 bpm $m lab/sets/toep_bpm_l1.json f2-l1-bpm-$n --par 4 > lab/logs/f2-l1-bpm-$n.log 2>&1 &
done
wait; echo KLAAR
