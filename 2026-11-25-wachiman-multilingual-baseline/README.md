# wachiman-multilingual baseline: how long the engine takes to read and classify a change

This is the starting measure for **wachiman-multilingual**, the work on language-aware analysis. Later changes to how the engine reads each language are compared with these numbers.

Date: 2026-11-25. Machine: Apple M5, 10 cores, 24 GB (from `sysctl`), Bun 1.4.2, git 2.54.0, one case at a time.
Engine: `niway-dev/wachiman` at `574c7b82083076de881823a676c182471ad3a184` (`origin/main`, "add a benchmark script and the engine baseline", #286), read-only use of `src/`.

This is the baseline for multi-language work (language detection and per-language parsers). It answers one
question: before any model runs, how much time does the engine spend reading a pull request and sorting its
files, and how much of that is the symbol extraction a per-language parser would replace?

## What is measured

Each stage calls the engine's real exported function and is timed on its own. Every number is the median of
5 runs, after one discarded warm-up run (the warm-up fetches git's lazy blobs and warms the JIT).

| Stage | Calls | Notes |
| --- | --- | --- |
| read: diff | `localFiles(repo, base, head)` from `src/connectors/local-git.ts` | three `git diff` runs (`--raw`, `--numstat`, patches) parsed into `ReviewFile[]` |
| read: contents | one `git cat-file --batch` over the head blobs of the changed files, written under a temp `headDir` | stands in for `snapshotHead`, which exports the whole tree; see "Not measured" |
| filter | `filterFiles(files, DEFAULT_EXCLUDE, [])` | no repository exclude, no scope |
| split | `splitUnreviewable(kept, headDir)` | binary detection |
| risk | `riskScore(path)` for every reviewable file | no path rules |
| module | `moduleKey(path)` for every reviewable file | |
| plan | `planBatches(reviewable, { maxLines: 1000, maxChars: 140000 })` | the engine's default limits |
| symbols | per batch: `addedLinesOf`, `extractCalledSymbols`, `definedSymbols`, `planEvidence` | `collectEvidence` is never called: no grep |

The stages are not a partition. `planBatches` calls `riskScore` and `moduleKey` itself, and `planEvidence`
calls both extractors again. The symbols column adds `addedLines + extractCalled + defined + planEvidence`
(the extractor times count only the files the engine reads, `SOURCE_EXTENSIONS`).

Per language, files and added lines are those of the reviewable files (after filter and split). The language
comes from the file extension (map in `scripts/run.ts`). The engine reads only files whose extension is in
`SOURCE_EXTENSIONS` (`ts tsx js jsx mjs cjs go py rs java kt swift vue svelte`). For every other language
the two extractors were called anyway, to show what they do to it. Those rows say "forced"; their cost is not
part of the engine's real symbols stage.

## Corpus

57 pull requests, none skipped.

- Martian: all 50 of `martian/worklist.tsv` (10 cal.com, 10 discourse-graphite, 10 grafana, 10 keycloak, 10 sentry; the two greptile forks count under their upstream). Each is
  fetched blobless, depth 1, from the benchmark fork `code-review-benchmark/<fork>`. For the "-flat" rows the
  worklist head is a commit that exists only on the benchmark machine, so the real head is read from the fork's PR #1 and the
  worklist base (the true merge base) is kept. The diff is the pull request's diff.
- t3code: `pingdotgg/t3code` #39445 (40 files) and #40132 (1010 files); merge commit against its first parent.
- agent-orchestrator: `OrchestratorInc/agent-orchestrator`, the 5 largest merged PRs by changed lines among the
  200 most recent merged PRs (`gh pr list --limit 200`): #8961, #8893, #8678, #9005, #8895; merge commit against
  its first parent. Older merged PRs were not searched. #8961 is an outlier: 2172 changed files, 161,052 added lines.

`scripts/cases.tsv` holds every base and head SHA.

## Results

### Per pull request (median of 5 runs, ms)

| PR | changed files | reviewable | added lines | patch KB | batches | read | classify (filter+split+risk+module+plan) | symbols | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| t3code-39445 | 40 | 40 | 8747 | 470 | 9 | 163.1 | 0.77 | 46.0 | 193.1 |
| t3code-40132 | 1010 | 1007 | 244567 | 25656 | 156 | 1060.5 | 29.9 | 1321.5 | 2408.9 |
| martian-cal.com-10600 | 16 | 16 | 280 | 25 | 1 | 66.6 | 0.39 | 1.49 | 69.6 |
| martian-cal.com-10967 | 22 | 22 | 368 | 44 | 1 | 69.1 | 0.51 | 1.85 | 71.5 |
| martian-cal.com-11059 | 40 | 40 | 375 | 36 | 1 | 71.7 | 0.84 | 4.24 | 77.7 |
| martian-cal.com-14740 | 15 | 15 | 555 | 24 | 1 | 70.3 | 0.35 | 2.85 | 74.0 |
| martian-cal.com-14943 | 3 | 3 | 38 | 2 | 1 | 60.6 | 0.12 | 0.20 | 60.9 |
| martian-cal.com-22345 | 2 | 2 | 114 | 17 | 1 | 76.6 | 0.10 | 0.87 | 77.6 |
| martian-cal.com-22532 | 17 | 17 | 379 | 20 | 1 | 61.9 | 0.43 | 1.38 | 63.6 |
| martian-cal.com-7232 | 10 | 10 | 241 | 24 | 1 | 94.2 | 0.33 | 1.93 | 96.4 |
| martian-cal.com-8087 | 12 | 12 | 82 | 18 | 1 | 72.2 | 0.28 | 0.62 | 73.1 |
| martian-cal.com-8330 | 4 | 4 | 111 | 8 | 1 | 68.1 | 0.12 | 0.79 | 69.1 |
| martian-discourse-graphite-1 | 3 | 3 | 20 | 3 | 1 | 97.4 | 0.12 | 0.06 | 97.6 |
| martian-discourse-graphite-10 | 36 | 36 | 449 | 27 | 1 | 80.3 | 0.68 | 0.06 | 81.0 |
| martian-discourse-graphite-2 | 18 | 18 | 156 | 17 | 1 | 66.5 | 0.42 | 0.03 | 67.0 |
| martian-discourse-graphite-3 | 10 | 10 | 155 | 8 | 1 | 58.9 | 0.23 | 0.13 | 59.2 |
| martian-discourse-graphite-4 | 28 | 27 | 653 | 23 | 1 | 68.5 | 0.51 | 0.20 | 69.2 |
| martian-discourse-graphite-5 | 5 | 5 | 54 | 2 | 1 | 56.9 | 0.08 | 0.02 | 57.0 |
| martian-discourse-graphite-6 | 5 | 5 | 44 | 4 | 1 | 53.7 | 0.15 | 0.01 | 53.9 |
| martian-discourse-graphite-7 | 32 | 32 | 115 | 32 | 1 | 56.6 | 0.18 | 0.05 | 56.9 |
| martian-discourse-graphite-8 | 16 | 16 | 389 | 26 | 1 | 55.7 | 0.45 | 0.35 | 56.6 |
| martian-discourse-graphite-9 | 7 | 7 | 31 | 3 | 1 | 61.6 | 0.18 | 0.02 | 61.8 |
| martian-grafana-103633 | 4 | 4 | 240 | 15 | 1 | 90.1 | 0.21 | 1.62 | 92.8 |
| martian-grafana-106778 | 14 | 14 | 542 | 56 | 1 | 58.6 | 0.41 | 2.31 | 61.2 |
| martian-grafana-107534 | 4 | 4 | 48 | 5 | 1 | 63.8 | 0.12 | 0.40 | 64.3 |
| martian-grafana-76186 | 8 | 8 | 137 | 18 | 1 | 50.1 | 0.24 | 0.81 | 51.1 |
| martian-grafana-79265 | 11 | 11 | 105 | 12 | 1 | 54.7 | 0.29 | 0.63 | 55.6 |
| martian-grafana-80329 | 3 | 3 | 199 | 14 | 1 | 61.7 | 0.11 | 1.32 | 63.2 |
| martian-grafana-90045 | 5 | 5 | 524 | 30 | 1 | 58.7 | 0.14 | 2.13 | 61.3 |
| martian-grafana-90939 | 1 | 1 | 13 | 1 | 1 | 60.6 | 0.07 | 0.14 | 60.8 |
| martian-grafana-94942 | 7 | 7 | 47 | 18 | 1 | 66.8 | 0.14 | 0.25 | 67.3 |
| martian-grafana-97529 | 5 | 5 | 25 | 8 | 1 | 55.9 | 0.14 | 0.19 | 56.2 |
| martian-keycloak-32918 | 4 | 4 | 268 | 21 | 1 | 59.5 | 0.18 | 1.96 | 61.5 |
| martian-keycloak-33832 | 12 | 12 | 673 | 27 | 1 | 54.0 | 0.38 | 2.31 | 56.6 |
| martian-keycloak-36880 | 10 | 10 | 866 | 73 | 2 | 54.4 | 0.25 | 4.30 | 58.8 |
| martian-keycloak-36882 | 11 | 10 | 70 | 7 | 1 | 55.8 | 0.28 | 0.29 | 56.4 |
| martian-keycloak-37038 | 19 | 19 | 831 | 57 | 1 | 61.3 | 0.75 | 3.20 | 65.0 |
| martian-keycloak-37429 | 48 | 48 | 343 | 58 | 1 | 81.3 | 1.18 | 1.01 | 83.3 |
| martian-keycloak-37634 | 28 | 28 | 722 | 42 | 1 | 59.1 | 1.31 | 2.78 | 62.9 |
| martian-keycloak-38446 | 8 | 8 | 256 | 28 | 1 | 54.8 | 0.32 | 1.89 | 57.7 |
| martian-keycloak-40940 | 4 | 4 | 51 | 4 | 1 | 57.1 | 0.13 | 0.39 | 57.7 |
| martian-keycloak-greptile-1 | 9 | 9 | 407 | 30 | 1 | 57.5 | 0.29 | 2.02 | 59.8 |
| martian-sentry-67876 | 3 | 3 | 247 | 19 | 1 | 55.5 | 0.10 | 1.44 | 56.9 |
| martian-sentry-77754 | 7 | 7 | 212 | 15 | 1 | 52.1 | 0.17 | 1.13 | 53.3 |
| martian-sentry-80168 | 4 | 4 | 249 | 28 | 1 | 56.0 | 0.12 | 1.48 | 57.7 |
| martian-sentry-80528 | 4 | 4 | 289 | 20 | 1 | 58.7 | 0.12 | 1.42 | 60.2 |
| martian-sentry-93824 | 6 | 6 | 199 | 18 | 1 | 53.5 | 0.13 | 1.10 | 55.0 |
| martian-sentry-95633 | 7 | 7 | 1276 | 53 | 2 | 58.8 | 0.24 | 6.28 | 65.4 |
| martian-sentry-greptile-1 | 3 | 3 | 128 | 7 | 1 | 65.1 | 0.12 | 0.78 | 66.0 |
| martian-sentry-greptile-2 | 9 | 9 | 183 | 21 | 1 | 67.4 | 0.21 | 1.28 | 68.9 |
| martian-sentry-greptile-3 | 8 | 8 | 480 | 24 | 1 | 57.5 | 0.16 | 2.15 | 60.0 |
| martian-sentry-greptile-5 | 106 | 106 | 2312 | 217 | 4 | 96.2 | 3.19 | 10.3 | 108.9 |
| orchestrator-8961 | 2172 | 1866 | 161052 | 11029 | 196 | 1120.6 | 72.9 | 525.1 | 1718.8 |
| orchestrator-8893 | 48 | 48 | 11192 | 419 | 13 | 127.2 | 1.66 | 50.9 | 179.7 |
| orchestrator-8678 | 26 | 26 | 3282 | 283 | 5 | 113.2 | 0.36 | 28.9 | 146.8 |
| orchestrator-9005 | 41 | 41 | 3979 | 224 | 6 | 94.8 | 0.72 | 36.2 | 132.5 |
| orchestrator-8895 | 41 | 41 | 3732 | 175 | 5 | 93.1 | 1.75 | 23.3 | 119.0 |

### Per stage, over all PRs (ms)

| stage | sum of medians | median PR | max PR | share of total |
| --- | ---: | ---: | ---: | ---: |
| readDiff | 3835.6 | 46.0 | 665.4 | 46.8% |
| readContents | 2062.2 | 16.1 | 667.4 | 25.2% |
| filter | 11.0 | 0.05 | 5.08 | 0.1% |
| split | 13.7 | 0.00 | 13.1 | 0.2% |
| risk | 10.7 | 0.04 | 4.59 | 0.1% |
| module | 0.79 | 0.01 | 0.24 | 0.0% |
| plan | 89.7 | 0.16 | 49.9 | 1.1% |
| addedLines | 28.9 | 0.04 | 14.4 | 0.4% |
| extractCalled | 784.4 | 0.47 | 506.4 | 9.6% |
| defined | 289.5 | 0.20 | 194.9 | 3.5% |
| planEvidence | 965.8 | 0.64 | 604.3 | 11.8% |
| total | 8198.3 | 63.6 | 2408.9 | 100.0% |

### Per language, over all PRs (reviewable files only)

| language | read by the engine's extractor | PRs | files | added lines | extractCalledSymbols ms | definedSymbols ms | extracted names | defined names | ms per 1k added lines (extract) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TypeScript | yes | 21 | 2078 | 318068 | 655.5 | 244.6 | 12491 | 40680 | 2.06 |
| Go | yes | 11 | 772 | 78196 | 100.4 | 34.8 | 10110 | 5404 | 1.28 |
| JSON | no (forced, for reference) | 12 | 206 | 23180 | 26.5 | 8.04 | 0 | 0 | 1.14 |
| Markdown | no (forced, for reference) | 7 | 115 | 5201 | 18.5 | 4.97 | 131 | 122 | 3.56 |
| Python | yes | 11 | 84 | 4302 | 7.23 | 3.42 | 408 | 205 | 1.68 |
| Java | yes | 10 | 98 | 4199 | 6.73 | 2.74 | 889 | 148 | 1.60 |
| YAML | no (forced, for reference) | 10 | 75 | 3583 | 4.90 | 2.13 | 5 | 2 | 1.37 |
| JavaScript | yes | 6 | 28 | 3167 | 4.70 | 1.65 | 233 | 782 | 1.48 |
| Protobuf | no (forced, for reference) | 1 | 1 | 1532 | 0.70 | 0.29 | 0 | 21 | 0.46 |
| SQL | no (forced, for reference) | 5 | 32 | 1325 | 2.07 | 0.58 | 59 | 0 | 1.57 |
| Ruby | no (forced, for reference) | 8 | 73 | 1260 | 2.15 | 0.97 | 90 | 68 | 1.71 |
| Kotlin | yes | 1 | 6 | 1168 | 2.67 | 0.97 | 166 | 251 | 2.29 |
| Swift | yes | 1 | 6 | 1159 | 1.96 | 0.99 | 133 | 291 | 1.69 |
| CSS | no (forced, for reference) | 6 | 44 | 918 | 1.32 | 0.44 | 93 | 10 | 1.44 |
| 23 minor types (under 500 added lines each; full list in raw/) | no (forced, for reference) | - | 122 | 1513 | 2.57 | 0.87 | 86 | 79 | 1.70 |

## Reading the numbers

- The per-PR "total" is dominated by reading from git. On a typical Martian PR (3 to 20 files) that is 50 to 100 ms,
  nearly all of it process start-up of the git calls; classification is under 1 ms and symbols under 5 ms.
- Classification (filter, split, risk, module, plan) stays small even at 1866 reviewable files (73 ms for orchestrator #8961).
- Symbol extraction is the only stage that grows with added lines: about 1.3 to 2.1 ms per 1,000 added lines for TypeScript, Go, Python, Java and JavaScript.
  Added to `planEvidence` (which repeats the work), it is the biggest stage on the two large PRs.
- The extractors are regexes written for TypeScript-like code. Ruby is not in `SOURCE_EXTENSIONS`, so discourse gets no
  extraction at all in the engine today; the forced Ruby row shows only that the regexes run on it and find some names.

## Experiment: one `git diff` instead of three

The engine reads a change with three `git diff` runs (`--raw`, `--numstat`, then the patches;
`localFiles` in `src/connectors/local-git.ts`). The same options can produce all three in one run:
`--raw --numstat -z` plus the patch options. Measured on the same 57 PRs and the same machine, median
of 7 interleaved runs each:

| | Three runs | One run | Change |
| --- | ---: | ---: | ---: |
| All 57 PRs, sum of medians | 3,549 ms | 1,747 ms | −51% |
| t3code #40132 (1,010 files) | 606 ms | 497 ms | −18% |
| agent-orchestrator #8961 (2,172 files) | 402 ms | 299 ms | −26% |
| t3code #39445 (40 files) | 110 ms | 64 ms | −42% |
| cal.com #22532 | 49 ms | 18 ms | −64% |

The saving is largest on small PRs, where most of the time is starting git and opening the
repository, which one run does once instead of three times. In all 57 PRs the patch part of the single
run is byte-identical to the separate patch run, and its first part matches the separate `--raw` run
(`scripts/diff-one-vs-three-equal.ts`). The engine would need a parser that splits the single output;
that parser was not written, so its cost is not in these numbers.

```sh
bun scripts/diff-one-vs-three.ts /tmp/classify-bench
bun scripts/diff-one-vs-three-equal.ts /tmp/classify-bench
```

## What is NOT measured

- The model, any network call to GitHub, and posting.
- `collectEvidence` (the grep over the repository): never called.
- `snapshotHead`, the engine's real export of the whole head tree. The harness reads and writes only the changed files' head blobs,
  because the clones are blobless and a full export would download every blob. The "read: contents" column is therefore a lower bound
  for the engine's real snapshot cost on large repositories.
- `resolveRefs`, instructions, policy and settings reads of `buildLocalInput`, and `git log` calls for title and author.
- Cold-cache cost: all timings are warm (blobs already local, git object store in the page cache).
- Repository path rules and `.wachiman` excludes: only `DEFAULT_EXCLUDE` is applied.
- Correctness of the extracted names: only their count is recorded.

## Reproduce

```sh
git -C <wachiman checkout> fetch origin
git -C <wachiman checkout> worktree add --detach /tmp/wm-main 574c7b82083076de881823a676c182471ad3a184
(cd /tmp/wm-main && bun install)
cd 2026-11-25-wachiman-multilingual-baseline/scripts
./make-cases.sh                                   # rewrites cases.tsv (needs gh; reads the Martian forks' PR #1)
cut -f1 cases.tsv | xargs -P 6 -I{} ./fetch.sh /tmp/classify-bench {}
./run-all.sh /tmp/wm-main /tmp/classify-bench     # serial; writes ../raw/<corpus>.jsonl
bun summarize.ts                                  # prints the tables above
```

`raw/*.jsonl` has one line per PR: the shape (files, lines, bytes, batches), the median of every stage, the five run totals, and the per-language
files, added lines, extraction ms and names. `make-cases.sh` hard-codes the t3code and agent-orchestrator merge SHAs; the orchestrator list came from the `gh pr list` call above on 2026-11-25.
