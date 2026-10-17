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
UNITS = {
    'orders': 'commands the human gave (A lines); not outcomes',
    'distinct plots': 'plots, each counted once',
    'tiles at save': 'city tiles in the save dump',
    'cities at save': 'cities in the save dump',
    'units at save': 'units in the save dump',
    'food per tile': 'mean food of the tiles counted',
    'hammers per tile': 'mean hammers of the tiles counted',
    'commerce per tile': 'mean commerce of the tiles counted',
    'turns': 'game turns',
    'turn': 'a game turn',
    'battles': 'C/R line pairs',
    'cities': 'cities (K, Z or M lines)',
    'units built': 'U lines',
    'techs': 'techs',
    'deals': 'D lines',
    'gold': 'gold',
    'per mille': 'parts per thousand',
    'share': 'a fraction of n; n is required',
    'xml': 'a value read from records.json',
    'derived xml': 'a value computed from records.json by a rule cited in source',
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
                     reason=None, xml=None, value=None, fmt='{}', label=None):
        """Count every value of rows[col] (one column per group if group is given). show limits the
        values listed and requires reason; the rendered table states what was left out and why.
        value(rows) -> number replaces the count (for a mean per value). xml names the record type
        whose effects docs.py must render for every value counted."""
        self._check(id, unit, who, turn, source, None)
        keyf = col if callable(col) else (lambda r: r[col])
        allv = collections.Counter(keyf(r) for r in rows)
        vals = [v for v, _ in allv.most_common()]
        if show is not None:
            if not reason: raise FigureError(f'{id}: showing {len(show)} of {len(vals)} values needs a reason')
            missing = [v for v in show if v not in allv]
            if missing: raise FigureError(f'{id}: shown values not in the data: {missing}')
        shown = vals if show is None else list(show)
        gs = groups or (sorted({r[group] for r in rows}) if group else ['all'])
        body = []
        for v in shown:
            line = [v]
            for g in gs:
                sub = [r for r in rows if keyf(r) == v and (group is None or r[group] == g)]
                line.append(fmt.format(value(sub)) if value and sub else (len(sub) if not value else '-'))
            body.append(line)
        tot = ['all values'] + [len([r for r in rows if group is None or r[group] == g]) for g in gs]
        if value is None: body.append(tot)
        if xml: self._xml(id, xml, vals)
        self.figs[id] = dict(kind='table', head=[label or (col if isinstance(col, str) else 'value')] + gs, rows=body,
                             unit=unit, who=who, turn=str(turn), source=source, n=len(rows),
                             values_total=len(vals), values_shown=len(shown), reason=reason,
                             left_out=[v for v in vals if v not in shown], xml=xml, values=vals)
        return allv

    def save(self):
        with open(self.path, 'w') as f:
            json.dump({'inputs': self.inputs, 'figures': self.figs, 'xml': self.xml}, f, indent=1, default=str)
