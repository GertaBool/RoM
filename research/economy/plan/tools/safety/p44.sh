#!/bin/bash
# P44, P45: goods unit and category in the resource records (GitLab 4bea4e0e; root-eco-gwf1f) against 9a5795e9
# (root-eco-gwf1), both with the 9a5795e9 harness DLL.
cd "$(dirname "$0")" && ./batch.sh P44 root-eco-gwf1f root-eco-gwf1 3 && ./batch.sh P45 root-eco-gwf1f root-eco-gwf1 3
