#!/bin/bash
# LQ.F11 safety runs: arm a LQ.F10 plus LQ.F11 (root-eco-lq11), arm b LQ.F10 alone (root-eco-lq10); same harness DLL b-lq10.
cd "$(dirname "$0")" && ./batch.sh P29 root-eco-lq11 root-eco-lq10 3 && ./batch.sh P30 root-eco-lq11 root-eco-lq10 3
