"""PR.F6.T2: scenarios declare their map scale. CvWBInterface.py reads a BeginEconomy block at the end of the
scenario file (after every block the base game's CvWBDesc.py reads, so the base game still loads the file), sets
the plot area after the map is applied (in-game load and WorldBuilder load), and appends the block when the
WorldBuilder saves. Python 2.4 (the game's), tabs, CRLF.
usage: pr_f6_t2_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
F = 'Assets/Python/EntryPoints/CvWBInterface.py'
pairs = []

def edit(old, new):
    p = os.path.join(mod, F)
    s = open(p, 'rb').read().decode('latin-1')
    nl = '\r\n' if '\r\n' in s else '\n'
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)
    open(p, 'wb').write(s.encode('latin-1'))
    pairs.append({'file': F, 'old': old, 'new': new})

HELPERS = '''########## Settlement Economy (PR.F6): the map scale a scenario declares, in a block after all CvWBDesc reads:
##########   BeginEconomy / plot area km2=<n> / EndEconomy
plotAreaKm2 = 0

def readPlotArea(fileName):
	"km2 of one plot from the file's BeginEconomy block; 0 when it has none"
	iArea = 0
	bIn = False
	try:
		f = open(fileName, 'r')
		for line in f.readlines():
			s = line.strip()
			if s == "BeginEconomy":
				bIn = True
			elif s == "EndEconomy":
				bIn = False
			elif bIn and s.startswith("plot area km2="):
				iArea = int(s.split("=", 1)[1])
		f.close()
	except (IOError, ValueError):
		iArea = 0
	return iArea

def applyPlotArea():
	"Declares the scenario's plot area on the map once the map is applied; logs when the scenario declares none"
	if plotAreaKm2 > 0:
		CyMap().setPlotAreaKm2(plotAreaKm2)
	else:
		CvUtil.pyPrint("scenario declares no plot area (BeginEconomy block): the whole-planet default applies")

def writePlotArea(fileName):
	"Appends the map's declared plot area to the file WBDesc.write has just written"
	if CyMap().isPlotAreaDeclared():
		f = open(fileName, 'a')
		f.write("BeginEconomy\\n\\tplot area km2=%d\\nEndEconomy\\n" % CyMap().getPlotAreaKm2())
		f.close()
########## Settlement Economy END

def writeDesc(argsList):
'''

edit('def writeDesc(argsList):\n', HELPERS)
edit('\treturn WBDesc.write(fileName)\n',
     '\tret = WBDesc.write(fileName)\n\twritePlotArea(fileName)\n\treturn ret\n')
edit('\tif WBDesc.read(fileName) < 0:\n\t\treturn -1\n\tif (WBDesc.applyMap() < 0):\n\t\treturn -1\n\treturn WBDesc.applyInitialItems()\n',
     '\tif WBDesc.read(fileName) < 0:\n\t\treturn -1\n'
     '\tglobal plotAreaKm2\n\tplotAreaKm2 = readPlotArea(fileName)\n'
     '\tif (WBDesc.applyMap() < 0):\n\t\treturn -1\n\tapplyPlotArea()\n\treturn WBDesc.applyInitialItems()\n')
edit('\tif (fileName!=lastFileRead):\n\t\tret=WBDesc.read(fileName)\n',
     '\tglobal plotAreaKm2\n\tplotAreaKm2 = readPlotArea(fileName)\n\tif (fileName!=lastFileRead):\n\t\tret=WBDesc.read(fileName)\n')
edit('\t"After reading, applies the map loaded data"\n\treturn WBDesc.applyMap()\n',
     '\t"After reading, applies the map loaded data"\n\tret = WBDesc.applyMap()\n\tapplyPlotArea()\n\treturn ret\n')

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
