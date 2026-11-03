#!/bin/bash
# P56, P57: the Mediterranean Standard scenario as GitLab d2a8f756 has it (BeginEconomy block, 4,470 km2; converted
# into root-eco-prf6t3/map.scn) against the scenario before the edits (root-eco-prf6t2), the same harness and DLL.
cd "$(dirname "$0")" && ./batch.sh P56 root-eco-prf6t3 root-eco-prf6t2 3 && ./batch.sh P57 root-eco-prf6t3 root-eco-prf6t2 3
