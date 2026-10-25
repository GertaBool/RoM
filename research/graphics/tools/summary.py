"""Totals from textures.csv: by format, by folder, duplicates, uncompressed and oversized textures.
Loose files replace packed members of the same path, as the game does."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1])))
eff = {}
for r in rows:                                   # loose last, so it wins
    if r['source'] != 'loose': eff.setdefault(r['path'], r)
for r in rows:
    if r['source'] == 'loose': eff[r['path']] = r
E = list(eff.values()); MB = lambda x: x / 2**20
print('effective textures', len(E), 'total %.0f MB' % MB(sum(int(r['data']) for r in E)))
by = collections.Counter(); cnt = collections.Counter()
for r in E: by[r['fmt']] += int(r['data']); cnt[r['fmt']] += 1
print('by format:'); [print('  %-10s %5d  %7.1f MB' % (k, cnt[k], MB(v))) for k, v in by.most_common()]
top = collections.Counter()
for r in E: top['/'.join(r['path'].split('/')[:3])] += int(r['data'])
print('by folder:'); [print('  %-45s %7.1f MB' % (k, MB(v))) for k, v in top.most_common(15)]
groups = collections.defaultdict(list)
for r in E: groups[r['sha1']].append(r)
dup = [(g[0], len(g)) for g in groups.values() if len(g) > 1]
print('identical content under several paths: %d groups, %d extra copies, %.1f MB extra' % (
    len(dup), sum(n - 1 for _, n in dup), MB(sum(int(g['data']) * (n - 1) for g, n in dup))))
unc = [r for r in E if r['fmt'][0] in 'AX' or r['fmt'].startswith('TGA')]
print('uncompressed: %d, %.1f MB' % (len(unc), MB(sum(int(r['data']) for r in unc))))
nomip = [r for r in E if r['fmt'] != 'unreadable' and int(r['mips']) == 1 and max(int(r['w']), int(r['h'])) >= 256 and r['fmt'][:3] != 'TGA']
print('256px or larger without mipmaps: %d' % len(nomip))
big = sorted(E, key=lambda r: -int(r['data']))[:15]
print('largest:'); [print('  %7.2f MB %5sx%-5s %-6s mips %-2s %s' % (MB(int(r['data'])), r['w'], r['h'], r['fmt'], r['mips'], r['path'])) for r in big]
