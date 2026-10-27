#!/bin/bash
# P37, P38: AI_baseBonusVal gate (GitLab 1fdd6ba1; root-eco-bv, f70541a9 XML) against cf43846b (root-eco-batch).
cd "$(dirname "$0")" && ./batch.sh P37 root-eco-bv root-eco-batch 3 && ./batch.sh P38 root-eco-bv root-eco-batch 3
