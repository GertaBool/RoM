"""GW.F5.T1/T2 with GW.F4.T3: the economy pass.
CvPlayer::doGoods(), called once per turn from CvPlayer::doTurn after doEspionagePoints and before the city loop.
Its steps, each a function, in this order: reset the cities' five flows; produce (PR); run recipes (IN.F1);
distribute (SD.F3); consume (CN); store and spoil (SD.F1, SD.F2); set each city's goods bonus from its stock
(GW.F4.T3). The steps other features fill are empty with a comment naming the feature. No random numbers; cities
in firstCity/nextCity order.
usage: gw_f5_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
pairs = []

def edit(f, old, new):
    p = os.path.join(mod, f)
    s = open(p, 'rb').read().decode('latin-1')
    nl = '\r\n' if '\r\n' in s else '\n'
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(old) == 1, (f, s.count(old), old[:80])
    s = s.replace(old, new)
    open(p, 'wb').write(s.encode('latin-1'))
    pairs.append({'file': f, 'old': old, 'new': new})

H, C = 'Assets/CvGameCoreDLL/CvPlayer.h', 'Assets/CvGameCoreDLL/CvPlayer.cpp'
STEPS = [('resetGoodsFlows', None), ('produceGoods', 'PR: tiles, improvements, buildings and specialists add to the stock and the produced flow'),
         ('runGoodsRecipes', 'IN.F1: buildings turn inputs into outputs'),
         ('distributeGoods', 'SD.F3: surpluses move to shortages within each trade network'),
         ('consumeGoods', 'CN: citizens use goods for their needs'),
         ('storeAndSpoilGoods', 'SD.F1, SD.F2: storage limits and spoilage'),
         ('updateGoodsBonus', None)]

edit(H, '\tvoid doEspionagePoints();\n',
     '\tvoid doEspionagePoints();\n'
     '\t// The economy pass (GW.F5): once per turn, before the cities, in this order\n'
     '\tvoid doGoods();\n' + ''.join('\tvoid %s();\n' % n for n, _ in STEPS))

edit(C, '\tdoEspionagePoints();\n\n\t// Allocate liquid gold',
     '\tdoEspionagePoints();\n\n\tdoGoods();\n\n\t// Allocate liquid gold')

body = ('// The economy pass (GW.F5): one call per player per turn, from doTurn before the city loop. The steps run in a fixed\n'
        '// order over the cities in firstCity/nextCity order and draw no random number.\n'
        'void CvPlayer::doGoods()\n{\n' + ''.join('\t%s();\n' % n for n, _ in STEPS) + '}\n\n'
        '// The five flows hold the last completed turn: cleared before this turn\'s steps fill them; the stock carries over.\n'
        'void CvPlayer::resetGoodsFlows()\n{\n\tint iLoop;\n'
        '\tfor (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))\n\t{\n'
        '\t\tfor (int iI = 0; iI < GC.getNumBonusInfos(); iI++)\n\t\t{\n'
        '\t\t\tBonusTypes eGood = (BonusTypes)iI;\n'
        '\t\t\tpLoopCity->changeGoodProduced(eGood, -pLoopCity->getGoodProduced(eGood));\n'
        '\t\t\tpLoopCity->changeGoodConsumed(eGood, -pLoopCity->getGoodConsumed(eGood));\n'
        '\t\t\tpLoopCity->changeGoodReceived(eGood, -pLoopCity->getGoodReceived(eGood));\n'
        '\t\t\tpLoopCity->changeGoodSent(eGood, -pLoopCity->getGoodSent(eGood));\n'
        '\t\t\tpLoopCity->changeGoodSpoiled(eGood, -pLoopCity->getGoodSpoiled(eGood));\n'
        '\t\t}\n\t}\n}\n\n')
for n, what in STEPS:
    if what:
        body += 'void CvPlayer::%s()\n{\n\t// Filled by %s\n}\n\n' % (n, what)
body += ('// The bridge (GW.F4.T3): a city with a stock of a good holds one instance of it in its trade network.\n'
         '// For PR: once a plot\'s good goes into the accounts, its direct plot-group count must stop, or it counts twice.\n'
         'void CvPlayer::updateGoodsBonus()\n{\n\tint iLoop;\n'
         '\tfor (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))\n\t{\n'
         '\t\tfor (int iI = 0; iI < GC.getNumBonusInfos(); iI++)\n\t\t{\n'
         '\t\t\tBonusTypes eGood = (BonusTypes)iI;\n'
         '\t\t\tint iSupplied = (pLoopCity->getGoodStock(eGood) > 0) ? 1 : 0;\n'
         '\t\t\tpLoopCity->changeGoodsBonus(eGood, iSupplied - pLoopCity->getGoodsBonus(eGood));\n'
         '\t\t}\n\t}\n}\n\n')
edit(C, 'void CvPlayer::doEspionagePoints()\n', body + 'void CvPlayer::doEspionagePoints()\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
