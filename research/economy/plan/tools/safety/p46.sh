#!/bin/bash
# P46, P47: goods accounts per city (GitLab 9213dc33; root-eco-gwf3) against 4bea4e0e (root-eco-gwf1f), the same
# XML (4bea4e0e), each with its harness DLL.
cd "$(dirname "$0")" && ./batch.sh P46 root-eco-gwf3 root-eco-gwf1f 3 && ./batch.sh P47 root-eco-gwf3 root-eco-gwf1f 3
