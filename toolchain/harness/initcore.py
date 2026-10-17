#!/usr/bin/env python3
"""Read the game setup from the CvInitCore block that sav2dat.py writes (<prefix>.init).

Follows CvInitCore::read in RoM's DLL field by field: game options, victories, and for
each player slot its custom names, civilization and leader index, team, handicap and slot
status.

usage: initcore.py <prefix>.init <CvEnums.h> <Assets/XML dir> [max_players=51]
"""
import json
import re
import struct
import sys


class Stream:
    def __init__(self, b):
        self.b, self.p = b, 0

    def i(self):
        v = struct.unpack_from('<i', self.b, self.p)[0]; self.p += 4; return v

    def ints(self, n):
        v = list(struct.unpack_from('<%di' % n, self.b, self.p)); self.p += 4 * n; return v

    def bools(self, n):
        v = list(self.b[self.p:self.p + n]); self.p += n; return [x != 0 for x in v]

    def s(self):  # narrow string
        n = self.i(); v = self.b[self.p:self.p + n].decode('latin-1'); self.p += n; return v

    def w(self):  # wide string
        n = self.i(); v = self.b[self.p:self.p + 2 * n].decode('utf-16-le', 'replace'); self.p += 2 * n; return v


def enum(header, name):
    t = open(header, encoding='latin-1').read()
    body = re.search(r'enum\s+(?:DllExport\s+)?%s\b[^{]*\{(.*?)\};' % name, t, re.S).group(1)
    body = re.sub(r'/\*.*?\*/|//[^\n]*', '', body, flags=re.S)
    names = [x.strip().split('=')[0].strip() for x in body.split(',')]
    names = [n for n in names if n and not n.startswith('NO_') and not n.startswith('#') and not n.startswith('NUM_')]
    return names


def xml_types(path):
    return re.findall(r'<Type>([^<]+)</Type>', open(path, encoding='latin-1').read())


def main(init, header, xmldir, max_players=51):
    st = Stream(open(init, 'rb').read())
    opts = enum(header, 'GameOptionTypes')
    mpopts = enum(header, 'MultiplayerOptionTypes')
    bug = bool(st.i() & 64)  # BUG_DLL_SAVE_FORMAT
    for _ in range(st.i()):
        st.s()
    out = {'type': st.i(), 'name': st.w()}
    st.w(); st.w()
    out['map'] = st.w()
    out['wbNoPlayers'] = st.bools(1)[0]
    out['worldsize'], out['climate'], out['sealevel'], out['era'], out['speed'], out['timer'], out['calendar'] = st.ints(7)
    ncmo = st.i(); st.i()
    st.ints(ncmo)
    out['victories'] = st.bools(st.i())
    if bug:
        st.i()  # number of game options, written for external tools
    out['options'] = [o for o, on in zip(opts, st.bools(len(opts))) if on]
    st.bools(len(mpopts)); st.bools(1)
    out['gameTurn'], out['maxTurns'], _, _ = st.ints(4)
    st.ints(2)
    # Custom names as set up for the game (leader name, civilization description, short
    # description, adjective). Empty or TXT_KEY_ values mean the XML default text.
    names, descs, shorts, adjs = ([st.w() for _ in range(max_players)] for _ in range(4))
    [st.w() for _ in range(max_players)]  # passwords
    [st.s() for _ in range(2 * max_players)]
    st.bools(max_players); [st.w() for _ in range(max_players)]
    civ, leader, team, hcap, color, art, slot, claim = (st.ints(max_players) for _ in range(8))
    # Civilization and leader indices stay numeric: RoM loads its XML in modules, so the
    # order of <Type> entries in one file is not the game's index order. Take the names
    # from the war log's P lines or the state dump. Handicaps and victories are single files.
    hcaps = [t for t in xml_types(xmldir + '/GameInfo/CIV4HandicapInfo.xml') if t.startswith('HANDICAP_')]
    vics = [t for t in xml_types(xmldir + '/GameInfo/CIV4VictoryInfo.xml') if t.startswith('VICTORY_')]
    out['victories'] = [v for v, on in zip(vics, out['victories']) if on]
    out['players'] = [{'id': i, 'leaderName': names[i], 'civDesc': descs[i], 'civShort': shorts[i],
                       'civAdjective': adjs[i], 'civ': civ[i], 'leader': leader[i], 'team': team[i],
                       'handicap': hcaps[hcap[i]] if 0 <= hcap[i] < len(hcaps) else hcap[i], 'slot': slot[i]}
                      for i in range(max_players) if civ[i] >= 0]
    out['bytesRead'] = st.p
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    print(json.dumps(main(a[0], a[1], a[2], *(int(x) for x in a[3:])), indent=1))
