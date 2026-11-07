#!/usr/bin/env python3
"""Add Wachiman reviews to a working copy of Martian's offline bench as tool `wachiman`.

Inputs: a .shas file (golden_url, pr number, base, head, commits, fork; tab-separated) and the
directory of `wachiman local --format json` results named <pr>.json. Every finding becomes one
candidate, because the GitHub Action posts every finding (blocker, fix and consider inline; info in
the review body). Candidate text is the finding's title and body, as a reviewer would read it.

Writes, inside <bench>/results:
  benchmark_data.json             a `wachiman` review per PR (review_comments = the findings)
  <model-dir>/candidates.json     candidates[golden_url]["wachiman"]
Never reads golden comment contents.

Usage: python3 -I to_martian.py <bench-dir> <model-dir-name> <shas-file> <reviews-dir> [<tool-name>]
"""
import json
import sys
from pathlib import Path


def main():
    bench, model_dir, shas, reviews = (Path(a) for a in sys.argv[1:5])
    tool = sys.argv[5] if len(sys.argv) > 5 else "wachiman"
    data_p = bench / "results" / "benchmark_data.json"
    cand_p = bench / "results" / model_dir / "candidates.json"
    data = json.loads(data_p.read_text())
    cands = json.loads(cand_p.read_text()) if cand_p.exists() else {}
    added, missing = 0, []
    for line in shas.read_text().splitlines():
        url, n = line.split("\t")[:2]
        rp = reviews / f"{n}.json"
        if not rp.exists() or rp.stat().st_size == 0:
            missing.append(n)
            continue
        result = json.loads(rp.read_text())
        findings = result.get("findings", [])
        comments = [{"path": f["path"], "line": f["line"] or None,
                     "body": f"{f['title']}\n\n{f['body']}"} for f in findings]
        entry = data[url]
        entry["reviews"] = [r for r in entry["reviews"] if r["tool"] != tool]
        entry["reviews"].append({"tool": tool, "repo_name": f"local:{n}", "pr_url": url,
                                 "review_comments": comments})
        cands.setdefault(url, {})[tool] = [{"text": c["body"], "path": c["path"], "line": c["line"],
                                            "source": "wachiman-json"} for c in comments]
        added += 1
    data_p.write_text(json.dumps(data))
    cand_p.parent.mkdir(parents=True, exist_ok=True)
    cand_p.write_text(json.dumps(cands))
    print(f"added {added} reviews for {tool}; missing: {missing or 'none'}")


if __name__ == "__main__":
    main()
