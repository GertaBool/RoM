// Engine interfaces for running CvGameCoreDLL without the game executable.
//
// Path finding (FAStar) and XML access (FXml) are real implementations; they
// drive the DLL's own callbacks exactly as the engine does. Rendering, sound,
// networking, UI and Python are inert: Python reports itself uninitialized, so
// the DLL skips its Python events and callbacks.
#include "CvGameCoreDLL.h"
#include "FAStarNode.h"
#include "CvInitCore.h"
#include "CvDLLEntityIFaceBase.h"
#include "engine_stubs.h"
#include "engine.h"
#include "xmldom.h"
#include <cstdio>
#include <cstdarg>
#include <map>
#include <set>
#include <vector>
#include <algorithm>
#include <malloc.h>

namespace
{
	HarnessConfig g_cfg;
	long g_pathSearches = 0;

	bool fileExists(const std::string& p)
	{
		DWORD a = GetFileAttributesA(p.c_str());
		return a != INVALID_FILE_ATTRIBUTES && !(a & FILE_ATTRIBUTE_DIRECTORY);
	}

	std::string normalize(const char* path)
	{
		std::string s(path);
		for (size_t i = 0; i < s.size(); ++i) if (s[i] == '/') s[i] = '\\';
		std::string out;
		for (size_t i = 0; i < s.size(); ++i)
			if (!(s[i] == '\\' && !out.empty() && out[out.size() - 1] == '\\')) out += s[i];
		return out;
	}

	// The engine resolves asset paths in the mod first, then in Beyond the Sword.
	std::string resolveAsset(const char* path)
	{
		std::string rel = normalize(path);
		// The game does not apply res\Fonts\GameFont_GlobalDefines.xml: its saves
		// carry the unpadded religion and corporation counts (16 and 27, not the
		// file's 138). Without this the harness cannot read real saves.
		// HARNESS_GAMEFONT=1 loads the file anyway.
		if (strstr(rel.c_str(), "GameFont_GlobalDefines") != NULL)
		{
			const char* szOn = getenv("HARNESS_GAMEFONT");
			if (szOn == NULL || strcmp(szOn, "1") != 0) return std::string();
		}
		if (fileExists(rel)) return rel;
		std::string low = rel;
		for (size_t i = 0; i < low.size(); ++i) low[i] = (char)tolower(low[i]);
		if (low.compare(0, 7, "assets\\") == 0) rel = rel.substr(7);
		const std::string bases[2] = { g_cfg.root + "\\" + g_cfg.modName + "Assets\\", g_cfg.root + "\\BTS\\Assets\\" };
		for (int i = 0; i < 2; ++i)
			if (fileExists(bases[i] + rel)) return bases[i] + rel;
		return std::string();
	}
}

void harnessLog(const char* fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	vfprintf(stdout, fmt, ap);
	va_end(ap);
	fflush(stdout);
}

long harnessPathSearches() { return g_pathSearches; }

//////////////////////////////////////////////////////////////////////////////
// FAStar: A* over the map grid with the engine's callback protocol.
//////////////////////////////////////////////////////////////////////////////
class FAStar
{
public:
	FAStar() : cols(0), rows(0), wrapX(false), wrapY(false), destValid(0), heuristic(0), cost(0), valid(0),
		notifyChild(0), notifyList(0), data(0), startX(-1), startY(-1), destX(-1), destY(-1), info(0),
		cardinal(false), haveSearch(false), last(0) {}
	int cols, rows;
	bool wrapX, wrapY;
	FAPointFunc destValid;
	FAHeuristic heuristic;
	FAStarFunc cost, valid, notifyChild, notifyList;
	const void* data;
	std::vector<FAStarNode> nodes;
	std::vector<FAStarNode*> open;
	int startX, startY, destX, destY, info;
	bool cardinal, haveSearch;
	FAStarNode* last;

	FAStarNode* node(int x, int y)
	{
		if (wrapX) x = (x % cols + cols) % cols;
		if (wrapY) y = (y % rows + rows) % rows;
		if (x < 0 || y < 0 || x >= cols || y >= rows) return NULL;
		return &nodes[y * cols + x];
	}
	int h(int x, int y) const
	{
		return (heuristic && destX >= 0) ? heuristic(x, y, destX, destY) : 0;
	}
	void reset()
	{
		for (size_t i = 0; i < nodes.size(); ++i)
		{
			nodes[i].clear();
			nodes[i].m_iX = (int)i % cols;
			nodes[i].m_iY = (int)i / cols;
		}
		open.clear();
		haveSearch = false;
		last = NULL;
	}
	void addChild(FAStarNode* parent, FAStarNode* child)
	{
		for (int i = 0; i < parent->m_iNumChildren; ++i) if (parent->m_apChildren[i] == child) return;
		if (parent->m_iNumChildren < 8) parent->m_apChildren[parent->m_iNumChildren++] = child;
	}
	void removeChild(FAStarNode* parent, FAStarNode* child)
	{
		for (int i = 0; i < parent->m_iNumChildren; ++i)
			if (parent->m_apChildren[i] == child)
			{
				parent->m_apChildren[i] = parent->m_apChildren[--parent->m_iNumChildren];
				parent->m_apChildren[parent->m_iNumChildren] = NULL;
				return;
			}
	}
	// A cheaper route reached a closed node: push the improvement to its subtree.
	void propagate(FAStarNode* n, int depth)
	{
		if (depth > 4096) return;
		for (int i = 0; i < n->m_iNumChildren; ++i)
		{
			FAStarNode* c = n->m_apChildren[i];
			if (c->m_pParent != n) continue;
			int step = cost ? cost(n, c, 0, data, this) : 1;
			int g = n->m_iKnownCost + step;
			if (g < c->m_iKnownCost)
			{
				c->m_iKnownCost = g;
				c->m_iTotalCost = g + c->m_iHeuristicCost;
				if (notifyChild) notifyChild(n, c, ASNC_PARENTADD_UP, data, this);
				propagate(c, depth + 1);
			}
		}
	}
	FAStarNode* popBest()
	{
		size_t best = 0;
		for (size_t i = 1; i < open.size(); ++i)
		{
			if (open[i]->m_iTotalCost < open[best]->m_iTotalCost ||
				(open[i]->m_iTotalCost == open[best]->m_iTotalCost && open[i]->m_iHeuristicCost < open[best]->m_iHeuristicCost))
				best = i;
		}
		FAStarNode* n = open[best];
		open[best] = open.back();
		open.pop_back();
		return n;
	}

	bool generate(int sx, int sy, int dx, int dy, bool bCardinal, int iInfo, bool bReuse)
	{
		++g_pathSearches;
		if (nodes.empty()) return false;
		const bool bReusable = bReuse && haveSearch && sx == startX && sy == startY && iInfo == info && bCardinal == cardinal;
		startX = sx; startY = sy; destX = dx; destY = dy; info = iInfo; cardinal = bCardinal;
		last = NULL;
		const bool bHasDest = dx >= 0 && dy >= 0 && node(dx, dy) != NULL;
		if (bHasDest && destValid && !destValid(dx, dy, data, this))
		{
			haveSearch = false;
			return false;
		}
		FAStarNode* dest = bHasDest ? node(dx, dy) : NULL;
		if (!bReusable)
		{
			reset();
			startX = sx; startY = sy; destX = dx; destY = dy; info = iInfo; cardinal = bCardinal;
			FAStarNode* s = node(sx, sy);
			if (s == NULL) return false;
			if (valid && !valid(NULL, s, 0, data, this)) return false;
			s->m_iKnownCost = 0;
			s->m_iHeuristicCost = h(sx, sy);
			s->m_iTotalCost = s->m_iHeuristicCost;
			if (notifyChild) notifyChild(NULL, s, ASNC_INITIALADD, data, this);
			s->m_eFAStarListType = FASTARLIST_OPEN;
			open.push_back(s);
			if (notifyList) notifyList(NULL, s, ASNL_STARTOPEN, data, this);
			haveSearch = true;
		}
		else
		{
			if (dest != NULL && dest->m_eFAStarListType == FASTARLIST_CLOSED)
			{
				last = dest;
				return true;
			}
			for (size_t i = 0; i < open.size(); ++i)
			{
				open[i]->m_iHeuristicCost = h(open[i]->m_iX, open[i]->m_iY);
				open[i]->m_iTotalCost = open[i]->m_iKnownCost + open[i]->m_iHeuristicCost;
			}
		}

		static const int dxs[8] = { 0, 1, 1, 1, 0, -1, -1, -1 };
		static const int dys[8] = { 1, 1, 0, -1, -1, -1, 0, 1 };
		while (!open.empty())
		{
			FAStarNode* best = popBest();
			best->m_eFAStarListType = FASTARLIST_CLOSED;
			if (notifyList) notifyList(best->m_pParent, best, ASNL_ADDCLOSED, data, this);
			if (best == dest)
			{
				last = best;
				return true;
			}
			for (int d = 0; d < 8; ++d)
			{
				if (bCardinal && (dxs[d] != 0 && dys[d] != 0)) continue;
				FAStarNode* n = node(best->m_iX + dxs[d], best->m_iY + dys[d]);
				if (n == NULL || n == best->m_pParent) continue;
				if (valid && !valid(best, n, 0, data, this)) continue;
				const int step = cost ? cost(best, n, 0, data, this) : 1;
				const int g = best->m_iKnownCost + step;
				if (n->m_eFAStarListType == NO_FASTARLIST)
				{
					n->m_pParent = best;
					n->m_iKnownCost = g;
					n->m_iHeuristicCost = h(n->m_iX, n->m_iY);
					n->m_iTotalCost = g + n->m_iHeuristicCost;
					addChild(best, n);
					if (notifyChild) notifyChild(best, n, ASNC_NEWADD, data, this);
					n->m_eFAStarListType = FASTARLIST_OPEN;
					open.push_back(n);
					if (notifyList) notifyList(best, n, ASNL_ADDOPEN, data, this);
				}
				else if (g < n->m_iKnownCost)
				{
					if (n->m_pParent) removeChild(n->m_pParent, n);
					n->m_pParent = best;
					addChild(best, n);
					n->m_iKnownCost = g;
					n->m_iTotalCost = g + n->m_iHeuristicCost;
					if (n->m_eFAStarListType == FASTARLIST_OPEN)
					{
						if (notifyChild) notifyChild(best, n, ASNC_OPENADD_UP, data, this);
					}
					else
					{
						if (notifyChild) notifyChild(best, n, ASNC_CLOSEDADD_UP, data, this);
						propagate(n, 0);
					}
				}
			}
		}
		// Exhausted. A flood fill (no destination) has succeeded in visiting everything.
		return dest == NULL;
	}
};

class FAStarIFace : public S_CvDLLFAStarIFaceBase
{
public:
	FAStar* create() { return new FAStar(); }
	void destroy(FAStar*& p, bool) { delete p; p = NULL; }
	bool GeneratePath(FAStar* f, int sx, int sy, int dx, int dy, bool bCardinal, int iInfo, bool bReuse)
	{
		return f->generate(sx, sy, dx, dy, bCardinal, iInfo, bReuse);
	}
	void Initialize(FAStar* f, int iColumns, int iRows, bool bWrapX, bool bWrapY, FAPointFunc dv, FAHeuristic hf,
		FAStarFunc cf, FAStarFunc vf, FAStarFunc nc, FAStarFunc nl, void* pData)
	{
		f->cols = iColumns; f->rows = iRows; f->wrapX = bWrapX; f->wrapY = bWrapY;
		f->destValid = dv; f->heuristic = hf; f->cost = cf; f->valid = vf; f->notifyChild = nc; f->notifyList = nl;
		f->data = pData;
		f->nodes.assign(iColumns * iRows, FAStarNode());
		f->reset();
	}
	void SetData(FAStar* f, const void* p) { f->data = p; }
	FAStarNode* GetLastNode(FAStar* f) { return f->last; }
	bool IsPathStart(FAStar* f, int x, int y) { return f->startX == x && f->startY == y; }
	bool IsPathDest(FAStar* f, int x, int y) { return f->destX == x && f->destY == y; }
	int GetStartX(FAStar* f) { return f->startX; }
	int GetStartY(FAStar* f) { return f->startY; }
	int GetDestX(FAStar* f) { return f->destX; }
	int GetDestY(FAStar* f) { return f->destY; }
	int GetInfo(FAStar* f) { return f->info; }
	void ForceReset(FAStar* f) { f->reset(); }
};

//////////////////////////////////////////////////////////////////////////////
// FXml over the small DOM in xmldom.cpp.
//////////////////////////////////////////////////////////////////////////////
class FXml : public XDoc {};
class FXmlSchemaCache {};

class XmlIFace : public S_CvDLLXmlIFaceBase
{
	static bool isTrue(const std::wstring& w) { return w == L"1" || w == L"true" || w == L"TRUE" || w == L"True"; }
	static XNode* walk(XNode* n, const std::vector<std::string>& parts, size_t i)
	{
		if (i == parts.size()) return n;
		for (size_t k = 0; k < n->kids.size(); ++k)
			if (n->kids[k]->tag == parts[i])
			{
				XNode* r = walk(n->kids[k], parts, i + 1);
				if (r) return r;
			}
		return NULL;
	}
	static int countPath(XNode* n, const std::vector<std::string>& parts, size_t i)
	{
		if (i == parts.size()) return 1;
		int c = 0;
		for (size_t k = 0; k < n->kids.size(); ++k)
			if (n->kids[k]->tag == parts[i]) c += countPath(n->kids[k], parts, i + 1);
		return c;
	}
	static int countTag(XNode* n, const std::string& tag)
	{
		int c = (n->tag == tag) ? 1 : 0;
		for (size_t k = 0; k < n->kids.size(); ++k) c += countTag(n->kids[k], tag);
		return c;
	}
	static std::vector<std::string> split(const char* p)
	{
		std::vector<std::string> parts;
		std::string s(p), cur;
		for (size_t i = 0; i <= s.size(); ++i)
		{
			if (i == s.size() || s[i] == '/') { if (!cur.empty()) parts.push_back(cur); cur.clear(); }
			else cur += s[i];
		}
		return parts;
	}
	static void copyOut(TCHAR* dst, const std::string& s)
	{
		size_t n = std::min<size_t>(s.size(), 1023);
		memcpy(dst, s.c_str(), n);
		dst[n] = 0;
	}
public:
	FXml* CreateFXml(FXmlSchemaCache*) { return new FXml(); }
	void DestroyFXml(FXml*& x) { delete x; x = NULL; }
	void DestroyFXmlSchemaCache(FXmlSchemaCache*& c) { delete c; c = NULL; }
	FXmlSchemaCache* CreateFXmlSchemaCache() { return new FXmlSchemaCache(); }
	bool LoadXml(FXml* x, const TCHAR* file)
	{
		std::string p = resolveAsset(file);
		if (p.empty()) { harnessLog("XML missing: %s\n", file); return false; }
		std::string err;
		if (!x->load(p, err)) { harnessLog("XML parse error in %s: %s\n", p.c_str(), err.c_str()); return false; }
		return true;
	}
	bool Validate(FXml*, TCHAR*) { return true; }
	bool LocateNode(FXml* x, const TCHAR* path)
	{
		if (!x->root) return false;
		XNode* n = walk(x->root, split(path), 0);
		if (!n) return false;
		x->cur = n;
		return true;
	}
	bool LocateFirstSiblingNodeByTagName(FXml* x, TCHAR* tag)
	{
		XNode* p = x->cur->parent;
		if (!p) return false;
		for (size_t i = 0; i < p->kids.size(); ++i) if (p->kids[i]->tag == tag) { x->cur = p->kids[i]; return true; }
		return false;
	}
	bool LocateNextSiblingNodeByTagName(FXml* x, TCHAR* tag)
	{
		XNode* p = x->cur->parent;
		if (!p) return false;
		for (size_t i = x->cur->index + 1; i < p->kids.size(); ++i) if (p->kids[i]->tag == tag) { x->cur = p->kids[i]; return true; }
		return false;
	}
	bool NextSibling(FXml* x)
	{
		XNode* p = x->cur->parent;
		if (!p || x->cur->index + 1 >= (int)p->kids.size()) return false;
		x->cur = p->kids[x->cur->index + 1];
		return true;
	}
	bool PrevSibling(FXml* x)
	{
		XNode* p = x->cur->parent;
		if (!p || x->cur->index == 0) return false;
		x->cur = p->kids[x->cur->index - 1];
		return true;
	}
	bool SetToChild(FXml* x)
	{
		if (x->cur->kids.empty()) return false;
		x->cur = x->cur->kids[0];
		return true;
	}
	bool SetToChildByTagName(FXml* x, const TCHAR* tag)
	{
		for (size_t i = 0; i < x->cur->kids.size(); ++i) if (x->cur->kids[i]->tag == tag) { x->cur = x->cur->kids[i]; return true; }
		return false;
	}
	bool SetToParent(FXml* x)
	{
		if (!x->cur->parent) return false;
		x->cur = x->cur->parent;
		return true;
	}
	int GetLastNodeTextSize(FXml* x) { return (int)textOf(x->cur).size() + 1; }
	bool GetLastNodeText(FXml* x, TCHAR* t) { copyOut(t, narrow(textOf(x->cur))); return true; }
	bool GetLastNodeValue(FXml* x, std::string& s) { s = narrow(textOf(x->cur)); return true; }
	bool GetLastNodeValue(FXml* x, std::wstring& s) { s = textOf(x->cur); return true; }
	bool GetLastNodeValue(FXml* x, char* s) { copyOut(s, narrow(textOf(x->cur))); return true; }
	bool GetLastNodeValue(FXml* x, wchar* s)
	{
		std::wstring w = textOf(x->cur);
		size_t n = std::min<size_t>(w.size(), 1023);
		memcpy(s, w.c_str(), n * sizeof(wchar));
		s[n] = 0;
		return true;
	}
	bool GetLastNodeValue(FXml* x, bool* b) { *b = isTrue(textOf(x->cur)); return true; }
	bool GetLastNodeValue(FXml* x, int* i) { *i = (int)wcstol(textOf(x->cur).c_str(), 0, 10); return true; }
	bool GetLastNodeValue(FXml* x, float* f) { *f = (float)wcstod(textOf(x->cur).c_str(), 0); return true; }
	bool GetLastNodeValue(FXml* x, unsigned int* u) { *u = (unsigned int)wcstoul(textOf(x->cur).c_str(), 0, 10); return true; }
	bool GetLastLocatedNodeType(FXml* x, TCHAR* t)
	{
		std::map<std::string, std::string>::const_iterator it = x->types.find(x->cur->tag);
		strcpy(t, it == x->types.end() ? "" : it->second.c_str());
		return true;
	}
	bool IsLastLocatedNodeCommentNode(FXml*) { return false; }
	int NumOfElementsByTagName(FXml* x, TCHAR* tag)
	{
		if (strchr(tag, '/')) return countPath(x->root, split(tag), 0);
		return countTag(x->root, tag);
	}
	int NumOfChildrenByTagName(FXml* x, const TCHAR* tag)
	{
		int c = 0;
		for (size_t i = 0; i < x->cur->kids.size(); ++i) if (x->cur->kids[i]->tag == tag) ++c;
		return c;
	}
	int GetNumSiblings(FXml* x) { return x->cur->parent ? (int)x->cur->parent->kids.size() - 1 : 0; }
	int GetNumChildren(FXml* x) { return (int)x->cur->kids.size(); }
	bool GetLastLocatedNodeTagName(FXml* x, TCHAR* t) { copyOut(t, x->cur->tag); return true; }
	bool IsAllowXMLCaching() { return false; }
	void MapChildren(FXml*) {}
};

//////////////////////////////////////////////////////////////////////////////
// Python: uninitialized. The DLL skips events and callbacks in that state.
//////////////////////////////////////////////////////////////////////////////
// The engine writes the Python return value even where the DLL ignores the
// call's success flag (e.g. CvPlayer::calculatePreInflatedCosts reads an
// uninitialized long otherwise). Results are the defaults of BTS's
// CvGameUtils.py / RoM's RoMGameUtils.py; the call still reports "not run", so
// callers that check it use their own fallbacks.
struct HarnessArgs { std::vector<PyObject*> items; };
static long argInt(void* pArgs, size_t i)
{
	HarnessArgs* a = (HarnessArgs*)pArgs;
	if (a == NULL || i >= a->items.size() || a->items[i] == NULL) return 0;
	PyObject* o = a->items[i];
	const char* szType = ((const char**)o->ob_type)[3];   // tp_name
	return (szType && strcmp(szType, "int") == 0) ? ((long*)o)[2] : 0;
}
// Wrapped C++ objects (CyCity*, CyPlot*, CyUnit*) arrive as "ptr" objects from
// the Boost.Python stub; each Cy wrapper's only member is the game object.
static void* argGameObject(void* pArgs, size_t i)
{
	HarnessArgs* a = (HarnessArgs*)pArgs;
	if (a == NULL || i >= a->items.size() || a->items[i] == NULL) return NULL;
	PyObject* o = a->items[i];
	const char* szType = ((const char**)o->ob_type)[3];   // tp_name
	if (szType == NULL || strcmp(szType, "ptr") != 0) return NULL;
	void* pWrapper = ((void**)o)[2];
	return pWrapper ? *(void**)pWrapper : NULL;
}

// Implemented in the harness DLL build (HarnessScenario.cpp), mirroring the scripts.
extern "C" __declspec(dllimport) int HH_pyCalculateScore(int, int, int);
extern "C" __declspec(dllimport) int HH_pyCityCaptureGold(void*);
extern "C" __declspec(dllimport) int HH_pyPillageGold(void*, void*);

static long pythonDefault(const char* fxn, void* args)
{
	if (strcmp(fxn, "calculateScore") == 0) return HH_pyCalculateScore(argInt(args, 0), argInt(args, 1), argInt(args, 2));
	if (strcmp(fxn, "doCityCaptureGold") == 0) return HH_pyCityCaptureGold(argGameObject(args, 0));
	if (strcmp(fxn, "doPillageGold") == 0) return HH_pyPillageGold(argGameObject(args, 0), argGameObject(args, 1));
	static const char* aszMinusOne[] = { "getUpgradePriceOverride", "getUnitCostMod", "getBuildingCostMod",
		"getConscriptUnitType", "AI_chooseTech", "getFirstRecommendedTech", "getSecondRecommendedTech",
		"getRecommendedUnit", "getRecommendedBuilding", "getCityFoundValue" };
	static const char* aszTrue[] = { "isPlayerResearch", "canDeclareWar", "canRazeCity", "isVictory", "isVictoryTest",
		"showTechChooserButton", "showExamineCityButton" };
	for (size_t i = 0; i < sizeof(aszMinusOne) / sizeof(aszMinusOne[0]); ++i) if (strcmp(fxn, aszMinusOne[i]) == 0) return -1;
	for (size_t i = 0; i < sizeof(aszTrue) / sizeof(aszTrue[0]); ++i) if (strcmp(fxn, aszTrue[i]) == 0) return 1;
	if (strcmp(fxn, "getExperienceNeeded") == 0)
	{
		const long iLevel = argInt(args, 0);   // BTS: level^2 + 1 (leader modifiers not applied)
		return iLevel * iLevel + 1;
	}
	return 0;
}

class PythonIFace : public S_CvDLLPythonIFaceBase
{
public:
	bool isInitialized() { return false; }
	const char* getMapScriptModule() { return "harness"; }
	bool pythonUsingDefaultImpl() { return true; }
	PyObject* MakeFunctionArgs(void** args, int argc)
	{
		HarnessArgs* a = new HarnessArgs();   // leaked deliberately: the DLL never frees argument tuples itself
		for (int i = 0; i < argc; ++i) a->items.push_back((PyObject*)args[i]);
		return (PyObject*)a;
	}
	bool callFunction(const char*, const char*, void*) { return false; }
	bool callFunction(const char*, const char* fxn, void* arg, long* result) { if (result) *result = pythonDefault(fxn, arg); return false; }
	bool callFunction(const char*, const char*, void*, CvString* result) { if (result) *result = ""; return false; }
	bool callFunction(const char*, const char*, void*, CvWString* result) { if (result) *result = L""; return false; }
	bool callFunction(const char*, const char*, void*, std::vector<byte>* pList) { if (pList) pList->clear(); return false; }
	bool callFunction(const char*, const char*, void*, std::vector<int>* pList) { if (pList) pList->clear(); return false; }
	bool callFunction(const char*, const char*, void*, int*, int* piSize) { if (piSize) *piSize = 0; return false; }
	bool callFunction(const char*, const char*, void*, std::vector<float>* pList) { if (pList) pList->clear(); return false; }
	bool callPythonFunction(const char*, const char* fxn, int iArg, long* result) { if (result) *result = pythonDefault(fxn, NULL); (void)iArg; return false; }
};

class EntityIFace : public CvDLLEntityIFaceBase {};

//////////////////////////////////////////////////////////////////////////////
// Utility: the root interface handed to CvGlobals::setDLLIFace.
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
// Profiler: the DLL's PROFILE/PROFILE_FUNC scopes (in builds made with
// FP_PROFILE_ENABLE) call BeginSample/EndSample. Inclusive time counts only the
// outermost activation of a recursive sample; self time excludes child samples.
//////////////////////////////////////////////////////////////////////////////
namespace
{
	struct ProfStat { std::string name; double incl, self; unsigned long calls; int depth; ProfStat() : incl(0), self(0), calls(0), depth(0) {} };
	struct ProfFrame { ProfileSample* s; LONGLONG t0; double child; };
	std::map<ProfileSample*, ProfStat> g_prof;
	std::vector<ProfFrame> g_profStack;
	double g_profFreq = 0;
	LONGLONG profNow() { LARGE_INTEGER t; QueryPerformanceCounter(&t); return t.QuadPart; }
}

void harnessProfileReset() { g_prof.clear(); g_profStack.clear(); }

void harnessProfileDump(FILE* f, int iTop)
{
	// HARNESS_PROFILE_SORT=incl sorts by inclusive time (callers), default self time.
	const char* szSort = getenv("HARNESS_PROFILE_SORT");
	const bool bIncl = szSort != NULL && strcmp(szSort, "incl") == 0;
	std::vector<std::pair<double, ProfStat*> > v;
	for (std::map<ProfileSample*, ProfStat>::iterator it = g_prof.begin(); it != g_prof.end(); ++it) v.push_back(std::make_pair(bIncl ? it->second.incl : it->second.self, &it->second));
	std::sort(v.begin(), v.end());
	std::reverse(v.begin(), v.end());
	fprintf(f, "%10s %10s %12s  %s\n", "self ms", "incl ms", "calls", "sample");
	for (size_t i = 0; i < v.size() && (int)i < iTop; ++i)
		fprintf(f, "%10.1f %10.1f %12lu  %s\n", v[i].second->self * 1000, v[i].second->incl * 1000, v[i].second->calls, v[i].second->name.c_str());
}

class Utility : public S_CvDLLUtilityIFaceBase
{
public:
	void BeginSample(ProfileSample* pSample)
	{
		if (g_profFreq == 0) { LARGE_INTEGER q; QueryPerformanceFrequency(&q); g_profFreq = (double)q.QuadPart; }
		ProfFrame fr = { pSample, profNow(), 0 };
		g_profStack.push_back(fr);
		ProfStat& st = g_prof[pSample];
		if (st.name.empty()) st.name = pSample->Name;
		++st.calls;
		++st.depth;
	}
	void EndSample(ProfileSample* pSample)
	{
		if (g_profStack.empty() || g_profStack.back().s != pSample) return;
		const ProfFrame fr = g_profStack.back();
		g_profStack.pop_back();
		const double dt = (profNow() - fr.t0) / g_profFreq;
		ProfStat& st = g_prof[pSample];
		st.self += dt - fr.child;
		if (--st.depth == 0) st.incl += dt;
		if (!g_profStack.empty()) g_profStack.back().child += dt;
	}
	EntityIFace entity;
	S_CvDLLInterfaceIFaceBase iface;
	S_CvDLLEngineIFaceBase engine;
	S_CvDLLIniParserIFaceBase ini;
	S_CvDLLSymbolIFaceBase symbol;
	S_CvDLLFeatureIFaceBase feature;
	S_CvDLLRouteIFaceBase route;
	S_CvDLLPlotBuilderIFaceBase plotBuilder;
	S_CvDLLRiverIFaceBase river;
	FAStarIFace fastar;
	XmlIFace xml;
	S_CvDLLFlagEntityIFaceBase flag;
	PythonIFace python;
	std::map<std::string, FILE*> logs;

	CvDLLEntityIFaceBase* getEntityIFace() { return &entity; }
	CvDLLInterfaceIFaceBase* getInterfaceIFace() { return &iface; }
	CvDLLEngineIFaceBase* getEngineIFace() { return &engine; }
	CvDLLIniParserIFaceBase* getIniParserIFace() { return &ini; }
	CvDLLSymbolIFaceBase* getSymbolIFace() { return &symbol; }
	CvDLLFeatureIFaceBase* getFeatureIFace() { return &feature; }
	CvDLLRouteIFaceBase* getRouteIFace() { return &route; }
	CvDLLPlotBuilderIFaceBase* getPlotBuilderIFace() { return &plotBuilder; }
	CvDLLRiverIFaceBase* getRiverIFace() { return &river; }
	CvDLLFAStarIFaceBase* getFAStarIFace() { return &fastar; }
	CvDLLXmlIFaceBase* getXMLIFace() { return &xml; }
	CvDLLFlagEntityIFaceBase* getFlagEntityIFace() { return &flag; }
	CvDLLPythonIFaceBase* getPythonIFace() { return &python; }

	void delMem(void* p) { free(p); }
	void* newMem(size_t n) { return malloc(n ? n : 1); }
	void delMem(void* p, const char*, int) { free(p); }
	void* newMem(size_t n, const char*, int) { return malloc(n ? n : 1); }
	void delMemArray(void* p, const char*, int) { free(p); }
	void* newMemArray(size_t n, const char*, int) { return malloc(n ? n : 1); }
	void* reallocMem(void* a, unsigned int n, const char*, int) { return realloc(a, n); }
	unsigned int memSize(void* a) { return (unsigned int)_msize(a); }
	void clearVector(std::vector<int>& v) { v.clear(); }
	void clearVector(std::vector<byte>& v) { v.clear(); }
	void clearVector(std::vector<float>& v) { v.clear(); }

	bool isGameActive() { return true; }
	int getCurrentLanguage() const { return 0; }
	bool isModularXMLLoading() const { return false; }
	int getMillisecsPerTurn() { return 0; }
	float getSecsPerTurn() { return 0.0f; }
	int getTurnsPerSecond() { return 1000; }
	int getTurnsPerMinute() { return 60000; }
	CvWString getMapScriptName() { return L"harness"; }

	void initGlobals()
	{
		GC.setPathFinder(fastar.create());
		GC.setInterfacePathFinder(fastar.create());
		GC.setStepFinder(fastar.create());
		GC.setRouteFinder(fastar.create());
		GC.setBorderFinder(fastar.create());
		GC.setAreaFinder(fastar.create());
		GC.setPlotGroupFinder(fastar.create());
	}

	void NiTextOut(const TCHAR* s) { harnessLog("[NiTextOut] %s\n", s); }
	void MessageBox(const TCHAR* t, const TCHAR* c) { harnessLog("[MessageBox] %s: %s\n", c, t); }
	bool GetAutorun() { return true; }

	bool cacheRead(CvCacheObject*, const TCHAR*) { return false; }
	bool cacheWrite(CvCacheObject*) { return false; }
	void destroyCache(CvCacheObject*& p) { p = NULL; }
	bool fileManagerEnabled() { return false; }

	void logMsg(const TCHAR* file, const TCHAR* buf, bool, bool)
	{
		std::string name(file);
		FILE*& f = logs[name];
		if (!f) f = fopen((g_cfg.logDir + "\\" + name).c_str(), "w");
		if (f) { fputs(buf, f); size_t n = strlen(buf); if (!n || buf[n - 1] != '\n') fputc('\n', f); fflush(f); }
	}

	std::map<std::wstring, std::wstring> text;
	CvWString getText(CvWString szIDTag, ...)
	{
		std::map<std::wstring, std::wstring>::const_iterator it = text.find(szIDTag.c_str());
		return it == text.end() ? szIDTag : CvWString(it->second.c_str());
	}
	CvWString getObjectText(CvWString szIDTag, uint, bool) { return szIDTag; }
	void addText(const TCHAR* tag, const wchar* s, const wchar*, const wchar*)
	{
		std::string t(tag);
		text[std::wstring(t.begin(), t.end())] = s;
	}
	uint getNumForms(CvWString) { return 1; }
	WorldSizeTypes getWorldSize() { return GC.getInitCore().getWorldSize(); }

	void enumerateFiles(std::vector<CvString>& files, const char* pattern)
	{
		files.clear();
		(void)pattern;   // modular XML loading is off: MLF lists module files itself
	}
	void enumerateModuleFiles(std::vector<CvString>& files, const CvString&, const CvString&, const CvString&, bool)
	{
		files.clear();
	}
	const char* getModName(bool) const { return g_cfg.modName.c_str(); }
};

CvDLLUtilityIFaceBase* harnessEngine(const HarnessConfig& cfg)
{
	g_cfg = cfg;
	static Utility* s_util = new Utility();
	return s_util;
}
