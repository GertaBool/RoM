"""PR.F8.T3 / FD.F1: food and drink values for the goods XML, computed from research/economy/data/nutrition.json.

For each food and drink good of nutrition.json it computes, per tonne of the good as stored:
  iSatietyPerTonne   satiety units per tonne = kcal per kg x edible x protein factor x 1000
                     (protein factor = (1 + k p q) / (1 + k p_ref q_ref); p = protein share of calories,
                     q = DIAAS capped at 1, with the defaults of nutrition.json for goods without a sourced DIAAS)
  iProteinPerTonne   kg of protein per tonne x edible
  iHydrationPercent  hydration index x 100, drinks only (milk 150; water would be 100)
and writes connector pairs that add the three fields just before the closing </BonusInfo> of each record of
Assets/XML/Terrain/CIV4BonusInfos.xml. Each pair's old text is the shortest run of lines, ending with that closing
tag, that is unique in the file (as pr_f6_t3_edits.py). The schema change that admits the fields belongs to FD.F1.T1.

usage: food_values_edits.py <mod checkout> [<pairs.json out>]   (without an output it prints the table only)"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', '..', 'data', 'nutrition.json')
REL = 'Assets/XML/Terrain/CIV4BonusInfos.xml'


def values(d):
    s = d['satiety']
    k, pref, qref = s['k'], s['p_ref'], s['q_ref']
    out = {}
    for g, v in d['goods'].items():
        kcal, prot, edible = v['kcal'], v['protein'], v['edible']
        p = (4.0 * prot / kcal) if kcal else 0.0
        q = v['diaas'] if v.get('diaas') is not None else (s['q_animal_default'] if g in d['animal_goods'] else s['q_plant_default'])
        q = min(q, 1.0)
        factor = (1 + k * p * q) / (1 + k * pref * qref)
        sat_kg = kcal * 10 * edible * factor                      # kcal per kg = kcal per 100 g x 10
        out[g] = {'factor': round(factor, 3), 'satiety_per_kg': round(sat_kg),
                  'iSatietyPerTonne': int(round(sat_kg * 1000)),  # bound: olive oil 884 kcal x 10 x 0.68 x 1000 < 2^31
                  'iProteinPerTonne': int(round(prot * 10 * edible)),
                  'iHydrationPercent': int(round(v['hydration'] * 100)) if v.get('hydration') is not None else 0}
    return out


def occurrences(s, sub):
    n, i = 0, s.find(sub)
    while i >= 0:
        n += 1; i = s.find(sub, i + 1)
    return n


def pairs_for(mod, vals):
    p = os.path.join(mod, REL)
    b = open(p, 'rb').read()
    s = b.decode('ascii')          # the connector rewrites edited files in UTF-8: refuse anything else
    nl = '\r\n' if '\r\n' in s else '\n'
    pairs, missing = [], []
    for g, v in vals.items():
        if not any(v[f] for f in ('iSatietyPerTonne', 'iProteinPerTonne', 'iHydrationPercent')):
            continue
        t = s.find('<Type>%s</Type>' % g)
        if t < 0:
            missing.append(g); continue
        close = s.find('</BonusInfo>', t)
        line_start = s.rfind(nl, 0, close) + len(nl)
        indent = s[line_start:close]
        inner = indent + '\t'
        add = ''.join('%s<%s>%d</%s>%s' % (inner, f, v[f], f, nl)
                      for f in ('iSatietyPerTonne', 'iProteinPerTonne', 'iHydrationPercent') if v[f])
        end = close + len('</BonusInfo>')
        head = s[:line_start]
        lines = head.split(nl)
        k = 1
        while True:
            old = nl.join(lines[-k:]) + s[line_start:end]
            if occurrences(s, old) == 1:
                break
            k += 1
        new = old[:len(old) - len(s[line_start:end])] + add + s[line_start:end]
        pairs.append({'file': REL, 'old': old, 'new': new, 'good': g})
    return pairs, missing


def main():
    d = json.load(open(DATA))
    vals = values(d)
    print('%-15s %7s %9s %12s %8s %6s' % ('good', 'factor', 'sat/kg', 'iSatiety/t', 'prot/t', 'hydr'))
    for g, v in vals.items():
        print('%-15s %7.2f %9d %12d %8d %6d' % (g, v['factor'], v['satiety_per_kg'], v['iSatietyPerTonne'],
                                               v['iProteinPerTonne'], v['iHydrationPercent']))
    if len(sys.argv) > 2:
        pairs, missing = pairs_for(sys.argv[1], vals)
        json.dump({'pairs': pairs, 'missing': missing}, open(sys.argv[2], 'w'), indent=0)
        print(len(pairs), 'pairs,', sum(len(json.dumps(x)) for x in pairs), 'bytes; missing records:', missing)


if __name__ == '__main__':
    main()
