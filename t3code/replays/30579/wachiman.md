# Wachiman 1.12.0 review: replay of pingdotgg/t3code#30579

Transcribed from `wachiman.json` (the `wachiman.review-result/1` output of the run). The CLI cannot render Markdown from a saved result, and a second run would cost a second review, so this file was produced from the JSON with `jq` and not by `wachiman local --format markdown`.

- Change: commit dcb8635 of t3bench-30579 against its parent (91dc71f)
- Head: `dcb8635831860544c038627e9d04bab8a1ce4f2d`, base: `91dc71f71d1b3a7cdcae5e0257f0003c43a803f0`
- Provider: Claude Opus 5.5 via Claude Code 2.1.321, effort high, profile isolated
- Coverage: 7 of 7 changed files reviewed; skipped 0, partial false

## Findings (2)

### W1. Timeline Add to chat does nothing for thread comments the host leaves out of `detail.comments`

- Severity: fix, confidence: high, topic: bug
- Location: `apps/web/src/components/pullRequest/PullRequestTimelineTab.tsx:686`

The timeline handler looks the clicked id up in `detail.comments` only and silently does nothing when it finds no match. `pullRequestConversationItems` notes that "some hosts only include a comment in the thread" and builds a normalized copy for those comments (pullRequestDetail.logic.ts:564-575). The timeline renders that copy, and `commentTimelineEvent` gives it a `body`, so the button appears (line 272). Clicking it then finds nothing: no chip and no toast. The event already carries `comment` (pullRequestDetail.logic.ts:522). Pass `event.comment` to the callback instead of re-finding it by id. `addCommentToChat` already maps a comment to its review thread.

### W2. Pull request reference dedupe matches on number, not URL

- Severity: fix, confidence: medium, topic: bug
- Location: `apps/web/src/components/pullRequest/PullRequestDetailPanel.tsx:1078`

`hasPullRequest` compares only `existing.pullRequest?.number === detail.number`. `buildPullRequestReferenceContext` keys on the URL because "repositories can share pull request numbers" (pullRequestDetail.logic.ts:1138-1139), and `pullRequest.url` is stored on the chip (pullRequestDetail.logic.ts:1124). Suppose the composer already holds a reference to repo A's #42 and the reader adds a remark from repo B's #42. The repo B reference, which carries the untrusted-data notice, is skipped, so the agent reads the remark against the wrong pull request with no visible sign. Compare `existing.pullRequest?.url === detail.url` instead.

