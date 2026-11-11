# Brief for a chunk annotator

You annotate one chunk (25 merged PRs) of pingdotgg/t3code. Read `README.md` first for goals,
schema and rules. Example of a finished chunk: `batches/2026-11-11/chunk-01.md` (same layout).

Rules: read-only toward GitHub (`gh` reads only). `/tmp/t3code-mine/repo` is a blobless clone:
git read commands only (show, diff, log, blame); never run its scripts or install anything.
Run python with `python3 -I`. Work from the `t3code/` directory. Other annotators run in
parallel: name every scratch file `/tmp/t3c-<day>-<chunk>-*`.

Input: `python3 -I scripts/show.py batches/<day>/raw.jsonl <k>` prints chunk k. Raw JSON (merge
commit, base/head, files, comment commit) is in `batches/<day>/raw.jsonl`.

## Priority: Track B (escaped bugs)

This is the main deliverable. For every PR in the chunk whose title starts with `fix` (any scope)
and changes non-test source, except trivial ones (copy, CSS spacing, test flake, CI only: one line
each, no SZZ):

1. The bug in one sentence (title, body, `git -C /tmp/t3code-mine/repo show <merge>`).
2. `python3 -I scripts/szz.py <mergeCommit> <source paths of the actual fix>` (~40 s each). Pick
   the most likely introducing PR; read it with
   `gh pr view <N> -R pingdotgg/t3code --json title,mergedAt,additions,deletions,changedFiles`.
   Confidence high/medium/low. Pure addition: "no SZZ target". SZZ often blames `#2829` (a
   380k-line import) or a pure refactor: treat those as noise and look past them to the next
   candidate, or to the origin the fix PR's body names.
3. Did a bot comment on that defect in the introducing PR?
   `gh api repos/pingdotgg/t3code/pulls/<N>/comments --paginate --jq '.[] | select(.user.login|test("coderabbit|macroscope")) | "\(.path):\(.line) \(.body[:300])"'`
   Result: caught-and-fixed, caught-and-ignored, missed, or bots-did-not-run.
4. Severity 1-5, and difficulty 1-5 to see it from the introducing PR's diff.

## Track A (bot findings): triage

One row per bot thread. Read code (`git -C /tmp/t3code-mine/repo show <sha>:<path>` at the
comment's commit and at the merge commit) only for threads the bot rates Major, High or Critical,
or that you judge real-bug. Pre-merge commits are often missing from the clone (squash merges);
read them with `gh api "repos/pingdotgg/t3code/contents/<path>?ref=<sha>" --jq .content | base64 -d`.
Everything else: judge from the thread and mark it "(unverified)".

## Output: `batches/<day>/chunk-NN.md`

1. Header: PRs covered, threads by bot, counts by verdict and outcome.
2. Track A table: `| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |`
3. Track B table: `| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |`
4. Catalogue candidates (real bugs, severity >= 3): id (kebab-case), PR(s), one-sentence golden a
   reviewer must state to count as catching it, base and head shas to replay, and who caught it
   (CodeRabbit, Macroscope, human, none). The head must still contain the bug:
   - Track B (escaped): the introducing PR's last commit,
     `gh pr view <N> -R pingdotgg/t3code --json commits --jq '.commits[-1].oid'`.
   - Track A fixed before merge: the commit the bot commented on (`commit` in raw.jsonl), never
     the PR's last commit, which already has the fix.
   Full 40-char shas only.
5. Observations: up to 5 bullets on bot behaviour.

Mark every claim not checked in code "(unverified)".

## Reply (under 120 words)

File path; counts (threads, verdicts, fix PRs traced, bot caught/missed at intro); catalogue
candidate ids with one line each; blockers.
