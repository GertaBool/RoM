"""Carry tables that refer to functions by id across a rebuild of functions.tsv (build.sh DLL-only mode).

usage: remap_ids.py <old map dir> <new map dir> <table>...
A function keeps its identity through its decorated name (functions.tsv 'key'), or scope, name and signature where
it has none. Rows whose function no longer exists are dropped and counted; py_to_cpp keeps the candidates that
remain. Prints one line per table."""
import csv, os, sys
csv.field_size_limit(10**9)
COLUMNS = {'py_to_cpp.tsv': 'functions', 'cpp_to_py.tsv': 'caller', 'event_handlers.tsv': 'function', 'hardcoded.tsv': 'function'}


def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE); return r.fieldnames, list(r)


def ident(r): return r['key'] or '%s::%s %s' % (r['scope'], r['name'], r['sig'])


old_dir, new_dir, tables = sys.argv[1], sys.argv[2], sys.argv[3:]
_, old = rows(os.path.join(old_dir, 'functions.tsv')); _, new = rows(os.path.join(new_dir, 'functions.tsv'))
by_ident = {}
for r in new: by_ident.setdefault(ident(r), r['id'])
remap = {r['id']: by_ident.get(ident(r)) for r in old}
for t in tables:
    col = COLUMNS[t]; fields, rs = rows(os.path.join(old_dir, t)); kept, dropped = [], 0
    for r in rs:
        ids = [remap.get(x) for x in r[col].split(',') if x] if r[col] else []
        if r[col] and not any(ids): dropped += 1; continue
        if r[col]:
            r[col] = ','.join(x for x in ids if x)
            if 'candidates' in r: r['candidates'] = str(len(r[col].split(',')))
        kept.append(r)
    with open(os.path.join(new_dir, t), 'w', newline='', encoding='utf-8') as f:
        f.write('\t'.join(fields) + '\n'); f.writelines('\t'.join(r[k] for k in fields) + '\n' for r in kept)
    print('%s: %d rows carried over, %d dropped (function gone)' % (t, len(kept), dropped))
