import json,sys,re,subprocess
C=__import__('os').environ['AO_CLONE']
def g(*a): return subprocess.run(['git','-C',C]+list(a),capture_output=True,text=True).stdout
res={r['pr']:r for r in json.load(open('analysis.json'))}
pr=int(sys.argv[1]); r=res[pr]; cap=int(sys.argv[2]) if len(sys.argv)>2 else 900
for f in r['f']:
    if f['adm'] and f['later'] and not f['fix']:
        print('=== id',f['id'],f['path'],f['hl'],f['head'][:0])
        d=g('diff','-U1',r['head'],r['phead'],'--',f['path'])
        for h in re.split(r'(?m)^(?=@@)',d)[1:]:
            m=re.match(r'@@ -(\d+)(?:,(\d+))?',h); s=int(m.group(1)); n=1 if m.group(2) is None else int(m.group(2))
            if s<=f['hl']<=s+n+1: print(h[:cap]); break
