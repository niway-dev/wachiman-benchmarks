# Wachiman benchmarks

The evidence behind [Wachiman](https://github.com/niway-dev/wachiman), the AI code reviewer: every
benchmark run against Pullfrog and CodeRabbit, the owner's verdict on each finding, and one
structured dataset of every review the three tools posted on GitHub.

This repository holds data and reports only. The reviewer's code, specs and decision records live in
[niway-dev/wachiman](https://github.com/niway-dev/wachiman).

## Start here

- **[results.md](results.md)**: every result so far in one page, newest first, each line linked to
  its full report. Read this first.
- **[dataset/](dataset/README.md)**: one row per posted finding (Wachiman, Pullfrog, CodeRabbit),
  with contracts, run logs, the run map and the verdict labels. Query it with `duckdb`, `jq` or a
  spreadsheet instead of re-reading the reports.

## Layout

| Path | What it is |
| --- | --- |
| [`results.md`](results.md) | Summary of every benchmark, with the runs behind each number. |
| [`kaipu-record-bug-catalogue.md`](kaipu-record-bug-catalogue.md) | The catalogued bugs of kaipu-record used as the answer key. |
| [`2026-10-31/`](2026-10-31/README.md) | Field benchmark: Wachi v1.2.0 and Pullfrog on the same heads of kaipu-record #463–#467 (plus #475). |
| [`2026-11-01/`](2026-11-01/README.md) | Controlled replay: Wachiman v1.3.0, Pullfrog and CodeRabbit on the same five PRs. |
| [`2026-11-02/`](2026-11-02/README.md) | Wachiman v1.4.0 on Opus, three runs, checked against the code. |
| [`2026-11-02-e1-sonnet/`](2026-11-02-e1-sonnet/README.md) | Wachiman v1.4.0 on Sonnet (experiment E1). |
| [`2026-11-02-field/`](2026-11-02-field/README.md) | Field run on the real kaipu-record workspaces PRs. |
| [`replay/`](replay/README.md) | How a pull request is replayed into the `kaipu-bench-*` repositories. |
| [`t3code/`](t3code/README.md) | Bug history of pingdotgg/t3code (791 merged PRs, 2026-11-06 to 11-11): CodeRabbit and Macroscope threads, escaped bugs traced to their introducing PR, a 183-row catalogue and a replay shortlist. No Wachiman run yet. |
| [`mining/`](mining) | Throwaway scripts that produced the bug catalogue (kept for provenance). |
| [`dataset/`](dataset/README.md) | The structured dataset and its raw GitHub API snapshots. |
| [`scripts/`](scripts) | `fetch`, `normalize`, `runs` and `labels`: rebuild the dataset from GitHub. `pair`: pair Wachiman with another reviewer commit by commit (below). |

Each dated folder has a `README.md` with the hypothesis, the runs and the conclusion, a `prs/` (or
`pr-*.md`) report per pull request with the verdict tables, and `raw/` with the posted comments.

## Compare Wachiman with another reviewer on live pull requests

`scripts/pair.ts` reads what Wachiman and another reviewer (CodeRabbit or Pullfrog) posted on a set
of pull requests and pairs them **commit by commit**. A pair is one commit both tools completed; only
pairs are comparable. A tool that refused (no credit), skipped (path filters), reviewed partially or
reviewed a different commit lands in `special-cases.csv` with the reason and what would make it
comparable, never in the comparable set. For every Wachiman review it records the engine version
(from the workflow run, since the review footer omits it), model, effort and posted cost; the other
tool's cost is recorded only when the tool publishes it (Pullfrog does, CodeRabbit does not).

```sh
bun scripts/pair.ts --repo niway-dev/kaipu-record --prs 534-540 --other coderabbit --out 2026-11-06-ci-vs-coderabbit/pairs
```

Writes `pairs.csv`, `special-cases.csv`, `reviews.csv`, `findings.csv` (one row per posted finding,
with `comparison: paired|special`) and a generated `pairs.md`. No model runs. The judgement of each
finding goes in a hand-written `verdicts.csv` next to them; the `wachiman-audit` skill in
[niway-dev/wachiman](https://github.com/niway-dev/wachiman/tree/main/skills) is the procedure.

## Rebuild the dataset

Requires [Bun](https://bun.sh) and an authenticated `gh`. See [dataset/README.md](dataset/README.md#re-run)
for the exact commands; `bun test` checks the parsers against real snapshots.

## Privacy

Everything here comes from public repositories. Quoted third-party text (Pullfrog and
CodeRabbit reviews, kaipu-record code excerpts) belongs to its authors and is reproduced for
research and comparison. Wachiman also runs on private repositories; their
reviews are not stored here, only aggregate counts in [dataset/README.md](dataset/README.md#privacy).

## History

These files lived in `docs/benchmark/` of niway-dev/wachiman until 2026-11-02 and were moved here
so the product repository stays small. Their earlier history is in that repository's git log.
