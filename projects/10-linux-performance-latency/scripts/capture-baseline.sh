#!/usr/bin/env bash
# Record the host facts that affect latency, so every result can be tied to the exact configuration.
# Usage: scripts/capture-baseline.sh <label>     → results/<timestamp>-<label>/system.txt
set -uo pipefail
label="${1:-baseline}"
dir="$(dirname "$0")/../results/$(date -u +%Y%m%dT%H%M%SZ)-$label"
mkdir -p "$dir"
out="$dir/system.txt"

section() { printf '\n===== %s =====\n' "$1" >> "$out"; }
run() { section "$*"; ( "$@" ) >> "$out" 2>&1 || echo "(not available)" >> "$out"; }

: > "$out"
run uname -a
run lscpu
run numactl --hardware
run cat /proc/cmdline                                        # isolcpus, nohz_full, etc.
run cat /sys/kernel/mm/transparent_hugepage/enabled
run cat /proc/sys/vm/swappiness
section "cpufreq governors"
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 2>/dev/null | sort | uniq -c >> "$out" || echo "(none)" >> "$out"
section "cpuidle states (cpu0)"
for s in /sys/devices/system/cpu/cpu0/cpuidle/state*; do
  [[ -d "$s" ]] && echo "$(cat "$s/name") latency=$(cat "$s/latency")us disabled=$(cat "$s/disable")" >> "$out"
done
section "IRQ affinity (top 15 by count)"
awk 'NR>1 {s=0; for(i=2;i<=NF;i++) if ($i ~ /^[0-9]+$/) s+=$i; print s, $0}' /proc/interrupts 2>/dev/null \
  | sort -rn | head -15 | cut -c1-160 >> "$out"
run systemctl is-active irqbalance
run sh -c 'ls /sys/class/net | grep -v lo | head -3 | xargs -I{} ethtool -c {}'   # interrupt coalescing
echo "wrote $out"
