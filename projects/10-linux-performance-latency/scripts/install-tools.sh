#!/usr/bin/env bash
# Tools for this project on Ubuntu/Debian. Run on the LAB HOST (see ADR-0001), not your laptop's Docker.
set -euo pipefail
sudo apt-get update
sudo apt-get install -y sockperf stress-ng numactl hwloc sysstat linux-tools-common "linux-tools-$(uname -r)" bpftrace
echo "Installed. Check: sockperf --version; perf --version; bpftrace --version"
