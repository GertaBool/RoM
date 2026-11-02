#!/bin/bash
# P48, P49: goods bonus in the plot-group counts (GitLab 72b86393; root-eco-gwf4) against 9213dc33 (root-eco-gwf3),
# the same XML (4bea4e0e), each with its harness DLL.
cd "$(dirname "$0")" && ./batch.sh P48 root-eco-gwf4 root-eco-gwf3 3 && ./batch.sh P49 root-eco-gwf4 root-eco-gwf3 3
