# kaipu-record PR #546: Wachiman snapshot before any Pullfrog run

Repository: niway-dev/kaipu-record (public). PR: "feat(editor): preview playback speed 0.5x to 2x (NIW2-666)".
Snapshot taken 2026-11-07 with the PR still open, head `9c07227`. Raw GitHub data is in the `.json` files;
`commits.tsv` lists the 14 commits (the first five were rebased onto `1e7cf17` at 03:22).

This is NOT a closed comparison. Two Pullfrog runs exist and both are confounded; see "Pullfrog runs".

## Wachiman findings (v from footer: Claude Opus 5.5, effort high; engine version not shown in the footer)

| Reviewed commit | Finding | Level | What happened next |
| --- | --- | --- | --- |
| `55ae970` (rebased: `1cc738a`) | Webcam seek lead is in wall seconds; at 2x or 0.5x the webcam bubble may lag and keep re-seeking. | consider | Fixed in `9c07227` "scale the webcam seek lead by the playback rate" (owner-accepted, fix landed after 6d2bf6a). |
| `93a721a` | The per-frame cut hand-off seeks the video at every boundary between source-contiguous clips (a split, not a delete), so playback stutters at each split. | fix | Fixed in `d222c3b` "hand off between contiguous clips without seeking the video" (owner-accepted). |

Rounds: 55ae970 (1 finding), 93a721a (1 finding), 6d2bf6a (0 findings). Cost per run: $0.47, $0.57, $0.55 (sum $1.59, from the footers).
CodeRabbit also commented once (issue comment, 03:22). Not analysed here.

## Replay plan (so Pullfrog sees the code Wachiman saw)

The current head already contains both fixes, so a Pullfrog run on it cannot be compared. Replay on pre-fix commits:

- finding 1: a commit that has the speed feature but not `9c07227`.
- finding 2: `93a721a`, the only state with the per-frame hand-off (`0c88e06`) and without `d222c3b`.

Both findings were verified against code by the owner's later fixes (`owner-accepted`), not yet re-read by me, so verdicts stay `unverified` until I read the code at those commits.

## Limits
One PR, one author, Wachiman only. No Pullfrog data. Version of the engine unknown (footer does not show it).

## Pullfrog runs (replay repo niway-dev/kaipu-bench-pullfrog-v3, head 93a721a, base 1e7cf17)

| Run | PR | Description | Effort (from log) | Repo notes seeded | Findings | Cost | Time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | #2 | original, final (mentions the later fixes) | medium | no (`existing=no`) | 2 | $1.00 | 119 s |
| 2 | #3 | minimal | high | yes (`existing=yes`) | 0 ("No new issues found") | $1.47 | about 3 min |

Model in both: claude-opus-5-5, Pullfrog 0.1.121 and 0.1.122. Wachiman ran Claude Opus 5.5 at effort high.

Run 1 findings: split seeks the video at every contiguous cut (same defect as Wachiman's `93a721a` finding;
owner fixed in `d222c3b`), and Play does nothing at the layout end (Wachiman did not report it; owner fixed in `e2ebac2`).
Run 1 did not report the webcam seek lead (Wachiman did). Run 2 reported nothing.

Why neither run is clean:
- Run 1 saw the final PR description, which names the later fixes. Its findings may come from that hint.
- Run 2 started with repo notes that run 1 wrote (Pullfrog keeps `pullfrog-learnings.md` per repository across runs).
- Description, effort and notes all changed between the runs, so none of them can be blamed for the difference.
- One run per configuration: run-to-run variance is unmeasured.

All verdicts stay `unverified` as to which tool found what on merit. Nothing here supports "Wachiman beats Pullfrog" or the reverse.

## Next, if continued
Clean replay: new empty repo (or delete Pullfrog's stored notes for this one), minimal description, same head, then
medium once and high once, plus a repeat of one of them to measure variance. About $1 to $1.50 per run.

## Cost note (owner concern, 2026-11-07)

Wachiman's cost is close to Pullfrog's on this PR, and the owner does not want that. Same code, same model (Opus 5.5):

| Reviewer | Effort | Runs | Cost to review the PR up to `93a721a` |
| --- | --- | --- | --- |
| Wachiman | high | 2 (whole PR $0.47, re-review $0.57) | $1.04 |
| Pullfrog | medium | 1 | $1.00 |
| Pullfrog | high | 1 | $1.47 |

Wachiman's third run (`6d2bf6a`, $0.55) is not in the table because it reviews later commits; with it the total is $1.59.
Wachiman pays for a re-review on every push; Pullfrog's one run covered the whole PR. One PR, so this is an observation, not a measured ratio.
To investigate in another thread: where Wachiman's per-run cost goes (cache write about 58k tokens per run, 9 to 12 turns), and whether a re-review needs the full read again.
