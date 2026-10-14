import json,sys
def load(root):
    rows=[json.loads(l) for l in open(root+'/m410-h.jsonl')]
    turns=[r for r in rows if 'p' in r]
    s1=json.load(open(root+'/m410-h.jsonl.state1.json'))
    return turns,s1
def summary(root):
    turns,s1=load(root)
    res={}
    for p in s1['players']:
        i=p['id']
        rr=sum(next(x for x in t['p'] if x['id']==i)['rr'] for t in turns if any(x['id']==i for x in t['p']))
        trouble=sum(next(x for x in t['p'] if x['id']==i)['trouble'] for t in turns if any(x['id']==i for x in t['p']))
        res[i]=dict(name=p['leader'][7:17],techs=len(p['techs']),cities=len(p['cities']),units=sum(p['units'].values()),
                    research=rr,trouble=trouble,unitCost=p['costs']['unit'],mil=[c for c in p['civics'] if c in('CIVIC_MERCENARIES','CIVIC_FORTIFICATION','CIVIC_RAIDERS','CIVIC_TRIBAL_WARFARE','CIVIC_MILITIA','CIVIC_JUNTA')],
                    scouts=sum(1 for u in p.get('unitList',[]) if u[1]=='explore'),writing='TECH_WRITING' in p['techs'],
                    buildings=sum(len(c['buildings']) for c in p['cities']))
    return res
a=summary(sys.argv[1]); b=summary(sys.argv[2])
print('%-11s %-30s | %-30s'%('', 'A: research techs cities units trouble', 'B'))
tot=[[0]*5,[0]*5]
for i in sorted(a):
    x=a[i]; y=b.get(i)
    if not y: continue
    f=lambda r:'%6d %3d %3d %4d %3d %4d %s%s'%(r['research'],r['techs'],r['cities'],r['units'],r['trouble'],r['scouts'],'W' if r['writing'] else '-',(r['mil'] or ['?'])[0][6:12])
    print('%-11s %s | %s'%(x['name'],f(x),f(y)))
    for k,r in enumerate((x,y)):
        for j,key in enumerate(['research','techs','cities','units','buildings']): tot[k][j]+=r[key]
print('totals research/techs/cities/units/buildings A',tot[0],'B',tot[1])
