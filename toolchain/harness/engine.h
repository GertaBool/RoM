// Engine side of the headless harness: implements the interfaces the game
// executable normally provides to CvGameCoreDLL.
#pragma once
#include <string>

struct HarnessConfig
{
	std::string root;      // directory containing Mods\<mod>\Assets and BTS\Assets
	std::string modName;   // "Mods\\Rise of Mankind\\"
	std::string logDir;    // where logMsg files go
};

class CvDLLUtilityIFaceBase;
CvDLLUtilityIFaceBase* harnessEngine(const HarnessConfig& cfg);
void harnessLog(const char* fmt, ...);
long harnessPathSearches();
