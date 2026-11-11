#!/usr/bin/env python3
"""Fetch one day of merged pingdotgg/t3code PRs with the AI reviewers' inline threads.

Usage: python3 -I fetch_day.py YYYY-MM-DD OUT.jsonl

One JSON line per merged PR: metadata, changed paths, and every review thread that a
bot (CodeRabbit, Macroscope) opened, with its severity, resolved/outdated flags and the
replies under it. Bot bodies are cleaned (HTML comments, <details> blocks and images
removed) and capped, so a batch stays small enough for one reviewer agent.

Read-only: it only calls `gh api graphql`.
"""
import json, re, subprocess, sys

REPO_OWNER, REPO_NAME = "pingdotgg", "t3code"
BOTS = {"coderabbitai", "macroscopeapp"}
BODY_CAP = 1200
REPLY_CAP = 400


def gql(query, **vars):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in vars.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(out.stderr)
    return json.loads(out.stdout)["data"]


def clean(body, cap):
    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    b = re.sub(r"<details>.*?</details>", "", b, flags=re.S)
    b = re.sub(r"<picture>.*?</picture>", "", b, flags=re.S)
    b = re.sub(r"<[^>]+>", "", b)
    b = re.sub(r"\n{3,}", "\n\n", b).strip()
    return b[:cap] + (" [...]" if len(b) > cap else "")


def severity(login, body):
    if login == "coderabbitai":
        m = re.search(r"\*\*(?:<picture>.*?</picture>)?\s*(Critical|Major|Minor|Trivial|Nitpick)\*\*\s*·\s*\*\*([^*]+)\*\*(?:\s*·\s*\*\*([^*]+)\*\*)?", body)
        return {"severity": m.group(1), "category": m.group(2), "effort": m.group(3)} if m else {}
    m = re.search(r"\*\*(Critical|High|Medium|Low)\*\*", body)
    return {"severity": m.group(1)} if m else {}


LIST = """query($q:String!,$after:String){search(query:$q,type:ISSUE,first:50,after:$after){
pageInfo{hasNextPage endCursor} nodes{... on PullRequest{number}}}}"""

PR = """query($n:Int!){repository(owner:"%s",name:"%s"){pullRequest(number:$n){
number title url mergedAt author{login} additions deletions changedFiles body
mergeCommit{oid} baseRefOid headRefOid labels(first:10){nodes{name}}
files(first:100){nodes{path additions deletions}}
reviewThreads(first:80){nodes{isResolved isOutdated path line originalLine
comments(first:8){nodes{author{login} body createdAt url originalCommit{oid}}}}}}}}""" % (REPO_OWNER, REPO_NAME)


def main(day, out_path):
    q = f"repo:{REPO_OWNER}/{REPO_NAME} is:pr is:merged merged:{day}"
    numbers, after = [], None
    while True:
        d = gql(LIST, q=q, **({"after": after} if after else {}))["search"]
        numbers += [n["number"] for n in d["nodes"] if n]
        if not d["pageInfo"]["hasNextPage"]:
            break
        after = d["pageInfo"]["endCursor"]
    numbers.sort(reverse=True)
    with open(out_path, "w") as out:
        for n in numbers:
            p = gql(PR, n=n)["repository"]["pullRequest"]
            threads = []
            for t in p["reviewThreads"]["nodes"]:
                cs = t["comments"]["nodes"]
                if not cs or not cs[0]["author"] or cs[0]["author"]["login"] not in BOTS:
                    continue
                first = cs[0]
                login = first["author"]["login"]
                threads.append({
                    "bot": login,
                    **severity(login, first["body"]),
                    "path": t["path"],
                    "line": t["line"] or t["originalLine"],
                    "resolved": t["isResolved"],
                    "outdated": t["isOutdated"],
                    "commit": (first.get("originalCommit") or {}).get("oid"),
                    "url": first["url"],
                    "body": clean(first["body"], BODY_CAP),
                    "replies": [{"by": (c["author"] or {}).get("login"), "body": clean(c["body"], REPLY_CAP)} for c in cs[1:]],
                })
            out.write(json.dumps({
                "number": p["number"], "title": p["title"], "url": p["url"],
                "mergedAt": p["mergedAt"], "author": (p["author"] or {}).get("login"),
                "additions": p["additions"], "deletions": p["deletions"], "changedFiles": p["changedFiles"],
                "mergeCommit": (p["mergeCommit"] or {}).get("oid"), "base": p["baseRefOid"], "head": p["headRefOid"],
                "labels": [l["name"] for l in p["labels"]["nodes"]],
                "files": [f["path"] for f in p["files"]["nodes"]],
                "body": clean(p["body"] or "", 1500),
                "threads": threads,
            }) + "\n")
            print(n, len(threads), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
