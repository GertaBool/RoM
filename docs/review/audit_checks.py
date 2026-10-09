"""Reproduce narrowly scoped review findings using source fragments, not BTS.

No game files are changed. Fakes implement only the contracts named below.
An exit status of zero means the recorded findings were reproduced, not that
the game passed its regression suite.
"""
import ast
import difflib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import types
import xml.etree.ElementTree as ET

ROOT = Path('/workspace/rise-of-mankind')
OUT = Path(__file__).resolve().parent
results = {}

# Compile the actual simultaneous-team selection block with minimal team fakes.
game = (ROOT/'Assets/CvGameCoreDLL/CvGame.cpp').read_text()
start = game.index('\telse if (isSimultaneousTeamTurns())',game.index('void CvGame::doTurn()'))
brace = game.index('{', start)
depth = 1
end = brace + 1
while depth:
    depth += (game[end] == '{') - (game[end] == '}')
    end += 1
block = game[brace:end]
cpp = r'''
#include <cstdio>
enum {MAX_TEAMS=3};
typedef int TeamTypes;
struct CvTeam {bool alive, active; bool isAlive(){return alive;}
 void setTurnActive(bool v){active=v;} int getAliveCount(){return 1;}};
CvTeam teams[MAX_TEAMS];
#define GET_TEAM(x) teams[x]
#define FAssert(x) ((void)0)
int getNumGameTurnActive(){return 1;}
int main(){for(int mask=1; mask<8; ++mask){
 for(int j=0;j<3;++j){teams[j].alive=(mask&(1<<j))!=0;teams[j].active=false;}
 int iI;
''' + block + r'''
 int selected=-1;for(int j=0;j<3;++j)if(teams[j].active)selected=j;
 std::printf("%d %d\n", mask, selected);
}}
'''
with tempfile.TemporaryDirectory() as folder:
    source=Path(folder)/'selection.cpp'; binary=Path(folder)/'selection'
    source.write_text(cpp)
    subprocess.run(['g++','-std=c++03','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)],check=True)
    lines=subprocess.check_output([str(binary)],text=True).splitlines()
    cases=[]
    for line in lines:
        mask,actual=map(int,line.split())
        expected=next(i for i in range(3) if mask&(1<<i))
        cases.append(dict(alive_mask=mask,expected_first_alive=expected,actual=actual))
    assert sum(c['actual']!=c['expected_first_alive'] for c in cases)==3
    results['simultaneous_team_selection']={'evidence':'Actual source block compiled against minimal team interface; 3 of 7 nonempty three-team configurations activate no team.', 'cases':cases}

# Execute the unchanged Python handler in isolation. The fake city's -1 result
# matches CyCity::getNumActiveBuilding when its native city pointer is null.
source=(ROOT/'Assets/Python/RoMEventManager.py').read_text()
method=source[source.index('\tdef onBeginPlayerTurn('):source.index('\tdef onBuildingBuilt(')]
method='\n'.join(line[1:] if line.startswith('\t') else line for line in method.splitlines())+'\n'
class City:
    def __init__(self,bank): self.bank=bank
    def getNumActiveBuilding(self,_): return self.bank
class Player:
    def __init__(self,ids): self.cities={i:City(int(i==ids[-1])) for i in ids};self.gold=1000
    def getTeam(self): return 0
    def getNumCities(self): return len(self.cities)
    def getCity(self,i): return self.cities.get(i,City(-1))
    def getGold(self): return self.gold
    def changeGold(self,n): self.gold+=n
class Context:
    def __init__(self,player): self.player=player
    def getPlayer(self,_): return self.player
    def getTeam(self,_): return types.SimpleNamespace(isHasTech=lambda tech:tech==1)
    def getBuildingInfo(self,_): return types.SimpleNamespace(getObsoleteTech=lambda:3)
handler=types.SimpleNamespace(iTECH_APPLIED_ECONOMICS=1,iTECH_FUNDAMENTALISM=2,
    iBUILDING_WORLD_BANK=4,augustusAIProfiler=types.SimpleNamespace(recordTurn=lambda *args:None),
    settlementTrainingProfiler=types.SimpleNamespace(recordTurn=lambda *args:None))
bank_cases=[]
for ids in [(0,1),(0,2)]:
    player=Player(ids); namespace={'gc':Context(player),'true':True,'false':False}
    exec(compile(method,'RoMEventManager.onBeginPlayerTurn','exec'),namespace)
    namespace['onBeginPlayerTurn'](handler,(25,0))
    bank_cases.append(dict(city_ids=ids,bank_city=ids[-1],initial_gold=1000,actual_gold=player.gold,expected_gold=1010))
assert [c['actual_gold'] for c in bank_cases]==[1010,1000]
results['sparse_city_ids']={'evidence':'Actual onBeginPlayerTurn handler with narrow engine-contract fakes; control and sparse-ID case.', 'cases':bank_cases}

# XML dispatch is into CvRandomEventInterface, not arbitrary Python modules.
py=(ROOT/'Assets/Python/EntryPoints/CvRandomEventInterface.py').read_text()
functions=set(re.findall(r'^def\s+(\w+)\s*\(',py,re.M))
exports=[]
visited=set()
def visit_config(name):
    if name in visited:return
    visited.add(name)
    path=ROOT/'Assets/Config'/(name+'.xml')
    if not path.exists():return
    root=ET.parse(path).getroot()
    for e in root.iter():
        if e.tag=='load':visit_config(e.get('mod') or e.get('name'))
        if e.tag=='export' and e.get('to')=='CvRandomEventInterface':
            name=e.get('as') or e.get('function')
            module=e.get('module') or root.get('module')
            matches=list((ROOT/'Assets/Python').rglob(module+'.py'))
            assert len(matches)==1
            content=matches[0].read_text()
            assert re.search(r'^def\s+'+re.escape(e.get('function'))+r'\s*\(',content,re.M)
            functions.add(name)
            exports.append(dict(name=name,module=module,configuration=str(path.relative_to(ROOT))))
visit_config('init')
missing=[]
for path in [ROOT/'Assets/XML/Events/CIV4EventInfos.xml',ROOT/'Assets/XML/Events/CIV4EventTriggerInfos.xml']:
    root=ET.parse(path).getroot()
    for record in root.iter():
        kids=list(record)
        types_=[e.text for e in kids if e.tag.split('}')[-1]=='Type']
        if not types_:continue
        for e in kids:
            tag=e.tag.split('}')[-1]; value=(e.text or '').strip()
            if tag.startswith('Python') and value and value not in functions:
                missing.append(dict(path=str(path.relative_to(ROOT)),type=types_[0],tag=tag,function=value,
                    similar_names=difflib.get_close_matches(value,functions,n=2,cutoff=.8)))
results['event_callback_bindings']={'evidence':'Exact, case-sensitive definitions in CvRandomEventInterface plus verified exports from recursively loaded BUG configs; no whole-module execution.', 'resolved_exports':exports,'missing':missing}
assert len(missing)==15

profiler=(ROOT/'Assets/Python/SettlementTrainingProfiler.py').read_text()
trainer=(ROOT/'Tools/SettlementModel/train_pairwise_ranker.py').read_text()
documentation=(ROOT/'Tools/SettlementModel/Docs/SETTLEMENT_MODEL_TRAINING.md').read_text()
assert 'SCHEMA_VERSION = 4' in profiler and 'requires schema-v4' in trainer and 'SettlementCandidates-v3.csv' in documentation
results['telemetry_documentation']={'profiler_schema':4,'trainer_requires_schema':4,'documented_example_schema':3}
(OUT/'audit-findings.json').write_text(json.dumps(results,indent=2))
print('REPRODUCED: team-selection gap in 3/7 nonempty team masks; sparse-ID World Bank omission; %d unresolved event bindings; telemetry documentation v3/v4 mismatch.' % len(missing))
print('These are scoped source diagnostics. The BTS executable was not run.')
