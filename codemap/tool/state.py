#!/usr/bin/env python3
"""Map the DLL's shared state: every class member, and every function that reads or writes it.

usage: state.py <CvGameCoreDLL source dir> [map dir]
Writes <map dir>/members.tsv (one row per member) and <map dir>/state.tsv (one row per function, member and kind of
access: a function that both reads and writes a member has two rows). Reads functions.tsv, calls.tsv, bases.tsv and overrides.tsv of the map through query.py.

How an access is found, from the source text of each function the map defines (comments and strings removed):
- members: from universal-ctags, kind member; where a member is both declared and defined (statics), the
  header's declaration is kept.
- direct: the member's name (m_...) appears in the body. The member is looked up in the function's class and
  its bases; a name declared in no such class is looked up in every class (column 'class' then lists them all).
- write: the name is assigned (=, +=, ..., ++, --), has its address taken (&m_x), is bound to a non-const
  reference (T& r = m_x), is the receiver of a mutating container call (push_back, erase, clear, insert,
  resize, assign, swap, pop_back, pop_front, push_front, and
  read, Read, reset, init, uninit on a member object), or is an argument of Read, memset, memcpy, std::fill,
  SAFE_DELETE, SAFE_DELETE_ARRAY, CvPopup_SetAtGrow or ReadStreamableFFreeListTrashArray (at any depth of nesting). Anything else is a read. In a const method, a
  member not declared mutable is only read, whatever the text looks like (passing &m_x to a const pointer).
- accessor: a function that passes a member's access on to its callers, by one of three rules: its body has
  at most ACCESSOR_LINES lines of code (every member it touches, both ways); it has a return statement whose
  expression names the member (a read); its name begins with set, change, AI_set or AI_change, the code's
  convention for mutators (a write). Its callers are given that access, with column 'via' naming the
  accessor; through a chain of accessors, the last one is named. A caller is any function that calls it, virtual calls included.
What it does not see: members reached through another object's public data (kOperation.iState is seen as the
use of the m_ container it was taken from, if that is in the same function), state held outside classes
(globals, statics), and functions that hand a member on in other ways (through
  an out parameter, or a longer function that only copies it into a local first). Nothing is left out of the output.
"""
import collections, csv, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import query as Q   # noqa: E402

ACCESSOR_LINES = 4
MUTATORS = r'(push_back|pop_back|push_front|pop_front|erase|clear|insert|resize|assign|swap|read|Read|reset|init|uninit)'
WRITE_CALLS = {'Read', 'ReadString', 'memset', 'memcpy', 'fill', 'SAFE_DELETE', 'SAFE_DELETE_ARRAY', 'CvPopup_SetAtGrow', 'ReadStreamableFFreeListTrashArray'}


def strip(t):
    """Blank out comments, string and character literals, keeping every newline."""
    out, i, n = [], 0, len(t)
    while i < n:
        c = t[i]
        if t.startswith('//', i):
            j = t.find('\n', i); j = n if j < 0 else j; out.append(' ' * (j - i)); i = j
        elif t.startswith('/*', i):
            j = t.find('*/', i + 2); j = n if j < 0 else j + 2
            out.append(re.sub(r'[^\n]', ' ', t[i:j])); i = j
        elif c in '"\'':
            j = i + 1
            while j < n and t[j] != c and t[j] != '\n':
                j += 2 if t[j] == '\\' else 1
            out.append(c + ' ' * (min(j, n) - i - 1) + (c if j < n else '')); i = j + 1
        else:
            out.append(c); i += 1
    return ''.join(out)


def skip_postfix(s, k):
    """Index after any [..], .x, ->x that follow a member name."""
    while True:
        while k < len(s) and s[k] in ' \t': k += 1
        if k < len(s) and s[k] == '[':
            d = 0
            while k < len(s):
                d += s[k] == '['; d -= s[k] == ']'; k += 1
                if d == 0: break
        elif s.startswith('.', k) or s.startswith('->', k):
            m = re.match(r'(\.|->)\s*\w+', s[k:])
            if not m: return k
            if re.match(r'\s*\(', s[k + m.end():]):   # a method call: stop before the method name
                return k
            k += m.end()
        else:
            return k


def enclosing_call(s, a):
    """The name of the call whose argument list holds position a, within the statement; '' if none."""
    d, k = 0, a - 1
    while k >= 0 and s[k] not in ';{}':
        if s[k] == ')': d += 1
        elif s[k] == '(':
            if d == 0:
                m = re.search(r'(\w+)\s*$', s[:k])
                return m.group(1) if m else ''
            d -= 1
        k -= 1
    return ''


def access(s, a, b):
    """'write' or 'read' for the member name at s[a:b]."""
    pre = re.sub(r'\(\s*(?:const\s+)?[\w:]+(?:\s*\*)*\s*\)\s*$', '', s[max(0, a - 60):a])   # drop a cast just before
    if re.search(r'(\+\+|--)\s*$', pre) or re.search(r'(?<![&\w)\]])&\s*$', pre): return 'write'
    if re.search(r'(?<![&\w)\]])&\s*\(\s*\w+\s*(\.|->)\s*$', pre): return 'write'   # &(obj.m_x)
    if re.search(r'(?<!const )\b[\w:<>]+\s*&\s*\w+\s*=\s*$', pre) and not re.search(r'\bconst\b[^;]*$', pre): return 'write'
    if enclosing_call(s, a) in WRITE_CALLS: return 'write'
    k = skip_postfix(s, b)
    rest = s[k:k + 40]
    if re.match(r'\s*(=(?!=)|\+=|-=|\*=|/=|%=|\|=|&=|\^=|<<=|>>=|\+\+|--)', rest): return 'write'
    if re.match(r'\s*(\.|->)\s*' + MUTATORS + r'\s*\(', rest): return 'write'
    return 'read'


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else Q.M
    files = sorted(f for f in os.listdir(src) if f.endswith(('.h', '.cpp', '.inl')))
    tags = subprocess.run(['ctags', '--output-format=json', '--fields=+nSKZt', '--c++-kinds=m', '--language-force=c++',
                           '--extras=-q', '-f', '-'] + files, cwd=src, capture_output=True, text=True).stdout
    decl = collections.defaultdict(dict)   # member name -> class -> (type, file, line)
    mutable = set()
    for ln in tags.splitlines():
        t = json.loads(ln)
        if t.get('_type') == 'tag' and t['name'].startswith('m_') and t.get('scope'):
            old = decl[t['name']].get(t['scope'])
            if old is None or (not old[1].endswith('.h') and t['path'].endswith('.h')):
                decl[t['name']][t['scope']] = (t.get('typeref', '').replace('typename:', ''), t['path'], t['line'])
            if 'mutable' in t.get('pattern', ''): mutable.add(t['name'])

    text = {}
    def body(f, a, e):
        if f not in text:
            p = os.path.join(src, f)
            text[f] = strip(open(p, encoding='latin-1').read()).split('\n') if os.path.exists(p) else None
        return None if text[f] is None else '\n'.join(text[f][a - 1:e])

    rows, touched, loc, rets = [], collections.defaultdict(dict), {}, {}
    for i, r in Q.F.items():
        if r['definition'] != '1' or not r['line'] or not r['end']: continue
        s = body(r['file'], int(r['line']), int(r['end']))
        if s is None: continue
        mine = Q.ancestors(r['scope']) if r['scope'] else set()
        brace = s.find('{')
        code = [l for l in (s[brace + 1:s.rfind('}')] if brace >= 0 else '').split('\n') if l.strip() not in ('', '{', '}')]
        loc[i] = len(code)
        rets[i] = s
        for m in re.finditer(r'\bm_\w+\b', s):
            nm = m.group(0)
            if nm not in decl: continue
            cls = sorted(c for c in decl[nm] if c in mine) or sorted(decl[nm])
            key = (nm, '|'.join(cls))
            acc = access(s, m.start(), m.end())
            if acc == 'write' and r['sig'].rstrip().endswith('const') and nm not in mutable and m.start() > brace:
                acc = 'read'   # a const method cannot change a member that is not mutable
            line = int(r['line']) + s.count('\n', 0, m.start())
            touched[i].setdefault(key + (acc,), line)   # reads and writes are kept apart, each at its first line
    for i, d in touched.items():
        for (nm, cls, acc), line in d.items():
            rows.append((i, nm, cls, acc, 'direct', '', line))

    # accessors pass a member's access on to their callers (see the docstring for the three rules)
    passes = collections.defaultdict(set)
    for i, d in touched.items():
        short = loc.get(i, 99) <= ACCESSOR_LINES
        mutator = re.match(r'(AI_)?(set|change)[A-Z]', Q.F[i]['name']) is not None
        for (nm, cls, acc) in d:
            if short or (acc == 'read' and re.search(r'\breturn\b[^;]*\b' + nm + r'\b', rets[i])) \
                    or (acc == 'write' and mutator):
                passes[i].add((nm, cls, acc))
    accessor = set(passes)
    seen = set((i, nm, cls, acc) for i, d in touched.items() for (nm, cls, acc) in d)
    for a in sorted(accessor):
        for (nm, cls, acc) in passes[a]:
            stack, done = [(c, a) for c in Q.up[a]], set()
            while stack:
                c, via = stack.pop()
                if (c, via) in done: continue
                done.add((c, via))
                if (c, nm, cls, acc) not in seen:
                    seen.add((c, nm, cls, acc))
                    rows.append((c, nm, cls, acc, 'accessor', via, ''))
                if c in accessor:
                    stack += [(cc, c) for cc in Q.up[c]]

    rows.sort(key=lambda x: (x[1], x[2], x[0], x[3], x[4], str(x[5]), str(x[6])))   # a total order: the same rows, the same file
    with open(os.path.join(out, 'state.tsv'), 'w', encoding='utf-8') as f:
        f.write('function\tname\tmember\tclass\taccess\thow\tvia\tline\n')
        for i, nm, cls, acc, how, via, line in rows:
            f.write(f'{i}\t{Q.name[i]}\t{nm}\t{cls}\t{acc}\t{how}\t{via}\t{line}\n')
    cnt = collections.defaultdict(collections.Counter)
    for i, nm, cls, acc, how, via, line in rows: cnt[(nm, cls)][(acc, how)] += 1
    with open(os.path.join(out, 'members.tsv'), 'w', encoding='utf-8') as f:
        f.write('member\tclass\ttype\tdeclared\twriters_direct\treaders_direct\twriters_via_accessor\treaders_via_accessor\n')
        for nm in sorted(decl):
            for c, (ty, p, l) in sorted(decl[nm].items()):
                k = next((k for k in cnt if k[0] == nm and c in k[1].split('|')), None)
                n = cnt[k] if k else collections.Counter()
                f.write(f"{nm}\t{c}\t{ty}\t{p}:{l}\t{n[('write','direct')]}\t{n[('read','direct')]}\t"
                        f"{n[('write','accessor')]}\t{n[('read','accessor')]}\n")
    print(f'{sum(len(v) for v in decl.values())} members, {len(rows)} accesses '
          f'({sum(1 for x in rows if x[4] == "direct")} direct), {len(accessor)} accessors', file=sys.stderr)


if __name__ == '__main__':
    main()
