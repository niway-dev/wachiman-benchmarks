# How long Wachiman's own code takes on large pull requests

**Status:** baseline measurements, one prototype and two follow-up experiments (a full saved index, ripgrep). No engine change has been made.
**Date:** 2026-11-21 and 2026-11-22. **Engine:** `niway-dev/wachiman` `main` at `26d23da`.
**Machine:** Apple M5, macOS, Bun 1.4.2, git 2.54.0. Local runs, not GitHub Actions.

## 1. Summary

- **Question.** Leaving the model's time aside, how long does the code around it take (filter, risk,
  batches, call-site evidence, prompt assembly, merge), and which part dominates?
- **Method.** `scripts/bench.ts` builds the review input from a merged commit the way `wachiman local
  --commit` does, then runs `reviewChange` with a stub provider that answers every batch instantly
  with full coverage and no findings. Every millisecond measured is engine code.
- **Result.** The call-site evidence step (`git grep`, one per symbol per batch) is almost all of it:
  47 s of 47 s on a 9k-line t3code PR, 17.6 min on a 338k-line one. Filtering, risk scoring and
  batching stay under 150 ms even at 3,867 files.
- **Why.** The search cost depends on the size of the repository, not of the pull request: every
  symbol is one pass over the whole head. t3code's head has 32k files and 417 MB, two thirds of them
  vendored references under `.repos/`, so one search takes about 0.65 s and a batch (12 symbols) about
  7 s. The searches also run with `spawnSync`, so the four concurrent batches do not overlap them.
- **Prototype.** One in-process pass over the head that looks for every symbol of every batch at once
  took 4.2 s where the current code took 17.6 min (1,499 searches, 475 distinct names), and 1.1 s on
  the small PR when `.repos/` is skipped. It counts matches only; it does not yet build excerpts and
  has not passed a full differential test against `git grep`.
- **ripgrep, one call for every name.** `rg -w -F` with all 475 names of t3code #40132 in one call
  took 0.9 to 1.3 s and returned the same lines `git grep` does. Unlike `git grep`, ripgrep does not
  slow down with many patterns. On the small PR, 64 names took 0.6 s against 36.6 s today.
- **A full saved index does not pay.** Indexing every word of the t3code head took 11.3 s and 1.8 GB
  of memory, and loading the saved index back took 1.5 s, slower than searching the head directly
  with ripgrep.
- **Tokens, not time.** Every prompt carries the list of every file of the review for orientation.
  On cal.com #28903 that list is about 283k characters in each of 463 prompts, roughly 78% of all the
  prompt text sent.

## 2. Workload

Merged pull requests from public repositories, chosen by size from the last 400 merged PRs of each.

| Repository | PR | Merge commit | Files changed / reviewable | Lines changed (reviewable) | Batches |
| --- | --- | --- | --- | --- | --- |
| pingdotgg/t3code | #39445 | `ccabed086a` | 40 / 40 | 9,011 | 9 |
| trpc/trpc | #7771 | `cb7660aee9` | 590 / 527 | 36,028 | 40 |
| calcom/cal.com | #27957 | `f8a93414a5` | 301 / 275 | 55,276 (deletions only) | 60 |
| pingdotgg/t3code | #40132 | `e97290a064` | 1,010 / 1,007 | 337,983 | 156 |
| calcom/cal.com | #28903 | `ab21c7f805` | 4,080 / 3,867 | 432,895 | 463 |

## 3. Results

Raw rows: `raw/core-timing.jsonl`.

| PR | Input (git diff + head snapshot) | Filter | Plan batches | `reviewChange` total | Of which evidence |
| --- | --- | --- | --- | --- | --- |
| t3code #39445 | 10.8 s | 0.15 ms | 1.4 ms | 47.0 s | 47.0 s |
| trpc #7771 | 1.1 s | 0.9 ms | 8 ms | 9.5 s | 9.4 s |
| cal.com #27957 | 4.9 s | 0.6 ms | 8 ms | 0.08 s | 0.006 s (no added lines) |
| t3code #40132 | 12.2 s | 2.0 ms | 28 ms | 1,058 s | 1,058 s |
| cal.com #28903 | 4.5 s | 7.9 ms | 142 ms | 46.6 s | 45.5 s |

Caveats:

- The t3code #40132 run shared the machine for about five minutes with another `git grep` test. Its
  mean of 6.8 s per batch agrees with the clean #39445 run (7.5 s per batch); repeat it alone before
  quoting it as exact.
- "Input" is local mode only (`git archive` of the head). In GitHub Actions the files come from the API
  and the head is a checkout; neither was measured here.
- Not measured: the GitHub source and sink (listing files, posting, `buildReview`), memory loading,
  the verifier's prompt, the distributed-repository context.
- Each batch's evidence step has a 20 s time box, so no batch exceeds that.

## 4. What the search time is made of

- `git grep -n -I -w -F` in a git checkout and in the local snapshot cost the same per symbol
  (about 1.3 s for one symbol on the t3code head, cold), so this is not a local-mode artifact.
- **Putting the 12 symbols of a batch in one `git grep` is slower, not faster:** 7.7 s for twelve
  separate searches, 108.8 s for one search with twelve `-e` patterns (`scripts/grepmulti.sh`, very
  common names, run alone). Excluding `.repos/` brought the multi-pattern pass to 42.1 s.
- Names repeat across batches: on t3code #40132, 1,499 searches covered 475 distinct names.

## 5. Prototype: one pass for the whole review

`scripts/index-proto.ts` plans the evidence of every batch first (pure, 0.6 s for 156 batches), takes
the union of the names, lists the source files with `git ls-files` and the same excludes, reads each
file once and counts the tokens that are wanted names. Raw rows: `raw/index-prototype.jsonl`.

| PR | Searches today | Distinct names | Files scanned | MB scanned | One pass |
| --- | --- | --- | --- | --- | --- |
| t3code #39445 | 73 | 64 | 27,789 | 216 | 4.1 s |
| t3code #39445, `.repos/` skipped | 73 | 64 | 7,480 | 85 | 1.1 s |
| t3code #40132 | 1,499 | 475 | 28,128 | 223 | 4.2 s |

It is not yet equivalent to the current step. It counts tokens, not matching lines (a line with the
name twice counts twice; five sampled names matched `git grep` exactly on the small PR and were 0.05% to
15% above it on the large one). It does not yet drop imports and comments, rank call sites or build the
excerpts. A replacement needs a differential test against the current `collectEvidence` output.

## 6. A full index of the whole repository, saved to disk

`scripts/full-index.ts` indexes every word of 3 to 64 characters in every source file (word to
file and line, one entry per line like `git grep -n`), saves it as gzipped JSON and loads it back.
Raw rows: `raw/full-index.jsonl`.

| Head | Files | MB | Distinct words | Line entries | Build | Memory | Saved | Load |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t3code `ccabed086a` | 27,789 | 216 | 368,058 | 16.7 M | 11.3 s | 1.8 GB | 53 MB | 1.5 s |
| t3code, `.repos/` skipped | 7,480 | 85 | 154,614 | 6.4 M | 3.6 s | 1.0 GB | 20 MB | 0.7 s |
| cal.com `ab21c7f805` | 5,034 | 21 | 73,681 | 1.4 M | 1.5 s | 290 MB | 4.5 MB | 0.13 s |
| trpc `cb7660aee9` | 1,132 | 4 | 13,050 | 0.3 M | 0.34 s | 87 MB | 0.9 MB | 0.02 s |

Reading the files is more than half of the build. A saved index would also have to be rebuilt or
patched for every head, and the head is the pull request's own content. This JavaScript format is
the simplest one; a compact binary format would load faster, but it is not measured here.

## 7. ripgrep

`scripts/rg-vs-grep.sh` searches the names that the engine would search on the t3code heads, with
the same extensions and excludes. `--hidden` is required: without it ripgrep skips `.repos/` and
finds half the lines. Raw rows: `raw/ripgrep.jsonl`.

| Head | Names | `git grep`, one call per name (today) | `rg`, one call per name | `rg`, all names in one call | same, `.repos/` skipped |
| --- | --- | --- | --- | --- | --- |
| t3code #39445 | 64 | 36.6 s | 29.2 s | 0.6 s | 0.2 s |
| t3code #40132 | 475 | not run (about 17.6 min in section 3) | not run | 0.9 to 1.3 s | 0.28 s |

- One call with all names returned 126,859 lines; `git grep` with the same patterns returned
  126,874. The 15-line gap is not explained yet.
- Most of the gain comes from making one call instead of many, not from using ripgrep instead of
  `git grep`: called once per name, ripgrep is only 20% faster. But `git grep` cannot be called once
  for every name (section 4), and ripgrep can.
- One call for 475 names prints 158 MB (1.2 M lines). A replacement would read that output as a
  stream and keep only what the caps allow.
- ripgrep is a separate binary that the engine would have to ship or find on the runner. That cost
  is not measured here.

## 8. Reproduce

```sh
git init repo && git -C repo remote add origin https://github.com/pingdotgg/t3code.git
git -C repo fetch --depth=2 origin ccabed086ad47294173769c77d2d44e55bb8bd0d
BENCH_LOG=1 bun scripts/bench.ts <wachiman>/src repo ccabed086ad47294173769c77d2d44e55bb8bd0d
# index prototype needs a checkout of the commit:
git -C repo worktree add --detach ../head ccabed086ad47294173769c77d2d44e55bb8bd0d
bun scripts/index-proto.ts <wachiman>/src repo ccabed086ad47294173769c77d2d44e55bb8bd0d ../head [--skip-vendored]
bun scripts/full-index.ts <wachiman>/src ../head /tmp/index.json.gz [--skip-vendored]
bun scripts/names.ts <wachiman>/src repo ccabed086ad47294173769c77d2d44e55bb8bd0d > names.txt
bash scripts/rg-vs-grep.sh ../head names.txt   # SKIP_GIT=1 skips the slow git grep row
```

Run measurements one at a time; two concurrent runs share the disk and distort each other.
