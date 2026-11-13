# Review focus

Look for the bug in how the changed code behaves at run time, not only in the changed lines.

1. Trace every changed function across files. For each one, open its callers and its callees,
   including unchanged files, and check that each caller passes what the function now expects
   and handles what it now returns or throws. Name any caller that relies on the old behavior.
2. For every process, request, session, lock, timer or permit the change starts or touches,
   list the order of events: start, success, cancel, timeout, retry, failure, and two
   concurrent calls. For each ordering, say what state is left behind and who releases it.
3. For every state the change adds or moves (a set, a flag, a file on disk, a cache entry, a
   token), list each transition and check that every path that should see the state still sees
   it, especially paths that remove an item before another loop reads the collection.
4. When a value crosses a boundary (client to server, TypeScript to shell script, one module's
   timeout to another's grace period, a git command's output to its consumer), check that both
   sides agree on its meaning, including empty, blank, reused and default values.

Report a finding only when you can name the concrete ordering or input that breaks it.
