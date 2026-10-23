"""Restore one installation: python restore.py /path/to/mod/CoffeeChain-backup-TIMESTAMP"""
from pathlib import Path
import sys,json,hashlib
b=Path(sys.argv[1]).resolve();root=b.parent;entries=json.loads((b/'restore.json').read_text())
for e in entries:
 p=root/e['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=e['new_sha256']:raise SystemExit('File changed since installation; refusing restore: '+str(p))
 if e['existed'] and not (b/e['path']).is_file():raise SystemExit('Missing backup: '+e['path'])
for e in entries:
 p=root/e['path']
 if e['existed']:p.write_bytes((b/e['path']).read_bytes())
 else:p.unlink()
print('Restored original files; backup retained.')
