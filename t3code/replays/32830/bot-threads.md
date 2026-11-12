# Reference bot threads: pingdotgg/t3code#32830

Original PR: https://github.com/pingdotgg/t3code/pull/32830 (fix(clients): unloaded thread links show their title and project icon), merged 2026-11-08.

Replay: base `e11c2fdca7d1e67b0a9ada3bdbd87314efa78557`, head `f54e7cf3db0def7e4e5b12e05401e7ae9966d9ae`.

These are the CodeRabbit (`coderabbitai`) and Macroscope (`macroscopeapp`) threads raised on the replay head or on a later commit of the PR: 3 of the PR's 3 threads. They are the reference that Wachiman's findings on the replay are compared with. "Claim" is the thread's own headline. "Our verdict" comes from [`batches/2026-11-08/chunk-01.md`](../../batches/2026-11-08/chunk-01.md) (Track A, row T#), as verdict (outcome). The chunk row says whether that verdict was checked in code or judged from the thread text.

| T# | bot | bot severity | path:line | commit | claim | our verdict | url |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | macroscopeapp | High | `apps/mobile/src/state/entities.ts:73` | f54e7cf3 | A pending or failed title lookup returns `"Thread"`, which `resolveThreadLink` treats as proof that the candidate exists; for a v1 link whose target is loaded in another environment, this stops `guessThreadLinkRef` from  | real-bug (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/32830#discussion_r4505111872) |
| 2 | coderabbitai | Minor | `apps/mobile/src/state/entities.ts:69` | f54e7cf3 | Refresh mobile title lookups after shell removals. | real-minor (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/32830#discussion_r4505124915) |
| 3 | coderabbitai | Major | `apps/mobile/src/state/entities.ts:73` | f54e7cf3 | Do not use the fallback title as proof that a thread exists. | real-bug (fixed-before-merge) | [thread](https://github.com/pingdotgg/t3code/pull/32830#discussion_r4505124918) |
