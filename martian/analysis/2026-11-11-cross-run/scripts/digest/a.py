import sys; sys.path.insert(0,'/tmp/martian-digest')
from load import *
CORE={"bug","security","concurrency","data","api","perf","test_gap","doc_defect"}
def fb(p,r,b): return (1+b*b)*p*r/(b*b*p+r) if p+r else 0
def summ(e,name):
    tp=fp=fn=cands=0; hc=0; ctp=cfn=0
    for u,r in e.items():
        tp+=r['tp'];fp+=r['fp'];fn+=r['fn'];cands+=r['total_candidates']
        hc+=sum(1 for g in r['true_positives'] if g['severity'].lower() in HC)
        ctp+=sum(1 for g in r['true_positives'] if g['category'] in CORE)
        cfn+=sum(1 for g in r['false_negatives'] if g['category'] in CORE)
    p=tp/(tp+fp);r=tp/(tp+fn)
    cp=ctp/(ctp+fp); cr=ctp/(ctp+cfn)
    print(f"{name:20s} PRs {len(e)} cands {cands} ({cands/len(e):.1f}/PR) TP {tp} FP {fp} FN {fn} R {r:.1%} P {p:.1%} F1 {fb(p,r,1):.1%} F2core {fb(cp,cr,2):.1%} HC {hc}/66")
for k,v in runs.items(): summ(v,k)
for k,v in comp.items(): summ(v,k)
# restricted to cal.com for 8-tools + wachiman runs
calu={u for u in comp['bugbot']}
print('--- Cal.com 10 PRs only')
for k,v in runs.items(): summ({u:r for u,r in v.items() if u in calu},k)
for k,v in comp.items(): summ({u:r for u,r in v.items() if u in calu},k)
