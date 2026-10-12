#!/usr/bin/env python3
"""Execute explicit phase snapshots; this never loads a BTS save or invents yields."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
FIELDS = {
    'unit_completion': 'progress needed current_production_no_overflow total_modifier base_modifier gold_percent overflow'.split(),
    'growth': 'population food food_kept threshold kept_percent food_yield consumption food_production disorder avoid_growth callback'.split(),
    'production': 'progress needed base_production total_modifier food_yield consumption_no_angry overflow feature food_production disorder callback choice_required process has_order allow_no_production'.split(),
}

def encode(record):
    if set(record) != {'id', 'phase', 'snapshot'} or not isinstance(record['id'], str):
        raise ValueError('each record requires exactly id (string), phase and snapshot')
    fields = FIELDS[record['phase']]
    state = record['snapshot']
    if set(state) != set(fields):
        raise ValueError('missing or unknown snapshot fields: ' + str(set(state) ^ set(fields)))
    values = [state[k] for k in fields]
    if any(type(v) is not int or not -(2**31) <= v < 2**31 for v in values):
        raise ValueError('snapshot values must be explicit signed 32-bit integers')
    return {'growth':'G','production':'P','unit_completion':'U'}[record['phase']] + ' ' + ' '.join(map(str, values)) + '\n'

def compile_runner(executable, *, sanitize=False):
    flags = ['g++', '-std=c++03', '-Wall', '-Wextra', '-Werror', '-O1']
    if sanitize:
        flags += ['-fsanitize=undefined', '-fno-sanitize-recover=undefined']
    subprocess.run(flags + [str(HERE/'runner.cpp'), '-o', str(executable)], check=True)

def execute(executable, records):
    data = ''.join(encode(r) for r in records)
    result = subprocess.run([str(executable)], input=data, capture_output=True, text=True, check=True)
    outputs = [json.loads(line) for line in result.stdout.splitlines()]
    if len(outputs) != len(records):
        raise RuntimeError('runner response count mismatch')
    return [dict(id=r['id'], phase=r['phase'], result=o) for r,o in zip(records,outputs)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshots', type=Path, help='JSONL; explicit fresh snapshot for each native phase')
    args = parser.parse_args()
    records = [json.loads(line) for line in args.snapshots.read_text().splitlines() if line.strip()]
    with tempfile.TemporaryDirectory(prefix='rom-economy-') as folder:
        exe = Path(folder)/'economy'; compile_runner(exe)
        for output in execute(exe, records): print(json.dumps(output))

if __name__ == '__main__':
    main()
