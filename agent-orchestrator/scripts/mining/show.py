import json,sys,subprocess
C=__import__('os').environ['AO_CLONE']
res=json.load(open('analysis.json'))
def area(r):
    d=subprocess.run(['git','-C',C,'diff','--name-only',r['base'],r['head']],capture_output=True,text=True).stdout.split()
    go=[x for x in d if x.endswith('.go')]; ts=[x for x in d if x.endswith(('.ts','.tsx'))]
    return 'go' if go and not ts else 'ts' if ts and not go else 'mixed'
out=[]
for r in res:
    if 'f' not in r: continue
    r['area']=area(r)
    a=[f for f in r['f'] if f['fix'] and f['adm'] and f['fxok']]
    r['a']=a
    if len(a)>=2:
        print(r['pr'],r['area'],prs:=None) if False else print(r['pr'],r['area'],len(a),r['stat'][:30])
        for f in a: print('   ',f['sev'][:5],f['path'][-45:],f['hl'],'|',f['head'][:90])
json.dump(res,open('analysis.json','w'),indent=1)
