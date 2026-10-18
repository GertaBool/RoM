"""Prediction register, evaluator and commit gate (method/mission/; paths and limits in method/config.json).

usage: ledger.py check                 register, history and ledger checks (check_all.py runs this)
       ledger.py evaluate              write mission/ledger.json from the register and the evidence
       ledger.py commit-msg <file>     commit-msg hook: the staged change against its trailers
       ledger.py seeds <P> [n]         the seeds the evidence runs of P must use
       ledger.py collect <P> <arm> <seat> <run dir>...   evidence values of harness runs (dirs s<seed>)
       ledger.py game <P> <WarLog.log> <name>            evidence value of one logged game
       ledger.py external <message file> <file>...       a commit in another repository (GitLab connector)
       ledger.py --selftest

Why (framework.md, reading record): a programme progresses only if its changes predict what was
not yet seen and some predictions come true (Lakatos); regulation needs the essential variables
fixed first and a second loop that changes the method when they do not move (Ashby). The rules:

  Variables   mission/variables.json: the essential variables, each a function below. Append-only.
  Register    mission/register.json: hypotheses, predictions, withdrawals. Append-only: the file at
              HEAD must be a prefix of the working file. A prediction names its line, hypotheses,
              variable, evidence kind (games or runs), claim and the change it predicts about; a
              prediction on a non-essential variable names the prediction it serves, and every chain
              ends on an essential variable within two links.
  Evidence    mission/evidence/<P>/: runs (<arm>.tsv: seed, value, run dir) or games (games.tsv:
              game, war log sha256, value, log path; logs are stable, rebuilt databases are not). Run seeds must come from seeds(P), derived from the
              entry's own text, so runs made before the claim was fixed cannot count, and no two
              predictions share seeds. A game counts only if its log starts at turn 0, reaches the
              claim's turn and has the claim's handicap.
  Status      computed live, never stored for a decision (ledger.json is a dated report): open; corroborated or not
              corroborated once the minimum evidence is in; withdrawn, or withdrawn after evidence
              (counted as not corroborated).
  Lines       untested; progressive (a corroborated prediction among its decided ones, and not the
              rest); degenerating (its last two decided predictions not corroborated); stalled (STALL
              commits serving its open predictions since its last decision, none of them evidence).
  Paths       a prediction names the paths its change may touch (files, or directories below a
              gated root; another repository's files prefixed config "external_prefix"). A commit
              serving it may touch no other gated file. Without paths (predictions registered
              before scopes): evidence only. A prediction's line is its hypotheses' line, so a new
              line needs new hypotheses.
  Commits     since the anchor (the commit adding the register), every commit that touches gated
              paths needs a trailer "Serves: P.." naming registered, unwithdrawn predictions whose
              evidence did not exist before it (only evidence commits may serve a prediction with
              evidence) and whose paths cover it; method paths need "Method: <reason>". A commit
              that missed its trailer is linked afterwards in late-links.json (append-only), never
              by rewriting history: a link that makes the commit keep every rule repairs it; one
              that does not is an acknowledged violation, and the lines it names stall until a
              decision. A build's provenance.json names what it serves and its patch, whose message
              serves the same. A new commit may not serve a degenerating or stalled line, except
              with evidence. A commit in another repository (ledger.py external, run by the Claude
              hook on the GitLab connector) is held to the same rules before it is made.
  Games       a games claim may name the DLL builds whose logs count (the H line's build field).
              Decisions from fewer than config "min_games_state" games are anecdotes: reported,
              but they do not move a line's state.
  Judgment    what cannot be computed (is a prediction new, do its paths fit, is a hypothesis a
              new core, is a method change sound) goes to the human: the Claude hook asks before any
              commit that adds register entries or changes method files.
"""
import hashlib, json, os, re, subprocess, sys


HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'config.json')))
STALL, MAX_DEPTH, MIN_RUNS = CFG['stall_commits'], CFG['max_depth'], CFG['min_runs']
MIN_GAMES, EXT = CFG['min_games_state'], CFG['external_prefix']
DIRS = [CFG['register_dir']] + CFG.get('legacy_register_dirs', [])  # current first; history may hold the others
M = CFG['register_dir']
REG, VAR, LED, LATE, EVD = (f'{M}/register.json', f'{M}/variables.json', f'{M}/ledger.json', f'{M}/late-links.json', f'{M}/evidence/')
FREE = {f'{d}/{n}' for d in DIRS for n in ('register.json', 'late-links.json', 'ledger.json')}
EVDS = tuple(f'{d}/evidence/' for d in DIRS)


def kind_of(path):
    """None (free: register, late links, report, documents), 'evidence', 'method' or 'gated'."""
    if path in FREE: return None
    if path.startswith(EVDS): return 'evidence'
    if path.startswith(tuple(CFG['method'])): return 'method'
    if path.startswith(tuple(CFG['gated'])): return 'gated'
    return None


def _load_variables():
    """The project's variable functions (config.json: variables_module, relative to the repository,
    whose root is the parent of method/)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('variables', os.path.join(os.path.dirname(HERE), CFG['variables_module']))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


VARMOD = _load_variables()
FUNCS, source_sha, LedgerError = VARMOD.FUNCS, VARMOD.source_sha, VARMOD.LedgerError


def git(root, *args):
    r = subprocess.run(['git', '-C', root] + list(args), capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def load(root, path, rev=None):
    """The JSON file in the working tree (rev None) or at a commit; None if absent."""
    if rev is None:
        p = os.path.join(root, path)
        return json.load(open(p)) if os.path.exists(p) else None
    s = git(root, 'show', f'{rev}:{path}')
    return json.loads(s) if s is not None else None


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'))


def seeds(entry, n=64):
    """Seeds of a prediction: from the SHA-256 of its entry, distinct, 1 .. 2^31 - 1."""
    out, i = [], 0
    while len(out) < n:
        h = hashlib.sha256((canon(entry) + f'#{i}').encode()).digest()
        s = int.from_bytes(h[:4], 'big') % (2 ** 31 - 1) + 1
        if s not in out: out.append(s)
        i += 1
    return out


# ---------- register ----------

def entries(reg):
    return {e['id']: e for e in reg or []}


def validate(reg, variables):
    """Structure, references and depth of the register. Returns a list of errors."""
    errs, ids = [], set()
    V = {v['id']: v for v in variables or []}
    for v in variables or []:
        if v.get('function') not in FUNCS: errs.append(f'variable {v.get("id")}: unknown function {v.get("function")}'); continue
        if FUNCS[v['function']][0] != v.get('kind'): errs.append(f'variable {v["id"]}: kind {v.get("kind")} for a {FUNCS[v["function"]][0]} function')
        if v.get('source_sha') != source_sha(v['function']):
            errs.append(f'variable {v["id"]}: the code of {v["function"]} changed since it was registered (register a new variable)')
    E = entries(reg)
    for e in reg or []:
        if e.get('id') in ids: errs.append(f'{e.get("id")}: defined twice')
        ids.add(e.get('id'))
        t = e.get('type')
        if t == 'hypothesis':
            if not e.get('line') or not e.get('text'): errs.append(f'{e["id"]}: a hypothesis needs line and text')
        elif t == 'prediction':
            for k in ('line', 'hypotheses', 'variable', 'evidence', 'claim', 'change'):
                if k not in e: errs.append(f'{e["id"]}: missing {k}')
            v = V.get(e.get('variable'))
            if v is None: errs.append(f'{e["id"]}: variable {e.get("variable")} not in variables.json'); continue
            for h in e.get('hypotheses', []):
                if E.get(h, {}).get('type') != 'hypothesis': errs.append(f'{e["id"]}: {h} is not a registered hypothesis')
                elif E[h]['line'] != e.get('line'):
                    errs.append(f'{e["id"]}: hypothesis {h} belongs to line {E[h]["line"]}, not {e.get("line")} (a new line needs new hypotheses)')
            errs += [f'{e["id"]}: {x}' for x in scope_errors(e.get('paths'))]
            if e.get('evidence') != v['kind']: errs.append(f'{e["id"]}: evidence {e.get("evidence")} for a {v["kind"]} variable')
            depth, cur, seen = 0, e, set()
            while not V[cur['variable']].get('essential'):
                p = cur.get('serves')
                if p is None or E.get(p, {}).get('type') != 'prediction' or p in seen:
                    errs.append(f'{e["id"]}: a non-essential variable needs a chain of served predictions ending on an essential one'); break
                seen.add(p); cur = E[p]; depth += 1
                if depth > MAX_DEPTH: errs.append(f'{e["id"]}: more than {MAX_DEPTH} links from an essential variable'); break
            c = e.get('claim', {})
            if v['kind'] == 'runs' and not all(k in c for k in ('direction', 'alpha', 'min_effect', 'min_n', 'seat')):
                errs.append(f'{e["id"]}: a runs claim needs direction, alpha, min_effect, min_n, seat')
            if v['kind'] == 'runs' and c.get('min_n', 0) < MIN_RUNS: errs.append(f'{e["id"]}: fewer than {MIN_RUNS} runs per arm (framework.md, section 7)')
            if v['kind'] == 'games' and not all(k in c for k in ('turn', 'op', 'reference', 'min_n')):
                errs.append(f'{e["id"]}: a games claim needs turn, op, reference, min_n')
            if v['kind'] == 'games' and not all(isinstance(r, list) and len(r) == 3 for r in c.get('reference', [])):
                errs.append(f'{e["id"]}: reference games are [game, war log sha256, value]')
        elif t == 'withdrawal':
            if E.get(e.get('of'), {}).get('type') != 'prediction': errs.append(f'{e["id"]}: withdraws no registered prediction')
            if not e.get('reason'): errs.append(f'{e["id"]}: a withdrawal needs a reason')
        else:
            errs.append(f'{e.get("id")}: unknown type {t}')
    return errs


def prefix_errors(name, old, new):
    old, new = old or [], new or []
    if len(new) < len(old) or any(canon(a) != canon(b) for a, b in zip(old, new)):
        return [f'{name}: entries at HEAD were changed or removed (append-only)']
    return []


# ---------- history ----------

def commits(root):
    """Commits from the anchor (the first adding the register) to HEAD, oldest first: (sha, parents, files, message)."""
    first = git(root, 'log', '--diff-filter=A', '--format=%H', '--', *[f'{d}/register.json' for d in DIRS])
    if not first or not first.split(): return []
    anchor = first.split()[-1]
    shas = [anchor] + (git(root, 'rev-list', '--reverse', f'{anchor}..HEAD') or '').split()
    out = []
    for s in shas:
        par = (git(root, 'log', '-1', '--format=%P', s) or '').split()
        files = (git(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', '--root', s) or '').split('\n')
        out.append((s, par, [f for f in files if f], git(root, 'log', '-1', '--format=%B', s) or ''))
    return out


def trailers(msg):
    serves = [p.strip() for m in re.findall(r'^Serves:\s*(.+)$', msg, re.M) for p in m.split(',') if p.strip()]
    method = bool(re.search(r'^Method:\s*\S', msg, re.M))
    return serves, method


def gated(files):
    """The files that need a Serves trailer: gated code and evidence."""
    return [f for f in files if kind_of(f) in ('gated', 'evidence')]


def touches_method(files):
    return [f for f in files if kind_of(f) == 'method']


def only_evidence(files):
    return all(kind_of(f) == 'evidence' for f in gated(files))


def evidence_of(files):
    """The predictions whose evidence the files are (current and earlier register directories)."""
    out = set()
    for f in files:
        for e in EVDS:
            if f.startswith(e): out.add(f[len(e):].split('/')[0])
    return out


def load_any(root, name, rev):
    """A register file at a commit, from the current directory or an earlier one (a move)."""
    for d in DIRS:
        x = load(root, f'{d}/{name}', rev)
        if x is not None: return x
    return None


def history(root):
    """Registration commit of each id, evidence commits per prediction, and the commit audit."""
    reg_at, ev_at, audit, served = {}, {}, [], []
    hist = commits(root)
    for s, par, files, msg in hist:
        for e in load_any(root, 'register.json', s) or []:
            reg_at.setdefault(e['id'], s)
        for p in evidence_of(files):
            ev_at.setdefault(p, []).append(s)
        served.append((s, par, files, msg))
    return hist, reg_at, ev_at


def ancestors(root, sha):
    return set((git(root, 'rev-list', sha) or '').split())


def scope_errors(paths):
    """A prediction's paths: what the change it predicts about may touch. Absent (as in predictions
    registered before scopes): evidence only. Each entry is a file, or a directory below a gated
    root (never a whole gated root, nor a method path); an external entry (another repository,
    prefixed EXT) names a file."""
    if paths is None: return []
    errs = []
    if not isinstance(paths, list) or not paths: return ['paths must be a non-empty list']
    for x in paths:
        if not isinstance(x, str) or not x: errs.append(f'path {x!r} is not a path'); continue
        if x.startswith(EXT):
            if x.endswith('/') or len(x) <= len(EXT): errs.append(f'external path {x} must name a file')
            continue
        if kind_of(x.rstrip('/') + ('/' if x.endswith('/') else '')) == 'method' or x.startswith(tuple(CFG['method'])):
            errs.append(f'path {x} is a method path'); continue
        if x.endswith('/') and any(g.startswith(x) for g in CFG['gated']):
            errs.append(f'path {x} is a whole gated root or wider'); continue
        if kind_of(x) != 'gated' and not any((x.endswith('/') and x.startswith(g)) for g in CFG['gated']):
            errs.append(f'path {x} is not gated')
    return errs


def covered(f, scope):
    return any(f == x or (x.endswith('/') and f.startswith(x)) for x in scope)


def problems(s, files, serves, method, E, reg_at, ev_at, wd, anc):
    """The rules one commit breaks, given the trailers it carries (or a late link's)."""
    prob = []
    if touches_method(files) and not method: prob.append('method paths without a Method trailer')
    g = gated(files)
    if g and not serves: prob.append('gated paths without a Serves trailer')
    only_ev = only_evidence(files)
    for p in serves:
        if E.get(p, {}).get('type') != 'prediction': prob.append(f'serves {p}, not a registered prediction'); continue
        if reg_at.get(p) not in anc: prob.append(f'serves {p}, registered later'); continue
        if p in wd and reg_at.get(wd[p]['id']) in anc and reg_at.get(wd[p]['id']) != s: prob.append(f'serves {p}, withdrawn')
        if not only_ev and any(c in anc and c != s for c in ev_at.get(p, [])): prob.append(f'serves {p}, whose evidence existed')
    for p in evidence_of(files):
        if p not in serves: prob.append(f'evidence of {p} without serving it')
    scope = [x for p in serves for x in E.get(p, {}).get('paths') or []]
    out = [f for f in g if kind_of(f) == 'gated' and not covered(f, scope)]
    if serves and out: prob.append(f'outside the paths of {", ".join(serves)}: {", ".join(out[:3])}' + (' ...' if len(out) > 3 else ''))
    return prob


def audit(root, hist, reg_at, ev_at, reg, late):
    """(violations, acknowledged). A violation linked late is repaired if the commit keeps every rule
    with the link's trailers; otherwise it is acknowledged, and the lines it names stall."""
    E = entries(reg)
    wd = {e['of']: e for e in reg or [] if e.get('type') == 'withdrawal'}
    L = {l['commit']: l for l in late or []}
    viol, ack = [], []
    for s, par, files, msg in hist:
        if len(par) > 1: continue  # merges bring in other branches' commits, audited there
        serves, method = trailers(msg)
        anc = ancestors(root, s)
        prob = problems(s, files, serves, method, E, reg_at, ev_at, wd, anc)
        if not prob: continue
        if s not in L: viol.append({'commit': s, 'problems': prob}); continue
        l = L[s]
        again = problems(s, files, l.get('serves') or [], bool(l.get('method')), E, reg_at, ev_at, wd, anc)
        if again:
            lines = sorted({E[p]['line'] for p in l.get('serves') or [] if p in E}) or ['(none)']
            ack.append({'commit': s, 'problems': again, 'lines': lines})
    return viol, ack


# ---------- evaluation ----------

def read_tsv(path):
    return [l.rstrip('\n').split('\t') for l in open(path) if l.strip() and not l.startswith('#')] if os.path.exists(path) else []


def evaluate(root, verify=True):
    reg = load(root, REG) or []
    V = {v['id']: v for v in load(root, VAR) or []}
    E = entries(reg)
    hist, reg_at, ev_at = history(root)
    wd = {e['of']: e for e in reg if e.get('type') == 'withdrawal'}
    preds = {}
    for e in reg:
        if e.get('type') != 'prediction': continue
        p, c, d = e['id'], e['claim'], os.path.join(root, EVD, e['id'])
        res = dict(line=e['line'], variable=e['variable'], status='open', n=None, detail='', rejected=[], unverified=0, anecdote=False)
        if V[e['variable']]['kind'] == 'runs':
            ok = set(seeds(e, 4096))
            arms = {}
            for arm in ('a', 'b'):
                vals, seen = [], set()
                for row in read_tsv(os.path.join(d, f'{arm}.tsv')):
                    sd, val = int(row[0]), float(row[1])
                    if sd not in ok: res['rejected'].append(f'{arm}: seed {sd} not of {p}'); continue
                    if sd in seen: res['rejected'].append(f'{arm}: seed {sd} twice'); continue
                    seen.add(sd); vals.append(val)
                    if len(row) > 2 and not os.path.isdir(row[2]): res['unverified'] += 1
                    if verify and len(row) > 2 and os.path.isdir(row[2]):
                        if abs(FUNCS[V[e['variable']]['function']][1](row[2], c['seat']) - val) > 1e-9:
                            raise LedgerError(f'{p}: {row[2]} does not give {val}')
                arms[arm] = vals
            res['n'] = [len(arms['a']), len(arms['b'])]
            if min(res['n']) >= c['min_n']:
                sys.path.insert(0, HERE)
                from stats import rank_welch
                import math
                t, df, pv, A = rank_welch(arms['a'], arms['b'])
                good = (A >= c['min_effect']) if c['direction'] == 'a>b' else (A <= 1 - c['min_effect'])
                # identical arms give no p-value: no difference, so the claim of one is not corroborated
                res['status'] = 'corroborated' if (not math.isnan(pv) and pv < c['alpha'] and good) else 'not corroborated'
                res['detail'] = f'p {pv:.4g}, A {A:.3f}'
        else:
            vals, refs = [], {r[1] for r in c['reference']}
            fn = FUNCS[V[e['variable']]['function']][1]
            for row in read_tsv(os.path.join(d, 'games.tsv')):
                game, sha, val = row[0], row[1], float(row[2])
                if sha in refs: res['rejected'].append(f'{game}: a reference game'); continue
                if len(row) > 3 and not os.path.exists(row[3]): res['unverified'] += 1
                if c.get('builds') and len(row) > 4 and row[4] not in c['builds']: res['rejected'].append(f'{game}: build {row[4]}'); continue
                if c.get('builds') and len(row) <= 4: res['rejected'].append(f'{game}: no build recorded'); continue
                if verify and len(row) > 3 and os.path.exists(row[3]):
                    if hashlib.sha256(open(row[3], 'rb').read()).hexdigest() != sha: raise LedgerError(f'{p}: {row[3]} changed')
                    got, why = fn(row[3], c)
                    if why or got != val: raise LedgerError(f'{p}: {game} gives {got} ({why}), not {val}')
                vals.append(val)
            res['n'] = len(vals)
            if len(vals) >= c['min_n']:
                med = lambda x: sorted(x)[len(x) // 2] if len(x) % 2 else (sorted(x)[len(x) // 2 - 1] + sorted(x)[len(x) // 2]) / 2
                a, b = med(vals), med([r[2] for r in c['reference']])
                hit = {'<': a < b, '>': a > b}[c['op']]
                res['status'] = 'corroborated' if hit else 'not corroborated'
                res['detail'] = f'median {a} against reference median {b}'
                res['anecdote'] = len(vals) < MIN_GAMES  # too few games to move the line's state
        if p in wd:
            before = [s for s in ev_at.get(p, []) if s in ancestors(root, reg_at.get(wd[p]['id'], 'HEAD'))]
            res['status'] = 'withdrawn after evidence' if before or res['status'] != 'open' else 'withdrawn'
        res['evidence_commits'] = ev_at.get(p, [])
        since = [h for h in hist[[x[0] for x in hist].index(reg_at[p]):] if trailers(h[3])[1]] if reg_at.get(p) in [x[0] for x in hist] else []
        res['method_changes_since_registration'] = [h[0] for h in since if h[0] != reg_at.get(p)]
        preds[p] = res
    lines = {}
    order = [e['id'] for e in reg if e.get('type') == 'prediction']
    decided_states = ('corroborated', 'not corroborated', 'withdrawn after evidence')
    late = load(root, LATE) or []
    violations, acknowledged = audit(root, hist, reg_at, ev_at, reg, late)
    for ln in sorted({r['line'] for r in preds.values()}):
        mine = [p for p in order if preds[p]['line'] == ln]
        dec = [p for p in mine if preds[p]['status'] in decided_states and not preds[p]['anecdote']]
        last_dec = max((preds[p]['evidence_commits'][-1] for p in dec if preds[p]['evidence_commits']), default=None,
                       key=lambda s: [h[0] for h in hist].index(s))
        idx = [h[0] for h in hist].index(last_dec) + 1 if last_dec else 0
        openp = {p for p in mine if preds[p]['status'] == 'open'}
        busy = sum(1 for s, par, files, msg in hist[idx:] if len(par) <= 1 and set(trailers(msg)[0]) & openp
                   and not only_evidence(files))
        acks = [a['commit'] for a in acknowledged if ln in a['lines'] and a['commit'] in [h[0] for h in hist[idx:]]]
        if len(dec) >= 2 and all(preds[p]['status'] != 'corroborated' for p in dec[-2:]): st = 'degenerating'
        elif busy >= STALL or acks: st = 'stalled'
        elif any(preds[p]['status'] == 'corroborated' for p in dec): st = 'progressive'
        else: st = 'untested'
        lines[ln] = dict(state=st, predictions=mine, decided=dec, commits_since_decision=busy, acknowledged_violations=acks)
    return dict(predictions=preds, lines=lines, violations=violations, acknowledged=acknowledged, late_links=len(late))


# ---------- checks ----------

def check(root):
    errs = []
    reg, var, late = load(root, REG), load(root, VAR), load(root, LATE)
    if reg is None:
        return ['register.json removed: the gate cannot be switched off by deleting it'] if load_any(root, 'register.json', 'HEAD') is not None else []
    errs += validate(reg, var)
    errs += prefix_errors('register.json', load_any(root, 'register.json', 'HEAD'), reg)
    errs += prefix_errors('variables.json', load_any(root, 'variables.json', 'HEAD'), var)
    errs += prefix_errors('late-links.json', load_any(root, 'late-links.json', 'HEAD'), late)
    if errs: return errs
    import glob
    since = ancestors_since_anchor(root)
    for pv in sorted(glob.glob(os.path.join(root, CFG['provenance']))):
        rel = os.path.relpath(pv, root)
        if git(root, 'log', '-1', '--format=%H', '--', rel).strip() in since:
            d = json.load(open(pv))
            sv, patch = d.get('serves'), d.get('patch')
            E = entries(reg)
            if not sv or any(E.get(p, {}).get('type') != 'prediction' for p in sv):
                errs.append(f'{rel}: "serves" must list registered predictions'); continue
            if not patch or not os.path.exists(os.path.join(root, patch)):
                errs.append(f'{rel}: "patch" must name the source change, committed in this repository'); continue
            msg = open(os.path.join(root, patch), encoding='latin-1').read().split('\n---\n', 1)[0]
            missing = [p for p in sv if p not in trailers(msg)[0]]
            if missing: errs.append(f'{rel}: the source change in {patch} does not serve {", ".join(missing)}')
    led = evaluate(root)
    errs += [f'commit {v["commit"][:10]}: {"; ".join(v["problems"])} (link it in late-links.json)' for v in led['violations']]
    return errs


def ancestors_since_anchor(root):
    return {h[0] for h in commits(root)}


def commit_msg(root, msgfile):
    """For the commit being made: trailers against the staged files, and the state of the lines served."""
    msg = open(msgfile).read()
    files = [f for f in (git(root, 'diff', '--cached', '--name-only') or '').split('\n') if f]
    serves, method = trailers(msg)
    errs = []
    if touches_method(files) and not method: errs.append('staged method paths need a "Method: <reason>" trailer')
    g = gated(files)
    if g and not serves: errs.append('staged gated paths need a "Serves: P.." trailer')
    reg = load(root, REG) or []
    E = entries(reg)
    led = evaluate(root, verify=False) if reg else {'predictions': {}, 'lines': {}}
    only_ev = only_evidence(files)
    for p in serves:
        if E.get(p, {}).get('type') != 'prediction': errs.append(f'{p} is not a registered prediction'); continue
        st = led['predictions'].get(p, {})
        if st.get('status', 'open') != 'open': errs.append(f'{p} is {st["status"]}')
        if not only_ev and st.get('evidence_commits'): errs.append(f'{p} has evidence: only evidence commits may serve it')
        ls = led['lines'].get(E[p]['line'], {}).get('state')
        if ls in ('degenerating', 'stalled') and not only_ev: errs.append(f'line {E[p]["line"]} is {ls}: only evidence, or a new line')
    for p in evidence_of(files):
        if p not in serves: errs.append(f'evidence of {p} staged without serving it')
    scope = [x for p in serves for x in E.get(p, {}).get('paths') or []]
    out = [f for f in g if kind_of(f) == 'gated' and not covered(f, scope)]
    if serves and out: errs.append(f'staged files outside the paths of {", ".join(serves)}: {", ".join(out[:3])}')
    return errs


def external(root, message, files):
    """A commit made in another repository (the GitLab connector): its trailers must serve open
    predictions without evidence, on lines neither degenerating nor stalled, whose paths name every
    file (as EXT + path)."""
    serves, method = trailers(message)
    reg = load(root, REG) or []
    E = entries(reg)
    errs = [] if serves else ['an external commit needs a "Serves: P.." trailer']
    led = evaluate(root, verify=False)
    for p in serves:
        if E.get(p, {}).get('type') != 'prediction': errs.append(f'{p} is not a registered prediction'); continue
        st = led['predictions'].get(p, {})
        if st.get('status', 'open') != 'open': errs.append(f'{p} is {st["status"]}')
        if st.get('evidence_commits'): errs.append(f'{p} has evidence: no further changes may serve it')
        ls = led['lines'].get(E[p]['line'], {}).get('state')
        if ls in ('degenerating', 'stalled'): errs.append(f'line {E[p]["line"]} is {ls}')
    scope = [x for p in serves for x in E.get(p, {}).get('paths') or []]
    out = [f for f in files if EXT + f not in scope]
    if serves and out: errs.append(f'files outside the paths of {", ".join(serves)}: {", ".join(out[:3])}')
    return errs


def log_build(log):
    """The DLL build a war log names in its H line (seventh field; logs before it have none)."""
    for f in VARMOD.log_lines(log):
        if f[0] == 'H': return f[6] if len(f) > 6 else None
    return None


def write_evaluation(root):
    """A dated report: gate decisions never read it, they evaluate live (a committed ledger would be
    stale at once, because committing it changes the history it summarises)."""
    led = dict(evaluate(root), as_of=(git(root, 'rev-parse', 'HEAD') or '').strip())
    with open(os.path.join(root, LED), 'w') as f:
        json.dump(led, f, indent=1, sort_keys=True); f.write('\n')
    return led


# ---------- evidence collection ----------

def collect(root, pid, arm, seat, dirs):
    E = entries(load(root, REG))
    e = E[pid]
    ok = set(seeds(e, 4096))
    V = {v['id']: v for v in load(root, VAR)}
    rows = []
    for d in dirs:
        m = re.search(r's(\d+)$', os.path.basename(os.path.normpath(d)))
        if not m: raise LedgerError(f'{d}: run directories are named s<seed>')
        sd = int(m.group(1))
        if sd not in ok: raise LedgerError(f'{d}: seed {sd} is not one of {pid}\'s')
        rows.append(f'{sd}\t{FUNCS[V[e["variable"]]["function"]][1](d, seat)}\t{os.path.abspath(d)}')
    p = os.path.join(root, EVD, pid)
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, f'{arm}.tsv'), 'a') as f:
        for r in rows: f.write(r + '\n')


def add_game(root, pid, log, name):
    """One logged game's value as evidence of pid: name, war log sha256, value, log path."""
    e = entries(load(root, REG))[pid]
    V = {v['id']: v for v in load(root, VAR)}
    got, why = FUNCS[V[e['variable']]['function']][1](log, e['claim'])
    if why: raise LedgerError(f'{log}: does not count ({why})')
    sha = hashlib.sha256(open(log, 'rb').read()).hexdigest()
    if sha in {r[1] for r in e['claim']['reference']}: raise LedgerError(f'{log}: a reference game of {pid}')
    build = log_build(log)
    if e['claim'].get('builds') and build not in e['claim']['builds']:
        raise LedgerError(f'{log}: written by build {build}, not one of {pid}\'s')
    p = os.path.join(root, EVD, pid)
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, 'games.tsv'), 'a') as f:
        f.write(f'{name}\t{sha}\t{got}\t{os.path.abspath(log)}\t{build or "-"}\n')


# ---------- self-test ----------

def selftest():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    try:
        g = lambda *a: subprocess.run(['git', '-C', d] + list(a), capture_output=True, text=True, check=True)
        g('init', '-q'); g('config', 'user.email', 't@t'); g('config', 'user.name', 't')
        os.makedirs(os.path.join(d, M)); os.makedirs(os.path.join(d, 'research/ai-warfare/tools'))
        w = lambda p, x: (os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True), open(os.path.join(d, p), 'w').write(x if isinstance(x, str) else json.dumps(x, indent=1)))
        def commit(msg):
            g('add', '-A'); r = subprocess.run(['git', '-C', d, 'commit', '-q', '-m', msg], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        var = [dict(id='E1', function='seat_captures', kind='runs', essential=True, text='seat captures', source_sha=source_sha('seat_captures')),
               dict(id='X1', function='turn_seconds', kind='runs', essential=False, text='inter', source_sha=source_sha('turn_seconds'))]
        H = dict(id='H1', type='hypothesis', line='war', text='h')
        P1 = dict(id='P1', type='prediction', line='war', hypotheses=['H1'], variable='E1', evidence='runs', change='c',
                  claim=dict(direction='a<b', alpha=0.05, min_effect=0.6, min_n=30, seat=1), paths=['research/ai-warfare/tools/x.py'])
        w(VAR, var); w(REG, [H, P1]); w('research/ai-warfare/tools/x.py', '1')
        commit('anchor\n\nMethod: start\nServes: P1')
        led = evaluate(d); assert led['predictions']['P1']['status'] == 'open' and not led['violations'], led
        # a code commit without a trailer is a violation until linked late
        w('research/ai-warfare/tools/x.py', '2'); commit('no trailer')
        bad = evaluate(d)['violations']; assert len(bad) == 1 and 'Serves' in bad[0]['problems'][0], bad
        w(LATE, [dict(commit=bad[0]['commit'], serves=['P1'], reason='missed')]); commit('late link')
        assert not evaluate(d)['violations']
        # editing a registered entry is refused
        w(REG, [H, dict(P1, change='other')]); assert any('append-only' in x for x in check(d)); w(REG, [H, P1])
        # depth: a non-essential prediction must serve a chain ending on an essential one within two links
        P2 = dict(P1, id='P2', variable='X1', serves='P1'); P3 = dict(P1, id='P3', variable='X1', serves='P2')
        P4 = dict(P1, id='P4', variable='X1', serves='P3')
        assert not validate([H, P1, P2, P3], var) and any('more than' in x for x in validate([H, P1, P2, P3, P4], var))
        assert any('chain' in x for x in validate([H, dict(P1, id='P5', variable='X1')], var))
        # fewer than 30 runs per arm is refused
        assert any('30 runs' in x for x in validate([H, dict(P1, id='P6', claim=dict(P1['claim'], min_n=5))], var))
        # evidence: foreign seeds rejected; once evidence exists, code commits may not serve P1
        sd = seeds(P1, 80)
        w(f'{EVD}P1/a.tsv', ''.join(f'{s}\t{i % 3}\n' for i, s in enumerate(sd[:30])) + '12345\t9\n')
        commit('evidence a\n\nServes: P1')
        r = evaluate(d)['predictions']['P1']; assert r['rejected'] == ['a: seed 12345 not of P1'] and r['status'] == 'open', r
        w('research/ai-warfare/tools/x.py', '3'); commit('tune\n\nServes: P1')
        assert any('evidence existed' in p for v in evaluate(d)['violations'] for p in v['problems'])
        w(LATE, [dict(commit=bad[0]['commit'], serves=['P1'], reason='missed'),
                 dict(commit=git(d, 'rev-parse', 'HEAD').strip(), serves=['P1'], reason='tuned after evidence: counted')]); commit('late link 2')
        w(f'{EVD}P1/b.tsv', ''.join(f'{s}\t{3 + i % 3}\n' for i, s in enumerate(sd[30:60]))); commit('evidence b\n\nServes: P1')
        r = evaluate(d)['predictions']['P1']; assert r['status'] == 'corroborated' and r['n'] == [30, 30], r
        assert evaluate(d)['lines']['war']['state'] == 'progressive'
        # a withdrawal after evidence counts against the line
        P7 = dict(P1, id='P7'); w(REG, [H, P1, P7]); commit('register P7')
        w(f'{EVD}P7/a.tsv', ''.join(f'{s}\t1\n' for s in seeds(P7, 30))); commit('evidence P7\n\nServes: P7')
        w(REG, [H, P1, P7, dict(id='W1', type='withdrawal', of='P7', reason='r')]); commit('withdraw')
        assert evaluate(d)['predictions']['P7']['status'] == 'withdrawn after evidence'
        # two failures in a row: the line degenerates and refuses new code commits
        P8 = dict(P1, id='P8'); w(REG, [H, P1, P7, dict(id='W1', type='withdrawal', of='P7', reason='r'), P8]); commit('register P8')
        w(f'{EVD}P8/a.tsv', ''.join(f'{s}\t5\n' for s in seeds(P8, 30))); w(f'{EVD}P8/b.tsv', ''.join(f'{s}\t5\n' for s in seeds(P8, 60)[30:]))
        commit('evidence P8\n\nServes: P8')
        led = evaluate(d); assert led['predictions']['P8']['status'] == 'not corroborated' and led['lines']['war']['state'] == 'degenerating', led['lines']
        P9 = dict(P1, id='P9'); w(REG, load(d, REG) + [P9]); commit('register P9')
        w('research/ai-warfare/tools/x.py', '4'); g('add', '-A')
        mf = os.path.join(d, 'msg'); open(mf, 'w').write('more\n\nServes: P9\n')
        assert any('degenerating' in x for x in commit_msg(d, mf)), commit_msg(d, mf)
        g('reset', '-q', '--hard')
        # a changed variable definition and a deleted register are refused
        assert any('changed since' in x for x in validate([H, P1], [dict(var[0], source_sha='0')]))
        os.remove(os.path.join(d, REG)); assert any('removed' in x for x in check(d)); g('checkout', '-q', '--', REG)
        assert check(d) == [], check(d)
        # games: a log counts from turn 0 through the claim's turn, at its handicap, with turn-start lines
        gv = dict(id='G1', function='cities_taken_by_turn', kind='games', essential=True, text='taken', source_sha=source_sha('cities_taken_by_turn'))
        w(VAR, var + [gv])
        log = lambda first, snap: ''.join([f'[1] H\t0\tGAMESPEED_MARATHON\tHANDICAP_NOBLE\t84\t46\n', 'P\t0\t0\tA\tA\t1\n', 'P\t1\t1\tB\tB\t0\n']
                                          + [f'T\t{t}\t0\n' for t in range(first, 5)] + ['K\t2\t1\t0\t3\t3\t1\n', 'K\t4\t1\t0\t5\t5\t1\n']
                                          + (['I\t2\t0\t1\t1\t0\t0\t1\n'] if snap else []))
        for name, first, snap in (('ok', 0, True), ('late', 3, True), ('old', 0, False)):
            open(os.path.join(d, name + '.log'), 'w').write(log(first, snap))
        ref_sha = hashlib.sha256(open(os.path.join(d, 'old.log'), 'rb').read()).hexdigest()
        HG = dict(id='HG', type='hypothesis', line='games', text='hg')
        PG = dict(id='PG', type='prediction', line='games', hypotheses=['HG'], variable='G1', evidence='games', change='c',
                  claim=dict(turn=3, handicap='HANDICAP_NOBLE', requires_snapshot=True, op='<', reference=[['old', ref_sha, 2]], min_n=1))
        w(REG, load(d, REG) + [HG, PG]); commit('register PG\n\nMethod: games variable')
        ctt = VARMOD.cities_taken_by_turn
        assert ctt(os.path.join(d, 'ok.log'), PG['claim']) == (1, None)
        assert 'starts at turn 3' in ctt(os.path.join(d, 'late.log'), PG['claim'])[1]
        try: add_game(d, 'PG', os.path.join(d, 'old.log'), 'old'); assert False
        except LedgerError as x: assert 'turn-start' in str(x), x
        add_game(d, 'PG', os.path.join(d, 'ok.log'), 'ok'); commit('evidence PG\n\nServes: PG')
        r = evaluate(d)['predictions']['PG']; assert r['status'] == 'corroborated' and r['n'] == 1, r
        open(os.path.join(d, 'ok.log'), 'a').write('T\t9\t0\n')
        try: evaluate(d); assert False
        except LedgerError as x: assert 'changed' in str(x), x
        open(os.path.join(d, 'ok.log'), 'w').write(log(0, True))  # restored: the log is as recorded again
        # scopes: what a prediction may be served with, fixed when it is registered
        assert any('whole gated root' in x for x in scope_errors(['toolchain/']))
        assert any('method path' in x for x in scope_errors(['method/ledger.py']))
        assert any('must name a file' in x for x in scope_errors(['gitlab:Assets/']))
        assert not scope_errors(['research/ai-warfare/tools/x.py', 'builds/war-log/', 'gitlab:Assets/a.cpp'])
        assert any('belongs to line' in x for x in validate([H, dict(P1, id='PX', line='other')], var))
        # a new line, a code change outside its prediction's paths, and a late link that does not repair it
        H2 = dict(id='H2', type='hypothesis', line='new', text='h2')
        PN = dict(P1, id='PN', line='new', hypotheses=['H2'], paths=['research/ai-warfare/tools/y.py'])
        w(REG, load(d, REG) + [H2, PN]); commit('register PN')
        w('research/ai-warfare/tools/z.py', '1'); commit('out of scope\n\nServes: PN')
        v = [x for x in evaluate(d)['violations'] if any('outside the paths' in p for p in x['problems'])]
        assert len(v) == 1, evaluate(d)['violations']
        w(LATE, load(d, LATE) + [dict(commit=v[0]['commit'], serves=['PN'], reason='still outside')]); commit('late link 3')
        led = evaluate(d)
        # the earlier late link for tuning after evidence does not repair its commit either: both are acknowledged
        assert not led['violations'] and sorted(a['lines'][0] for a in led['acknowledged']) == ['new', 'war'], led['acknowledged']
        assert led['lines']['new']['state'] == 'stalled', led['lines']['new']
        # an external commit (another repository) names its files in the prediction's paths
        PE = dict(P1, id='PE', line='ext', hypotheses=['H3'], paths=['gitlab:Assets/a.cpp'])
        w(REG, load(d, REG) + [dict(id='H3', type='hypothesis', line='ext', text='h3'), PE]); commit('register PE')
        assert external(d, 'x\n\nServes: PE\n', ['Assets/a.cpp']) == []
        assert any('outside the paths' in x for x in external(d, 'x\n\nServes: PE\n', ['Assets/b.cpp']))
        assert any('needs a "Serves' in x for x in external(d, 'x\n', ['Assets/a.cpp']))
        # builds: a games claim may name the DLL builds whose logs count
        open(os.path.join(d, 'b1.log'), 'w').write(log(0, True).replace('46\n', '46\tB1\n', 1))
        open(os.path.join(d, 'b2.log'), 'w').write(log(0, True).replace('46\n', '46\tB2\n', 1))
        assert log_build(os.path.join(d, 'b1.log')) == 'B1' and log_build(os.path.join(d, 'ok.log')) is None
        PB = dict(PG, id='PB', claim=dict(PG['claim'], builds=['B1'], min_n=1))
        w(REG, load(d, REG) + [PB]); commit('register PB')
        try: add_game(d, 'PB', os.path.join(d, 'b2.log'), 'b2'); assert False
        except LedgerError as x: assert 'build B2' in str(x), x
        add_game(d, 'PB', os.path.join(d, 'b1.log'), 'b1'); commit('evidence PB\n\nServes: PB')
        r = evaluate(d)['predictions']['PB']
        assert r['status'] == 'corroborated' and r['anecdote'] and evaluate(d)['lines']['games']['state'] == 'untested', r
        # a build's provenance names the predictions it serves and its patch, whose message serves them too
        w('builds/x/provenance.json', dict(serves=['PE'], patch='fixes/x.patch'))
        w('fixes/x.patch', 'Subject: x\n\nno trailer\n---\n diff\n')
        commit('build\n\nServes: PE')
        assert any('does not serve PE' in x for x in check(d)), check(d)
        print('ledger selftest: ok')
    finally:
        shutil.rmtree(d)


def main():
    root = git(HERE, 'rev-parse', '--show-toplevel').strip()
    a = sys.argv[1:]
    if a == ['--selftest']: return selftest()
    if a[:1] == ['check']:
        errs = check(root)
        for e in errs: print(f'ledger: {e}')
        sys.exit(1 if errs else 0)
    if a[:1] == ['evaluate']: write_evaluation(root); return
    if a[:1] == ['commit-msg']:
        errs = commit_msg(root, a[1])
        for e in errs: print(f'ledger: {e}', file=sys.stderr)
        sys.exit(1 if errs else 0)
    if a[:1] == ['seeds']:
        print(' '.join(map(str, seeds(entries(load(root, REG))[a[1]], int(a[2]) if len(a) > 2 else 64)))); return
    if a[:1] == ['collect']: collect(root, a[1], a[2], int(a[3]), a[4:]); return
    if a[:1] == ['game']: add_game(root, a[1], a[2], a[3]); return
    if a[:1] == ['external']:
        errs = external(root, open(a[1]).read(), a[2:])
        for e in errs: print(f'ledger: {e}', file=sys.stderr)
        sys.exit(1 if errs else 0)
    print(__doc__); sys.exit(2)


if __name__ == '__main__':
    main()
