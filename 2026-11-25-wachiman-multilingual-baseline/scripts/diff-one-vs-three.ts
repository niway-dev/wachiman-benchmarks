import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
const root = process.argv[2] ?? "/tmp/classify-bench";
const DIFF = ["-c","diff.suppressBlankEmpty=false","diff","-M","--no-ext-diff","--no-textconv","--no-color","--no-relative","--src-prefix=a/","--dst-prefix=b/","--diff-algorithm=default","--indent-heuristic","-O/dev/null"];
const PATCH = ["--inter-hunk-context=1","-U3"];
const git = (dir: string, args: string[]) => { const r = Bun.spawnSync(["git","-C",dir,...args],{maxBuffer:1<<30}); if (r.exitCode) throw new Error(r.stderr.toString()); return r.stdout; };
const med = (xs: number[]) => xs.sort((a,b)=>a-b)[xs.length>>1];
let tot3=0, tot1=0, n=0, mismatch=0; const rows: string[] = [];
for (const id of readdirSync(root)) {
  const d = join(root,id); if (!existsSync(join(d,".base"))) continue;
  const b = readFileSync(join(d,".base"),"utf8").trim(), h = readFileSync(join(d,".head"),"utf8").trim();
  const three = () => Buffer.concat([git(d,[...DIFF,"--raw","-z",b,h]), git(d,[...DIFF,"--numstat","-z",b,h]), git(d,[...DIFF,...PATCH,b,h])]);
  const one = () => git(d,[...DIFF,...PATCH,"--raw","--numstat","-z",b,h]);
  three(); one();
  const t3: number[] = [], t1: number[] = [];
  for (let i=0;i<7;i++){ let s=performance.now(); three(); t3.push(performance.now()-s); s=performance.now(); one(); t1.push(performance.now()-s); }
  const m3=med(t3), m1=med(t1); tot3+=m3; tot1+=m1; n++;
  rows.push(`${id}\t${m3.toFixed(1)}\t${m1.toFixed(1)}\t${(100*(m1-m3)/m3).toFixed(0)}%`);
}
console.log(rows.sort((a,b)=>parseFloat(b.split("\t")[1])-parseFloat(a.split("\t")[1])).slice(0,8).join("\n"));
console.log(`cases ${n}  three ${tot3.toFixed(0)} ms  one ${tot1.toFixed(0)} ms  change ${(100*(tot1-tot3)/tot3).toFixed(0)}%`);
