#!/bin/bash
# all.sh: the safety runs of the settlement-economy predictions so far (register text: arm a the change, arm b
# the state before it; g0 GitLab main 71de0ab, g1 bd217d67, g2 e694caf0, g3 487f7e0f; prepare.sh makes them).
cd "$(dirname "$0")"
./batch.sh P21 root-eco-g1 root-eco-g0 3 && ./batch.sh P22 root-eco-g1 root-eco-g0 3 &&
./batch.sh P23 root-eco-g2 root-eco-g1 3 && ./batch.sh P24 root-eco-g2 root-eco-g1 3 &&
./batch.sh P25 root-eco-g3 root-eco-g2 3 && ./batch.sh P26 root-eco-g3 root-eco-g2 3
