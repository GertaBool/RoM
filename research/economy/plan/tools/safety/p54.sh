#!/bin/bash
# P54, P55: a scenario declaring its map scale (root-eco-prf6t2b: Mediterranean Standard with a BeginEconomy block,
# 31,250 km2, in its map.scn) against the same scenario without it (root-eco-prf6t2), the same harness and DLL (857ca9f3).
cd "$(dirname "$0")" && ./batch.sh P54 root-eco-prf6t2b root-eco-prf6t2 3 && ./batch.sh P55 root-eco-prf6t2b root-eco-prf6t2 3
