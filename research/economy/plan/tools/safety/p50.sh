#!/bin/bash
# P50, P51: the economy pass (GitLab ba209b49; root-eco-gwf5) against 72b86393 (root-eco-gwf4), the same XML
# (4bea4e0e), each with its harness DLL.
cd "$(dirname "$0")" && ./batch.sh P50 root-eco-gwf5 root-eco-gwf4 3 && ./batch.sh P51 root-eco-gwf5 root-eco-gwf4 3
