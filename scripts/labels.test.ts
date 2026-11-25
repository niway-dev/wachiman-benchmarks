import { expect, test } from "bun:test";
import { labelledRuns } from "./labels.ts";

test("a run that caught no expected issue is still a labelled run", () => {
  const md = [
    "## Expected issues",
    "",
    "| ID | Issue | W7 | W8 |",
    "|---|---|---|---|",
    "| E1 | A | yes | no |",
    "| E2 | B | partial | no |",
  ].join("\n");
  expect(labelledRuns(md, "doc", "463")).toEqual([
    { run_label: "W7", original_pr: "463", doc: "doc", expected_total: 2, expected_caught: ["E1"], expected_partial: ["E2"] },
    { run_label: "W8", original_pr: "463", doc: "doc", expected_total: 2, expected_caught: [], expected_partial: [] },
  ]);
});
