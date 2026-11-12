## Values that cross a boundary

For every value the added lines pass across a file, module or process boundary, open the code
on the other side and record one entry of `contracts` for it. The entry's `evidence` must include
the path:line you opened on the other side. If you could not find that code, set `status` to
"open" and start `open_question` with "not found:" followed by what you searched for. An entry
without a line from the other side does not answer the question. When the other side shows a
defect, report it as a finding as well. A class below that the change does not touch needs no
entry.

1. A timeout, delay or grace period: name every other timer on the same operation (the callee's
   own timeout, a kill or shutdown grace, a retry delay, a drain), each with its path:line and
   value, and compare the numbers. Does the outer bound leave room for the inner ones to finish?
2. An option or argument passed to another module or process: show the line where the callee
   reads it and say what the callee does when it is undefined, null or left at its default.
   Count the call sites that pass it and the ones that do not.
3. A collection or state the change adds to or removes from: list every loop or reader of it,
   each with its path:line, and say what each one now skips or sees twice, in particular a reader
   that runs after the removal.
4. An id, pid, token or session key that is stored and later compared or acted on: name every
   other place that creates one, and say whether it can change, expire or be reused between the
   store and the use.
5. The output of an external command (git, a shell utility, a script): say what it prints on
   empty input, on no match and on blank or unusual lines, and what the consumer does with each.
6. A list sent to a save, sync or delete endpoint: say what happens with two entries that share
   a key, and whether a missing entry is treated differently from an empty one. Name the line on
   the receiving side that decides.
