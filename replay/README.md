# Replay repositories

`bench.sh` builds, runs and collects the code-review benchmark: it replays real
[niway-dev/kaipu-record](https://github.com/niway-dev/kaipu-record) pull requests in throwaway
public repositories, one per reviewer (`niway-dev/kaipu-bench-<reviewer>[-vN]`), so that no
reviewer reads another's comments.

## Usage in one minute

```sh
cd replay
./bench.sh create wachi kaipu-bench-wachi-v3      # repo + main + replay branches; setup PR is #1
# owner: install the apps, add the ANTHROPIC_API_KEY secret (the links are printed)
./bench.sh open kaipu-bench-wachi-v3               # replay PRs (#2...) and the review trigger
./bench.sh rounds kaipu-bench-wachi-v3 2 3         # wachi only: extra rounds on the same commits
./bench.sh collect kaipu-bench-wachi-v3 out/ v3    # bot reviews and comments -> out/v3-pr-<n>-*.md
```

Add `--dry-run` to any command to print every `gh` and `git` command without running it.
Prerequisites: `gh` logged in as `csdev19` (checked, never switched), the SSH alias
`github-csdev`, and a kaipu-record clone that contains every SHA of the manifest
(`KAIPU_CLONE`, default `/tmp/kaipu-mine/repo`). Bash 3.2 compatible.

## Subcommands

| Command | What it does |
| --- | --- |
| `create <wachi\|pullfrog\|coderabbit> <repo-name> [manifest]` | Creates the public repository. `main` is one fresh commit: the README plus the reviewer's files. Pushes `replay/pr-<n>/{base,head}` at the manifest SHAs and checks them on the remote. Then registers and disables the replayed workflows (below) and prints the owner's setup links. |
| `open <repo-name> [manifest]` | Opens one `[replay] <title>` PR per manifest row, head into base, labelled `replay`, body = preamble + the original description. Skips a pair that already has an open PR. Then triggers the reviewer on the PRs it created. |
| `rounds <repo-name> <k...>` | Wachi repositories only. Pushes `replay/pr-<n>/head-r<k>` at the same head SHA and opens one `[replay r<k>]` PR per row and round, because the engine does not review a head it already marked. |
| `collect <repo-name> <out-dir> [label]` | Saves, per replay PR, the bot reviews, the bot inline comments and (CodeRabbit) the bot issue comments to `<out-dir>/<label>-pr-<num>-{reviews,comments,issue-comments}.md`. For Pullfrog it also writes each run's cost row to `<out-dir>/<label>-costs.txt`. `label` defaults to the repository name without `kaipu-bench-`. |

The reviewer comes from the repository name (`kaipu-bench-wachi-v2` is Wachi). Triggers on `open`
and `rounds`:

| Reviewer | `main` carries | Trigger |
| --- | --- | --- |
| wachi | `wachi-workflow.yml` as `.github/workflows/wachi-bench.yml` | comment `/wachi review` |
| pullfrog | kaipu-record's `pullfrog.yml`, unchanged | none; Pullfrog runs when the PR opens |
| coderabbit | nothing | comment `@coderabbitai review` |

CodeRabbit needs the comment because it reads `.coderabbit.yaml` from the PR's head commit, and
kaipu-record's own file there limits automatic review to the production and master branches, so
the automatic review always skips. A config on `main` cannot change that.

## Why `create` registers and disables workflows

The replayed commits carry kaipu-record's workflows. Two of them (`agent-review.yml`, Wachi
v1.2.0, and `pr-checks.yml`) would run as soon as the reviewer's API key secret exists, and the
first would post another reviewer's comments. GitHub lists a workflow only after an event has used
it, so `create` opens one draft setup PR, polls `gh workflow list --all` for up to about 90
seconds, runs `gh workflow disable` on both and closes the PR. If they never appear, the script
warns and continues; disable them by hand under Actions before adding a secret.

The setup PR takes number 1, so the benchmark PRs of a repository start at #2.

## Files

- `bench.sh`: the script.
- `manifest-2026-10-31.tsv`: tab-separated kaipu PR number, base SHA, head SHA, original title.
  Pass another manifest as the last argument of `create` and `open` (or set `BENCH_MANIFEST`,
  which `rounds` uses). `#` lines and blank lines are ignored.
- `repo-README.md`: the readme `create` puts in each repository, under a one-line header naming
  the repository, the reviewer and the manifest.
- `wachi-workflow.yml`: the on-demand Wachi workflow. A `pull_request` event would use the
  workflow at the replayed commit, not this one, hence `/wachi review`. The pin in it names the
  engine version under test.

## Details worth knowing

- `pullfrog.yml` is read from `origin/main` of the clone (`KAIPU_PULLFROG_REF`), not from the
  working tree, which may predate it. The commit message of the repository's `main` records the
  kaipu-record SHA it came from.
- `open` and `rounds` trigger only the PRs they create. To re-trigger a skipped one, comment by hand.
- `--dry-run` still reads the manifest and checks the local clone; it never calls `gh`, pushes or
  creates files outside what it prints.
- The cost row of a Pullfrog run is the first non-separator line after the `Cost ($)` header in
  `gh run view <id> --log`; a run without one gets a placeholder line. Actions logs expire, so
  collect soon after the runs.
