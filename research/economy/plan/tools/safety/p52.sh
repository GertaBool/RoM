#!/bin/bash
# P52, P53: the map scale on CvMap (GitLab 857ca9f3; root-eco-prf6) against ba209b49 (root-eco-gwf5), the same XML
# (4bea4e0e), each with its harness DLL.
cd "$(dirname "$0")" && ./batch.sh P52 root-eco-prf6 root-eco-gwf5 3 && ./batch.sh P53 root-eco-prf6 root-eco-gwf5 3
