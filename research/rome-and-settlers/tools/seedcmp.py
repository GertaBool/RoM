import json,sys,glob,os,statistics as st
base=sys.argv[1]; variants=sys.argv[2:]
def run_stats(root):
    rows=[json.loads(l) for l in open(root+'/m410-h.jsonl')]
    turns=[r for r in rows if 'p' in r]
    s1=json.load(open(root+'/m410-h.jsonl.state1.json'))
    s0=json.load(open(root+'/m410-h.jsonl.state0.json'))
    tot=dict(research=0,techs=0,cities=0,buildings=0,units=0,merc=0,trouble=0,scouts=0,settlers=0)
    for t in turns:
        for x in t['p']:
            tot['research']+=x['rr']; tot['trouble']+=x['trouble']
    t0={p['id']:len(p['techs']) for p in s0['players']}
    for p in s1['players']:
        tot['techs']+=len(p['techs'])-t0.get(p['id'],0)
        tot['cities']+=len(p['cities']); tot['buildings']+=sum(len(c['buildings']) for c in p['cities'])
        tot['units']+=sum(p['units'].values()); tot['merc']+= 'CIVIC_MERCENARIES' in p['civics']
        tot['scouts']+=sum(1 for u in p['unitList'] if u[1]=='explore'); tot['settlers']+=p['units'].get('settle',0)
    rome=[p for p in s1['players'] if p['leader']=='LEADER_AUGUSTUS']
    r=dict(research=sum(next((x['rr'] for x in t['p'] if x['id']==3),0) for t in turns),
           trouble=sum(next((x['trouble'] for x in t['p'] if x['id']==3),0) for t in turns))
    if rome:
        p=rome[0]; r.update(techs=len(p['techs']),writing=int('TECH_WRITING' in p['techs']),cities=len(p['cities']),
            merc=int('CIVIC_MERCENARIES' in p['civics']),units=sum(p['units'].values()),unitCost=p['costs']['unit'])
        wt=[t['t'] for t in turns if next((x['techs'] for x in t['p'] if x['id']==3),0)>=0]
    return tot,r,s1['turn']
for v in variants:
    roots=sorted(glob.glob(os.path.join(base,v+'-*')))
    res=[]
    for rt in roots:
        try: res.append(run_stats(rt))
        except Exception as e: print('skip',rt,e)
    if not res: continue
    print('==',v,'runs',len(res),'end turns',[x[2] for x in res])
    for k in ['research','techs','cities','buildings','units','merc','trouble','scouts','settlers']:
        vals=[x[0][k] for x in res]
        print('  all  %-9s mean %8.1f sd %7.1f  %s'%(k,st.mean(vals),st.pstdev(vals),vals))
    for k in ['research','trouble','techs','writing','cities','merc','units','unitCost']:
        vals=[x[1].get(k,0) for x in res]
        print('  rome %-9s mean %8.1f  %s'%(k,st.mean(vals),vals))
