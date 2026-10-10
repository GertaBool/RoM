#!/usr/bin/env python3
"""Reproduce source-level defects without modifying or running the BTS DLL.

Usage: python3 deep_source_probes.py /path/to/rise-of-mankind
Exit zero means the documented observations reproduced, NOT that the game passed.
C++ fragments are extracted from the pinned source and compiled with UBSan.
Adapters supply only the contracts documented in each probe's evidence record.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import types
import xml.etree.ElementTree as ET

COMMIT = "1ab4f99a76adb530f86b278390ab8139ef41cc96"
NATIVE = "Assets/CvGameCoreDLL/"


def masked(text):
    pattern = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*[\s\S]*?\*/|//[^\n]*'
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m[0]), text)


def block(text, signature):
    start = text.index(signature)
    clean = masked(text)
    begin = clean.index("{", start)
    depth = 1
    end = begin + 1
    while depth:
        depth += (clean[end] == "{") - (clean[end] == "}")
        end += 1
    return text[start:end]


def xml(path):
    root = ET.parse(path).getroot()
    for node in root.iter():
        node.tag = node.tag.split("}")[-1]
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("deep-findings.json"))
    args = parser.parse_args()
    root = args.source.resolve()
    revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if revision != COMMIT:
        parser.error("Review is pinned to " + COMMIT)
    files = {}
    fragments = []

    def read(path):
        if path not in files:
            raw = (root / path).read_bytes()
            committed = subprocess.check_output(["git", "-C", str(root), "show", COMMIT + ":" + path])
            if raw != committed:
                raise RuntimeError("Modified reviewed source: " + path)
            files[path] = {"sha256": hashlib.sha256(raw).hexdigest(),
                           "text": raw.decode("latin1").replace("\r\n", "\n")}
        return files[path]["text"]

    def evidence(path, fragment):
        source = read(path)
        start = source.index(fragment)
        item = {"path": path, "start_line": source.count("\n", 0, start) + 1,
                "line_count": len(fragment.splitlines()),
                "normalized_fragment_sha256": hashlib.sha256(fragment.encode()).hexdigest()}
        fragments.append(item)
        return fragment

    def compile_run(name, source):
        with tempfile.TemporaryDirectory(prefix="rom-probe-") as folder:
            cpp = Path(folder) / (name + ".cpp")
            binary = Path(folder) / name
            cpp.write_text(source)
            subprocess.run(["g++", "-std=c++03", "-Wall", "-Wextra", "-Werror",
                            "-fsanitize=undefined", "-fno-sanitize-recover=undefined",
                            "-I", str(root / NATIVE), str(cpp), "-o", str(binary)], check=True)
            return subprocess.check_output([str(binary)], text=True).strip()

    ppath = NATIVE + "CvPlayerAI.cpp"
    upath = NATIVE + "CvUnitAI.cpp"
    player, unit = read(ppath), read(upath)
    findings = []

    # Canal expression is the only nonzero-return expression in the full method.
    canal = block(player, "int CvPlayerAI::AI_getPlotCanalValue(")
    expression = re.search(r"return 10 \* std::min\(0,.*?;", canal)[0]
    evidence(ppath, expression)
    assert set(re.findall(r"return ([^;]+);", masked(canal))) == {
        "0", "10 * std::min(0, pSecondWaterArea->getNumTiles() - 2)"}
    rows = compile_run("canal", r'''
#include <algorithm>
#include <iostream>
struct Area {int tiles; int getNumTiles() const {return tiles;}};
int score(int tiles){Area area={tiles};Area* pSecondWaterArea=&area;
EXPRESSION
}
int main(){int cases[]={1,2,3,10,100,1000};for(int i=0;i<6;++i)
 std::cout<<cases[i]<<" "<<score(cases[i])<<"\n";}
'''.replace("EXPRESSION", expression))
    canal_cases = [dict(zip(("second_water_area_tiles", "value"), map(int, row.split())))
                   for row in rows.splitlines()]
    assert all(c["value"] <= 0 for c in canal_cases)
    fort = block(unit, "bool CvUnitAI::AI_fortTerritory(")
    gate = fort[fort.index("int iValue = 0;"):fort.index("int iBestTempBuildValue")]
    evidence(upath, gate)
    assert "if (iValue > 0)" in gate
    findings.append({"id": "D01", "title": "Canal-only fort value cannot enter candidate evaluation",
                     "evidence_level": "compiled_source_expression_and_inspected_consumer",
                     "cases": canal_cases,
                     "boundary": "Prior canal guards only return zero; no pathfinding or game execution needed for the nonpositive-value conclusion."})

    # Execute the unchanged candidate-build loop with legal synthetic builds.
    build_loop = evidence(upath, block(fort, "for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)"))
    output = compile_run("fort", r'''
#include <climits>
#include <iostream>
#define MAX_INT INT_MAX
#define FAssertMsg(x,y) ((void)0)
typedef int BuildTypes;
typedef int ImprovementTypes;
enum {NO_IMPROVEMENT=-1,NO_BUILD=-1};
struct CvPlot {};
struct Build {int time;int getImprovement()const{return 0;}int getTime()const{return time;}};
struct Improvement {bool isActsAsCity()const{return true;}int getDefenseModifier()const{return 50;}};
struct Globals {Build builds[2];Improvement imp;
 int getNumBuildInfos()const{return 2;}
 const Build& getBuildInfo(int i)const{return builds[i];}
 const Improvement& getImprovementInfo(int)const{return imp;}} GC;
bool canBuild(CvPlot*,BuildTypes){return true;}
void run(int first,int second,int strategic){GC.builds[0].time=first;GC.builds[1].time=second;
 CvPlot plot;CvPlot* pLoopPlot=&plot;int iValue=strategic;
 int iBestTempBuildValue=MAX_INT;BuildTypes eBestTempBuild=NO_BUILD;
LOOP
 std::cout<<first<<" "<<second<<" "<<strategic<<" "<<GC.builds[eBestTempBuild].time<<" "<<iValue<<"\n";
}
int main(){run(1000,2000,500);run(2000,1000,500);run(1000,2000,10);}
'''.replace("LOOP", build_loop))
    fort_cases = [dict(zip(("first_time", "second_time", "location_value", "selected_time", "remaining_value"),
                           map(int, row.split()))) for row in output.splitlines()]
    assert [c["selected_time"] for c in fort_cases] == [2000, 2000, 2000]
    assert [c["remaining_value"] for c in fort_cases] == [4, 9, 4]
    findings.append({"id": "D02", "title": "Fort build loop loses location utility and depends on candidate order",
                     "evidence_level": "compiled_actual_candidate_loop", "cases": fort_cases,
                     "boundary": "Adapter gives both builds equal defensive properties and legal status. Real fort upgrades differ in defense; this probe establishes overwritten utility, order dependence and inverse-time minimization, not a universal preference for the basic fort."})

    # Deserialize reset statements and the actual hysteresis block, without a fake save parser.
    reset_function = block(player, "void CvPlayerAI::read(")
    reset = reset_function[reset_function.index("m_iAIAgenda ="):reset_function.index("uint uiFlag=0;")]
    reset = evidence(ppath, reset)
    agenda = block(player, "void CvPlayerAI::AI_updateAgenda(")
    hysteresis = evidence(ppath, agenda[agenda.index("AIAgendaTypes eOldAgenda"):agenda.index("m_iAIAgenda = eBestAgenda;")])
    header = read(NATIVE + "CvPlayerAI.h")
    agenda_enum = block(header, "enum AIAgendaTypes") + ";"
    write = block(player, "void CvPlayerAI::write(")
    assert "m_iAIAgenda" not in masked(write) and "m_iAINavalPriority" not in masked(write)
    definitions_path = "Assets/XML/GlobalDefinesAlt.xml"
    read(definitions_path)
    definitions = {n.findtext("DefineName"): n.findtext("iDefineIntVal")
                   for n in xml(root / definitions_path).findall("Define")}
    minimum = int(definitions["AI_AGENDA_SWITCH_MIN_MARGIN"])
    percentage = int(definitions["AI_AGENDA_SWITCH_PERCENT"])
    variables = sorted(set(re.findall(r"\bm_\w+", reset)))
    vector_names = set(re.findall(r"(m_\w+)\.clear\(\)", reset))
    declarations = []
    for name in variables:
        if name in vector_names:
            declarations.append("std::vector<int> " + name + ";")
        elif name == "m_aiAIAgendaBudget":
            declarations.append("int " + name + "[NUM_AI_BUDGET_TYPES];")
        else:
            declarations.append("int " + name + ";")
    read(NATIVE + "AIHierarchyPolicy.h")
    output = compile_run("agenda", r'''
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
#include "AIHierarchyPolicy.h"
ENUM
enum {AI_BAD_START_NONE=0,NUM_AI_BUDGET_TYPES=5};
DECLARATIONS
int range(int n,int lo,int hi){return std::max(lo,std::min(n,hi));}
struct Globals {int getDefineINT(const char* name)const{
 return std::strcmp(name,"AI_AGENDA_SWITCH_MIN_MARGIN")==0?MINIMUM:PERCENTAGE;}} GC;
void loadReset(){RESET}
int select(){bool bEmergency=false,bBadStartDirective=false;
 int aiScore[NUM_AI_AGENDA_TYPES]={0};aiScore[AI_AGENDA_EXPAND_LAND]=1000;aiScore[AI_AGENDA_SCIENCE]=1100;
 AIAgendaTypes eBestAgenda=AI_AGENDA_SCIENCE;int iBestScore=1100;
HYSTERESIS
 return eBestAgenda;
}
int main(){m_iAIAgenda=AI_AGENDA_EXPAND_LAND;m_iAINavalPriority=900;
 std::cout<<select()<<" "<<AIHierarchyPolicy::preferSeaSettlement(100,100,m_iAINavalPriority)<<"\n";
 loadReset();std::cout<<select()<<" "<<AIHierarchyPolicy::preferSeaSettlement(100,100,m_iAINavalPriority)<<" "<<m_iAINavalPriority<<"\n";
}
'''.replace("ENUM", agenda_enum).replace("DECLARATIONS", "\n".join(declarations))
        .replace("MINIMUM", str(minimum)).replace("PERCENTAGE", str(percentage))
        .replace("RESET", reset).replace("HYSTERESIS", hysteresis))
    before, after = [list(map(int, row.split())) for row in output.splitlines()]
    assert before == [2, 1] and after == [7, 0, 0], output
    findings.append({"id": "D03", "title": "Loading discards agenda hysteresis and derived strategic intent",
                     "evidence_level": "compiled_actual_reset_and_hysteresis_blocks_plus_production_policy",
                     "before": {"agenda_after_review": "EXPAND_LAND", "prefer_sea": True, "naval_priority": 900},
                     "after_reset": {"agenda_after_review": "SCIENCE", "prefer_sea": False, "naval_priority": 0},
                     "fixture_scores": {"EXPAND_LAND": 1000, "SCIENCE": 1100},
                     "xml_hysteresis": {"minimum_margin": minimum, "percent": percentage},
                     "boundary": "Controlled branch inputs; no full save file or engine continuation. Direct getters do not rebuild intent. Exact in-game divergence timing still needs a matching DLL trace."})

    # Real base XML graph, exact native helper. Three unknown technologies share a prerequisite.
    tech_path = "Assets/XML/Technologies/CIV4TechInfos.xml"
    read(tech_path)
    techs = {n.findtext("Type"): n for n in xml(root / tech_path).findall(".//TechInfo")}
    names = ["TECH_AGRICULTURE", "TECH_ANIMAL_HUSBANDRY", "TECH_THE_WHEEL", "TECH_CHARIOTRY"]
    unknown = set(names[1:])
    ids = {name: i for i, name in enumerate(names)}
    # Agriculture and every prerequisite outside the selected unknown set are known.
    rows = []
    for name in names:
        node = techs[name]
        ands = [ids.get(x.text, 0) for x in node.findall("AndPreReqs/PrereqTech")]
        ors = [ids.get(x.text, 0) for x in node.findall("OrPreReqs/PrereqTech")]
        rows.append((int(node.findtext("iCost")), ands, ors))
    helper = evidence(ppath, block(player, "int AI_cachedTechPathLength("))
    initialization = []
    for i, (cost, ands, ors) in enumerate(rows):
        initialization.append("GC.tech[%d].cost=%d;" % (i, cost))
        initialization += ["GC.tech[%d].a[%d]=%d;" % (i, j, value) for j, value in enumerate(ands)]
        initialization += ["GC.tech[%d].o[%d]=%d;" % (i, j, value) for j, value in enumerate(ors)]
    output = compile_run("research", r'''
#include <algorithm>
#include <climits>
#include <iostream>
#include <vector>
#define MAX_INT INT_MAX
#define __int64 long long
typedef int TechTypes;
enum {NO_TECH=-1};
struct Tech {int cost,a[8],o[8];Tech():cost(0){for(int i=0;i<8;++i)a[i]=o[i]=-1;}
 int getPrereqAndTechs(int i)const{return a[i];}int getPrereqOrTechs(int i)const{return o[i];}};
struct Globals {Tech tech[4];int getNUM_AND_TECH_PREREQS()const{return 8;}
 int getNUM_OR_TECH_PREREQS()const{return 8;}const Tech& getTechInfo(int i)const{return tech[i];}} GC;
struct Team {bool isHasTech(int i)const{return i==0;}int getResearchCost(int i)const{return GC.tech[i].cost;}} team;
#define GET_TEAM(x) team
struct CvPlayerAI {bool isResearchingTech(int)const{return false;}int getTeam()const{return 0;}};
HELPER
int main(){INIT
 CvPlayerAI player;std::vector<int> cache(4,-1);std::vector<char> visiting(4,0);
 std::cout<<AI_cachedTechPathLength(player,3,false,cache,visiting)<<" ";
 cache.assign(4,-1);visiting.assign(4,0);
 std::cout<<AI_cachedTechPathLength(player,3,true,cache,visiting)<<"\n";
}
'''.replace("HELPER", helper).replace("INIT", "\n".join(initialization)))
    steps, cost = map(int, output.split())
    unique_cost = sum(int(techs[n].findtext("iCost")) for n in unknown)
    assert (steps, cost, unique_cost) == (4, 268, 218)
    findings.append({"id": "D04", "title": "Research path heuristic counts shared prerequisites repeatedly",
                     "evidence_level": "compiled_actual_helper_with_base_xml_dependencies",
                     "unknown_techs": names[1:], "known_prerequisites": "All others in this fixture",
                     "reported_steps": steps, "distinct_required_techs": len(unknown),
                     "reported_cost": cost, "distinct_base_cost": unique_cost,
                     "boundary": "Uses base XML costs as mocked team research costs; runtime modifiers and module overlays are excluded. This is a heuristic distortion, not a claim that research charges the treasury twice."})

    # Execute original Python methods under narrow adapters; these bodies use no
    # Python-2-specific arithmetic, so Python 3 does not alter the tested behavior.
    py_path = "Assets/Python/RoMEventManager.py"
    source = read(py_path)
    begin = source.index("\t\tself.asBuildingUpgradeLine_Upgrade_Name =")
    end = source.index("\t\tself.iBUILDING_CRUSADE =", begin)
    initialization = evidence(py_path, source[begin:end])
    method_start = source.index("\tdef onLoadGame(")
    method_end = source.index("\tdef onGameStart(", method_start)
    method = evidence(py_path, source[method_start:method_end])
    names_to_ids = {}

    def type_id(name):
        return names_to_ids.setdefault(name, len(names_to_ids))

    context = types.SimpleNamespace(getInfoTypeForString=type_id,
                                    getBuildingInfo=lambda i: i, getNumBuildingInfos=lambda: 1000)
    namespace = {"gc": context, "CvUtil": types.SimpleNamespace(findInfoTypeNum=lambda _f, _n, name: type_id(name))}
    method_body = "\n".join(line[1:] if line.startswith("\t") else line
                            for line in method.splitlines()) + "\n"
    exec(compile(method_body, py_path, "exec"), namespace)
    profiler = types.SimpleNamespace(initialize=lambda _: None)
    manager = types.SimpleNamespace(augustusAIProfiler=profiler, settlementTrainingProfiler=profiler)
    exec(compile(textwrap.dedent(initialization), py_path, "exec"), {"self": manager})
    lengths = []
    for _ in range(3):
        namespace["onLoadGame"](manager, ())
        lengths.append(len(manager.aiBuildingUpgradeLine_Upgrade_InfoTypeNum))
    assert lengths[0] > 0 and lengths == [lengths[0] * i for i in (1, 2, 3)]
    findings.append({"id": "D05", "title": "Repeated OnLoad appends duplicate building-upgrade pairs",
                     "evidence_level": "executed_actual_python_initializer_and_OnLoad_method",
                     "pair_counts_after_load": lengths,
                     "unique_pairs": len(set(zip(manager.aiBuildingUpgradeLine_Upgrade_InfoTypeNum,
                                                  manager.aiBuildingUpgradeLine_Obsolete_InfoTypeNum))),
                     "boundary": "Same manager instance; profiler and info lookups are adapters. Confirms growth and duplicate work, not an accumulating gameplay bonus."})

    contracts = []
    # Full native lookup body: preserve its generation-checked and slot-only paths.
    handle_path = NATIVE + "FFreeListTrashArray.h"
    handles = read(handle_path)
    lookup = evidence(handle_path, block(handles, "T* FFreeListTrashArray<T>::getAt("))
    defines = "\n".join(line for line in handles.splitlines() if line.startswith("#define FLTA_"))
    output = compile_run("handles", r'''
#include <cassert>
#include <cstddef>
#include <iostream>
DEFINES
namespace FFreeList {enum {INVALID_INDEX=-1};}
struct Entity {int id;int getID()const{return id;}};
template<class T> struct FFreeListTrashArray {
 struct Node {T* pData;}; Node* m_pArray;int m_iLastIndex;
 T* getAt(int iID)const;
};
template<class T>
LOOKUP
int main(){Entity first={8192},replacement={24576};
 FFreeListTrashArray<Entity>::Node nodes[1];nodes[0].pData=&first;
 FFreeListTrashArray<Entity> list;list.m_pArray=nodes;list.m_iLastIndex=0;
 std::cout<<(list.getAt(8192)==&first)<<" "<<(list.getAt(0)==&first)<<" ";
 nodes[0].pData=&replacement;
 std::cout<<(list.getAt(8192)==NULL)<<" "<<(list.getAt(0)==&replacement)<<" "
          <<(list.getAt(24576)==&replacement)<<" "<<(list.getAt(-1)==NULL)<<"\n";
}
'''.replace("DEFINES", defines).replace("LOOKUP", lookup))
    assert output == "1 1 1 1 1 1", output
    contracts.append({"id": "C01", "title": "Native full-ID lookup rejects stale generations; slot-only lookup accepts current occupant",
                      "evidence_level": "compiled_actual_getAt_body",
                      "initial_id": 8192, "replacement_id": 24576, "slot": 0,
                      "all_six_checks_passed": True,
                      "boundary": "Adapter replaces a slot occupant directly; native allocation/removal, overflow and save I/O are not executed."})

    event_path = "Assets/Python/BUG/BugEventManager.py"
    event_source = read(event_path)
    start = event_source.index("\tdef _handleDefaultEvent(")
    end = event_source.index("\tdef _handleConsumableEvent(", start)
    default_event = evidence(event_path, event_source[start:end])
    default_event = "\n".join(line[1:] if line.startswith("\t") else line
                              for line in default_event.splitlines()) + "\n"

    class LegacyDict(dict):
        def has_key(self, key):
            return key in self

    balance = [1000]
    callback_trace = []

    def mutate_then_raise(_args):
        balance[0] += 10
        callback_trace.append({"handler": "first", "gold": balance[0]})
        raise RuntimeError("probe exception after mutation")

    def observe_and_mutate(_args):
        callback_trace.append({"handler": "second_observes", "gold": balance[0]})
        balance[0] += 5

    event_ns = {"BugUtil": types.SimpleNamespace(trace=lambda *_: callback_trace.append({"exception_logged": True}))}
    exec(compile(default_event, event_path, "exec"), event_ns)
    event_manager = types.SimpleNamespace(EventHandlerMap=LegacyDict(probe=[mutate_then_raise, observe_and_mutate]))
    event_ns["_handleDefaultEvent"](event_manager, "probe", ())
    assert balance[0] == 1015
    assert callback_trace == [{"handler": "first", "gold": 1010}, {"exception_logged": True},
                              {"handler": "second_observes", "gold": 1010}]
    contracts.append({"id": "C02", "title": "Ordinary BUG dispatch preserves partial effects and continues after a handler exception",
                      "evidence_level": "executed_actual_default_dispatch_method",
                      "trace": callback_trace, "final_gold": balance[0],
                      "boundary": "Synthetic handlers and a dict.has_key compatibility adapter; no native callback bridge or Python 2 interpreter execution."})

    result = {"source_commit": COMMIT, "binary_executed": False,
              "meaning_of_success": "All documented defect observations reproduced",
              "compiler": subprocess.check_output(["g++", "-dumpfullversion"], text=True).strip(),
              "compiler_flags": ["-std=c++03", "-Wall", "-Wextra", "-Werror", "-fsanitize=undefined", "-fno-sanitize-recover=undefined"],
              "source_files": {path: data["sha256"] for path, data in sorted(files.items())},
              "extracted_fragments": fragments, "findings": findings, "verified_contracts": contracts}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for finding in findings:
        print(finding["id"] + ": reproduced — " + finding["title"])
    for contract in contracts:
        print(contract["id"] + ": verified — " + contract["title"])


if __name__ == "__main__":
    main()
