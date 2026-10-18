#!/usr/bin/env python3
"""Moved to method/hooks/claude_precommit.py. Kept so that a session started with the old hook
path keeps working."""
import os, runpy

root = os.environ.get('CLAUDE_PROJECT_DIR') or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
runpy.run_path(os.path.join(root, 'method/hooks/claude_precommit.py'), run_name='__main__')
