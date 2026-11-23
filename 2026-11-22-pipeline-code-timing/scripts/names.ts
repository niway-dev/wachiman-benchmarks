// Prints the distinct evidence names every batch of a commit would search, one per line.
const [src, repoDir, commit] = process.argv.slice(2);
const { buildLocalInput } = await import(`${src}/connectors/local-git.ts`);
const eng = await import(`${src}/engine.ts`); const ev = await import(`${src}/evidence.ts`); const { loadConfig } = await import(`${src}/config.ts`);
const input = buildLocalInput({ repoDir, commit, paths: [], log: () => {}, warn: () => {} }).input;
const config = loadConfig({}, () => {});
const kept = eng.filterFiles(input.files, [...eng.DEFAULT_EXCLUDE, ...config.exclude], input.scope).kept;
const batches = eng.planBatches(kept, { maxLines: config.batchLines, maxChars: config.batchChars }, input.pathRules);
const names = new Set<string>();
for (const b of batches) for (const s of ev.planEvidence(b.files.map((f: any) => ({ filename: f.filename, addedLines: ev.addedLinesOf(f.patch) }))).symbols) names.add(s.name);
console.log([...names].join("\n"));
