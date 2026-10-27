#!/bin/bash
# P35, P36: batched good-count updates (GitLab cf43846b; root-eco-batch, same XML as f70541a9) against f70541a9 (root-eco-fix1).
cd "$(dirname "$0")" && ./batch.sh P35 root-eco-batch root-eco-fix1 3 && ./batch.sh P36 root-eco-batch root-eco-fix1 3
