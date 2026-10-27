"""GW.F1.T1/T2: GoodUnit and GoodCategory on BonusInfo (D22).
Schema: two optional text elements at the end of BonusInfo (CIV4TerrainSchema.xml).
CvBonusInfo: m_iGoodUnit, m_iGoodCategory, indices into fixed lists written from proposals.json
('units', 'categories'), -1 when absent; an unknown text goes to CvBonusInfo_read.log and an assert.
Read in read(CvXMLLoadUtility*), carried by copyNonDefaults, kept in the cache stream behind uiFlag 1.
No game code reads them.
usage: gw_f1_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
prop = json.load(open(os.path.join(HERE, '..', '..', 'proposals.json')))
UNITS, CATS = prop['units'], prop['categories']
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

def clist(names):
    return ', '.join('"%s"' % n for n in names)

# T1: schema
SCH = 'Assets/XML/Terrain/CIV4TerrainSchema.xml'
edit(SCH,
     '\t\t<element type="bUseLSystem" minOccurs="0"/>\n\t</ElementType>\n\t<ElementType name="BonusInfos" content="eltOnly">',
     '\t\t<element type="bUseLSystem" minOccurs="0"/>\n\t\t<element type="GoodUnit" minOccurs="0"/>\n'
     '\t\t<element type="GoodCategory" minOccurs="0"/>\n\t</ElementType>\n\t<ElementType name="BonusInfos" content="eltOnly">')
edit(SCH,
     '\t<ElementType name="ArtDefineTag" content="textOnly"/>\n\t<ElementType name="Type" content="textOnly"/>',
     '\t<ElementType name="ArtDefineTag" content="textOnly"/>\n'
     '\t<!-- GW.F1 (D22): unit: %s; category: %s -->\n'
     '\t<ElementType name="GoodUnit" content="textOnly"/>\n\t<ElementType name="GoodCategory" content="textOnly"/>\n'
     '\t<ElementType name="Type" content="textOnly"/>' % (', '.join(UNITS), ', '.join(CATS)))

# T2: header
H = 'Assets/CvGameCoreDLL/CvInfos.h'
edit(H,
     '\tconst TCHAR* getButton() const; // Exposed to Python\n\tDllExport const CvArtInfoBonus* getArtInfo() const; // Exposed to Python\n',
     '\tconst TCHAR* getButton() const; // Exposed to Python\n\tDllExport const CvArtInfoBonus* getArtInfo() const; // Exposed to Python\n\n'
     '\t// Goods catalogue (GW.F1, D22): index into the fixed lists below, -1 when the record has none\n'
     '\tint getGoodUnit() const;\n\tint getGoodCategory() const;\n'
     '\tstatic int getNumGoodUnits();\n\tstatic const char* getGoodUnitName(int i);\n'
     '\tstatic int getNumGoodCategories();\n\tstatic const char* getGoodCategoryName(int i);\n')
edit(H,
     '\tbool m_bNormalize;\n\n\tCvString m_szArtDefineTag;\n',
     '\tbool m_bNormalize;\n\n\tint m_iGoodUnit;\n\tint m_iGoodCategory;\n\n\tCvString m_szArtDefineTag;\n')

# T2: source
C = 'Assets/CvGameCoreDLL/CvInfos.cpp'
edit(C, 'm_bNormalize(false),\nm_piYieldChange(NULL),\nm_piImprovementChange(NULL),\nm_pbTerrain(NULL),\nm_pbFeature(NULL),\nm_pbFeatureTerrain(NULL)\n{',
        'm_bNormalize(false),\nm_iGoodUnit(-1),\nm_iGoodCategory(-1),\nm_piYieldChange(NULL),\nm_piImprovementChange(NULL),\nm_pbTerrain(NULL),\nm_pbFeature(NULL),\nm_pbFeatureTerrain(NULL)\n{')
edit(C, 'const TCHAR* CvBonusInfo::getButton() const\n{',
     '// Goods catalogue (GW.F1, D22): the texts GoodUnit and GoodCategory take, as in\n'
     '// research/economy/plan/proposals.json (units, categories)\n'
     'static const char* const s_aszGoodUnits[] = { %s };\n'
     'static const char* const s_aszGoodCategories[] = { %s };\n'
     'static const int NUM_GOOD_UNITS = sizeof(s_aszGoodUnits) / sizeof(s_aszGoodUnits[0]);\n'
     'static const int NUM_GOOD_CATEGORIES = sizeof(s_aszGoodCategories) / sizeof(s_aszGoodCategories[0]);\n\n'
     '// the index of szVal in aszNames; -1 for an empty text, and for an unknown one, which is reported\n'
     'static int findGoodName(const CvString& szVal, const char* const* aszNames, int iNum, const char* szTag, const char* szType)\n'
     '{\n\tif (szVal.empty())\n\t{\n\t\treturn -1;\n\t}\n'
     '\tfor (int i = 0; i < iNum; i++)\n\t{\n\t\tif (szVal == aszNames[i])\n\t\t{\n\t\t\treturn i;\n\t\t}\n\t}\n'
     '\tCvString szError;\n\tszError.Format("%%s: unknown %%s \'%%s\'", szType, szTag, szVal.c_str());\n'
     '\tgDLL->logMsg("CvBonusInfo_read.log", szError.c_str());\n\tFAssertMsg(false, szError.c_str());\n\treturn -1;\n}\n\n'
     'int CvBonusInfo::getGoodUnit() const\n{\n\treturn m_iGoodUnit;\n}\n\n'
     'int CvBonusInfo::getGoodCategory() const\n{\n\treturn m_iGoodCategory;\n}\n\n'
     'int CvBonusInfo::getNumGoodUnits()\n{\n\treturn NUM_GOOD_UNITS;\n}\n\n'
     'const char* CvBonusInfo::getGoodUnitName(int i)\n{\n\tFAssertMsg(i >= 0 && i < NUM_GOOD_UNITS, "Index out of bounds");\n\treturn s_aszGoodUnits[i];\n}\n\n'
     'int CvBonusInfo::getNumGoodCategories()\n{\n\treturn NUM_GOOD_CATEGORIES;\n}\n\n'
     'const char* CvBonusInfo::getGoodCategoryName(int i)\n{\n\tFAssertMsg(i >= 0 && i < NUM_GOOD_CATEGORIES, "Index out of bounds");\n\treturn s_aszGoodCategories[i];\n}\n\n'
     'const TCHAR* CvBonusInfo::getButton() const\n{' % (clist(UNITS), clist(CATS)))
edit(C, '\tm_pbFeatureTerrain = new bool[GC.getNumTerrainInfos()];\n\tstream->Read(GC.getNumTerrainInfos(), m_pbFeatureTerrain);\n}\n\nvoid CvBonusInfo::write(FDataStreamBase* stream)\n{\n\tCvInfoBase::write(stream);\n\n\tuint uiFlag=0;',
        '\tm_pbFeatureTerrain = new bool[GC.getNumTerrainInfos()];\n\tstream->Read(GC.getNumTerrainInfos(), m_pbFeatureTerrain);\n\n'
        '\tm_iGoodUnit = -1;\n\tm_iGoodCategory = -1;\n\tif (uiFlag >= 1)\n\t{\n\t\tstream->Read(&m_iGoodUnit);\n\t\tstream->Read(&m_iGoodCategory);\n\t}\n}\n\n'
        'void CvBonusInfo::write(FDataStreamBase* stream)\n{\n\tCvInfoBase::write(stream);\n\n\tuint uiFlag=1;')
edit(C, '\tstream->Write(GC.getNumTerrainInfos(), m_pbFeatureTerrain);\n}\n\nbool CvBonusInfo::read(CvXMLLoadUtility* pXML)',
        '\tstream->Write(GC.getNumTerrainInfos(), m_pbFeatureTerrain);\n\n'
        '\tstream->Write(m_iGoodUnit);\n\tstream->Write(m_iGoodCategory);\n}\n\nbool CvBonusInfo::read(CvXMLLoadUtility* pXML)')
edit(C, '\tpXML->SetVariableListTagPair(&m_pbFeatureTerrain, "FeatureTerrainBooleans", sizeof(GC.getTerrainInfo((TerrainTypes)0)), GC.getNumTerrainInfos());\n\n\treturn true;\n}\n/****',
        '\tpXML->SetVariableListTagPair(&m_pbFeatureTerrain, "FeatureTerrainBooleans", sizeof(GC.getTerrainInfo((TerrainTypes)0)), GC.getNumTerrainInfos());\n\n'
        '\tpXML->GetChildXmlValByName(szTextVal, "GoodUnit");\n\tm_iGoodUnit = findGoodName(szTextVal, s_aszGoodUnits, NUM_GOOD_UNITS, "GoodUnit", getType());\n'
        '\tpXML->GetChildXmlValByName(szTextVal, "GoodCategory");\n\tm_iGoodCategory = findGoodName(szTextVal, s_aszGoodCategories, NUM_GOOD_CATEGORIES, "GoodCategory", getType());\n\n'
        '\treturn true;\n}\n/****')
edit(C, '\tif (isNormalize() == bDefault) m_bNormalize = pClassInfo->isNormalize();\n',
        '\tif (isNormalize() == bDefault) m_bNormalize = pClassInfo->isNormalize();\n'
        '\tif (getGoodUnit() == -1) m_iGoodUnit = pClassInfo->getGoodUnit();\n'
        '\tif (getGoodCategory() == -1) m_iGoodCategory = pClassInfo->getGoodCategory();\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
