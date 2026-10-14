import json,re,collections,sys
root=sys.argv[1]; pre=sys.argv[2] if len(sys.argv)>2 else 'm410-h.jsonl'
d0=json.load(open(root+'/'+pre+'.state0.json')); d1=json.load(open(root+'/'+pre+'.state1.json'))
names={p['id']:p['leader'][7:17] for p in d0['players']}
turn=None; pl=None
fin=collections.Counter(); disb=collections.Counter(); branch=collections.Counter()
for line in open(root+'/logs/BBAI.log',errors='replace'):
    m=re.search(r'Player (\d+) \(.*\) setTurnActive for turn (\d+)',line)
    if m: pl=int(m.group(1)); turn=int(m.group(2)); continue
    if re.search(r'finishes production of unit TXT_KEY_UNIT_SETTLER ',line): fin[pl]+=1
    if 'no deliverable site, disbanded' in line: disb[pl]+=1
    m=re.search(r'uses (.*settler.*)$',line.strip())
    if m and 'escort' not in m.group(1) and 'sea' not in m.group(1): branch[(m.group(1))]+=1
c0={p['id']:len(p['cities']) for p in d0['players']}; c1={p['id']:len(p['cities']) for p in d1['players']}
s0={p['id']:p['units'].get('settle',0) for p in d0['players']}
s1={p['id']:p['units'].get('settle',0) for p in d1['players']}
print('player      cities  settlers@start trained disbanded settlers@end  cityDelta')
tot=[0]*5
for i in sorted(names):
    r=[s0.get(i,0),fin[i],disb[i],s1.get(i,0),c1.get(i,0)-c0.get(i,0)]
    tot=[a+b for a,b in zip(tot,r)]
    print('%2d %-11s %2d %8d %8d %8d %8d %8d'%(i,names[i],c0.get(i,0),*r))
print('total             %8d %8d %8d %8d %8d'%tuple(tot))
print(dict(branch))
