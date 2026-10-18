"""Figure registry: every figure an analysis document may state, with what it counts.

A figure is written only through Registry.fig or Registry.census_table, which refuse a
figure without a unit from UNITS, an actor (who), a turn and a source. census_table counts
every value of a column; showing fewer needs a stated reason, which the rendered document
prints. Documents take their numbers from the registry by id (tools/docs.py); a number typed
into a document is an error there.

Registry file (JSON): {"inputs": {path: sha256}, "figures": {id: {...}}}. docs.py check
recomputes the input hashes, so a registry older than its tables is an error.
"""
import collections, hashlib, json, os

# A unit names one kind of thing. There is deliberately no unit for a sum of food, hammers
# and commerce: they are counted apart.
# Scale (Stevens' levels, as in the Formelsammlung's "metrische, ordinale oder nominale"
# Realisierungen): a mean is defined only on a metric scale; counts are metric.
UNITS = {
    'orders': ('metric', 'commands the human gave (A lines); not outcomes'),
    'distinct plots': ('metric', 'plots, each counted once'),
    'tiles at save': ('metric', 'city tiles in the save dump'),
    'cities at save': ('metric', 'cities in the save dump'),
    'units at save': ('metric', 'units in the save dump'),
    'food per tile': ('metric', 'mean food of the tiles counted'),
    'hammers per tile': ('metric', 'mean hammers of the tiles counted'),
    'commerce per tile': ('metric', 'mean commerce of the tiles counted'),
    'turns': ('metric', 'a number of game turns'),
    'turn': ('ordinal', 'a game turn: ordered; differences are turns, a mean of turns is not used'),
    'battles': ('metric', 'C/R line pairs'),
    'cities': ('metric', 'cities (K, Z or M lines)'),
    'units built': ('metric', 'U lines'),
    'techs': ('metric', 'techs'),
    'deals': ('metric', 'D lines'),
    'gold': ('metric', 'gold'),
    'per mille': ('metric', 'parts per thousand'),
    'share': ('metric', 'a fraction of n; n is required'),
    'rank': ('ordinal', 'a position in an order'),
    'yield per turn': ('metric', 'food, hammers or commerce per turn of a whole empire (CvPlayer::calculateTotalYield, calculateTotalCommerce)'),
    'AI value': ('ordinal', 'a score the AI code computes to compare options (AI_civicValue, AI_techValue); the code compares and scales it, it has no unit'),
    'category': ('nominal', 'a type name; only counted, never averaged'),
    'xml': ('nominal', 'a value read from records.json, as written there'),
    'derived xml': ('metric', 'a value computed from records.json by a rule cited in source'),
    'seconds': ('metric', 'wall-clock time of one run'),
    'bytes': ('metric', 'size'),
    'lines': ('metric', 'lines of a file'),
}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
NONE_VALUES = {'-', 'NONE', ''}   # "no improvement", "no feature": counted, no record


class FigureError(ValueError):
    pass


class Registry:
    def __init__(self, path, inputs, records=None):
        """inputs: files the figures are computed from. Paths outside the repository are stored
        as absolute paths and checked only where they exist. records: records.json, loaded."""
        self.path = path
        base = os.path.dirname(os.path.abspath(path))
        self.inputs = {}
        for p in inputs:
            a = os.path.abspath(p)
            self.inputs[os.path.relpath(a, base) if a.startswith(REPO) else a] = sha(p)
        self.figs, self.records, self.xml = {}, records, {}
        # The command that wrote the registry, so check_all.py --reproduce can run it again.
        import sys
        # Paths inside the repository are written as '@repo/<path>', everything else as given.
        rel = lambda a: '@repo/' + os.path.relpath(os.path.abspath(a), REPO) if (
            os.path.exists(a) or a == path) and os.path.abspath(a).startswith(REPO) else a
        self.command = [rel(a) for a in sys.argv]

    def _xml(self, id, rtype, vals):
        if self.records is None: raise FigureError(f'{id}: xml={rtype} needs records')
        tab = self.records[rtype]
        pre = {'ImprovementInfo': 'IMPROVEMENT_', 'BuildInfo': 'BUILD_', 'UnitInfo': 'UNIT_', 'BuildingInfo': 'BUILDING_',
               'FeatureInfo': 'FEATURE_', 'TerrainInfo': 'TERRAIN_', 'BonusInfo': 'BONUS_', 'RouteInfo': 'ROUTE_',
               'PromotionInfo': 'PROMOTION_', 'CivicInfo': 'CIVIC_', 'TechInfo': 'TECH_'}.get(rtype, '')
        store = self.xml.setdefault(rtype, {})
        for v in vals:
            if v in NONE_VALUES: continue
            k = v if v in tab else pre + v
            if k not in tab: raise FigureError(f'{id}: {v} has no {rtype} record')
            store[v] = tab[k]

    def _check(self, id, unit, who, turn, source, n):
        if id in self.figs: raise FigureError(f'{id}: defined twice')
        if unit not in UNITS: raise FigureError(f'{id}: unit {unit!r} not in figlib.UNITS')
        for k, v in (('who', who), ('turn', turn), ('source', source)):
            if v is None or str(v).strip() == '': raise FigureError(f'{id}: {k} is missing')
        if unit == 'share' and not n: raise FigureError(f'{id}: a share needs n')

    def fig(self, id, value, unit, who, turn, source, n=None):
        """One number (or short text) with what it counts."""
        self._check(id, unit, who, turn, source, n)
        self.figs[id] = dict(kind='value', value=value, unit=unit, who=who, turn=str(turn), source=source, n=n)
        return value

    def census_table(self, id, rows, col, unit, who, turn, source, group=None, groups=None, show=None,
                     reason=None, xml=None, value=None, fmt='{}', label=None, stat=None):
        """Count every value of rows[col] (one column per group if group is given). show limits the
        values listed and requires reason; the rendered table states what was left out and why.
        value(rows) -> number replaces the count (for a mean per value). xml names the record type
        whose effects docs.py must render for every value counted."""
        self._check(id, unit, who, turn, source, None)
        if value is not None:
            if stat not in ('mean', 'median'): raise FigureError(f'{id}: a value function needs stat="mean" or "median"')
            if stat == 'mean' and UNITS[unit][0] != 'metric': raise FigureError(f'{id}: a mean of {unit} ({UNITS[unit][0]} scale)')
        keyf = col if callable(col) else (lambda r: r[col])
        gkey = (lambda r: r[group]) if group else (lambda r: 'all')
        # One pass: the cells of the contingency table K^T G (K, G one-hot), sparse, with the
        # rows of each cell kept only when a value function needs them.
        allv, cells, members, gsize = collections.Counter(), collections.Counter(), collections.defaultdict(list), collections.Counter()
        for r in rows:
            v, g = keyf(r), gkey(r)
            allv[v] += 1; cells[v, g] += 1; gsize[g] += 1
            if value: members[v, g].append(r)
        # The classes of the key partition the rows (each row has one value), so the cells sum
        # to the number of rows. A failure means the key or the grouping is wrong.
        if sum(allv.values()) != len(rows) or sum(cells.values()) != len(rows):
            raise FigureError(f'{id}: counts do not sum to the {len(rows)} rows')
        vals = [v for v, _ in allv.most_common()]
        if show is not None:
            if not reason: raise FigureError(f'{id}: showing {len(show)} of {len(vals)} values needs a reason')
            missing = [v for v in show if v not in allv]
            if missing: raise FigureError(f'{id}: shown values not in the data: {missing}')
        shown = vals if show is None else list(show)
        gs = groups or (sorted(gsize) if group else ['all'])
        if groups and set(gsize) - set(groups):
            raise FigureError(f'{id}: groups in the data but not in the table: {sorted(set(gsize) - set(groups))}')
        body = []
        for v in shown:
            if value: body.append([v] + [fmt.format(value(members[v, g])) if members[v, g] else '-' for g in gs])
            else: body.append([v] + [cells[v, g] for g in gs])
        tot = ['all values'] + [gsize[g] for g in gs]
        if value is None: body.append(tot)
        if xml: self._xml(id, xml, vals)
        self.figs[id] = dict(kind='table', head=[label or (col if isinstance(col, str) else 'value')] + gs, rows=body,
                             unit=unit, who=who, turn=str(turn), source=source, n=len(rows),
                             values_total=len(vals), values_shown=len(shown), reason=reason,
                             left_out=[v for v in vals if v not in shown], xml=xml, values=vals, stat=stat or 'count')
        return allv

    def result_table(self, id, head, rows, unit, who, turn, source, over, n=None, xml=None, xml_vals=None):
        """A table whose rows are a declared, complete list (`over`: the models or classes evaluated),
        not a census. Every row's first cell must be the matching member of `over`, in order.
        xml names the record type of the types the table lists (xml_vals); docs.py then requires their effects."""
        self._check(id, unit, who, turn, source, n)
        if xml: self._xml(id, xml, xml_vals)
        if [r[0] for r in rows] != list(over): raise FigureError(f'{id}: rows {[r[0] for r in rows]} are not {list(over)}')
        if any(len(r) != len(head) for r in rows): raise FigureError(f'{id}: a row does not match the header')
        self.figs[id] = dict(kind='table', head=list(head), rows=[list(r) for r in rows], unit=unit, who=who, turn=str(turn),
                             source=source, n=n, values_total=len(rows), values_shown=len(rows), reason=None,
                             left_out=[], xml=xml, values=list(over), stat='result',
                             xml_values=sorted(set(xml_vals)) if xml else None)

    def save(self):
        with open(self.path, 'w') as f:
            json.dump({'command': self.command, 'inputs': self.inputs, 'figures': self.figs, 'xml': self.xml}, f, indent=1, default=str)
