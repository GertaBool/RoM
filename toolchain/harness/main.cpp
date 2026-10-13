// Headless driver for CvGameCoreDLL: boots the DLL, loads the mod's XML, sets
// up a scripted map and lets the AI play. usage: harness.exe <scenario> [turns] [plain]
#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "CvArtFileMgr.h"
#include "engine.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>

#define HH extern "C" __declspec(dllimport)
HH int HH_type(const char*);
HH void HH_setPlot(int, int, int, int);
HH void HH_finishMap();
HH void HH_revealAll(int);
HH void HH_setTech(int, int);
HH int HH_initCity(int, int, int);
HH int HH_initUnit(int, int, int, int, int);
HH int HH_snapshot(int, char*, int);
HH void HH_newGame(int, int, int, const char**, const char**, const char*, const char*, const char*, const char**, int, unsigned int);
HH void HH_startGame(int);
HH void HH_beginPlay();
HH int HH_gameTurn();
HH void HH_update();
HH int HH_numCities(int);
HH int HH_cityAt(int, int);
HH int HH_debugSites(int, int, int, char*, int);
HH int HH_probePath(int, int, int, int, char*, int);
HH void HH_setGold(int, int);
HH void HH_setCityPopulation(int, int, int);
HH int HH_economy(int, char*, int);

static bool loadXml()
{
	CvXMLLoadUtility* xml = new CvXMLLoadUtility();
	bool ok = true;
	ok = xml->SetGlobalDefines() && ok;
	ok = xml->SetGlobalTypes() && ok;
	ok = xml->LoadBasicInfos() && ok;
	ok = xml->LoadPlayerOptions() && ok;
	CvArtFileMgr::GetInstance().Reset();   // art defines + lookup maps, as the engine does
	ok = xml->LoadPreMenuGlobals() && ok;
	ok = xml->SetPostGlobalsGlobalDefines() && ok;
	ok = xml->SetupGlobalLandscapeInfo() && ok;
	ok = xml->LoadGraphicOptions() && ok;
	ok = xml->LoadPostMenuGlobals() && ok;
	delete xml;
	harnessLog("XML loaded (%s)\n", ok ? "ok" : "with errors");
	return ok;
}

static void snapshot(int ePlayer)
{
	static char buf[1 << 16];
	int n = HH_snapshot(ePlayer, buf, sizeof(buf) - 1);
	buf[n < 0 ? 0 : n] = 0;
	harnessLog("%s", buf);
}

// Two islands separated by a coastal channel. The AI's capital is on the west
// island; the east island is empty, revealed and settleable only by sea.
static void islandsScenario(int iTurns, int iEastX, bool bPlain)
{
	const int W = iEastX + 13, H = 16;
	const char* civs[] = { "CIVILIZATION_ENGLAND" };
	const char* leaders[] = { "LEADER_ELIZABETH" };
	const char* options[] = { "GAMEOPTION_NO_BARBARIANS", "GAMEOPTION_NO_GOODY_HUTS", "GAMEOPTION_NO_EVENTS" };
	HH_newGame(W, H, 1, civs, leaders, bPlain ? "HANDICAP_NOBLE" : "HANDICAP_SETTLER", "GAMESPEED_NORMAL", "ERA_ANCIENT", options, 3, 12345u);
	const int coast = HH_type("TERRAIN_COAST"), grass = HH_type("TERRAIN_GRASS"), plains = HH_type("TERRAIN_PLAINS");
	for (int x = 0; x < W; ++x)
		for (int y = 0; y < H; ++y)
		{
			const bool west = x >= 9 && x <= 11 && y >= 6 && y <= 8;   // 3x3: no legal second city site
			const bool east = x >= iEastX && x <= iEastX + 10 && y >= 2 && y <= 13;
			if (west || east) HH_setPlot(x, y, 1 /*PLOT_LAND*/, ((x + y) % 3 == 0) ? plains : grass);
			else HH_setPlot(x, y, 3 /*PLOT_OCEAN*/, coast);
		}
	HH_finishMap();
	HH_startGame(-1);
	HH_revealAll(0);
	HH_initCity(0, 11, 7);   // east shore of the home island
	const int settler = HH_initUnit(0, HH_type("UNIT_SETTLER"), 11, 7, HH_type("UNITAI_SETTLE"));
	const int escort = HH_initUnit(0, HH_type("UNIT_WARRIOR"), 11, 7, HH_type("UNITAI_CITY_DEFENSE"));
	HH_initUnit(0, HH_type("UNIT_WARRIOR"), 11, 7, HH_type("UNITAI_CITY_DEFENSE"));
	const int ship = HH_initUnit(0, HH_type("UNIT_GALLEY"), 11, 7, HH_type("UNITAI_SETTLER_SEA"));
	harnessLog("units: settler %d escort %d ship %d\n", settler, escort, ship);
	// Default: a reserve and a grown capital so upkeep never disbands the ship
	// or escort before the voyage. "plain" starts at Noble without either.
	if (!bPlain)
	{
		HH_setGold(0, 1000);
		HH_setCityPopulation(11, 7, 3);
	}
	HH_beginPlay();

	int iLastTurn = -1;
	long iUpdates = 0;
	while (HH_gameTurn() < iTurns && iUpdates < 2000000)
	{
		if (HH_gameTurn() != iLastTurn)
		{
			iLastTurn = HH_gameTurn();
			harnessLog("== turn %d: %d cities\n", iLastTurn, HH_numCities(0));
			snapshot(0);
			{
				char eco[1024];
				int n = HH_economy(0, eco, sizeof(eco) - 1);
				eco[n < 0 ? 0 : n] = 0;
				harnessLog("%s", eco);
			}
			if (iLastTurn <= 0)
			{
				static char dbg[1 << 15];
				int n = HH_debugSites(0, settler, ship, dbg, sizeof(dbg) - 1);
								n += HH_probePath(0, ship, iEastX - 1, 7, dbg + n, sizeof(dbg) - 1 - n);
				dbg[n < 0 ? 0 : n] = 0;
				harnessLog("%s", dbg);
			}
		}
		HH_update();
		++iUpdates;
	}
	int eastCities = 0;
	for (int x = iEastX; x <= iEastX + 10; ++x) for (int y = 2; y <= 13; ++y) if (HH_cityAt(x, y) == 0) ++eastCities;
	harnessLog("RESULT turn %d: player 0 has %d cities, %d on the east island\n", HH_gameTurn(), HH_numCities(0), eastCities);
}

int main(int argc, char** argv)
{
	char exe[MAX_PATH];
	GetModuleFileNameA(NULL, exe, MAX_PATH);
	std::string root(exe);
	root = root.substr(0, root.find_last_of('\\'));

	HarnessConfig cfg;
	cfg.root = root;
	cfg.modName = "Mods\\Rise of Mankind\\";
	cfg.logDir = root + "\\logs";
	CreateDirectoryA(cfg.logDir.c_str(), NULL);

	CvGlobals::getInstance().setDLLIFace(harnessEngine(cfg));
	GC.init();
	if (!loadXml()) harnessLog("continuing despite XML errors\n");
	const char* scenario = argc > 1 ? argv[1] : "islands";
	const int turns = argc > 2 ? atoi(argv[2]) : 30;
	const bool plain = argc > 3 && strcmp(argv[3], "plain") == 0;
	if (strcmp(scenario, "islands") == 0) islandsScenario(turns, 17, plain);       // one sailing turn
	else if (strcmp(scenario, "mid") == 0) islandsScenario(turns, 21, plain);    // two sailing turns
	else if (strcmp(scenario, "far") == 0) islandsScenario(turns, 27, plain);    // beyond the settlement candidate range
	else if (strcmp(scenario, "xml") != 0) harnessLog("unknown scenario %s\n", scenario);
	return 0;
}
