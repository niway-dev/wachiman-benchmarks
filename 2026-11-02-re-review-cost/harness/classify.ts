#!/usr/bin/env bun
/**
 * Classifies every turn of traced calls (`call-N.jsonl`, Claude Code `stream-json --verbose`).
 *
 *   bun classify.ts <run dir> [<run dir>…]       one JSON summary per run dir on stdout
 *
 * A turn is one assistant message (one API request): Claude Code streams a message's blocks as
 * several `assistant` events with the same `message.id`, and the last one holds its usage. Each
 * turn's tool calls get a class; a turn with several calls splits its weight equally among them.
 *
 * Classes:
 *   read-changed-full     Read of a file of the batch, whole file (no offset/limit)
 *   read-changed-part     Read of a file of the batch with offset/limit
 *   read-unchanged        Read of any other repository file
 *   read-threads          Read of threads.json in the run dir
 *   read-pr               Read of pr.json
 *   read-evidence         Read of evidence.json
 *   search                Grep or Glob
 *   final-output          StructuredOutput: findings, thread replies, contracts, all in one call
 *   no-tool               a turn with no tool call (thinking or text only)
 *
 * Cost per turn: the call's total_cost_usd split over its turns in proportion to each turn's token
 * weight (input 1, 5-minute cache write 1.25, 1-hour cache write 2, cache read 0.1, output 5:
 * the ratios of Anthropic's list prices, so the absolute price does not matter). This is turn
 * attribution: a turn's cost is mostly the context it re-reads, so a big read early makes every
 * later turn dearer. `resultChars` per class is the other view: what each class put into context.
 *
 * `contextCostUsd` is the third view, closer to what is billed: the prompt (written once, re-read by
 * every request), each tool result's tokens (written once, re-read by every later request), and
 * the output tokens, at prices fitted to these calls (cache write 6.25, cache read 0.5, output 25
 * USD per million tokens). It does not include the system prompt's shared cache read beyond the
 * first request's, so it sums a little under the reported total.
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

type Usage = {
  input_tokens?: number;
  output_tokens?: number;
  cache_read_input_tokens?: number;
  cache_creation_input_tokens?: number;
  cache_creation?: { ephemeral_5m_input_tokens?: number; ephemeral_1h_input_tokens?: number };
};

const weight = (u: Usage) => {
  const c5 = u.cache_creation?.ephemeral_5m_input_tokens;
  const c1 = u.cache_creation?.ephemeral_1h_input_tokens;
  const write =
    c5 !== undefined || c1 !== undefined ? (c5 ?? 0) * 1.25 + (c1 ?? 0) * 2 : (u.cache_creation_input_tokens ?? 0) * 1.25;
  return (u.input_tokens ?? 0) + write + (u.cache_read_input_tokens ?? 0) * 0.1 + (u.output_tokens ?? 0) * 5;
};

function batchFiles(prompt: string) {
  const m = prompt.match(/This part holds exactly these files[^\n]*\n([\s\S]*?)\n\n/);
  return new Set(
    (m?.[1] ?? "")
      .split("\n")
      .map((l) => l.match(/^- (.+?) \+\d+ −\d+$/)?.[1])
      .filter((x): x is string => !!x),
  );
}

function classify(name: string, input: Record<string, unknown>, files: Set<string>) {
  if (name === "Grep" || name === "Glob") return "search";
  if (name === "StructuredOutput") return "final-output";
  if (name !== "Read") return `other:${name}`;
  const path = String(input.file_path ?? "");
  if (/agent-review-[^/]+\/threads\.json$/.test(path)) return "read-threads";
  if (/agent-review-[^/]+\/pr\.json$/.test(path)) return "read-pr";
  if (/agent-review-[^/]+\/evidence\.json$/.test(path)) return "read-evidence";
  const rel = path.replace(/^.*\/kaipu-[0-9a-f]{7}\//, "");
  if (files.has(rel)) return input.offset !== undefined || input.limit !== undefined ? "read-changed-part" : "read-changed-full";
  return "read-unchanged";
}

export function summarise(runDir: string) {
  const calls = readdirSync(runDir)
    .filter((f) => /^call-\d+\.jsonl$/.test(f))
    .sort();
  const byClass: Record<string, { turns: number; costUsd: number; calls: number; resultChars: number }> = {};
  const add = (k: string, turns: number, cost: number, n = 0, chars = 0) => {
    const e = (byClass[k] ??= { turns: 0, costUsd: 0, calls: 0, resultChars: 0 });
    e.turns += turns;
    e.costUsd += cost;
    e.calls += n;
    e.resultChars += chars;
  };
  const ctx: Record<string, number> = {};
  const addCtx = (k: string, usd: number) => void (ctx[k] = (ctx[k] ?? 0) + usd);
  let totalCost = 0;
  let totalTurns = 0;
  const perCall: unknown[] = [];
  const timeline: string[] = [];
  for (const f of calls) {
    const n = f.match(/\d+/)![0];
    // The wrapper's copy of the prompt; the published runs keep only the engine's prompt-N.txt.
    const promptPath = [`call-${n}.prompt.txt`, `prompt-${n}.txt`].map((f) => join(runDir, f)).find((f) => existsSync(f))!;
    const prompt = readFileSync(promptPath, "utf8");
    const files = batchFiles(prompt);
    const events = readFileSync(join(runDir, f), "utf8")
      .split("\n")
      .filter(Boolean)
      .map((l) => JSON.parse(l));
    const result = events.filter((e) => e.type === "result").at(-1);
    if (!result) continue;
    const turns = new Map<string, { usage: Usage; tools: { id: string; name: string; input: Record<string, unknown> }[] }>();
    const resultSize = new Map<string, number>();
    for (const e of events) {
      if (e.type === "assistant" && e.message?.id) {
        const t = turns.get(e.message.id) ?? { usage: {}, tools: [] };
        t.usage = e.message.usage ?? t.usage;
        for (const b of e.message.content ?? [])
          if (b.type === "tool_use") t.tools.push({ id: b.id, name: b.name, input: b.input ?? {} });
        turns.set(e.message.id, t);
      }
      if (e.type === "user")
        for (const b of e.message?.content ?? [])
          if (b.type === "tool_result") {
            const c = b.content;
            const text = typeof c === "string" ? c : Array.isArray(c) ? c.map((x: { text?: string }) => x.text ?? "").join("") : "";
            resultSize.set(b.tool_use_id, text.length);
          }
    }
    const list = [...turns.values()];
    // Context view: the cache write of request k+1 holds what request k's tools returned (and its
    // output); it is split among those tool results by size, and each result is then re-read by
    // every later request. Prices fitted to these calls' reported totals (USD per token).
    const P = { write1h: 6.25e-6, read: 0.5e-6, out: 25e-6 };
    list.forEach((t, k) => {
      const next = list[k + 1];
      const later = list.length - (k + 2);
      const chars = t.tools.map((tool) => resultSize.get(tool.id) ?? 0);
      const total = chars.reduce((a, b) => a + b, 0);
      if (k === 0) {
        const w = t.usage.cache_creation_input_tokens ?? 0;
        addCtx("prompt", w * P.write1h + w * P.read * (list.length - 1) + (t.usage.cache_read_input_tokens ?? 0) * P.read * list.length);
      }
      if (!next || total === 0) return;
      const w = next.usage.cache_creation_input_tokens ?? 0;
      t.tools.forEach((tool, i) => {
        const tok = (w * chars[i]) / total;
        addCtx(classify(tool.name, tool.input, files), tok * P.write1h + tok * P.read * Math.max(later, 0));
      });
    });
    addCtx("output", (result.usage?.output_tokens ?? 0) * P.out);
    const sum = list.reduce((s, t) => s + weight(t.usage), 0) || 1;
    const cost = result.total_cost_usd ?? 0;
    totalCost += cost;
    totalTurns += result.num_turns ?? list.length;
    list.forEach((t, i) => {
      const c = (weight(t.usage) / sum) * cost;
      if (t.tools.length === 0) {
        add("no-tool", 1, c);
        timeline.push(`call ${n} turn ${i + 1}: (no tool) $${c.toFixed(3)}`);
        return;
      }
      const share = 1 / t.tools.length;
      const labels: string[] = [];
      for (const tool of t.tools) {
        const k = classify(tool.name, tool.input, files);
        add(k, share, c * share, 1, resultSize.get(tool.id) ?? 0);
        const target = String(tool.input.file_path ?? tool.input.pattern ?? "").replace(/^.*\/kaipu-[0-9a-f]{7}\//, "").replace(/^.*agent-review-[^/]+\//, "");
        const range = tool.input.offset !== undefined ? ` @${tool.input.offset}+${tool.input.limit ?? ""}` : "";
        labels.push(`${k}${tool.name === "StructuredOutput" ? "" : ` ${target}${range}`} (${resultSize.get(tool.id) ?? 0} ch)`);
      }
      timeline.push(`call ${n} turn ${i + 1}: $${c.toFixed(3)} ${labels.join(" | ")}`);
    });
    const so = result.structured_output ?? {};
    perCall.push({
      call: Number(n),
      turns: result.num_turns,
      assistantMessages: list.length,
      costUsd: cost,
      terminal: result.terminal_reason ?? result.subtype,
      durationMs: result.duration_ms,
      outputTokens: result.usage?.output_tokens,
      cacheRead: result.usage?.cache_read_input_tokens,
      cacheWrite: result.usage?.cache_creation_input_tokens,
      finalChars: {
        findings: JSON.stringify(so.findings ?? []).length,
        thread_replies: JSON.stringify(so.thread_replies ?? []).length,
        contracts: JSON.stringify(so.contracts ?? []).length,
        summary: String(so.summary ?? "").length,
      },
      findings: (so.findings ?? []).length,
      threadReplies: (so.thread_replies ?? []).length,
      contracts: (so.contracts ?? []).length,
    });
  }
  return { runDir, totalCost, totalTurns, byClass, contextCostUsd: ctx, perCall, timeline };
}

if (import.meta.main) {
  for (const d of process.argv.slice(2)) console.log(JSON.stringify(summarise(d), null, 2));
}
