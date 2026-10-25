#!/usr/bin/env python3
"""Tables from the graphics runs of the headless harness (toolchain/harness/README.md, Graphics),
460 AD autosave, turns 356 to 359.

usage: harness_counts.py engine <zero.log> <off.log> <on.log> <nograph.log> > engine-calls.tsv
       harness_counts.py billboard <run.log> <map file> > billboard-ad460.json

engine:    calls into the engine interfaces and dirty bits set (HARNESS_PY_COUNTS) over three turns,
           with the calls made while setting graphics up (the 0-turn run, column setup) removed;
           columns paging off, paging on, no graphics. Create calls are inflated: the harness's
           stubs return no object, so the DLL creates again where the game would keep one.
billboard: the lines of the diagnostic billboard build (research/graphics/tools/harness-billboard.patch):
           rebuilds, the code that set each billboard or layout dirty (named from the DLL's map file
           with addr2sym.py, which needs llvm-undname), and the timed scoreboard calls.
"""
import json, os, re, subprocess, sys

DIRTY = ['SelectionCamera', 'Fog', 'GlobeLayer', 'GlobeInfo', 'Waypoints', 'PercentButtons', 'MiscButtons',
         'PlotListButtons', 'SelectionButtons', 'CitizenButtons', 'ResearchButtons', 'Event', 'Center', 'GameData',
         'Score', 'TurnTimer', 'Help', 'MinimapSection', 'SelectionSound', 'Cursor', 'CityInfo', 'UnitInfo', 'Popup',
         'CityScreen', 'InfoPane', 'Flag', 'HighlightPlot', 'ColoredPlots', 'BlockadedPlots', 'Financial_Screen',
         'Foreign_Screen', 'Soundtrack', 'Domestic_Advisor', 'Espionage_Advisor', 'Advanced_Start']   # CvEnums.h InterfaceDirtyBits


def counts(path):
    d = {}
    for l in open(path, errors='replace'):
        m = re.match(r'\s+(engine|dirty)\s+(\S+)\s+(\d+)\s+(\d+)', l)
        if m:
            name = m.group(2) if m.group(1) == 'engine' else 'dirty bit ' + DIRTY[int(m.group(2))] + '_DIRTY_BIT'
            d[name] = int(m.group(3))
    return d


def engine(zero, off, on, nog):
    z, a, b, c = counts(zero), counts(off), counts(on), counts(nog)
    rows = sorted(set(a) | set(b), key=lambda k: -(a.get(k, 0) - z.get(k, 0)))
    print('call\tsetup\tpaging_off\tpaging_on\tno_graphics')
    for k in rows:
        print(f'{k}\t{z.get(k, 0)}\t{a.get(k, 0) - z.get(k, 0)}\t{b.get(k, 0) - z.get(k, 0)}\t{c.get(k, 0)}')


def names(mapfile, addrs):
    tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'addr2sym.py')
    out = subprocess.run([sys.executable, tool, mapfile] + addrs, capture_output=True, text=True).stdout.splitlines()
    return [re.sub(r'^\S+ \+\S+ (public: |private: |protected: )?', '', l) for l in out]


def billboard(log, mapfile):
    text = open(log, errors='replace').read().replace('\r', '')
    res = {}
    m = re.search(r'billboard frames (\d+), with a rebuild (\d+), rebuilds (\d+), most in one frame (\d+), cities rebuilt (\d+), text time ([\d.]+) s', text)
    res['billboard'] = dict(zip(['updates', 'updates_with_a_rebuild', 'rebuilds', 'most_in_one_update', 'cities_rebuilt', 'dll_text_seconds'],
                                [int(x) for x in m.groups()[:5]] + [float(m.group(6))]))
    res['layout_rebuilds'] = int(re.search(r'layout rebuilds (\d+)', text).group(1))
    m = re.search(r'visibility dirty: other teams (\d+) \(clean before (\d+)\), active team (\d+) \(clean before (\d+)\)', text)
    if m:
        res['visibility_setter'] = dict(zip(['other_teams_calls', 'other_teams_from_clean', 'active_team_calls', 'active_team_from_clean'], map(int, m.groups())))
    for kind in ('infodirty', 'layoutdirty'):
        rows = sorted(((a, int(n)) for a, n in re.findall(rf'^{kind} (\w+) (\d+)', text, re.M)), key=lambda r: -r[1])
        res[kind + '_setters'] = [dict(setter=s, count=n) for (a, n), s in zip(rows, names(mapfile, [a for a, n in rows]))]
    m = re.search(r'scoreboard rows (\d+), war-trade denials asked (\d+); ms per redraw: attitude ([\d.]+), talk\+worst enemy ([\d.]+), WHEOOH ([\d.]+), trade network ([\d.]+), revealed cities ([\d.]+)', text)
    res['scoreboard_dll_ms_per_redraw'] = dict(zip(['rows', 'war_trade_denials', 'attitude', 'willing_to_talk_and_worst_enemy', 'wheooh', 'trade_network', 'revealed_cities'],
                                                   [int(m.group(1)), int(m.group(2))] + [float(x) for x in m.groups()[2:]]))
    json.dump(res, sys.stdout, indent=1); print()


if __name__ == '__main__':
    if sys.argv[1] == 'engine': engine(*sys.argv[2:6])
    elif sys.argv[1] == 'billboard': billboard(*sys.argv[2:4])
