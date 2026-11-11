# Chunk 03: PRs #24202..#19585 (2026-11-07, last chunk of the day)

## 1. Header

- PRs covered: 6 (#24202, #23878, #22160, #19660, #19659, #19585). 1 has no bot thread (#24202).
- Bot threads: 16 total. CodeRabbit 14, Macroscope 2.
- Verdicts: real-bug 0, real-minor 13, nit 2, wrong 1, unclear 0.
- Outcomes: fixed-before-merge 9, fixed-then-moot 1 (#23878 T4), disputed 6 (author declined, bot withdrew or went quiet), ignored 0.
- Code checked at the merge commit: #23878 T4/T6, #19659 T1. Everything else is judged from thread text and replies (unverified in code).
- Track B: 5 fix PRs, all touch non-trivial source. SZZ run on all 5. Bots at the introducing PR: missed 5 of 5 (none caught). All 6 PRs merge into `main` (no stack branches).
- Caveat: SZZ blamed refactors or giant imports for #24202 (#25464, #89) and #19659 (#2829). I looked past them with `git log -S` (see notes).
- Caveat: raw.jsonl `head` for #19659 (df15852ba2) is the PR head; the bug threads sit on earlier commits, listed in section 4.

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23878 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | error handling | no | `Effect.option` turns an unreadable unit into "absent", skipping the base-dir guard on direct `install` calls. Outdated+resolved, "Addressed in ca05875". Later removed again (author in T8: fail-closed read "was cut"). (unverified) |
| 23878 | 2 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Docs should name which `t3 service` commands leave another home alone. Doc wording. Addressed in ca05875 (unverified). |
| 23878 | 3 | CR | Minor | real-minor | disputed | 1 | 3 | data integrity | no | Hand-edited quoted `Environment="T3CODE_HOME=..."` is not parsed. Author: T3 never writes that form and other commands share the parser. Bot withdrew. |
| 23878 | 4 | CR | Major | real-minor | fixed-before-merge, then moot | 2 | 3 | cross-file contract | no | `restart`/`withStopped` compare `path.resolve`, install compares realpath, so a symlink alias can skip stopping. Author replied "fixed in defd523". Checked at merge: `restart` (l.970-980) and `withStopped` (l.1000-1010) still use `path.resolve`, and `otherBaseDirOf` (l.658-663) does too, so the realpath handling was later cut and all paths agree on `path.resolve`. Bot "addressed" status is stale; severity 2 because the failure mode is a refusal. |
| 23878 | 5 | CR | Major | real-minor | disputed | 2 | 4 | race/ordering | no | Two concurrent `install` runs from different homes can overwrite each other (no cross-process lock). Author: same race exists on main, out of scope. Bot withdrew. (unverified) |
| 23878 | 6 | MS | High | real-minor | disputed | 2 | 3 | cross-file contract | no | `--base-dir` symlink to the installed home gets `BootServiceOtherBaseDirError`. Checked at merge: comparison is `path.resolve` only (l.661), so the claim holds, but the result is a refusal that names the working `--base-dir`; no data change. Author declined on purpose. High is overrated, sev 2. |
| 23878 | 7 | CR | Minor | real-minor | disputed | 2 | 3 | cross-file contract | no | Same symlink point as T6 (CodeRabbit cites a learning). Author declined; bot withdrew. |
| 23878 | 8 | CR | Minor | real-minor | disputed | 2 | 3 | error handling | no | Repeat of T1: unit-read failure treated as absent. Author's first reason (the later write also fails) was wrong, as CodeRabbit showed (`rename` can replace an unreadable unit); author agreed but kept it out, because the unit sits in the user's own config dir. Left in the merged code (the `Effect.option` read is at l.810 area, unverified in detail). |
| 23878 | 9 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | other | no | `--base-dir ${path}` in the suggested command breaks on spaces. Fixed in cef38a5 with a shared quoting formatter and a shell round-trip test (reply). |
| 22160 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | UI state | no | Delete button stays enabled while confirm or delete is pending, so repeat clicks queue extra dialogs. Fixed in b6296cc (per-row lock, reply + bot confirmation). |
| 19660 | 1 | CR | Minor (Security, advanced tier) | real-minor | fixed-before-merge | 2 | 3 | security | no | Raw ACP diagnostic text copied into the RPC-facing error detail. Bot itself said the "major" framing is unsupported. Fixed in 28fd524: only a fixed constant string is returned. Merged code confirms `refreshFailureDetail` returns constants (diff of 9f00ced8da). |
| 19659 | 1 | MS | High | real-minor | fixed-before-merge | 2 | 4 | data integrity | no | A required form field named `__proto__` is dropped by `content[id] = value`, so an incomplete form is accepted. Real mechanism. Merged code uses `Object.fromEntries` (elicitationForm.ts l.218-220) and the client builders were changed too. Exotic field name, so sev 2. |
| 19659 | 2 | CR | Minor | real-minor | fixed-before-merge | 2 | 3 | state machine | no | `minItems`/`maxItems` not validated (NaN, min > max leaves a required form uncancellable). Author declines forms when min > max or exceeds choices (8827df5); NaN cannot arrive over JSON. Bot accepted. |
| 19659 | 3 | CR | Minor | nit | fixed-before-merge | 1 | 1 | other | no | Windows-skipped test needs a tracking issue (repo rule). Author folded the assertions into the existing test. |
| 19659 | 4 | CR | Minor | wrong | disputed | 1 | 3 | cross-file contract | no | Claims omitted `required` blocks skipping optional fields. Author showed native forms use the `live` response path, not `message`; bot withdrew. |
| 19585 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | race/ordering | yes | Eviction ran before the offer, so a notification arriving after the queue ended could drop backlog the reader still drains. Fixed in e4d691e9 (offer first, evict only on success) with a public test (reply + bot confirmation). Bug existed only inside this PR. |

## 3. Track B (escaped bugs)

| fix PR | bug (one line) | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 24202 | Sidebar open/closed state was written to a `sidebar_state` cookie on every toggle, never read back, so a collapsed sidebar reopens after relaunch (issue #24191) | #89 "Add server-side orchestration engine with event sourcing" (+45611/-14914, 265 files, 2026-02-26); the cookie code came with commit ad9bc6c1df4 "adopt new sidebar primitives" (found with `git log -S SIDEBAR_COOKIE_NAME`) | medium | missed (Macroscope commented on that exact `cookieStore` line, but about Chromium-only availability, not "nothing reads it back") | 2 | 2 | SZZ blamed #25464 (refactor, 12 lines) and #89 (2); #25464 is noise. A shadcn template copied without its read side; visible in one file if you ask "who reads this cookie". |
| 23878 | `t3 service install` with a different `--base-dir` than the installed unit rewrote the service to serve the empty default `~/.t3`; app then showed no projects/threads (issue #23858) | #4286 "Add remote server updates and standalone service management" (+2566/-149, 36 files, 2026-07-22). Missing guard on `install`; the fix is almost all additions. SZZ gave #27996 (4 lines in `up.ts`, a `t3 up` feature) and #11702 (1 line) as the touched lines | low-medium | missed. Near-miss: in #11702 CodeRabbit flagged that `restart` acts on a service owned by another baseDir (same class, other command); in #4286 Macroscope flagged non-atomic unit write only | 4 | 4 | Cross-command invariant ("a unit belongs to one home") that no single diff states. Data stays on disk, so severity 4 not 5. |
| 19660 | Antigravity model refresh replaced a recognizable "python-socks is required" failure with a generic message | #9348 "Add Google Antigravity via the official ACP agent" (+21470/-1388, 169 files, 2026-09-03); 3 of 3 blamed lines | low (only the generic fallback string) | missed (11 bot comments, none on refresh error text) | 2 | 3 | Diagnosability gap, not a crash. Arguably an enhancement. |
| 19659 | Antigravity dropped the form-elicitation capability; shared ACP form handling ignored titled multi-select and returned wrongly typed answers (issue #30851) | #2829 / #664bd5e524b (moved into the shared ACP package, #17354): `elicitationContent` (string/number/boolean/array filter, no schema) came with #2829's orchestrator; capability omission belongs to #9348 | low | missed (not checked on #2829: 380k-line import, treated as noise) | 3 | 4 | SZZ #2829 (46 lines), #17206 (12), #20417 (6), #26167 (3); only #2829/#9348 are plausible origins. Feature gap more than regression. |
| 19585 | Raw ACP notification stream kept up to 32 payloads even if unread; 8 MiB notifications pinned about 252 MiB per connection | #8187 "perf(server): cut idle CPU use and stop provider event leaks" (+913/-98, 19 files, 2026-09-01) added the count cap `MAX_BUFFERED_RAW_NOTIFICATIONS = 32` with no size bound (`git log -S`); unbounded raw stream dates from #1355 (ACP support, +26731) | low | missed (Macroscope/CodeRabbit left 25 comments on #8187, one about dropped transient session updates, none about payload size) | 3 | 3 | SZZ: #1355 26 lines, #8187 3. Numbers in the fix PR body are synthetic (unverified). Memory pressure, not a crash in normal use. |

## 4. Catalogue candidates (severity >= 3, real bug)

Track B escaped (head = introducing PR's last commit).

- `service-install-overwrites-other-base-dir` (fix #23878, introduced by #4286; bots: none). Golden: `t3 service install` rewrites an existing per-user service unit even when the unit's `T3CODE_HOME` is a different `--base-dir`, pointing the service at an empty home; install must read the installed unit's home and refuse before writing. Base 9a0a07167f0623c3a7db0ffeff2e3939760309df, head 781006f0054f3e40ec7f7eadd612b037ea52f5ff. Replay: maybe (origin confidence low-medium; the fix PR #23878 itself, base 006d7e38f0485431c314a1afcc39fa823f379092, is a cleaner replay of the same bug if #4286 is judged too big).
- `acp-raw-notification-unbounded-bytes` (fix #19585, introduced by #8187; bots: none). Golden: the raw ACP notification queue is capped only by count (32), not by size, so unread large notifications keep hundreds of MiB alive per connection; the cap must also bound total bytes. Base c1c2d5401de5a352cf6722959de076c3da63d233, head fdcf91481addce8a8baa7529d77834c670277fb0. Replay: low value (origin confidence low; severity 3 is memory only).

Track A fixed before merge, severity >= 3 real-bug: none in this chunk. #19659 T1 (`__proto__` field dropped, Macroscope, commit 70e476b3157cc789e2f42f0e019a49175769099a) is sev 2, so not catalogued.

## 5. Observations

- Both bots reviewed #23878 heavily (9 threads), and the author declined 5 of them with specific reasons (scope, same behaviour on main). CodeRabbit withdrew each time, and the thread outcome is "disputed" rather than "ignored".
- A "fixed" status can go stale. #23878 T4 was marked addressed, but the merged file shows the realpath handling removed again (restart/withStopped/otherBaseDirOf all use `path.resolve`). Bot status flags are not final-state evidence.
- Macroscope commented on the cookie line in #89 and on non-atomic unit writes in #4286, yet neither touched the defect later fixed there. Comments on the same line are not coverage of the same bug.
- CodeRabbit conceded when the author gave a code-grounded reason (#19659 T4, #23878 T3/T5/T7), and also corrected the author's wrong reasoning (T8, `rename` can replace an unreadable unit).
- CodeRabbit labelled #19660 T1 as a security finding but rated it Minor and itself said the "major" framing was unsupported; the fix (constants only) was cheap.
