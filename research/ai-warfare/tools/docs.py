#!/usr/bin/env python3
"""Render and check analysis documents written as templates (<name>.md.in -> <name>.md).

usage: docs.py render <template.md.in>     writes <name>.md next to it
       docs.py check  <template.md.in>     errors on stderr, exit 1 if any

A template names its registries (tools/figlib.py) in header lines, relative to itself:
  <!-- registry: ../games/game4/workers.fig.json -->
and takes every number from them:
  {{id}}            a value figure
  {{table:id}}      a census table, with what it counts, and what it leaves out and why
  {{effects:id}}    the XML record of every value the table counted (all fields set)
  {{eff:id:VALUE:field}}  one XML field of one counted value

Checks (each failure is an error):
  number   a number typed in the text (outside {{ }}, `code`, links, heading and list numbers,
           and after 'game', 'section', 'step', 'rule', 'chapter')
  id       a placeholder naming no figure, or a figure without unit, who, turn or source
  cover    a table showing fewer values than it counted, without a reason
  effects  a table with an XML record type whose {{effects:id}} is not in the document
  stale    an input of a registry whose hash differs from the one the figures were made from
  render   (check_all.py) the committed .md differs from what the template renders
The rendered document ends with every figure it used: value, unit, who, turn, n, source.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
import figlib

PH = re.compile(r'\{\{([^{}]+)\}\}')
ALLOW_BEFORE = re.compile(r'(?:game|games|section|sections|step|steps|rule|rules|chapter|Game|Section|Step|Rule)\s+$')
NUM = re.compile(r'(?<![A-Za-z_\d.])\d+(?:[.,]\d+)*(?![A-Za-z_\d])')
SKIP_FIELDS = {'ArtDefineTag', 'Civilopedia', 'Description', 'Help', 'Strategy', 'Button', 'HotKey', 'EntityEvent',
               'WorldSoundscapeAudioScript', '_sources', '_index', 'bGraphicalOnly', 'bUseLSystem', 'Type'}


def load(tpl):
    text = open(tpl, encoding='utf-8').read()
    base = os.path.dirname(os.path.abspath(tpl))
    regs = [os.path.normpath(os.path.join(base, m)) for m in re.findall(r'<!--\s*registry:\s*(\S+)\s*-->', text)]
    figs, xml, errs = {}, {}, []
    for r in regs:
        if not os.path.exists(r): errs.append(f'stale: registry {r} missing'); continue
        d = json.load(open(r))
        rb = os.path.dirname(r)
        for p, h in d['inputs'].items():
            a = p if os.path.isabs(p) else os.path.normpath(os.path.join(rb, p))
            if os.path.isabs(p) and not os.path.exists(a): continue   # outside the repository, not here
            if not os.path.exists(a): errs.append(f'stale: {r}: input {p} missing')
            elif figlib.sha(a) != h: errs.append(f'stale: {r}: input {p} changed since the figures were made')
        figs.update(d['figures'])
        for t, recs in d.get('xml', {}).items(): xml.setdefault(t, {}).update(recs)
    return text, figs, xml, errs


def compact(v):
    if isinstance(v, (list, dict)): return json.dumps(v, separators=(',', ':'))
    return str(v)


def set_fields(rec):
    out = []
    for k, v in rec.items():
        if k in SKIP_FIELDS or v in (None, '', [], {}, False, 0, 'NONE'): continue
        if isinstance(v, list) and all(x in (0, None, '', [], False) for x in v): continue
        out.append((k, v))
    return out


def render_ph(key, figs, xml, used, errs):
    if key.startswith('table:'):
        id = key[6:]; f = figs.get(id)
        if not f or f['kind'] != 'table': errs.append(f'id: {id} is not a table figure'); return '?'
        used.append(id)
        lines = ['| ' + ' | '.join(map(str, f['head'])) + ' |', '|' + '---|' * len(f['head'])]
        lines += ['| ' + ' | '.join(map(str, r)) + ' |' for r in f['rows']]
        if f['values_shown'] < f['values_total']:
            if not f.get('reason'): errs.append(f'cover: {id} shows {f["values_shown"]} of {f["values_total"]} values without a reason')
            cov = f'Shown {f["values_shown"]} of {f["values_total"]} values. Left out: {", ".join(map(str, f["left_out"]))}. Reason: {f.get("reason")}'
        else:
            cov = f'Every value counted ({f["values_total"]}).'
        lines.append('')
        lines.append(f'*{f["unit"]}; who: {f["who"]}; turn: {f["turn"]}; rows counted: {f["n"]}; source: {f["source"]}. {cov}*')
        return '\n'.join(lines)
    if key.startswith('effects:'):
        id = key[8:]; f = figs.get(id)
        if not f or not f.get('xml'): errs.append(f'id: {id} has no XML record type'); return '?'
        recs = xml.get(f['xml'], {})
        lines = [f'| {f["xml"]} | Fields set (records.json) |', '|---|---|']
        for v in f['values']:
            if v in figlib.NONE_VALUES: lines.append(f'| {v} | (none: no record) |'); continue
            if v not in recs: errs.append(f'effects: {id}: no record for {v}'); continue
            lines.append(f'| {v} | ' + '; '.join(f'`{k}` {compact(x)}' for k, x in set_fields(recs[v])) + ' |')
        lines.append('')
        lines.append('*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*')
        return '\n'.join(lines)
    if key.startswith('eff:'):
        _, id, v, field = key.split(':', 3)
        f = figs.get(id)
        rec = xml.get(f['xml'], {}).get(v) if f and f.get('xml') else None
        if rec is None or field not in rec: errs.append(f'effects: {key} not found'); return '?'
        used.append(id)
        return compact(rec[field])
    f = figs.get(key)
    if not f or f['kind'] != 'value': errs.append(f'id: {key} is not a value figure'); return '?'
    for k in ('unit', 'who', 'turn', 'source'):
        if not f.get(k): errs.append(f'id: {key}: {k} missing')
    if f.get('unit') not in figlib.UNITS: errs.append(f'id: {key}: unit {f.get("unit")!r} not in figlib.UNITS')
    used.append(key)
    return compact(f['value'])


def prose_numbers(text):
    """Numbers typed in the text, with their line."""
    out = []
    infence = False
    for i, line in enumerate(text.split('\n'), 1):
        if line.strip().startswith('```'): infence = not infence; continue
        if infence or line.strip().startswith('<!--'): continue
        s = PH.sub(' ', line)
        s = re.sub(r'`[^`]*`', ' ', s)
        s = re.sub(r'\]\([^)]*\)', ']', s)
        s = re.sub(r'^\s*#+\s*[\d.]*', '', s)
        s = re.sub(r'^\s*\d+\.\s', '', s)
        for m in NUM.finditer(s):
            if ALLOW_BEFORE.search(s[:m.start()]): continue
            out.append((i, m.group(), line.strip()[:80]))
    return out


def process(tpl):
    text, figs, xml, errs = load(tpl)
    for i, n, l in prose_numbers(text):
        errs.append(f'number: line {i}: {n!r} typed by hand: {l}')
    used = []
    body = PH.sub(lambda m: render_ph(m.group(1).strip(), figs, xml, used, errs), text)
    for id, f in figs.items():
        if f['kind'] == 'table' and f.get('xml') and f'{{{{effects:{id}}}}}' not in text and f'table:{id}' in text:
            errs.append(f'effects: table {id} counts {f["xml"]} values; {{{{effects:{id}}}}} is missing')
    seen, rows = set(), []
    for id in used:
        if id in seen: continue
        seen.add(id); f = figs[id]
        v = compact(f['value']) if f['kind'] == 'value' else f'table, {f["values_total"]} values'
        rows.append(f'| `{id}` | {v} | {f["unit"]} | {f["who"]} | {f["turn"]} | {f.get("n") or ""} | {f["source"]} |')
    body = re.sub(r'<!--\s*registry:[^>]*-->\n?', '', body)
    body = (f'<!-- Rendered by tools/docs.py from {os.path.basename(tpl)}. Do not edit; edit the template. -->\n'
            + body.rstrip('\n') + '\n\n## Figures used\n\n| Figure | Value | Unit | Who | Turn | n | Source |\n'
            '|---|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n')
    return body, errs


def main():
    cmd, tpl = sys.argv[1], sys.argv[2]
    body, errs = process(tpl)
    for e in errs: print(f'{tpl}: {e}', file=sys.stderr)
    if cmd == 'render' and not errs:
        open(tpl[:-3], 'w', encoding='utf-8').write(body)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
