# Audit brief: are these review findings true?

An automated code reviewer raised findings on a pull request. For some of them (the `audit_ids`) we need an
independent, sceptical check: **is the claim true in the code, and how much does it matter?** You are not told
whether anyone else agreed with them. Do not review the pull request yourself and do not add findings.

## Inputs for PR `<KEY>` (given in the task)

- `inputs/<KEY>.json`: `checkout` (a directory with the repository at the pull request's head commit),
  `audit_ids` (the findings to audit) and `findings` (all findings on this PR, for context and duplicates).
- `inputs/<KEY>.diff`: the pull request's diff (base to head).

Read only those two files and the `checkout` directory. Do not read anything else in the benchmark repository
(it holds reference answers that would bias the audit). Do not modify the checkout, do not run its tests or
install anything; reading code and `git log`/`git show` inside the checkout is enough.

## Method, per audited finding

1. State the claim in one sentence.
2. Try to **refute** it: open the code it cites, the callers, the types, the tests, the framework contract.
   Look for the guard, the earlier validation or the caller that makes the failure impossible.
3. If you cannot refute it, try to **construct** the failure: a concrete input, state or call path, and what
   goes wrong. Cite file and line for each step.
4. Decide one verdict:
   - `real-defect`: true, introduced or exposed by this PR, and causes wrong behaviour, a crash, data loss, a
     security or concurrency problem for an input or state you can name.
   - `real-minor`: true, but low impact: style, naming, docs, a missing test, a maintainability concern, an
     unlikely edge case with no real consequence, or a problem that existed before this PR.
   - `wrong`: the claim is false; say which code refutes it.
   - `unverifiable`: depends on facts not in the repository (production data, an external service) and you
     could neither refute nor construct it.
5. `duplicate_of`: the id of another finding in `findings` that reports the same root cause, or null.
6. `would_fix`: would a maintainer of this repository change the code because of this comment? yes / no / maybe.

Be strict: `real-defect` needs the named failing path with citations. A plausible-sounding claim you did not
trace is `unverifiable` or `real-minor`, not `real-defect`.

## Output

Write `outputs/<KEY>.json` (valid JSON, nothing else in the file):

```json
{"pr": "<KEY>", "audits": [{"id": 0, "claim": "...", "verdict": "real-defect", "duplicate_of": null,
  "would_fix": "yes", "evidence": "file:line steps, 2 to 5 sentences", "confidence": "high|medium|low"}]}
```

One entry per id in `audit_ids`, no others. Reply with one line: the path written and the verdict counts.
