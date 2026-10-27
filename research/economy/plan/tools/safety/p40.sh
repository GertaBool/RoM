#!/bin/bash
# P40, P41: copyNonDefaults carries every member read (GitLab 84ea7fc5; root-eco-gwf7) against 1fdd6ba1 (root-eco-bv).
cd "$(dirname "$0")" && ./batch.sh P40 root-eco-gwf7 root-eco-bv 3 && ./batch.sh P41 root-eco-gwf7 root-eco-bv 3
