#!/bin/bash
# LQ.F10 safety runs: arm a the lumber camp branch (root-eco-lq10, harness DLL b-lq10), arm b 02d5f85a (root-eco-g4).
cd "$(dirname "$0")" && ./batch.sh P27 root-eco-lq10 root-eco-g4 3 && ./batch.sh P28 root-eco-lq10 root-eco-g4 3
