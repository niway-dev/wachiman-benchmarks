import { expect, test } from "bun:test";
import { martianRow, parseRunName } from "./martian-runs.ts";

test("parseRunName reads version, model, effort, repeat and verifier", () => {
  expect(parseRunName("2026-11-12-v1.9.0-sonnet-5-5-high-r2")).toEqual({
    date: "2026-11-12", version: "v1.9.0", model: "claude-sonnet-5-5", effort: "high", repeat: 2, verifier: "",
  });
  expect(parseRunName("2026-11-07-v1.9.0-opus-5-5")).toMatchObject({ model: "claude-opus-5-5", effort: "", repeat: 1 });
  expect(parseRunName("2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier")).toMatchObject({
    version: "v1.10.0", model: "claude-haiku-5-5", effort: "high", verifier: "claude-opus-5-5",
  });
  expect(parseRunName("2026-11-11-keycloak-range-fix")).toBeNull();
});

test("martianRow flattens metrics and marks partial runs", () => {
  const metrics = {
    quality: { all: { tp: 121, fp: 196, fn: 52, precision: 0.381703, recall: 0.699422, f1: 0.493877, hc: 54, hc_total: 66, prs: 50 } },
    product_cost: { findings: 306, total_usd: 16.5377884, per_pr_median_usd: 0.2387088, per_pr_p90_usd: 0.4352692, per_hc_found_usd: 0.3062553, minutes_median: 1.28595, minutes_max: 8.02 },
    judge_cost: { usd: 107.9622 },
  };
  const row = martianRow("2026-11-26-v1.22.0-sonnet-5-5-high", metrics);
  expect(row).toMatchObject({ version: "v1.22.0", full_run: true, precision: 0.3817, hc_recall: 0.8182, cost_usd: 16.5378, minutes_median: 1.29, judge_cost_usd: 107.96 });
  const partial = martianRow("2026-11-11-keycloak-range-fix", { quality: { all: { prs: 2 } } });
  expect(partial).toMatchObject({ version: "", model: "", full_run: false, date: "2026-11-11", prs: 2 });
});
