import json,sys,re,subprocess
C=__import__('os').environ['AO_CLONE']
def g(*a): return subprocess.run(['git','-C',C]+list(a),capture_output=True,text=True).stdout
res={r['pr']:r for r in json.load(open('analysis.json'))}
raw={}
pr=int(sys.argv[1]); r=res[pr]
cm={c['id']:c for c in json.load(open(f'c/{pr}.json'))}
for f in r['f']:
    if not f['adm'] or not (f['fix'] and f['fxok'] or f['later']): continue
    if f['head'] and False: pass
    b=cm[f['id']]['body']
    b=re.sub(r'<picture>.*?</picture>','',b); b=re.sub(r'<details>.*','',b,flags=re.S)
    b=re.sub(r'```suggestion.*?```','[suggestion omitted]',b,flags=re.S)
    print('=== id',f['id'],f['sev'],f['path'],'head-line',f['hl'],'fix',f['fix'][:8] or 'LATER-CHANGE')
    print(b.strip()[:int(sys.argv[2]) if len(sys.argv)>2 else 700])
    L=f['hl']
    src=g('show',f"{r['head']}:{f['path']}").split('\n')
    print('--- code@head')
    for i in range(max(1,L-3),min(len(src),L+3)+1): print(('>' if i==L else ' '),i,src[i-1][:150])
