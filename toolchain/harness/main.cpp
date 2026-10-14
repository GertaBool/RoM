// Headless driver for CvGameCoreDLL: boots the DLL, loads the mod's XML, sets
// up a map and lets the AI play. usage:
//   harness.exe <islands|mid|far> [turns] [plain]
//   harness.exe scenario <scn> <speed|-> <handicap> <seed> <turns> <out.jsonl> [detailEvery]
//   harness.exe save <init> <game> <turns> <out.jsonl> [detailEvery] [stuckUpdates]
#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "CvArtFileMgr.h"
#include "engine.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <map>
#include <string>

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
HH int HH_loadScenario(const char*, const char*, const char*, unsigned int, char*, int);
HH void HH_telemetryReset();
HH int HH_telemetryHeader(char*, int);
HH int HH_telemetry(char*, int, int, int);
HH int HH_gameState();
HH int HH_loadSave(const char*, const char*, char*, int);
HH int HH_stuckReport(char*, int);
HH int HH_infoCounts(char*, int);
HH int HH_autoPlayHumans(int);
HH int HH_dumpState(const char*);

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

// A WorldBuilder scenario converted by wbs2scn.py, played by AI players only.
// Writes one JSON line per game turn to szOut (header line first).
// HARNESS_SNAPSHOT=t1,t2,...: at the start of each listed game turn write
// <out>.t<turn>.init and <out>.t<turn>.game, which "harness.exe save" loads.
// Looked up at run time: older DLL builds lack HH_saveState.
static void maybeSnapshot(const char* szOut, int iTurn)
{
	// HARNESS_RAND_LOG=t: from game turn t on, log every random number the DLL
	// draws, with its purpose, to logs\rand.log (to find where two runs part).
	const char* szRandFrom = getenv("HARNESS_RAND_LOG");
	if (szRandFrom != NULL && iTurn >= atoi(szRandFrom))
	{
		GC.getLogging() = true;
		GC.getRandLogging() = true;
	}
	const char* szList = getenv("HARNESS_SNAPSHOT");
	if (szList == NULL) return;
	bool bListed = false;
	for (const char* p = szList; *p != 0; )
	{
		char* pEnd;
		const long iListed = strtol(p, &pEnd, 10);
		if (pEnd == p) break;
		if (iListed == iTurn) bListed = true;
		p = (*pEnd == ',') ? pEnd + 1 : pEnd;
	}
	if (!bListed) return;
	typedef int (*SaveFn)(const char*, const char*);
	HMODULE hDll = GetModuleHandleA("CvGameCoreDLL.dll");
	const SaveFn pfnSave = hDll != NULL ? (SaveFn)GetProcAddress(hDll, "HH_saveState") : NULL;
	if (pfnSave == NULL) { harnessLog("snapshot turn %d: this DLL build cannot write snapshots\n", iTurn); return; }
	char szInit[1024], szGame[1024];
	_snprintf(szInit, sizeof(szInit), "%s.t%d.init", szOut, iTurn); szInit[sizeof(szInit) - 1] = 0;
	_snprintf(szGame, sizeof(szGame), "%s.t%d.game", szOut, iTurn); szGame[sizeof(szGame) - 1] = 0;
	harnessLog("snapshot turn %d: %s, %d bytes\n", iTurn, szGame, pfnSave(szInit, szGame));
}

extern std::map<std::string, long> g_pyCallCounts;
// HARNESS_PY_COUNTS=1: Python callbacks (engine.cpp) and events (the DLL) of the run.
static void printPythonCounts(int iTurns)
{
	if (getenv("HARNESS_PY_COUNTS") == NULL) return;
	const int iPer = iTurns > 0 ? iTurns : 1;
	harnessLog("python callbacks over %d turns (total, per turn):\n", iPer);
	for (std::map<std::string, long>::const_iterator it = g_pyCallCounts.begin(); it != g_pyCallCounts.end(); ++it)
		harnessLog("  callback %-32s %10ld %10ld\n", it->first.c_str(), it->second, it->second / iPer);
	typedef int (*CountFn)(char*, int);
	HMODULE hDll = GetModuleHandleA("CvGameCoreDLL.dll");
	const CountFn pfn = hDll != NULL ? (CountFn)GetProcAddress(hDll, "HH_eventCounts") : NULL;
	if (pfn == NULL) return;
	static char buf[1 << 16];
	pfn(buf, sizeof(buf));
	char* p = buf;
	char szName[256];
	long n;
	int iRead;
	while (sscanf(p, "%255s %ld%n", szName, &n, &iRead) == 2) { harnessLog("  event    %-32s %10ld %10ld\n", szName, n, n / iPer); p += iRead; }
}

static void scenarioRun(const char* szScn, const char* szSpeed, const char* szHandicap, unsigned int uiSeed,
	int iTurns, const char* szOut, int iDetailEvery)
{
	char log[8192];
	const int iPlayers = HH_loadScenario(szScn, szSpeed, szHandicap, uiSeed, log, sizeof(log));
	harnessLog("scenario %s: %d players, seed %u\n%s", szScn, iPlayers, uiSeed, log);
	if (iPlayers <= 0) return;
	FILE* f = fopen(szOut, "w");
	if (f == NULL) { harnessLog("cannot write %s\n", szOut); return; }
	static std::vector<char> buf(1 << 20);
	HH_telemetryReset();
	int n = HH_telemetryHeader(&buf[0], (int)buf.size());
	fwrite(&buf[0], 1, n, f); fputc('\n', f); fflush(f);
	const int iStart = HH_gameTurn();
	int iLastTurn = -1;
	DWORD uiTurnStart = GetTickCount();
	long iUpdates = 0;
	for (;;)
	{
		const int iTurn = HH_gameTurn();
		if (iTurn != iLastTurn)
		{
			const DWORD uiNow = GetTickCount();
			const int iMs = iLastTurn < 0 ? 0 : (int)(uiNow - uiTurnStart);
			uiTurnStart = uiNow;
			iLastTurn = iTurn;
			iUpdates = 0;
			const int iDetail = (iDetailEvery > 0 && (iTurn - iStart) % iDetailEvery == 0) ? 1 : 0;
			for (;;)
			{
				n = HH_telemetry(&buf[0], (int)buf.size(), iDetail, iMs);
				if (n >= 0) break;
				buf.resize(-n * 2);
			}
			fwrite(&buf[0], 1, n, f); fputc('\n', f); fflush(f);
			maybeSnapshot(szOut, iTurn);
			if (iTurn - iStart >= iTurns || HH_gameState() != 0) break;
		}
		HH_update();
		if (++iUpdates > 100000) { harnessLog("turn %d did not finish after %ld updates\n", iTurn, iUpdates); break; }
	}
	fclose(f);
	printPythonCounts(HH_gameTurn() - iStart);
	harnessLog("RESULT scenario turn %d state %d\n", HH_gameTurn(), HH_gameState());
}

// A save split by sav2dat.py: load it, play iTurns turns and record telemetry.
// When a turn does not end, report the groups that keep it open.
static void saveRun(const char* szInit, const char* szGame, int iTurns, const char* szOut, int iDetailEvery, long iStuckUpdates)
{
	static char log[1 << 16];
	HH_infoCounts(log, sizeof(log));
	harnessLog("info counts: %s", log);
	const int iAlive = HH_loadSave(szInit, szGame, log, sizeof(log));
	harnessLog("save %s: result %d\n%s", szGame, iAlive, log);
	if (iAlive <= 0) return;
	// The harness cannot press "end turn": human seats play as AI (autorun).
	harnessLog("autoplay: %d human seat(s) handed to the AI\n", HH_autoPlayHumans(iTurns + 1));
	const std::string szState0 = std::string(szOut) + ".state0.json", szState1 = std::string(szOut) + ".state1.json";
	HH_dumpState(szState0.c_str());
	FILE* f = fopen(szOut, "w");
	if (f == NULL) { harnessLog("cannot write %s\n", szOut); return; }
	static std::vector<char> buf(1 << 20);
	HH_telemetryReset();
	int n = HH_telemetryHeader(&buf[0], (int)buf.size());
	fwrite(&buf[0], 1, n, f); fputc('\n', f); fflush(f);
	const int iStart = HH_gameTurn();
	int iLastTurn = -1;
	DWORD uiTurnStart = GetTickCount();
	long iUpdates = 0;
	harnessProfileReset();
	for (;;)
	{
		const int iTurn = HH_gameTurn();
		if (iTurn != iLastTurn)
		{
			const DWORD uiNow = GetTickCount();
			const int iMs = iLastTurn < 0 ? 0 : (int)(uiNow - uiTurnStart);
			harnessLog("turn %d (%d ms, %ld updates)\n", iTurn, iMs, iUpdates);
			uiTurnStart = uiNow;
			iLastTurn = iTurn;
			iUpdates = 0;
			const int iDetail = (iDetailEvery > 0 && (iTurn - iStart) % iDetailEvery == 0) ? 1 : 0;
			for (;;)
			{
				n = HH_telemetry(&buf[0], (int)buf.size(), iDetail, iMs);
				if (n >= 0) break;
				buf.resize(-n * 2);
			}
			fwrite(&buf[0], 1, n, f); fputc('\n', f); fflush(f);
			maybeSnapshot(szOut, iTurn);
			if (iTurn - iStart >= iTurns || HH_gameState() != 0) break;
		}
		HH_update();
		++iUpdates;
		if (iUpdates == iStuckUpdates || iUpdates == iStuckUpdates * 2 || iUpdates == iStuckUpdates * 4)
		{
			HH_stuckReport(log, sizeof(log));
			harnessLog("STUCK turn %d after %ld updates (%d ms):\n%s", iTurn, iUpdates, (int)(GetTickCount() - uiTurnStart), log);
		}
		if (iUpdates > iStuckUpdates * 4) { harnessLog("ABORT: turn %d did not end\n", iTurn); break; }
	}
	fclose(f);
	HH_dumpState(szState1.c_str());
	printPythonCounts(HH_gameTurn() - iStart);
	harnessLog("RESULT save turn %d state %d\n", HH_gameTurn(), HH_gameState());
	harnessProfileDump(stdout, 60);
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
	if (argc > 1 && strcmp(argv[1], "scenario") == 0)
	{
		// harness.exe scenario <file.scn> <GAMESPEED_...|-> <HANDICAP_...> <seed> <turns> <out.jsonl> [detail every N turns]
		if (argc < 8) { harnessLog("usage: harness.exe scenario <scn> <speed|-> <handicap> <seed> <turns> <out.jsonl> [detailEvery]\n"); return 2; }
		scenarioRun(argv[2], argv[3], argv[4], (unsigned int)strtoul(argv[5], NULL, 10), atoi(argv[6]), argv[7], argc > 8 ? atoi(argv[8]) : 10);
		return 0;
	}
	if (argc > 1 && strcmp(argv[1], "save") == 0)
	{
		// harness.exe save <file.init> <file.game> <turns> <out.jsonl> [detailEvery] [stuckUpdates]
		if (argc < 6) { harnessLog("usage: harness.exe save <init> <game> <turns> <out.jsonl> [detailEvery] [stuckUpdates]\n"); return 2; }
		saveRun(argv[2], argv[3], atoi(argv[4]), argv[5], argc > 6 ? atoi(argv[6]) : 10, argc > 7 ? atol(argv[7]) : 5000);
		return 0;
	}
	const char* scenario = argc > 1 ? argv[1] : "islands";
	const int turns = argc > 2 ? atoi(argv[2]) : 30;
	const bool plain = argc > 3 && strcmp(argv[3], "plain") == 0;
	if (strcmp(scenario, "islands") == 0) islandsScenario(turns, 17, plain);       // one sailing turn
	else if (strcmp(scenario, "mid") == 0) islandsScenario(turns, 21, plain);    // two sailing turns
	else if (strcmp(scenario, "far") == 0) islandsScenario(turns, 27, plain);    // beyond the settlement candidate range
	else if (strcmp(scenario, "xml") != 0) harnessLog("unknown scenario %s\n", scenario);
	return 0;
}
