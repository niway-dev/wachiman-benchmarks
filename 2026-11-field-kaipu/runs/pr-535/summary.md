# kaipu-record [#535](https://github.com/niway-dev/kaipu-record/pull/535) · [`1fb882cd`](https://github.com/niway-dev/kaipu-record/commit/1fb882cd7b110cb57ca84893802d50978e3ba26d)

- **Title:** feat(recorder): ship native cursor capture on by default, flag kept as a kill switch
- **Run:** 2026-11-06T19:03:58Z, locally on the claude.ai subscription (no API key). Costs are API-equivalent estimates.
- **Engine:** Wachiman v1.8.0, `agent-review local`, Haiku 5.5 effort high.
- **Commit reviewed:** the first commit CodeRabbit reviewed
- **Code:** 6 files, +68/−16.
- **CodeRabbit:** 1 inline comment(s) and 1 review(s) on this PR so far (1 inline at the reviewed commit).

## Cost and work

| Step | Model | Calls | Turns | Time | Output | Cache read | Estimate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Propose | Haiku 5.5 high | 1 | 35 | 306 s | 44.1k | 1.4M | $0.25 |
| Filter | code | — | — | — | — | — | $0 |
| Verify | claude-opus-5-5 | 1 | 6 | 28 s | 2.4k | 90.0k | $0.33 |
| Verify | claude-sonnet-5-5 | 1 | 5 | 24 s | 2.9k | 58.2k | $0.16 |

## Findings: 7 candidate(s) after the filters, 0 dropped by them

| id | Haiku said | Finding | opus keeps? | sonnet keeps? |
| --- | --- | --- | --- | --- |
| c1 | consider · bug | `apps/kaipu-record/src/shared/analytics.ts:26` Default-on flag makes every non-macOS take report 'Experimental native capture' | ✅ consider | ✅ consider |
| c2 | consider · bug | `apps/kaipu-record/src/renderer/src/features/recording/recorder-store.ts:523` Packaged builds no longer show why a take fell back to Chromium | ✅ consider | ✅ consider |
| c3 | consider · docs | `apps/documentation/src/content/docs/desktop/analytics-and-flags.mdx:69` Kill switch does not reach users with diagnostics off or no flag response | ✅ consider | ✅ consider |
| c4 | consider · docs | `apps/documentation/src/content/docs/desktop/analytics-and-flags.mdx:58` Flag docs say 'Frame' and omit the watermark exception | ✗ | ✗ |
| c5 | consider · question | `apps/documentation/src/content/docs/backlog/cursor-sprite-capture.md:8` Is the owner gate in ADR 0047 met before the flag goes on by default? | ✅ consider | ✗ |
| c6 | consider · docs | `apps/kaipu-record/src/shared/analytics.ts:19` Stale 'experiments stay off' comment and misleading test name | ✅ info | ✅ info |
| c7 | consider · docs | `apps/documentation/src/content/docs/backlog/cursor-sprite-capture.md:3` Frontmatter description still describes a deferred feature | ✗ | ✗ |

### Reasons: opus

- **c1** keep: Confirmed. ipc.ts:51-61 sets experimentalRequested from the flag before it checks the platform, and recorder-engine.ts:430-433 then reports the fallback. Now that the default is true, every Windows/Linux take hits this path: dev builds show a 10 s toast and packaged builds log a misleading 'Experimental native capture' line.
- **c2** keep: True, and this PR causes it: packaged builds now only console.info the fallback reason, and the console is not collected. Now that native is the default, a missing helper or a failed preparation in the wild leaves no trace in telemetry. Fair to ask whether those error cases should go to captureEvent.
- **c3** keep: Confirmed in analytics-client.ts:77-79: when PostHog has not started (diagnostics off, no key) or returns undefined, the fallback, now true, applies. Those users cannot be switched off remotely, so the doc's 'Every build reads false' overclaims the kill switch.
- **c4** drop: Too minor. 'Frame' is the label users see, and the backlog banner already states the watermark exception. The table row is only a summary.
- **c5** keep: ADR 0047 still says the flag is off (line 21), sets an owner gate for turning it on, and lists 'Turning the flag on' as a non-goal (line 117). This PR turns the flag on without updating the ADR or confirming the gate, which conflicts with the repo's rule that docs stay honest.
- **c6** keep: The doc comment right above the changed default still says 'experiments stay off', which this PR makes false. It is a one-line fix. The complaint about the test name is weaker.
- **c7** drop: This was already stale before the PR, when the status was 'In progress', and the PR does not touch the frontmatter. Too minor to post.

### Reasons: sonnet

- **c1** keep: Confirmed. `capability()` in ipc.ts counts the flag as a request before it checks the platform, and recorder-engine.ts:430 then emits the 'Experimental native capture: using Chromium' message. With the default flipped to true, every Windows or Linux take now hits it. Before, the default was false and it never did. The effect is small (a dev toast, or a console line in packaged builds), but this PR causes it.
- **c2** keep: Valid question. With native capture now the default, a packaged build that falls back to Chromium because the helper is missing or failed to prepare gives the user and the team no signal beyond a console line. Those two cases are errors, not diagnostics, and should reach analytics or keep a user-visible signal.
- **c3** keep: Confirmed from the code shown. `isFlagEnabled` returns the default when PostHog is not started (diagnostics off) or the flag is unresolved (offline), and the default is now true. The doc's claim that 'every build reads false' is therefore too broad, and those users cannot be switched off remotely. The doc should state that scope.
- **c4** drop: Nitpick. 'Frame' is the product label, and the backlog banner already names the watermark exception. The flag table row does not need to repeat either.
- **c5** drop: Speculative. Both ADRs are only Proposed, so nothing accepted is breached. Whether the owner's gate was met is the author's call and not a defect in the diff. Stale ADR status text is too minor for a PR comment.
- **c6** keep: True and caused by this PR. The FLAG_DEFAULTS comment says 'experiments stay off', but the one experiment flag now defaults to on. It is a quick comment fix. The test name is a nitpick.
- **c7** drop: Pre-existing. The description already contradicted the earlier in-progress banner, and this PR only changes the banner's status. It is too minor to comment on.
