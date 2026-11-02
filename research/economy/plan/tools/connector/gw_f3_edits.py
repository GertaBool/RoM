"""GW.F3.T1/T2 with GW.F6.T1: goods accounts per settlement in CvCity.
Six int arrays per good: the stock (carried from turn to turn) and the last completed turn's produced, consumed,
received, sent and spoiled, in whole units of the good's GoodUnit. Allocated and zeroed in reset(), freed in
uninit(), saved at the end of CvCity::write behind uiFlag 1 (a uiFlag 0 save loads with zeros). Accessors
getGood<Account>(BonusTypes) and changeGood<Account>(BonusTypes, int): index asserts, each account kept in
0..MAX_INT (GW.F6.T1) with an assert when a change would take it below 0. Nothing calls them yet (GW.F5 will).
usage: gw_f3_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
ACC = ['Stock', 'Produced', 'Consumed', 'Received', 'Sent', 'Spoiled']
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

H, C = 'Assets/CvGameCoreDLL/CvCity.h', 'Assets/CvGameCoreDLL/CvCity.cpp'

# header: accessors after the bonus counts, members after m_paiNumCorpProducedBonuses
decl = ''.join('\tint getGood%s(BonusTypes eGood) const;\n\tvoid changeGood%s(BonusTypes eGood, int iChange);\n' % (a, a) for a in ACC)
edit(H, '\tbool changeNumBonusesNoCorporation(BonusTypes eIndex, int iChange);\t// true if a corporation of the city consumes eIndex\n',
     '\tbool changeNumBonusesNoCorporation(BonusTypes eIndex, int iChange);\t// true if a corporation of the city consumes eIndex\n\n'
     '\t// Goods accounts (GW.F3): per good, in whole units of its GoodUnit (CvBonusInfo::getGoodUnit). The stock carries\n'
     '\t// over from turn to turn; the other five are the last completed turn\'s flows, reset by the economy pass (GW.F5).\n'
     '\t// Bounds (GW.F6): each account is kept in 0..MAX_INT; tighter bounds come from the records once PR sets\n'
     '\t// harvest and storage quantities.\n' + decl)
edit(H, '\tint* m_paiNumCorpProducedBonuses;\n\tint* m_paiProjectProduction;\n',
     '\tint* m_paiNumCorpProducedBonuses;\n'
     + ''.join('\tint* m_paiGood%s;\n' % a for a in ACC) +
     '\tint* m_paiProjectProduction;\n')

# constructor, uninit, reset
edit(C, '\tm_paiNumCorpProducedBonuses = NULL;\n\tm_paiProjectProduction = NULL;\n',
     '\tm_paiNumCorpProducedBonuses = NULL;\n' + ''.join('\tm_paiGood%s = NULL;\n' % a for a in ACC) + '\tm_paiProjectProduction = NULL;\n')
edit(C, '\tSAFE_DELETE_ARRAY(m_paiNumCorpProducedBonuses);\n\tSAFE_DELETE_ARRAY(m_paiProjectProduction);\n',
     '\tSAFE_DELETE_ARRAY(m_paiNumCorpProducedBonuses);\n' + ''.join('\tSAFE_DELETE_ARRAY(m_paiGood%s);\n' % a for a in ACC) + '\tSAFE_DELETE_ARRAY(m_paiProjectProduction);\n')
edit(C, '\t\tm_paiNumCorpProducedBonuses = new int[GC.getNumBonusInfos()];\n'
        '\t\tfor (iI = 0; iI < GC.getNumBonusInfos(); iI++)\n\t\t{\n'
        '\t\t\tm_paiNoBonus[iI] = 0;\n\t\t\tm_paiFreeBonus[iI] = 0;\n\t\t\tm_paiNumBonuses[iI] = 0;\n\t\t\tm_paiNumCorpProducedBonuses[iI] = 0;\n',
     '\t\tm_paiNumCorpProducedBonuses = new int[GC.getNumBonusInfos()];\n'
     + ''.join('\t\tm_paiGood%s = new int[GC.getNumBonusInfos()];\n' % a for a in ACC) +
     '\t\tfor (iI = 0; iI < GC.getNumBonusInfos(); iI++)\n\t\t{\n'
     '\t\t\tm_paiNoBonus[iI] = 0;\n\t\t\tm_paiFreeBonus[iI] = 0;\n\t\t\tm_paiNumBonuses[iI] = 0;\n\t\t\tm_paiNumCorpProducedBonuses[iI] = 0;\n'
     + ''.join('\t\t\tm_paiGood%s[iI] = 0;\n' % a for a in ACC))

# accessors after getNumCorpProducedBonuses
impl = ('// Goods accounts (GW.F3). Adds iChange to the account of eGood and keeps it in 0..MAX_INT (GW.F6): the sum is\n'
        '// taken in 64 bits, a result below 0 is a caller\'s error (asserted) and is set to 0.\n'
        'static void changeGoodAccount(int* paiAccount, BonusTypes eGood, int iChange)\n{\n'
        '\tFAssertMsg(eGood >= 0 && eGood < GC.getNumBonusInfos(), "eGood out of range");\n'
        '\t__int64 iNew = (__int64)paiAccount[eGood] + iChange;\n'
        '\tFAssertMsg(iNew >= 0, "goods account would go below 0");\n'
        '\tpaiAccount[eGood] = (int)std::max<__int64>(0, std::min<__int64>(MAX_INT, iNew));\n}\n\n')
for a in ACC:
    impl += ('int CvCity::getGood%s(BonusTypes eGood) const\n{\n'
             '\tFAssertMsg(eGood >= 0 && eGood < GC.getNumBonusInfos(), "eGood out of range");\n'
             '\treturn m_paiGood%s[eGood];\n}\n\n'
             'void CvCity::changeGood%s(BonusTypes eGood, int iChange)\n{\n'
             '\tchangeGoodAccount(m_paiGood%s, eGood, iChange);\n}\n\n') % (a, a, a, a)
edit(C, '\treturn m_paiNumCorpProducedBonuses[eIndex];\n}\n\n\nbool CvCity::isCorporationBonus(BonusTypes eBonus) const\n',
     '\treturn m_paiNumCorpProducedBonuses[eIndex];\n}\n\n\n' + impl + 'bool CvCity::isCorporationBonus(BonusTypes eBonus) const\n')

# save: flag 1, accounts at the end of CvCity::write and read
edit(C, '\tuint uiFlag=0;\n\tpStream->Write(uiFlag);\t\t// flag for expansion\n\n\tpStream->Write(m_iID);\n',
     '\tuint uiFlag=1;\t// 1: goods accounts (GW.F3) at the end\n\tpStream->Write(uiFlag);\t\t// flag for expansion\n\n\tpStream->Write(m_iID);\n')
wr = ''.join('\tpStream->Write(GC.getNumBonusInfos(), m_paiGood%s);\n' % a for a in ACC)
rd = ''.join('\t\tpStream->Read(GC.getNumBonusInfos(), m_paiGood%s);\n' % a for a in ACC)
edit(C, '\tfor (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)\n'
        '\t{\n\t\tpStream->Write((*it).first);\n\t\tpStream->Write((*it).second);\n\t}\n}\n',
     '\tfor (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)\n'
     '\t{\n\t\tpStream->Write((*it).first);\n\t\tpStream->Write((*it).second);\n\t}\n\n' + wr + '}\n')
edit(C, '\t\tm_aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));\n\t}\n}\n',
     '\t\tm_aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));\n\t}\n\n'
     '\tif (uiFlag >= 1)\t// older saves keep the zeros reset() set\n\t{\n' + rd + '\t}\n}\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
