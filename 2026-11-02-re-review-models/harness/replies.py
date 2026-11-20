# replies.py: per run, thread replies on threads whose file is in the push's delta ("on delta"),
# and how many of the threads that BOTH Opus baseline runs answered on delta files it left unanswered.
import json, glob, os, re, sys, collections
OLD = "../2026-11-02-re-review-cost/raw/runs"
NEW = "raw/runs"
RAW = "../2026-11-02-field/raw"
def delta_files(prompt):
    m = re.search(r"This part holds exactly these files, and their diff is at the end of this prompt:\n(.*?)\n\n", prompt, re.S)
    return {re.match(r"- (\S+) ", l).group(1) for l in m.group(1).split("\n")} if m else set()
def replies(dirp):
    ids = {}
    for r in sorted(glob.glob(dirp + "/result-*.json")):
        for t in (json.load(open(r)).get("structuredOutput") or {}).get("thread_replies") or []:
            ids[t["comment_id"]] = t["status"]
    return ids
def prompts(dirp):
    return "\n".join(open(p).read() for p in sorted(glob.glob(dirp + "/prompt-*.txt")))
rows = []
for case in sorted(os.listdir(NEW)):
    if not os.path.isdir(f"{NEW}/{case}"): continue
    pr = case.split("-")[0]
    path_of = {c["id"]: c["path"] for c in json.load(open(f"{RAW}/pr-{pr}-comments.json"))}
    delta = delta_files(prompts(f"{OLD}/{case}/base"))
    b1, b2 = replies(f"{OLD}/{case}/base"), replies(f"{OLD}/{case}/base2")
    need = {i for i in set(b1) & set(b2) if path_of.get(i) in delta}
    need1 = {i for i in set(b1) | set(b2) if path_of.get(i) in delta}
    for arm in sorted(os.listdir(f"{NEW}/{case}")):
        d = f"{NEW}/{case}/{arm}"
        if not os.path.isdir(d): continue
        rp = replies(d)
        rows.append((case, arm, len(rp), sum(1 for i in rp if path_of.get(i) in delta), len(need), len(need - set(rp)), len(need1), len(need1 - set(rp))))
    rows.append((case, "Opus-1", len(b1), sum(1 for i in b1 if path_of.get(i) in delta), len(need), len(need - set(b1)), len(need1), len(need1 - set(b1))))
    rows.append((case, "Opus-2", len(b2), sum(1 for i in b2 if path_of.get(i) in delta), len(need), len(need - set(b2)), len(need1), len(need1 - set(b2))))
print("case\tarm\treplies\ton_delta\tneeded_both_opus\tmissing_of_those\tneeded_either_opus\tmissing_of_those")
for r in rows: print("\t".join(map(str, r)))
