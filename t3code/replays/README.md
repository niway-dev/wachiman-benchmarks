# t3code replays for Wachiman

Five merged pingdotgg/t3code pull requests, replayed as pull requests in the public repository [niway-dev/t3code-bench-wachi](https://github.com/niway-dev/t3code-bench-wachi). Wachiman reviews each replay later, and its findings are compared with the CodeRabbit and Macroscope threads the original PR received. This directory holds the setup only; no Wachiman run has happened yet.

- [`manifest.tsv`](manifest.tsv): one row per case: original PR, merge day, base, head, replay PR URL.
- `<pr>/bot-threads.md`: the reference bot threads for that case, with our verdict from the day's chunk.

## No API keys

Wachiman runs locally on the owner's machine, on the owner's Claude subscription. Its findings are posted on the replay PRs with `gh`. The replay repository has GitHub Actions disabled and no secrets, and none of the review apps that comment on PRs (CodeRabbit, Amp) is enabled for it. `replay/bench.sh` and its `wachi` mode were not used, because that mode installs a workflow that needs `ANTHROPIC_API_KEY`.

## How the five cases were picked

One PR per merge day, from the batches of 2026-11-06 to 2026-11-11 (2026-11-07 has no case). Each PR:

- was merged into `main`, not into a stack branch;
- has at most 40 changed files and 3000 added lines;
- has at least 3 bot threads, of which at least 2 are `real-bug` or `real-minor` in our chunk verdicts;
- is not #2829.

Among the qualifying PRs of a day, we preferred the most `real-bug` verdicts and Major/High/Critical bot severities, and the bot-caught cases of [`../replay-shortlist.md`](../replay-shortlist.md). Shortlist case 7 (#30556) is included. Shortlist cases 8 (#33618) and 10 (#27791) qualify but were replaced by #33758 for 2026-11-10: in both, the earliest commit a bot reviewed was dropped from the PR by a force push, so that state cannot be rebuilt from the PR's commits. Shortlist case 9 (#33503) has fewer than 3 bot threads.

| PR | day | files | +lines (base..head) | bot threads | useful (real-bug + real-minor) | real-bug |
| --- | --- | --- | --- | --- | --- | --- |
| [#30579](https://github.com/pingdotgg/t3code/pull/30579) | 2026-11-06 | 7 | 375 | 9 | 8 (MS 3, CR 5) | 3 |
| [#32830](https://github.com/pingdotgg/t3code/pull/32830) | 2026-11-08 | 4 | 109 | 3 | 3 (MS 1, CR 2) | 2 |
| [#24079](https://github.com/pingdotgg/t3code/pull/24079) | 2026-11-09 | 5 | 193 | 10 | 8 (MS 4, CR 4) | 5 |
| [#33758](https://github.com/pingdotgg/t3code/pull/33758) | 2026-11-10 | 6 | 243 | 8 | 8 (MS 5, CR 3) | 6 |
| [#30556](https://github.com/pingdotgg/t3code/pull/30556) | 2026-11-11 | 6 | 202 | 6 | 4 (MS 1, CR 3) | 2 |

## Base and head

- **Head** is the earliest commit that any bot reviewed: among the commits of the PR's bot threads, the one that is an ancestor of all the others. It is never the PR's last commit, which already contains the fixes the bots asked for. For all five cases the head is in the PR's final commit list, and every bot thread of the PR was raised on the head or on a later commit, so all of them are reference threads.
- **Base** is the merge base of the PR's `baseRefOid` and the head. The rule was to use `baseRefOid` directly, but in all five cases it is not an ancestor of the head: the PRs were rebased or had `main` merged in before merging, so `baseRefOid` is `main` at merge time and a diff from it would include unrelated `main` changes. The merge base is what GitHub diffs against, and in every case it equals the parent of the PR's first commit. The original `baseRefOid` is kept in [`manifest.tsv`](manifest.tsv).

All shas are full 40-character pingdotgg/t3code shas, and the base is an ancestor of the head in each case.

## How the replay branches were built

The full t3code history is not pushed. For each case, `replay/pr-<n>/base` is one parentless commit with the exact tree of the base, and `replay/pr-<n>/head` is one commit with the exact tree of the head and the replay base as its parent. `git diff --shortstat` between the two replay commits was checked to match the original base..head diff. The original shas are in the commit messages, the replay PR bodies, and the manifest. The trees include t3code's `LICENSE` (MIT).

## Reference threads

`<pr>/bot-threads.md` lists the bot threads raised on the head or later, with the bot, its severity, `path:line` (the line in the commit the bot commented on), the thread's headline claim, our verdict and outcome from the chunk's Track A table, and the thread URL. A Wachiman finding matches a reference thread when it states the same defect, not when it only touches the same line.
