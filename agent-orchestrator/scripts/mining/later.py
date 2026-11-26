import json,re,subprocess
C=__import__('os').environ['AO_CLONE']
def g(*a): return subprocess.run(['git','-C',C]+list(a),capture_output=True,text=True).stdout
res=json.load(open('analysis.json'))
for r in res:
    if 'f' not in r: continue
    ph='refs/ao-pr/%d'%r['pr']
    r['phead']=g('rev-parse',ph).strip()
    cache={}
    for f in r['f']:
        f['later']=None
        if f['hl'] is None or not f['adm']: continue
        p=f['path']
        if p not in cache:
            d=g('diff','-U0',r['head'],ph,'--',p); s=set()
            for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+',d,re.M):
                st=int(m.group(1)); n=1 if m.group(2) is None else int(m.group(2))
                s.update(range(st,st+n))   # n==0 pure insertion: nothing
            cache[p]=s
        f['later']= f['hl'] in cache[p]
json.dump(res,open('analysis.json','w'),indent=1)
for r in res:
    if 'f' not in r: continue
    acc=[f for f in r['f'] if f['adm'] and (f['fix'] and f['fxok'] or f['later'])]
    mk=[f for f in acc if f['fix']]
    if len(acc)>=2 and r['area'] in('go',) or (len(acc)>=2 and r['pr'] in (8720,8732,8734,8874,8875,9073,9076,9054,9095,8832)):
        print(r['pr'],r['area'],len(mk),len(acc))
