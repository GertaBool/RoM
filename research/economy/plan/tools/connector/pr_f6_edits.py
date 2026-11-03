"""PR.F6.T1: the map scale. CvMap::m_iPlotAreaKm2, the area of one plot in km2 as the map or scenario declares it
(0: not declared). getPlotAreaKm2() returns the declared value, else the whole-planet default (Earth's surface over
the map's plots). A map script's optional getPlotAreaKm2() declares it when the map is generated (CvMap::reset
without init data, where the script's latitudes are read too); a scenario declares it through CyMap.setPlotAreaKm2
(CvWBInterface.py, PR.F6.T2). Saved behind CvMap uiFlag 1. Nothing reads it yet (PR.F1 will).
usage: pr_f6_edits.py <mod checkout> <pairs.json out>"""
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

D = 'Assets/CvGameCoreDLL/'
H, C, YH, YC, YI = D + 'CvMap.h', D + 'CvMap.cpp', D + 'CyMap.h', D + 'CyMap.cpp', D + 'CyMapInterface.cpp'

def line(f, start):
    s = open(os.path.join(mod, f), 'rb').read().decode('latin-1')
    return next(l for l in s.replace('\r\n', '\n').split('\n') if l.startswith(start))

l = line(H, '\tint getBottomLatitude();')
edit(H, l + '\n', l + '\n\n'
     '\t// Map scale (PR.F6): km2 of one plot as the map or scenario declares it; undeclared: Earth\'s surface over the plots\n'
     '\tint getPlotAreaKm2() const;\n\tvoid setPlotAreaKm2(int iNewValue);\n\tbool isPlotAreaDeclared() const;\n')
edit(H, '\tint m_iBottomLatitude;\n\tint m_iNextRiverID;\n',
        '\tint m_iBottomLatitude;\n\tint m_iNextRiverID;\n\tint m_iPlotAreaKm2;\t// 0: not declared\n')

edit(C, '\tm_iTopLatitude = std::min(m_iTopLatitude, 90);\n',
     '\t// Map scale (PR.F6): a map script may declare the area of one plot; a scenario declares it after loading\n'
     '\tm_iPlotAreaKm2 = 0;\n'
     '\tif (!pInitInfo)\n\t{\n'
     '\t\tlong lPlotArea = 0;\n'
     '\t\tbool bOk = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getPlotAreaKm2", NULL, &lPlotArea);\n'
     '\t\tif (bOk && !gDLL->getPythonIFace()->pythonUsingDefaultImpl() && lPlotArea > 0)\n\t\t{\n'
     '\t\t\tm_iPlotAreaKm2 = (int)lPlotArea;\n\t\t}\n'
     '\t\telse\n\t\t{\n'
     '\t\t\tCvString szLog;\n'
     '\t\t\tszLog.Format("map script %S declares no getPlotAreaKm2(): the whole-planet default applies", gDLL->getMapScriptName().GetCString());\n'
     '\t\t\tgDLL->logMsg("CvMap_plotArea.log", szLog.c_str());\n\t\t}\n\t}\n\n'
     '\tm_iTopLatitude = std::min(m_iTopLatitude, 90);\n')

edit(C, 'int CvMap::getTopLatitude()\n{\n\treturn m_iTopLatitude;\n}\n',
     'int CvMap::getTopLatitude()\n{\n\treturn m_iTopLatitude;\n}\n\n'
     '// Earth\'s surface, 510,100,000 km2, over the map\'s plots when the map declares no scale; at least 1\n'
     'int CvMap::getPlotAreaKm2() const\n{\n'
     '\tif (m_iPlotAreaKm2 > 0)\n\t{\n\t\treturn m_iPlotAreaKm2;\n\t}\n'
     '\tint iPlots = m_iGridWidth * m_iGridHeight;\n'
     '\treturn (iPlots > 0) ? std::max(1, 510100000 / iPlots) : 1;\n}\n\n'
     'void CvMap::setPlotAreaKm2(int iNewValue)\n{\n'
     '\tFAssertMsg(iNewValue >= 0, "plot area must not be negative");\n'
     '\tm_iPlotAreaKm2 = std::max(0, iNewValue);\n}\n\n'
     'bool CvMap::isPlotAreaDeclared() const\n{\n\treturn m_iPlotAreaKm2 > 0;\n}\n')

edit(C, '\tuint uiFlag=0;\n\tpStream->Write(uiFlag);\t\t// flag for expansion\n\n\tpStream->Write(m_iGridWidth);\n',
     '\tuint uiFlag=1;\t// 1: plot area (PR.F6)\n\tpStream->Write(uiFlag);\t\t// flag for expansion\n\n\tpStream->Write(m_iGridWidth);\n')
edit(C, '\tpStream->Read(&m_bWrapX);\n\tpStream->Read(&m_bWrapY);\n',
     '\tpStream->Read(&m_bWrapX);\n\tpStream->Read(&m_bWrapY);\n\n'
     '\tm_iPlotAreaKm2 = 0;\n\tif (uiFlag >= 1)\n\t{\n\t\tpStream->Read(&m_iPlotAreaKm2);\n\t}\n')
edit(C, '\tpStream->Write(m_bWrapX);\n\tpStream->Write(m_bWrapY);\n',
     '\tpStream->Write(m_bWrapX);\n\tpStream->Write(m_bWrapY);\n\n\tpStream->Write(m_iPlotAreaKm2);\n')

l = line(YH, '\tint getBottomLatitude();')
edit(YH, l + '\n', l + '\n\tint getPlotAreaKm2();\n\tvoid setPlotAreaKm2(int iNewValue);\n\tbool isPlotAreaDeclared();\n')
edit(YC, 'int CyMap::getTopLatitude()\n{\n\treturn m_pMap ? m_pMap->getTopLatitude() : -1;\n}\n',
     'int CyMap::getTopLatitude()\n{\n\treturn m_pMap ? m_pMap->getTopLatitude() : -1;\n}\n\n'
     'int CyMap::getPlotAreaKm2()\n{\n\treturn m_pMap ? m_pMap->getPlotAreaKm2() : -1;\n}\n\n'
     'void CyMap::setPlotAreaKm2(int iNewValue)\n{\n\tif (m_pMap)\n\t{\n\t\tm_pMap->setPlotAreaKm2(iNewValue);\n\t}\n}\n\n'
     'bool CyMap::isPlotAreaDeclared()\n{\n\treturn m_pMap ? m_pMap->isPlotAreaDeclared() : false;\n}\n')
l = line(YI, '\t\t.def("getBottomLatitude"')
edit(YI, l + '\n', l + '\n'
     '\t\t.def("getPlotAreaKm2", &CyMap::getPlotAreaKm2, "int () - km2 of one plot (declared by the map or scenario, else Earth\'s surface over the plots)")\n'
     '\t\t.def("setPlotAreaKm2", &CyMap::setPlotAreaKm2, "void (int) - declare the km2 of one plot (0: undeclared)")\n'
     '\t\t.def("isPlotAreaDeclared", &CyMap::isPlotAreaDeclared, "bool () - whether the map or scenario declared its plot area")\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
