import json,re,subprocess
C=__import__('os').environ['AO_CLONE']
def g(*a): return subprocess.run(['git','-C',C]+list(a),capture_output=True,text=True).stdout
res={r['pr']:r for r in json.load(open('analysis.json'))}
for pr in (8720,9076,9036,9095,8714,9055,8764):
    r=res[pr]
    for f in r['f']:
        if not(f['adm'] and f['later'] and not f['fix']): continue
        src=g('show',f"{r['head']}:{f['path']}").split('\n')
        line=src[f['hl']-1].strip()
        sh=g('log','--reverse','--format=%h %s','-S'+line,f"{r['head']}..{r['phead']}",'--',f['path']).strip().split('\n')[:2]
        f['fixfull']=g('log','--reverse','--format=%H','-S'+line,f"{r['head']}..{r['phead']}",'--',f['path']).split()[:1]
        print(pr,f['id'],f['path'][-25:],f['hl'],sh)
json.dump(list(res.values()),open('analysis.json','w'),indent=1)
