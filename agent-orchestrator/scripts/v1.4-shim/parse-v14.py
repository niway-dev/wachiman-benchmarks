#!/usr/bin/env python3
"""Turn v1.4.0 dry-run logs (<id>.log) into <id>.json with one entry per finding.

Usage: python3 -I parse-v14.py <run-dir>
Inline findings are the "--- path:line ---" blocks; findings off the diff are the bullets of the
review body's "### Outside the diff" section. Each review's own "N finding(s)" count is checked.
"""
import glob, json, re, sys
HEAD = re.compile(r'^\S*\s*\*\*(Blocker|Fix|Consider)\s*·\s*([^:]+):\s*(.*?)\s*\(confidence \w+\)\*\*\s*', re.S)
OUT = re.compile(r'\S*\s*\*\*(Blocker|Fix|Consider)\s*·\s*([^:]+):\s*(.*?)\s*\(confidence \w+\)\*\*\s*\(`([^`:]+):?(\d*)[^`]*`\):\s*(.*)', re.S)
for f in sorted(glob.glob(f"{sys.argv[1]}/*.log")):
    if f.endswith(".gh.log"):
        continue
    t = open(f).read()
    t = t[t.find("--- review at"):]
    blocks = re.split(r"^--- (.+?) ---\n", t, flags=re.M)[1:]
    body, found = blocks[1], []
    m = re.search(r"### Outside the diff\n(.*?)(?=\n### |\n<details>)", body, re.S)
    for item in re.findall(r"^- (.*?)(?=^- |\Z)", m.group(1), re.S | re.M) if m else []:
        h = OUT.match(item)
        if not h:
            sys.exit(f"unparsed outside-diff finding in {f}")
        found.append({"severity": h[1].lower(), "kind": h[2], "title": h[3], "path": h[4], "line": h[5], "body": h[6].strip(), "outside": True})
    for k in range(2, len(blocks), 2):
        b = blocks[k + 1].replace("👮 **Wachiman** · ", "").split("<!-- wachi:finding -->")[0].strip()
        h = HEAD.match(b)
        if not h:
            sys.exit(f"unparsed finding in {f}")
        path, _, line = blocks[k].rpartition(":")
        found.append({"severity": h[1].lower(), "kind": h[2], "title": h[3], "path": path, "line": line, "body": b[h.end():].strip()})
    n = re.search(r"(\d+) finding\(s\)", body)
    if (int(n[1]) if n else 0) != len(found):
        sys.exit(f"count mismatch in {f}")
    cost = re.search(r"\$([0-9.]+)</sub>", body)
    json.dump({"engine": "1.4.0", "cost_usd": float(cost[1]) if cost else None, "findings": found}, open(f[:-4] + ".json", "w"), indent=1)
