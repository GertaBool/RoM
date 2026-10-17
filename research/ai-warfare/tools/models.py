#!/usr/bin/env python3
"""Test models of one human decision class across games (framework.md, section 6).

usage: models.py <class> <registry.fig.json> <games dir> game3 game4 ...   (needs cases_<class>.csv)
       run with ~/.cache/rom-ana/bin/python

Leave one game out: every model is fitted on the other games' cases and scored on the held-out
game's; hits are summed over the held-out games. Models (cues are binary; each is oriented on the
training cases so that 1 points to y = 1):
  base    the training majority
  single  the one cue with the most training hits
  fft     fast-and-frugal tree: every cue order and every exit direction is tried (exhaustive;
          ties: fewer cues looked up, then the first found); the last cue decides both ways
  tally   y = 1 when at least k oriented cues are 1; k fitted on training
  logit   logistic regression on the same cues (rival, weighted)
  cart    classification tree of depth 3 (rival)
Also, per held-out game: n and the hits of base, single, fft and logit.
Columns: hits and n over held-out cases; hit rate; balanced accuracy (mean of the two class hit
rates, pooled); p: exact two-sided McNemar test against base on the same cases. Also the fft
fitted on all games, written out as a rule.
"""
import csv, itertools, os, sys

import numpy as np
from scipy.stats import binomtest
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

CLS, REG, GD, GAMES = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
data, paths = {}, []
for g in GAMES:
    p = os.path.join(GD, g, f'cases_{CLS}.csv')
    R = list(csv.DictReader(open(p)))
    if R: data[g] = R; paths.append(p)
cues = [c for c in next(iter(data.values()))[0] if c not in ('seq', 'turn', 'y')]
XY = {g: (np.array([[int(r[c]) for c in cues] for r in R]), np.array([int(r['y']) for r in R])) for g, R in data.items()}


def orient(X, y):
    o = []
    for i in range(X.shape[1]):
        on, off = y[X[:, i] == 1], y[X[:, i] == 0]
        p1 = on.mean() if len(on) else 0.5; p0 = off.mean() if len(off) else 0.5
        o.append(p1 >= p0)
    return np.array(o)


def apply_o(X, o): return np.where(o, X, 1 - X)


def fft_predict(X, order, exits):
    out = np.empty(len(X), int); used = np.zeros(len(X))
    for j, x in enumerate(X):
        for lv, i in enumerate(order):
            used[j] += 1
            if lv == len(order) - 1: out[j] = x[i]; break
            if x[i] == exits[lv]: out[j] = exits[lv]; break
    return out, used.mean()


def fit(name, X, y):
    o = orient(X, y); Xo = apply_o(X, o); n = X.shape[1]
    if name == 'base':
        m = int(y.mean() > 0.5); return lambda Z: np.full(len(Z), m), f'always {m}'
    if name == 'single':
        acc = [(Xo[:, i] == y).mean() for i in range(n)]; i = int(np.argmax(acc))
        return lambda Z, i=i: apply_o(Z, o)[:, i], f'y = 1 exactly when {cues[i]} = {1 if o[i] else 0}'
    if name == 'fft':
        best = None
        for order in itertools.permutations(range(n)):
            for exits in itertools.product((1, 0), repeat=n - 1):
                pr, used = fft_predict(Xo, order, exits)
                key = (-(pr == y).mean(), used)
                if best is None or key < best[0]: best = (key, order, exits)
        _, order, exits = best
        v = lambda i, e: e if o[i] else 1 - e      # oriented value e as the cue's own value
        rule = '; '.join((f'if {cues[i]} = {v(i, exits[lv])} then y = {exits[lv]}' if lv < n - 1 else
                          f'else y = 1 exactly when {cues[i]} = {v(i, 1)}') for lv, i in enumerate(order))
        return lambda Z: fft_predict(apply_o(Z, o), order, exits)[0], rule
    if name == 'tally':
        s = Xo.sum(1); ks = list(range(n + 2)); acc = [((s >= k).astype(int) == y).mean() for k in ks]
        k = ks[int(np.argmax(acc))]; return lambda Z: (apply_o(Z, o).sum(1) >= k).astype(int), f'at least {k} of {n}'
    if len(set(y)) < 2: m = int(y[0]); return lambda Z: np.full(len(Z), m), f'always {m}'
    if name == 'logit':
        mdl = LogisticRegression(C=1.0, solver='lbfgs').fit(Xo, y); return lambda Z: mdl.predict(apply_o(Z, o)), 'weights'
    mdl = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xo, y); return lambda Z: mdl.predict(apply_o(Z, o)), 'tree'


MODELS = ['base', 'single', 'fft', 'tally', 'logit', 'cart']
pred = {m: [] for m in MODELS}; truth = []; held = []
for g in data:
    tr = [h for h in data if h != g]
    if not tr: continue
    X = np.vstack([XY[h][0] for h in tr]); y = np.concatenate([XY[h][1] for h in tr])
    truth.append(XY[g][1]); held.append(g)
    for m in MODELS: pred[m].append(fit(m, X, y)[0](XY[g][0]))
truth = np.concatenate(truth)
rows = []
for m in MODELS:
    p = np.concatenate(pred[m]); hit = p == truth
    bal = np.mean([hit[truth == c].mean() for c in (0, 1) if (truth == c).any()])
    b = int((hit & ~(np.concatenate(pred['base']) == truth)).sum()); c = int((~hit & (np.concatenate(pred['base']) == truth)).sum())
    pv = binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    rows.append([m, int(hit.sum()), len(truth), f'{hit.mean():.3f}', f'{bal:.3f}', '-' if m == 'base' else f'{pv:.3g}'])
reg = Registry(REG, paths)
games = ', '.join(data)
reg.result_table(f'{CLS}_models', ['model', 'hits', 'n', 'hit rate', 'balanced', 'p vs base'], rows, 'share',
                 'human', f'all turns of {games}', f'models.py, leave one game out over {games}', MODELS, n=len(truth))
pg = [[g, len(truth_g)] + [int((pred[m][k] == truth_g).sum()) for m in ('base', 'single', 'fft', 'logit')]
      for k, (g, truth_g) in enumerate(zip(held, [XY[g][1] for g in held]))]
reg.result_table(f'{CLS}_by_game', ['held-out game', 'n', 'base hits', 'single hits', 'fft hits', 'logit hits'], pg, 'turns'
                 if CLS != 'order_unit' else 'orders', 'human', f'all turns of {games}', 'models.py, each game held out in turn',
                 held, n=len(truth))
Xa = np.vstack([XY[g][0] for g in data]); ya = np.concatenate([XY[g][1] for g in data])
reg.fig(f'{CLS}_fft_rule', fit('fft', Xa, ya)[1], 'category', 'human', f'all turns of {games}', 'models.py, fft fitted on all games')
reg.fig(f'{CLS}_single_rule', fit('single', Xa, ya)[1], 'category', 'human', f'all turns of {games}', 'models.py, single cue on all games')
reg.fig(f'{CLS}_cues', ', '.join(cues), 'category', 'human', '-', f'cases_{CLS}.csv header')
reg.save()
for r in rows: print(' | '.join(map(str, r)), file=sys.stderr)
print('fft on all:', fit('fft', Xa, ya)[1], '| single on all:', fit('single', Xa, ya)[1], file=sys.stderr)
