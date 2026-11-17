#!/bin/bash
# Fase 1: benchmark 110 parkeeruitspraken, 4 modellen, laag 2 en laag 1, reasoning-budget 4000 voor alle modellen.
cd "$(dirname "$0")/.."
export LAB_EFFORT=budget:4000
for m in deepseek/deepseek-v4.1-flash qwen/qwen3.8-flash qwen/qwen3.7-plus mistralai/mistral-small-2603; do
  n=$(basename $m)
  python3 -I lab/run.py v3 parkeren $m lab/sets/bench_parkeren.json f1-v3-$n --par 8 > lab/logs/f1-v3-$n.log 2>&1 &
  python3 -I lab/run.py l1 parkeren $m lab/sets/bench_parkeren.json f1-l1-$n --par 4 > lab/logs/f1-l1-$n.log 2>&1 &
done
wait
echo KLAAR
