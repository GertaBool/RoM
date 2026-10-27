#!/bin/bash
# P33, P34: GitLab f70541a9 (the produced-goods AI term fixed; root-eco-fix1) against LQ.F10 as committed (root-eco-lq10).
cd "$(dirname "$0")" && ./batch.sh P33 root-eco-fix1 root-eco-lq10 3 && ./batch.sh P34 root-eco-fix1 root-eco-lq10 3
