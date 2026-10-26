#!/bin/bash
# LQ.F10 as committed (P31, P32: GitLab 6c7605d2, the same tree as root-eco-lq10) against 02d5f85a, then LQ.F11 (P29, P30).
cd "$(dirname "$0")" && ./batch.sh P31 root-eco-lq10 root-eco-g4 3 && ./batch.sh P32 root-eco-lq10 root-eco-g4 3 && ./lq11.sh
