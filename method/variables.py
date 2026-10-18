"""The essential (and intermediate) variables of this project: what its predictions are about.

Each is a function the ledger calls on a piece of evidence (a war log, or a harness run directory),
and each registered variable stores the SHA-256 of its function's code (source_sha), so a changed
definition is caught: a new definition needs a new variable. Another project replaces this file and
names it in config.json ("variables_module").
"""
import hashlib, json, os, re


class LedgerError(ValueError):
    pass


# ---------- essential and intermediate variables ----------

def log_lines(path):
    """The war log's lines as field lists, without the engine's timestamps (as extract.py reads it)."""
    for raw in open(path, encoding='latin-1'):
        line = re.sub(r'^\[[^\]]*\]\s*', '', raw.rstrip('\r\n'))
        if line.strip(): yield line.split('\t')


def v_cities(log, claim, side):
    """Cities the human took (or lost) by the claim's turn, from the war log; (None, reason) when the
    game does not count: not one human, not logged from turn 0 to that turn, another handicap, or,
    if the claim requires it, no turn-start lines (played before the snapshot DLL)."""
    P, turns, hc, K, snap = {}, [], None, [], False
    for f in log_lines(log):
        if f[0] == 'P': P[int(f[1])] = int(f[5])
        elif f[0] == 'T': turns.append(int(f[1]))
        elif f[0] == 'H' and hc is None: hc = f[3]
        elif f[0] == 'K': K.append((int(f[1]), int(f[2]), int(f[3])))
        elif f[0] == 'I': snap = True
    humans = [p for p, h in P.items() if h]
    if len(humans) != 1: return None, 'not exactly one human player'
    if not turns or min(turns) != 0: return None, f'log starts at turn {min(turns) if turns else None}'
    if max(turns) < claim['turn']: return None, f'log ends at turn {max(turns)}'
    if claim.get('handicap') and hc != claim['handicap']: return None, f'handicap {hc}'
    if claim.get('requires_snapshot') and not snap: return None, 'no turn-start lines (played before the snapshot DLL)'
    h = humans[0]
    return sum(1 for t, old, new in K if t <= claim['turn'] and (new if side == 'taken' else old) == h), None


def v_run(run_dir, name, seat):
    lines = [json.loads(l) for l in open(os.path.join(run_dir, 'run.jsonl')) if l.startswith('{"t"')]
    if name == 'seat_captures':
        return sum(1 for d in lines for e in d.get('ev') or [] if 'capture' in e and e.get('by') == seat)
    if name == 'turn_seconds':
        return sum(d.get('ms', 0) for d in lines) / 1000.0
    if name == 'run_completed':
        return int('RESULT' in open(os.path.join(run_dir, 'run.log'), errors='replace').read())
    raise LedgerError(f'unknown run variable {name}')


def cities_taken_by_turn(log, claim):
    return v_cities(log, claim, 'taken')


def cities_lost_by_turn(log, claim):
    return v_cities(log, claim, 'lost')


def seat_captures(run_dir, seat):
    return v_run(run_dir, 'seat_captures', seat)


def turn_seconds(run_dir, seat):
    return v_run(run_dir, 'turn_seconds', seat)


def run_completed(run_dir, seat):
    return v_run(run_dir, 'run_completed', seat)


FUNCS = {f.__name__: ('games', f) for f in (cities_taken_by_turn, cities_lost_by_turn)}
FUNCS.update({f.__name__: ('runs', f) for f in (seat_captures, turn_seconds, run_completed)})


def source_sha(name):
    """The hash of a variable's code: the function and the helpers it calls."""
    import inspect
    kind, f = FUNCS[name]
    src = inspect.getsource(f) + (inspect.getsource(v_cities) + inspect.getsource(log_lines) if kind == 'games' else inspect.getsource(v_run))
    return hashlib.sha256(src.encode()).hexdigest()
