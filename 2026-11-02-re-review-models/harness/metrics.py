# metrics.py <runs-dir>: per run, cost / turns / requests (distinct assistant message ids) / findings
# / thread replies, as TSV. Reads result-N.json (the engine's view) and call-N.jsonl (the trace).
import json, sys, glob, os
runs = sys.argv[1]
print("case\tarm\tcost\tturns\trequests\tstatus\tfindings\treplies\tcalls")
for d in sorted(glob.glob(os.path.join(runs, "*", "*"))):
    if not os.path.isdir(d): continue
    case, arm = d.split(os.sep)[-2:]
    results = sorted(glob.glob(os.path.join(d, "result-*.json")))
    if not results: continue
    cost = turns = req = fnd = rep = 0; status = []
    for r in results:
        j = json.load(open(r)); cost += j["costUsd"]; turns += j["turns"]; status.append(j["terminalReason"])
        so = j.get("structuredOutput") or {}
        fnd += len(so.get("findings") or []); rep += len(so.get("thread_replies") or [])
        trace = r.replace("result-", "call-").replace(".json", ".jsonl")
        ids = set()
        for l in open(trace):
            if '"type":"assistant"' in l:
                try: ids.add(json.loads(l)["message"]["id"])
                except Exception: pass
        req += len(ids)
    print(f"{case}\t{arm}\t{cost:.3f}\t{turns}\t{req}\t{','.join(status)}\t{fnd}\t{rep}\t{len(results)}")
