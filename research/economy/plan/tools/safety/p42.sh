#!/bin/bash
# P42, P43: GoodUnit and GoodCategory on BonusInfo (GitLab 9a5795e9; root-eco-gwf1: f70541a9 XML with the new
# schema) against 84ea7fc5 (root-eco-gwf7: f70541a9 XML).
cd "$(dirname "$0")" && ./batch.sh P42 root-eco-gwf1 root-eco-gwf7 3 && ./batch.sh P43 root-eco-gwf1 root-eco-gwf7 3
