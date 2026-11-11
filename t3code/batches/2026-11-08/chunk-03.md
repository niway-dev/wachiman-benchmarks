# Chunk 03: PRs #23821..#21524 (2026-11-08, last chunk of the day, 6 PRs)

## 1. Header

- PRs covered: 6 (#23821, #23486, #22295, #21596, #21592, #21524). 3 have no bot thread. All merged into `main` (no stack branches).
- Bot threads: 6 total. CodeRabbit 5, Macroscope 1.
- Verdicts: real-bug 1 (#21524 T1), real-minor 5 (#23486 T1, #21596 T1, #21524 T3-T5), wrong 1 (#21524 T2), nit 0, unclear 0.
- Outcomes: fixed-before-merge 5 (#23486 T1, #21524 T1, T3, T4, T5), disputed 1 (#21524 T2, bot withdrew), ignored/withdrawn 1 (#21596 T1, bot withdrew).
- Code checked: only the #23486 diff and the #21596 diff (merge commits). Verdicts for #21524 come from thread text and replies (unverified in code).
- Track B: 5 `fix` PRs traced (#23821 is `perf`, skipped). SZZ script returned "pure addition" for all five; for #23486 and #21596 that is wrong (they edit existing lines), so I blamed by hand with `git blame` on the parent. Treat `szz.py` as unreliable when a fix changes lines inside an expression (unverified why).

## 2. Track A (bot threads)

| PR | T# | bot | bot sev | verdict | outcome | sev | diff | class | replay | finding + evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23486 | 1 | CR | Minor | real-minor | fixed-before-merge | 2 | 2 | other | no | `VSCode://` link survives the app check but the sanitizer compares scheme case-sensitively, so the link is stripped. Author confirmed, fixed in d388b09 with a rehype step (`rehypeNormalizeLocalEditorLinks` seen in merged diff). CR's suggested stage was wrong, the author corrected it. |
| 21596 | 1 | CR | Minor | real-minor | ignored (bot withdrew) | 1 | 3 | other | no | Astral character on Option chord: `core.ts` uses UTF-16 length. Author: pre-existing, no standard macOS layout does this; CR withdrew. Not verified in code. |
| 21524 | 1 | MS | Medium | real-bug | fixed-before-merge | 3 | 4 | cross-file contract | yes | `mise x claude@2.0.0` wrapper: resolver probes plain `mise which claude`, offers `mise upgrade claude`, which updates the configured install, not what the wrapper runs. Fixed in 4578871d9a (wrapper naming a version stays manual). Thread outdated+resolved, reply states fix (unverified in code). Macroscope's own reply says it could not act, irrelevant. |
| 21524 | 2 | CR | Minor | wrong | disputed | 1 | 2 | other | no | Wants mise lookups cached by environment. Author shows `resolveLatestVersion` bypasses `ProviderLatestVersions.cached`; CR withdrew. |
| 21524 | 3 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | `MISE_<TOOL>_VERSION` inline overrides before `mise x` not recognised, same wrong-install upgrade as T1. Fixed in 9f99667. (unverified) |
| 21524 | 4 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Wrapper that sources a file exporting a version override. Fixed in 2255ebb (sourcing keeps manual). (unverified) |
| 21524 | 5 | CR | Minor | real-minor | fixed-before-merge | 2 | 4 | cross-file contract | no | Conditional `if ...; then . file; fi` source still missed. Author replaced the pattern list with a "single `mise x` command only" rule in abc8b3d. (unverified) |

Note: T1, T3, T4, T5 on #21524 are one defect family (a wrapper script can choose a different tool version than the resolver probes). Four rounds of bot review each found a new variant; the author ended with a whitelist rule. The family is the interesting item, not the individual threads.

## 3. Track B (escaped bugs)

| fix PR | bug | introducing PR | conf | bots at intro | sev | diff | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 23486 | Chat links `cursor://file/...` and `vscode://file/...` do nothing on desktop (allowlist in `parseSafeExternalUrl`, sanitizer and URL transform all dropped them). | #7697 "restrict editor deep links" (+64/-6, merged 2026-08-21) | low | 1 CR thread and 1 Macroscope thread, both about a dropped comment, not about the missing local file links (missed) | 2 | 5 | Blamed lines are the `SAFE_WEB_PROTOCOLS.has(...)` return from #7697 (hand blame). More a missing capability than a regression: #7697 deliberately blocked other schemes. Not a reviewer-detectable bug. |
| 22295 | macOS Bash terminals started as non-login shells, so `~/.bash_profile` was not loaded. | no SZZ target (pure addition) | n/a | n/a | 2 | 4 | Behaviour never existed; needs macOS shell-startup knowledge. |
| 21596 | Option chords on macOS sent as Alt (`ESC @`), so Option-layer characters (German `@`, `|`, `[ ]`) never typed. | #7485 "encode shifted characters correctly in the terminal" (+28/-2, merged 2026-08-21) | medium | CR 1 summary, Macroscope 1 thread (Shift+Space), cursor 1; none about Option (missed) | 3 | 4 | Hand blame: `ghosttyConsumedMods` lines come from #7485 (18f6d03), which only handled Shift. Affects non-US Mac users in the terminal; the layout knowledge is the hard part. Macroscope's Medium thread on #7485 concerned a different defect (Shift+Space), so not caught. |
| 21592 | Calendar access prompt: hosted commands touching Calendar crash/denied because `NSCalendars*UsageDescription` keys were missing from the macOS plist. | no SZZ target (pure addition) | n/a | n/a | 3 | 5 | macOS runtime knowledge only; invisible in any diff that does not touch Calendar. (Impact claim unverified; title says "declare access".) |
| 21524 | Provider installed through mise updated with its own updater, creating an untracked copy. | no SZZ target (pure addition of a feature; titled `fix`) | n/a | n/a | 2 | 3 | Effectively a feature. #23821 is `perf`, not traced. |

## 4. Catalogue candidates (severity >= 3, real bugs)

- `mise-wrapper-version-mismatch` (Track A, fixed before merge, caught by Macroscope then by CodeRabbit variants). PR #21524.
  Golden: a mise wrapper script (`mise x claude@2.0.0 -- claude`, or one with a version override or sourced file) runs a version other than the config-selected one, so the resolver's plain `mise which`/active-install probe offers `mise upgrade` for an install the wrapper does not use.
  Base: `6417151c093e54dbba0e6c824c69d03983793b9a`. Head to replay: `db188bf04b11673b7d97b02dd283844992930c3e` (the commit Macroscope commented on, bug still present).
  Caught by: Macroscope (T1), CodeRabbit (T3-T5, later variants).
- `terminal-option-layer-dropped-on-mac` (Track B, escaped). Fix PR #21596, introduced by #7485.
  Golden: `ghosttyConsumedMods` only reports Shift as consumed, so on macOS an Option chord that produces a layout character is sent as Alt+base (`ESC @`) and the character is never typed.
  Base: parent of the #7485 merge, head: `bf93f14d3f5588cf2c3d2df6c036f0d76484f7ce` (last commit of #7485). The base sha was not resolved here; derive it from the PR (unverified). Caught by: none. Confidence low-medium that a reviewer could see it from the diff, because it needs knowledge of macOS Option-layer behaviour.
- Not catalogued: `mac-calendar-usage-description` (#21592, sev 3 but no introducing PR and not visible in a diff).

## 5. Observations

- #21524 shows bots working well on a design hole: four threads over four commits, each variant fixed, ending in a rule rewrite. The cost was one reviewer round per variant instead of a single "enumerate wrapper behaviours" finding.
- CodeRabbit withdrew two findings after the author replied with facts (#21596 T1, #21524 T2). Both were reasonable guesses without the cross-file context.
- On #23486 CodeRabbit proposed fixing the wrong stage (`urlTransform` after sanitizing); the author corrected it from knowledge of the pipeline order.
- Macroscope answered "unable to act, no permissions" to a reply on #21524, i.e. it cannot follow up in this repo; CodeRabbit did.
- Both Track B bugs with sev >= 3 are platform-behaviour bugs (macOS Option layer, Calendar plist) that no diff-only reviewer would see; the earlier PRs had bots running but not on those points.
