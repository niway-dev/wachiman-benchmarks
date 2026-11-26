"""Write runs/pr-<n>/summary.md for one run, then the runs table in the field README.

Usage: python3 -I report.py <field-dir> <pr>
"""

import json
import os
import sys

BEGIN, END = "<!-- runs:begin -->", "<!-- runs:end -->"


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def money(x):
    return "—" if x is None else (f"${x:.2f}" if x >= 0.01 else f"${x:.4f}")


def tokens(n):
    return f"{n / 1000:.1f}k" if n < 1_000_000 else f"{n / 1_000_000:.1f}M"


def haiku_cost(run):
    ex = (load(os.path.join(run, "haiku.json"), {}) or {}).get("execution", {}) or {}
    u = ex.get("usage") or {}
    return {
        "cost": ex.get("costUsdEstimate"),
        "calls": ex.get("calls"),
        "turns": ex.get("turns"),
        "seconds": round((ex.get("durationMs") or 0) / 1000),
        "output": u.get("output", 0),
        "cacheRead": u.get("cacheRead", 0),
        "stop": ex.get("stop"),
    }


def summary(run, pr):
    meta = load(os.path.join(run, "meta.json"), {})
    cands = load(os.path.join(run, "candidates.json"), {"candidates": [], "dropped": []})
    verifiers = {}
    for name in sorted(os.listdir(run)):
        if name.startswith("verify-") and name.endswith(".json"):
            verifiers[name[7:-5]] = load(os.path.join(run, name), {})
    cr = load(os.path.join(run, "coderabbit.json"), {}) or {}
    h = haiku_cost(run)
    lines = [
        f"# kaipu-record [#{pr}](https://github.com/niway-dev/kaipu-record/pull/{pr}) · "
        f"[`{meta.get('sha', '')[:8]}`](https://github.com/niway-dev/kaipu-record/commit/{meta.get('sha', '')})",
        "",
        f"- **Title:** {meta.get('title', '')}",
        f"- **Run:** {meta.get('ranAt', '')}, locally on the claude.ai subscription (no API key). Costs are API-equivalent estimates.",
        f"- **Engine:** Wachiman {meta.get('engine', '')}, `agent-review local`, Haiku 5.5 effort high.",
        f"- **Commit reviewed:** {meta.get('commitReason', '')}",
        f"- **Code:** {meta.get('files', '?')} files, +{meta.get('added', '?')}/−{meta.get('removed', '?')}.",
        f"- **CodeRabbit:** {len(cr.get('comments', []))} inline comment(s) and {len(cr.get('reviews', []))} review(s) on this PR so far "
        f"({cr.get('atCommit', 0)} inline at the reviewed commit).",
        "",
        "## Cost and work",
        "",
        "| Step | Model | Calls | Turns | Time | Output | Cache read | Estimate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        f"| Propose | Haiku 5.5 high | {h['calls']} | {h['turns']} | {h['seconds']} s | {tokens(h['output'])} | {tokens(h['cacheRead'])} | {money(h['cost'])} |",
        f"| Filter | code | — | — | — | — | — | $0 |",
    ]
    for label, v in verifiers.items():
        u = v.get("usage", {})
        lines.append(
            f"| Verify | {v.get('model', label)} | 1 | {v.get('turns')} | {round((v.get('durationMs') or 0) / 1000)} s | "
            f"{tokens(u.get('output', 0))} | {tokens(u.get('cacheRead', 0))} | {money(v.get('costUsd'))} |"
        )
    lines += [
        "",
        f"## Findings: {len(cands['candidates'])} candidate(s) after the filters, {len(cands['dropped'])} dropped by them",
        "",
        "| id | Haiku said | Finding | " + " | ".join(f"{k} keeps?" for k in verifiers) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in verifiers) + " |",
    ]
    by = {k: {x.get("id"): x for x in v.get("verdicts", [])} for k, v in verifiers.items()}
    for c in cands["candidates"]:
        cells = []
        for k in verifiers:
            v = by[k].get(c["id"])
            cells.append("—" if not v else (f"✅ {v['severity']}" if v.get("keep") else "✗"))
        title = c["title"].replace("|", "\\|")
        lines.append(f"| {c['id']} | {c['severity']} · {c['topic']} | `{c['path']}:{c['line']}` {title} | " + " | ".join(cells) + " |")
    if cands["dropped"]:
        lines += ["", "Dropped by the filters:", ""]
        lines += [f"- `{d['path']}:{d['line']}` {d['title']}: {d['dropReason']}" for d in cands["dropped"]]
    for k, v in verifiers.items():
        lines += ["", f"### Reasons: {k}", ""]
        lines += [f"- **{x.get('id')}** {'keep' if x.get('keep') else 'drop'}: {x.get('reason', '')}" for x in v.get("verdicts", [])]
    with open(os.path.join(run, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    kept = {k: sum(1 for x in v.get("verdicts", []) if x.get("keep")) for k, v in verifiers.items()}
    return {
        "pr": pr,
        "sha": meta.get("sha", "")[:8],
        "ranAt": meta.get("ranAt", "")[:10],
        "size": f"{meta.get('files', '?')} f, +{meta.get('added', '?')}/−{meta.get('removed', '?')}",
        "candidates": len(cands["candidates"]),
        "kept": kept,
        "haiku": h["cost"],
        "verify": {k: v.get("costUsd") for k, v in verifiers.items()},
        "cr": len(cr.get("comments", [])),
    }


def index(field):
    runs_dir = os.path.join(field, "runs")
    rows = []
    for name in sorted(os.listdir(runs_dir), key=lambda s: int(s.split("-")[1]) if s.startswith("pr-") else 0):
        if name.startswith("pr-") and os.path.exists(os.path.join(runs_dir, name, "summary.json")):
            rows.append(load(os.path.join(runs_dir, name, "summary.json")))
    out = [
        "| PR | Commit | Run | Size | Haiku candidates | Opus keeps | Sonnet keeps | CodeRabbit comments | Haiku | Opus verify | Sonnet verify |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    tot = {"h": 0.0, "o": 0.0, "s": 0.0}
    for r in rows:
        tot["h"] += r["haiku"] or 0
        tot["o"] += r["verify"].get("opus") or 0
        tot["s"] += r["verify"].get("sonnet") or 0
        out.append(
            f"| [#{r['pr']}](runs/pr-{r['pr']}/summary.md) | `{r['sha']}` | {r['ranAt']} | {r['size']} | {r['candidates']} | "
            f"{r['kept'].get('opus', '—')} | {r['kept'].get('sonnet', '—')} | {r['cr']} | {money(r['haiku'])} | "
            f"{money(r['verify'].get('opus'))} | {money(r['verify'].get('sonnet'))} |"
        )
    out.append(f"| **{len(rows)} PRs** | | | | | | | | **{money(tot['h'])}** | **{money(tot['o'])}** | **{money(tot['s'])}** |")
    readme = os.path.join(field, "README.md")
    with open(readme, encoding="utf-8") as f:
        text = f.read()
    a, b = text.index(BEGIN) + len(BEGIN), text.index(END)
    with open(readme, "w", encoding="utf-8") as f:
        f.write(text[:a] + "\n\n" + "\n".join(out) + "\n\n" + text[b:])


def main():
    field, pr = sys.argv[1], sys.argv[2]
    run = os.path.join(field, "runs", f"pr-{pr}")
    s = summary(run, pr)
    with open(os.path.join(run, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)
    index(field)


if __name__ == "__main__":
    main()
