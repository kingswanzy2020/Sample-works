#!/usr/bin/env bash
# Generate interference while you measure. Each mode is a different "noisy neighbour".
# Usage: MODE=cpu NOISE_CPUS=2 DURATION=40 scripts/noise.sh
set -euo pipefail
MODE="${MODE:-cpu}"; DURATION="${DURATION:-40}"; NOISE_CPUS="${NOISE_CPUS:-}"
pin=""; [[ -n "$NOISE_CPUS" ]] && pin="taskset -c $NOISE_CPUS"
case "$MODE" in
  cpu)     $pin stress-ng --cpu 0 --timeout "${DURATION}s" ;;               # compute-heavy neighbour
  cache)   $pin stress-ng --cache 0 --timeout "${DURATION}s" ;;             # thrash shared CPU caches
  memory)  $pin stress-ng --vm 2 --vm-bytes 75% --timeout "${DURATION}s" ;; # memory pressure / bandwidth
  io)      $pin stress-ng --hdd 2 --timeout "${DURATION}s" ;;               # disk I/O and its interrupts
  syscall) $pin stress-ng --switch 0 --timeout "${DURATION}s" ;;            # context-switch storm
  *) echo "unknown MODE: $MODE (cpu|cache|memory|io|syscall)"; exit 1 ;;
esac
