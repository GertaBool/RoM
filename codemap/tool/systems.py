#!/usr/bin/env python3
"""Sort every function of the map into a category and a system, and measure each.

usage: systems.py [--tsv <out file>]
Reads codemap/map. A function's category comes from its file (first matching rule of CATEGORIES); its system,
within the categories that hold game rules, from its name (first matching rule of SYSTEMS), otherwise from
its class. Prints, for every category and system: functions, lines, calls out and in (own functions only),
and the calls between categories. --tsv writes one row per function: id, category, system, name, file.
The rules are written out below; they sort by name and file, not by what the code does.
"""
import collections, csv, os, re, sys

M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'map')
csv.field_size_limit(1 << 30)
def read(n): return list(csv.DictReader(open(os.path.join(M, n), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))

CATEGORIES = [   # (category, rule on the file name); first match wins
    ('1 engine boundary', r'^(CvGameCoreDLL\.(cpp|h)|CvDLL\w*IFaceBase\.h|FDataStreamBase\.h|CvDLLEntity\.(cpp|h)|'
                          r'CvGameInterface\.cpp|CvDllTranslator\.cpp|CvDLLPython\.cpp)$'),
    ('2 infrastructure', r'^(FFreeList\w*\.h|LinkedList\.h|CvString\.h|FVariableSystem\.(h|inl)|FAssert\.cpp|'
                         r'FDialogTemplate\.cpp|CvRandom\.cpp|CvStructs\.(cpp|h)|CvMessageData\.(cpp|h)|CvMessageControl\.cpp)$'),
    ('3 rule data', r'^(CvInfos\.(cpp|h)|CvInfoWater\.cpp|CvXMLLoadUtility\w*\.(cpp|h)|CvGlobals\.(cpp|h)|'
                    r'CvArtFileMgr\.(cpp|h)|CvInitCore\.(cpp|h)|CvBugOptions\.cpp)$'),
    ('5 AI', r'^(\w+AI\.(cpp|h)|AI\w+\.h|BetterBTSAI\.cpp|ResearchPathPlan\.h|CvResearchGraph\.h)$'),
    ('6 interface', r'^(CvDLLWidgetData|CvGameTextMgr|CvDLLButtonPopup|CvPopupInfo|CvPopupReturn|CvTalkingHeadMessage|'
                    r'CvReplayInfo|CvReplayMessage|CvHallOfFameInfo|CvStatistics|CvDiploParameters)\.(cpp|h)$'),
    ('7 Python bridge', r'^(Cy\w+\.(cpp|h)|CvDllPythonEvents\.cpp|CvEventReporter\.cpp)$'),
    ('4 game state and rules', r'^(CvGame|CvMap|CvPlot|CvArea|CvPlotGroup|CvFractal|CvMapGenerator|CvPlayer|CvTeam|CvCity|'
                               r'CvUnit|CvSelectionGroup|CvDeal|CvGameCoreUtils)\.(cpp|h)$'),
]

SYSTEMS = [   # (system, rule on the function's name); for the game-state and AI categories; first match wins
    ('save and load', r'^(read|write)$'),
    ('turn and update', r'^(AI_)?(doTurn\w*|update|updateMoves|setTurnActive|doTurnUnits\w*|AI_doTurn\w*|AI_update|'
                        r'AI_unitUpdate|reset|init|uninit|AI_reset|AI_init|AI_uninit)$'),
    ('graphics paging', r'(Paging|Graphics|BulkReveal|DeferredReveal|pageGraphics|MemoryPressure)'),
    ('logging', r'(^log|Log$|warLog|WarLog|BBAI|Telemetry)'),
    ('random numbers', r'(Rand|Random)'),
    ('victory and score', r'(ictory|Score|score|Winner|Hall)'),
    ('movement and paths', r'(^path|Path|^step|Step)'),
    ('combat', r'(ombat|ttack|efend|efense|ithdraw|ollateral|ombard|irstStrike|amage|Heal|heal|ntercept|irStrike|'
               r'uke|lank|angeStrike|Odds|Strength|Retreat|Capture|Kill|Battle)'),
    ('espionage', r'(spionage|Spy|spy|Sabotage|Steal|Infiltrat)'),
    ('religion', r'(eligion|Holy|issionar|nquisition|Convert)'),
    ('corporations', r'(orporation|eadquarters|ranchise)'),
    ('diplomacy and war', r'(War|war|Peace|peace|ttitude|iplo|Deal|deal|Vassal|vassal|ribute|Alliance|OpenBorders|'
                          r'Contact|Denial|Memory|Trade(?!Route)|Surrender|Capitulat|Embargo|Treaty|Hegemon|Dogpile)'),
    ('votes and diplomacy victory', r'(Vote|vote|Secretary|Council|Resolution)'),
    ('civics', r'(ivic|narchy|evolution)'),
    ('research', r'(Tech|tech|esearch|Beaker)'),
    ('great people and golden age', r'(reatPeople|reatPerson|reatGeneral|olden)'),
    ('happiness and health', r'(appy|appiness|ngry|ealth|ontent|WarWeariness)'),
    ('economy', r'(Gold|gold|ommerce|aintenance|nflation|Tax|pkeep|Hurry|hurry|TradeRoute|Budget|Treasury|Cost|Price|Expense|Income)'),
    ('culture and borders', r'(ulture|Border|border|Owner|wnership|Influence)'),
    ('growth and food', r'(Food|food|rowth|tarv|Population|population|Pop$|Pop[A-Z])'),
    ('production and building', r'(roduction|Build|build|onstruct|Train|train|Create|create|Order|order|Queue|queue|'
                                r'Wonder|Project|Process)'),
    ('improvements, routes and bonuses', r'(mprovement|Route|route|Feature|feature|Worker|worker|errain|Bonus|bonus|Resource)'),
    ('promotions and experience', r'(romotion|xperience|Level|pgrade)'),
    ('events', r'(Event|Trigger|Quest)'),
    ('movement and paths', r'(Move|move|Path|path|Transport|ransport|Cargo|cargo|Load|load|Airlift|Paradrop|Teleport|'
                           r'Escort|Group|Join|Split|Mission|Land(ing)?$|Sea|Domain)'),
    ('visibility', r'(isib|eveal|nvisible|Fog|See|Sight)'),
    ('settlement', r'(Found|found|Settle|settle|Site|CitySite)'),
    ('map and geometry', r'(Plot|plot|Area|area|Map|map|Distance|distance|Adjacent|Coast|Water|River|Lake|XY|Direction)'),
]
CLASS_FALLBACK = {   # system when no name rule matches: by class
    'CvGame': 'game (other)', 'CvGameAI': 'game (other)', 'CvMap': 'map and geometry', 'CvPlot': 'map and geometry',
    'CvArea': 'map and geometry', 'CvPlotGroup': 'map and geometry', 'CvFractal': 'map and geometry',
    'CvMapGenerator': 'map and geometry', 'CvPlayer': 'player (other)', 'CvPlayerAI': 'player (other)',
    'CvTeam': 'team (other)', 'CvTeamAI': 'team (other)', 'CvCity': 'city (other)', 'CvCityAI': 'city (other)',
    'CvUnit': 'unit (other)', 'CvUnitAI': 'unit (other)', 'CvSelectionGroup': 'unit (other)',
    'CvSelectionGroupAI': 'unit (other)', 'CvDeal': 'diplomacy and war', '': 'shared helpers'}
AI_LAYER = {'CvUnitAI': 'unit AI', 'CvSelectionGroupAI': 'group AI', 'CvCityAI': 'city AI', 'CvPlayerAI': 'player AI',
            'CvTeamAI': 'team AI', 'CvGameAI': 'game AI'}


def classify(r):
    f = r['file']
    if re.match(r'(FFreeList\w*|CLinkList|CLLNode|FVariableSystem)\b', r['scope']):   # container templates, wherever instantiated
        return '2 infrastructure', 'containers, strings, asserts'
    cat = next((c for c, rx in CATEGORIES if re.search(rx, f)), '8 unassigned')
    name = r['name']
    if cat == '5 AI':
        layer = AI_LAYER.get(r['scope']) or ('AI policies (' + f[:-2] + ')' if re.match(r'AI\w+\.h$', f) else 'AI support')
        if layer in AI_LAYER.values():
            sysn = next((s for s, rx in SYSTEMS if re.search(rx, name)), None)
            return cat, f'{layer}: {sysn}' if sysn else layer
        return cat, layer
    if cat == '4 game state and rules':
        sysn = next((s for s, rx in SYSTEMS if re.search(rx, name)), None)
        return cat, sysn or CLASS_FALLBACK.get(r['scope'], r['scope'] + ' (other)')
    sub = {'1 engine boundary': lambda: 'DLL entry and exe interfaces',
           '2 infrastructure': lambda: ('network messages' if f.startswith(('CvMessage',)) else
                                        'random numbers' if f.startswith('CvRandom') else 'containers, strings, asserts'),
           '3 rule data': lambda: ('XML loading' if f.startswith('CvXMLLoad') else 'rule records (infos)' if f.startswith(('CvInfo', 'CvArtFile'))
                                   else 'globals and setup' if f.startswith(('CvGlobals', 'CvInitCore')) else 'BUG options'),
           '6 interface': lambda: ('tooltips and help' if f.startswith(('CvDLLWidgetData', 'CvGameTextMgr')) else
                                   'popups' if f.startswith(('CvDLLButtonPopup', 'CvPopup')) else 'messages, replays, statistics'),
           '7 Python bridge': lambda: ('events to Python' if f.startswith(('CvDllPythonEvents', 'CvEventReporter')) else
                                       'bindings (Python wrappers)')}
    return cat, sub.get(cat, lambda: 'unassigned')()


def main():
    F = {r['id']: r for r in read('functions.tsv') if r['definition'] == '1'}
    cs = {i: classify(r) for i, r in F.items()}
    lines = {i: (int(r['end']) - int(r['line']) + 1) if r['line'] and r['end'] else 0 for i, r in F.items()}
    out_, in_ = collections.Counter(), collections.Counter()
    cat_m = collections.Counter()
    pairs = set()
    for c in read('calls.tsv'):
        a, b = c['caller'], c['callee']
        if a in F and b in F and (a, b) not in pairs:
            pairs.add((a, b)); out_[cs[a]] += 1; in_[cs[b]] += 1; cat_m[(cs[a][0], cs[b][0])] += 1
    if '--tsv' in sys.argv:
        with open(sys.argv[sys.argv.index('--tsv') + 1], 'w', encoding='utf-8') as o:
            o.write('id\tcategory\tsystem\tname\tfile\n')
            for i in sorted(F, key=int):
                r = F[i]; o.write(f"{i}\t{cs[i][0]}\t{cs[i][1]}\t{(r['scope'] + '::' if r['scope'] else '') + r['name']}\t{r['file']}\n")
    by = collections.defaultdict(list)
    for i, k in cs.items(): by[k].append(i)
    cats = sorted({k[0] for k in by})
    print(f'functions {len(F)}; distinct caller-callee pairs between own functions {len(pairs)}')
    for cat in cats:
        ks = sorted((k for k in by if k[0] == cat), key=lambda k: -len(by[k]))
        n = sum(len(by[k]) for k in ks)
        print(f'\n{cat}: {n} functions, {sum(lines[i] for k in ks for i in by[k])} lines')
        for k in ks:
            ex = sorted(by[k], key=lambda i: -lines[i])[:3]
            print(f'  {k[1]:44} {len(by[k]):5} fn {sum(lines[i] for i in by[k]):7} lines  out {out_[k]:6} in {in_[k]:6}  e.g. ' +
                  ', '.join((F[i]['scope'] + '::' if F[i]['scope'] else '') + F[i]['name'] for i in ex))
    print('\ncalls between categories (distinct caller-callee pairs; row calls column)')
    print('from \\ to\t' + '\t'.join(c.split()[0] for c in cats))
    for a in cats: print(a + '\t' + '\t'.join(str(cat_m[(a, b)]) for b in cats))


if __name__ == '__main__':
    main()
