#!/usr/bin/env python3
"""Check or apply/stage the reviewed patch on a clean, pinned source checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--check', action='store_true', help='validate without modifying the checkout')
    args = parser.parse_args()
    source = args.source.resolve()
    manifest = json.loads((HERE/'manifest.json').read_text())
    patch = HERE/manifest['patch']

    def git(*command):
        return subprocess.check_output(['git', '-C', str(source)]+list(command), text=True).strip()

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

    if digest(patch) != manifest['patch_sha256']:
        parser.error('Patch checksum differs from the published manifest')
    if Path(git('rev-parse', '--show-toplevel')).resolve() != source:
        parser.error('Pass the source repository root')
    if git('rev-parse', 'HEAD') != manifest['base_commit']:
        parser.error('Expected base commit '+manifest['base_commit']+'; no files were changed')
    if git('status', '--porcelain', '--untracked-files=all'):
        parser.error('Use a clean checkout; preserve or commit existing work first')
    for name, hashes in manifest['files'].items():
        if digest(source/name) != hashes['before_sha256']:
            parser.error('Unexpected original file content: '+name)
    git('apply', '--check', '--index', str(patch))
    if args.check:
        print('Patch checksum, base files and indexed application check passed; no files changed.')
        return
    git('apply', '--index', str(patch))
    for name, hashes in manifest['files'].items():
        if digest(source/name) != hashes['after_sha256']:
            raise SystemExit('Post-application mismatch: '+name+'; inspect staged changes')
    print('Applied and staged the source fixes; every changed file matches the tested content.')
    print('Run python3 Tools/run_regression_suite.py in the source checkout.')
    print('The bundled DLL is unchanged. New version-6 saves require a rebuilt DLL.')


if __name__ == '__main__':
    main()
