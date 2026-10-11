#!/usr/bin/env python3
"""Compile, verify and measure isolated C++03 algorithms; no game execution."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import tempfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='optionally verify the real base-XML fixture')
    parser.add_argument('--output', type=Path, default=HERE/'results.json')
    args = parser.parse_args()
    evidence = json.loads((HERE/'fixtures.json').read_text())
    if args.source:
        raw = (args.source/evidence['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != evidence['sha256']:
            raise SystemExit('Technology XML differs from the recorded fixture source')
        tree = ET.fromstring(raw)
        for node in tree.iter():
            node.tag = node.tag.split('}')[-1]
        techs = {node.findtext('Type'):node for node in tree.findall('.//TechInfo')}
        for name, expected in evidence['technologies'].items():
            node = techs[name]
            actual = {'cost':int(node.findtext('iCost')),
                      'and':[x.text for x in node.findall('AndPreReqs/PrereqTech')],
                      'or':[x.text for x in node.findall('OrPreReqs/PrereqTech')]}
            if actual != expected:
                raise SystemExit('Fixture mismatch: '+name)
    common = ['g++','-std=c++03','-Wall','-Wextra','-Werror']
    checked = common+['-O1','-fsanitize=undefined','-fno-sanitize-recover=undefined']
    measured = common+['-O2']
    with tempfile.TemporaryDirectory(prefix='rom-algorithm-lab-') as folder:
        check = Path(folder)/'checked'
        bench = Path(folder)/'measured'
        subprocess.run(checked+[str(HERE/'lab.cpp'),'-o',str(check)],check=True)
        verification = json.loads(subprocess.check_output([str(check)],text=True))
        subprocess.run(measured+[str(HERE/'lab.cpp'),'-o',str(bench)],check=True)
        runs = []
        for _ in range(8):
            records = [json.loads(line) for line in subprocess.check_output([str(bench),'measure'],text=True).splitlines()]
            assert records[0] == verification
            runs.append(records[1:])
        summary = []
        for index, record in enumerate(runs[0]):
            stable = {k:v for k,v in record.items() if k!='cpu_ms'}
            assert all({k:v for k,v in rows[index].items() if k!='cpu_ms'}==stable for rows in runs)
            samples = [rows[index]['cpu_ms'] for rows in runs[1:]]
            summary.append(dict(stable,cpu_ms_median=statistics.median(samples),cpu_ms_samples=samples))
    result = {'scope':'isolated synthetic algorithms and a base-XML graph fixture; no DLL/game timings',
              'source_sha256':hashlib.sha256((HERE/'lab.cpp').read_bytes()).hexdigest(),
              'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
              'platform':platform.platform(),'verification_flags':checked[1:],'measurement_flags':measured[1:],
              'warmup_runs':1,'measured_runs':7,'clock':'C clock() process CPU time',
              'xml_fixture_checked':bool(args.source),'verification':verification,'measurements':summary}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(verification))
    for row in summary:
        print(row['kind'],row.get('k',row.get('n')),str(row['cpu_ms_median'])+' ms',
              'checks='+str(row.get('candidate_checks',row.get('edge_checks'))))
    print('Timings exclude game-state extraction, pathfinding and simulation.')


if __name__ == '__main__':
    main()
