"""Economy and building-value summary from a state dump with HARNESS_VALUE_DIAG."""
import json, sys, collections
d = json.load(open(sys.argv[1]))
print('turn', d['turn'], 'year', d['year'])
for p in d['players']:
    e = p.get('econ', {})
    print('%-26s cities %2d gold %5d pct g/r/c/e %s flex %s target %5d extra %d commerce %4d calcGold %4d research %4d costs %4d anarchy %d avoid %d fin %d wars %d chosen %d' % (
        p['leader'][7:], len(p['cities']), p['gold'], e.get('pct'), e.get('flex'), e.get('goldTarget', -1), e.get('extraGoldTarget', 0),
        e.get('commerce', 0), e.get('calcGold', 0), e.get('calcResearch', 0), e.get('costs', 0), e.get('anarchy', 0),
        e.get('avoidScience', 0), e.get('finTrouble', 0), e.get('wars', 0), e.get('chosenWars', 0)))
top = collections.Counter(); first = collections.Counter(); seen = collections.Counter()
for p in d['players']:
    for c in p['cities']:
        bv = c.get('bv')
        if not bv: continue
        first[bv[0][0]] += 1
        for name, v, cost, turns in bv:
            seen[name] += 1
            top[name] += v
print('Top-valued building per city:', first.most_common(15))
print('Mean value when constructible:', sorted(((n, top[n] // seen[n], seen[n]) for n in seen), key=lambda x: -x[1])[:30])
