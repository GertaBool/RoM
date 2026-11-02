"""GW.F4.T1/T2: the bridge from the goods accounts to the engine's resource counts.
CvCity::m_paiGoodsBonus: per good, the instances the accounts supply (set by the economy pass, GW.F4.T3).
getGoodsBonus/changeGoodsBonus follow changeFreeBonus: take the city plot's goods out of its plot group, change,
put them back. Saved behind CvCity uiFlag 2. CvPlot::updatePlotGroupBonus counts it next to the free bonus.
usage: gw_f4_edits.py <mod checkout> <pairs.json out>"""
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

H, C, PL = 'Assets/CvGameCoreDLL/CvCity.h', 'Assets/CvGameCoreDLL/CvCity.cpp', 'Assets/CvGameCoreDLL/CvPlot.cpp'

# the changeFreeBonus declaration line, whatever its trailing comment
s = open(os.path.join(mod, H), 'rb').read().decode('latin-1')
line = next(l for l in s.split('\r\n') if l.startswith('\tvoid changeFreeBonus(BonusTypes eIndex, int iChange);'))
edit(H, line + '\n',
     line + '\n'
     '\tint getGoodsBonus(BonusTypes eIndex) const;\t// instances of eIndex the goods accounts supply (GW.F4)\n'
     '\tvoid changeGoodsBonus(BonusTypes eIndex, int iChange);\t// as changeFreeBonus: counted in the plot group\n')
edit(H, '\tint* m_paiGoodSpoiled;\n', '\tint* m_paiGoodSpoiled;\n\tint* m_paiGoodsBonus;\n')

edit(C, '\tm_paiGoodSpoiled = NULL;\n', '\tm_paiGoodSpoiled = NULL;\n\tm_paiGoodsBonus = NULL;\n')
edit(C, '\tSAFE_DELETE_ARRAY(m_paiGoodSpoiled);\n', '\tSAFE_DELETE_ARRAY(m_paiGoodSpoiled);\n\tSAFE_DELETE_ARRAY(m_paiGoodsBonus);\n')
edit(C, '\t\tm_paiGoodSpoiled = new int[GC.getNumBonusInfos()];\n',
        '\t\tm_paiGoodSpoiled = new int[GC.getNumBonusInfos()];\n\t\tm_paiGoodsBonus = new int[GC.getNumBonusInfos()];\n')
edit(C, '\t\t\tm_paiGoodSpoiled[iI] = 0;\n', '\t\t\tm_paiGoodSpoiled[iI] = 0;\n\t\t\tm_paiGoodsBonus[iI] = 0;\n')
edit(C, '\t\tm_paiFreeBonus[eIndex] += iChange;\n\t\tFAssert(getFreeBonus(eIndex) >= 0);\n\t\tplot()->updatePlotGroupBonus(true);\n\t}\n}\n',
     '\t\tm_paiFreeBonus[eIndex] += iChange;\n\t\tFAssert(getFreeBonus(eIndex) >= 0);\n\t\tplot()->updatePlotGroupBonus(true);\n\t}\n}\n\n'
     'int CvCity::getGoodsBonus(BonusTypes eIndex) const\n{\n'
     '\tFAssertMsg(eIndex >= 0 && eIndex < GC.getNumBonusInfos(), "eIndex out of range");\n'
     '\treturn m_paiGoodsBonus[eIndex];\n}\n\n'
     'void CvCity::changeGoodsBonus(BonusTypes eIndex, int iChange)\n{\n'
     '\tFAssertMsg(eIndex >= 0 && eIndex < GC.getNumBonusInfos(), "eIndex out of range");\n\n'
     '\tif (iChange != 0)\n\t{\n'
     '\t\tplot()->updatePlotGroupBonus(false);\n'
     '\t\tm_paiGoodsBonus[eIndex] += iChange;\n'
     '\t\tFAssert(getGoodsBonus(eIndex) >= 0);\n'
     '\t\tplot()->updatePlotGroupBonus(true);\n\t}\n}\n')
edit(C, '\tuint uiFlag=1;\t// 1: goods accounts (GW.F3) at the end\n',
        '\tuint uiFlag=2;\t// 1: goods accounts (GW.F3) at the end; 2: then the goods bonus (GW.F4)\n')
edit(C, '\tpStream->Write(GC.getNumBonusInfos(), m_paiGoodSpoiled);\n}\n',
        '\tpStream->Write(GC.getNumBonusInfos(), m_paiGoodSpoiled);\n\tpStream->Write(GC.getNumBonusInfos(), m_paiGoodsBonus);\n}\n')
edit(C, '\t\tpStream->Read(GC.getNumBonusInfos(), m_paiGoodSpoiled);\n\t}\n}\n',
        '\t\tpStream->Read(GC.getNumBonusInfos(), m_paiGoodSpoiled);\n\t}\n'
        '\tif (uiFlag >= 2)\n\t{\n\t\tpStream->Read(GC.getNumBonusInfos(), m_paiGoodsBonus);\n\t}\n}\n')
edit(PL, '\t\t\t\taiChange[iI] += iSign * pPlotCity->getFreeBonus((BonusTypes)iI);\n',
         '\t\t\t\taiChange[iI] += iSign * (pPlotCity->getFreeBonus((BonusTypes)iI) + pPlotCity->getGoodsBonus((BonusTypes)iI));\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
