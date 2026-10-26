#!/usr/bin/env python3
"""Inventory of the code that reads a plot's resource token, for component LQ: every call of getBonusType and
getNonObsoleteBonusType in the DLL source and the mod's Python, with the enclosing function. Classifications live in
callsites.json ('classes', keyed by enclosing function, with 'class_meaning'); this tool keeps the inventory current,
preserves the classifications and lists functions not yet classified. check_plan.py imports scan().
usage: callsites.py <mod checkout> [plan dir]"""
import glob, json, os, re, sys

PAT = re.compile(r'\b(getBonusType|getNonObsoleteBonusType)\s*\(')
FN_CPP = re.compile(r'^[A-Za-z_][\w\s\*&:<>,/]*?\b(\w+::~?\w+)\s*\(')
FN_PY = re.compile(r'^\s*def\s+(\w+)\s*\(')


def scan(mod):
    """Every call site: file (relative to the checkout), line, enclosing function, call, text."""
    sites = []
    files = sorted(glob.glob(os.path.join(mod, 'Assets', 'CvGameCoreDLL', '*.cpp'))) + \
        sorted(glob.glob(os.path.join(mod, 'Assets', 'Python', '**', '*.py'), recursive=True))
    for f in files:
        rel = os.path.relpath(f, mod); py = f.endswith('.py')
        fn = cls = None
        for i, line in enumerate(open(f, encoding='latin-1'), 1):
            if py:
                m = re.match(r'^class\s+(\w+)', line)
                if m: cls = m.group(1)
                m = FN_PY.match(line)
                if m: fn = (cls + '.' if cls and line.startswith((' ', '\t')) else '') + m.group(1)
            else:
                m = FN_CPP.match(line)
                if m and ('{' in line or ';' not in line): fn = m.group(1)
            m = PAT.search(line)
            if m and not line.lstrip().startswith(('//', '#')):
                sites.append(dict(file=rel, line=i, function=fn, call=m.group(1), text=line.strip()[:160]))
    return sites


if __name__ == '__main__':
    mod = sys.argv[1]
    here = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, 'callsites.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    classes = old.get('classes', {})
    sites = scan(mod)
    funcs = sorted({(s['file'], s['function']) for s in sites})
    unclassified = sorted({s['function'] for s in sites if s['function'] not in classes})
    json.dump(dict(about=__doc__.split('\n')[0], class_meaning=old.get('class_meaning', {}), classes=classes, sites=sites, unclassified=unclassified),
              open(path, 'w'), indent=1)
    print('%d call sites in %d functions (%d DLL, %d Python); %d functions unclassified' % (
        len(sites), len(funcs), sum(1 for s in sites if s['file'].endswith('.cpp')), sum(1 for s in sites if s['file'].endswith('.py')), len(unclassified)))
