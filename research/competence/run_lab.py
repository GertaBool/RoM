#!/usr/bin/env python3
"""Validate a research scheduling model; this does not execute RoM or a save."""
import argparse
import itertools
import hashlib
import platform
import json
from pathlib import Path
import random
import statistics
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent

def example(name, jobs, *, horizon=8, production=2, income=1, required=0, deadline=0):
    return dict(name=name, jobs=jobs, horizon=horizon, production=production,
                income=income, required=required, deadline=deadline)

FIXTURES = [
    example('investment_delivers_defender_sooner', [[0,1,4,1,0,0,0,0], [1,2,1,0,4,3,0,0], [0,1,12,1,0,0,0,0]], required=4, deadline=5),
    example('imminent_attack_requires_guard_first', [[0,1,4,1,0,0,0,0], [1,2,1,0,4,3,0,0], [0,1,6,1,0,0,0,0]], required=4, deadline=3),
    example('peace_has_no_mandatory_guard', [[0,1,4,1,0,0,0,0], [1,2,1,0,4,3,0,0], [0,1,6,1,0,0,0,0]]),
    example('civic_with_no_payoff', [[0,1,2,0,0,0,0,1]]),
    example('mine_connection_then_recruit', [[0,2,2,0,2,0,0,0], [1,2,1,0,0,0,0,0], [3,1,8,1,0,0,15,0]], horizon=6, required=4),
]

def simulate(m, starts):
    """Independent calendar replay of absolute start times, no planner routines."""
    n=len(m['jobs']); finishes=[-1]*n; remaining=[0]*n; done=set(); value=0
    for tick in range(m['horizon']):
        active=[]; resources=set()
        for i,(req,uses,effort,*_) in enumerate(m['jobs']):
            if starts[i]==tick:
                if any((req>>j)&1 and j not in done for j in range(n)): return None
                remaining[i]=effort
            if remaining[i]>0:
                wanted={bit for bit in range(4) if uses&(1<<bit)}
                if wanted & resources: return None
                resources |= wanted; active.append(i)
        rate=m['production']+sum(m['jobs'][i][4] for i in done)
        if not any(m['jobs'][i][7] for i in active):
            value+=m['income']+sum(m['jobs'][i][5] for i in done)
        completed=[]
        for i in active:
            remaining[i]-=rate if m['jobs'][i][3] else 1
            if remaining[i]<=0:
                completed.append(i);finishes[i]=tick+1;value+=m['jobs'][i][6]
        done.update(completed)
        if m['deadline'] and tick+1>=m['deadline']:
            if any(m['required']&(1<<i) and i not in done for i in range(n)): return None
    if any(m['required']&(1<<i) and i not in done for i in range(n)): return None
    return value,finishes

def exhaustive(m):
    best=None
    for starts in itertools.product(range(-1,m['horizon']),repeat=len(m['jobs'])):
        if any(m['required']&(1<<i) and starts[i]<0 for i in range(len(starts))):continue
        r=simulate(m,starts)
        if r is not None and (best is None or r[0]>best):best=r[0]
    return best

def encoded(m,width):
    prefix=[len(m['jobs']),m['horizon'],m['production'],m['income'],m['required'],m['deadline'],width]
    return ' '.join(map(str,prefix))+'\n'+'\n'.join(' '.join(map(str,j)) for j in m['jobs'])+'\n'

def run(exe, models, width):
    r=subprocess.run([str(exe)],input=''.join(encoded(m,width) for m in models),text=True,capture_output=True,check=True)
    rows=[json.loads(s) for s in r.stdout.splitlines()];assert len(rows)==len(models)
    for m,row in zip(models,rows):
        for k in ['search','greedy']:
            answer=row[k]
            if answer['feasible']:
                replay=simulate(m,answer['start'])
                assert replay is not None and replay==(answer['utility'],answer['finish']),(m,k,answer,replay)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'results.json');args=ap.parse_args()
    rng=random.Random(73219);random_models=[]
    for k in range(160):
        n=rng.randint(2,4);jobs=[];h=rng.randint(3,6)
        for i in range(n):
            req=sum(1<<j for j in range(i) if rng.randrange(4)==0)
            uses=1<<rng.randrange(3)
            jobs.append([req,uses,rng.randint(1,5),int(uses==1),rng.randrange(3),rng.randrange(3),rng.randrange(-2,5),int(rng.randrange(15)==0)])
        random_models.append(example('random_'+str(k),jobs,horizon=h,production=rng.randint(1,3),income=rng.randrange(3),required=rng.randrange(1<<n),deadline=rng.choice([0,h])))
    models=FIXTURES+random_models
    oracle=[exhaustive(m) for m in models]
    with tempfile.TemporaryDirectory(prefix='rom-planning-lab-') as temp:
        checked=Path(temp)/'checked';fast=Path(temp)/'fast'
        flags=['g++','-std=c++03','-Wall','-Wextra','-Werror']
        subprocess.run(flags+['-O1','-fsanitize=undefined','-fno-sanitize-recover=undefined',str(HERE/'planning_lab.cpp'),'-o',str(checked)],check=True)
        exact=run(checked,models,0)
        for m,row,expected in zip(models,exact,oracle):
            found=row['search'];assert found['exact']
            assert found['feasible']==(expected is not None),(m,found,expected)
            if expected is not None:assert found['utility']==expected,(m,found,expected)
        beams={str(w):run(checked,models,w) for w in [1,8,32]}
        summary={}
        for width,rows in beams.items():
            regrets=[];misses=0;limited=0
            for r,optimum in zip(rows,oracle):
                found=r['search'];limited+=not found['exact']
                if optimum is not None:
                    if not found['feasible']:misses+=1
                    else:regrets.append(optimum-found['utility']);assert found['utility']<=optimum
                if r['greedy']['feasible']:
                    assert found['feasible'] and found['utility']>=r['greedy']['utility']
            summary[width]={'budget_limited_cases':limited,'feasible_optimum_but_no_plan':misses,
                            'suboptimal_feasible_cases':sum(x>0 for x in regrets),'max_utility_regret':max(regrets,default=0)}
        first=exact[0]['search'];assert first['finish'][2]==5 and not exact[0]['greedy']['feasible']
        assert exact[1]['search']['start'][2]==0
        assert exact[2]['search']['start'][2]==-1
        assert exact[3]['search']['start'][0]==-1
        assert exact[4]['search']['start'][2]>=exact[4]['search']['finish'][1]
        subprocess.run(flags+['-O2',str(HERE/'planning_lab.cpp'),'-o',str(fast)],check=True)
        run(fast,models,32);times=[]
        for _ in range(7):
            start=time.perf_counter();run(fast,models,32);times.append((time.perf_counter()-start)*1000)
        output={'scope':'Abstract scheduling model, not a DLL or engine replay','random_seed':73219,
                'cpp_sha256':hashlib.sha256((HERE/'planning_lab.cpp').read_bytes()).hexdigest(),
                'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
                'platform':platform.platform(),'clock':'Python time.perf_counter wall time',
                'oracle':'Independent exhaustive enumeration of absolute job start calendars',
                'oracle_cases':len(models),'native_standard':'C++03','ubsan':'fatal','beam_comparison':summary,
                'fixtures':[dict(model=m,exact=row,beam_1=beams['1'][i]['search']) for i,(m,row) in enumerate(zip(FIXTURES,exact))],
                'timing':{'scope':'165-case optimized subprocess batch including serialization and Python witness checks; no native engine calls',
                          'runs_ms':times,'median_ms':statistics.median(times)}}
        args.output.write_text(json.dumps(output,indent=2)+'\n')
        print('PASS:',len(models),'calendar oracles; all returned schedules independently replayed; feasible fallback preserved.')
        print(json.dumps(summary,indent=2));print('Batch median ms:',output['timing']['median_ms'])
        for m,r in zip(FIXTURES,exact):print(m['name'],r['search'])

if __name__=='__main__':main()
