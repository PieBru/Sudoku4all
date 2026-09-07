/* Training solver gate — run: node tests/training.test.mjs
   Extracts the solver from ../sudoku.html and verifies all 19 detectors on
   fixtures: each board completes under singles + that technique alone, and the
   completion equals the board's unique solution (soundness oracle, FR-003). */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const html = readFileSync(new URL("../sudoku.html", import.meta.url), "utf8");
const js = html.match(/<script>([\s\S]*)<\/script>/)[1];
const { N, GROUPS, TRAIN_TECHNIQUES, solveWithAllowed, countSolutions, genFull, makePuzzle } =
  Function(
    js +
      ";return {N,GROUPS,TRAIN_TECHNIQUES,solveWithAllowed,countSolutions,genFull,makePuzzle};",
  )();

/* independent brute-force solver (oracle): returns the first solution of a
   known-unique board — deliberately shares no code with the technique solver */
function bruteSolve(bd) {
  const b = bd.slice();
  const okAt = (i, v) => {
    const r = (i / 9) | 0, c = i % 9;
    for (let k = 0; k < 9; k++) {
      if (k !== c && b[r * 9 + k] === v) return false;
      if (k !== r && b[k * 9 + c] === v) return false;
    }
    const r0 = ((r / 3) | 0) * 3, c0 = ((c / 3) | 0) * 3;
    for (let dr = 0; dr < 3; dr++) for (let dc = 0; dc < 3; dc++) {
      const j = (r0 + dr) * 9 + c0 + dc;
      if (j !== i && b[j] === v) return false;
    }
    return true;
  };
  const rec = () => {
    let best = -1, bestC = 10;
    for (let i = 0; i < 81; i++) {
      if (b[i]) continue;
      let opts = [];
      for (let v = 1; v <= 9; v++) if (okAt(i, v)) opts.push(v);
      if (opts.length < bestC) { best = i; bestC = opts.length; bestOpts = opts; }
      if (bestC === 0) break;
    }
    if (best < 0) return true;
    if (bestC === 0) return false;
    for (const v of bestOpts) {
      b[best] = v;
      if (rec()) return true;
      b[best] = 0;
    }
    return false;
  };
  let bestOpts = [];
  rec();
  return b;
}

const SINGLES = ["naked_single", "hidden_single"];
/* FR-002: exactly the 19 stable snake_case IDs, cheapest-first order */
assert.deepEqual(TRAIN_TECHNIQUES, [
  "naked_single", "hidden_single",
  "naked_pair", "naked_triple", "naked_quad",
  "hidden_pair", "hidden_triple", "hidden_quad",
  "pointing", "claiming",
  "x_wing", "swordfish", "jellyfish",
  "skyscraper", "two_string_kite", "turbot_fish",
  "xy_wing", "xyz_wing", "w_wing",
]);

/* fixtures: unique-solution boards needing each technique (found via seeded
   random carve + solver search, committed as static data) */
const FIXTURES = {
  "naked_pair": "006007090801060740497251000962008107000009020170000000650000078008000500013005060",
  "naked_triple": "020108709073009400940237008080005602000000900052000080207400005504002000060000040",
  "naked_quad": "605703429009000000020006000700054296090060054006900010072800640300500980000000301",
  "hidden_pair": "000215040204860700500000000341000080028001490750000002000008070000602034060407009",
  "hidden_triple": "019680025805000900000051806008402000006000082000508060003100600000005210007246590",
  "hidden_quad": "000198723020006090000005000007041060600700002010063800100002000083610009006030210",
  "pointing": "902005001430007090070000000020760004600901300010350006000090802000480100040072000",
  "claiming": "180239604030000500700500000300060100050000000040000097410705800800041702070006340",
  "x_wing": "060758003000032040030000105090010062100207009020060700300006524000500010645001080",
  "swordfish": "420000700510040002000710040000003006009500300001000000300860005050097163190200004",
  "jellyfish": "475290800920186040800075030130007280000001304600000100590000020040002000712800400",
  "skyscraper": "080500004006290571007600800804009056005060940060010000008000210702086090000007360",
  "two_string_kite": "040070508083100000007400003050700006000000402000690000001807060306900107000016094",
  "turbot_fish": "028100007160000430035000002000003700957018000300000914000700341514009270000041809",
  "xy_wing": "230040000000007000400032050700803004143000207008700301070056900904201000062070000",
  "xyz_wing": "900000862000002014040081039360007045080300270000506000000000951607000400490003680",
  "w_wing": "309206000500034090074009030620090040900001200030060005040610009005347008003025017"
};

let checked = 0;
for (const [t, puzStr] of Object.entries(FIXTURES)) {
  const puz = [...puzStr].map(Number);
  /* oracle: the board has exactly one solution */
  const cnt = countSolutions(puz, 2);
  assert.equal(cnt, 1, `${t}: fixture not well-posed (${cnt} solutions)`);
  const sol = bruteSolve(puz);
  const r = solveWithAllowed(puz, [...SINGLES, t]);
  /* FR-003 soundness via oracle: completion must equal the unique solution */
  assert.ok(r.completed, `${t}: fixture did not complete (rounds=${r.rounds})`);
  assert.deepEqual(r.board, sol, `${t}: completion diverges from unique solution`);
  /* FR-005: technique appears in used log */
  assert.ok(r.used.includes(t), `${t}: not in used log ${JSON.stringify(r.used)}`);
  /* FR-007: deterministic */
  const r2 = solveWithAllowed(puz, [...SINGLES, t]);
  assert.deepEqual(r2, r, `${t}: nondeterministic result`);
  checked++;
}
console.log(`fixtures: ${checked} techniques verified (completion = unique solution)`);

/* singles are exercised by every fixture; assert they appear in used logs */
const anyR = solveWithAllowed([...FIXTURES.x_wing].map(Number), [...SINGLES, "x_wing"]);
assert.ok(anyR.used.includes("naked_single") || anyR.used.includes("hidden_single"));
console.log("singles: present in used logs");

/* FR-009: restrictability — x_wing fixture completes with x_wing allowed, stuck without */
const fw = [...FIXTURES.x_wing].map(Number);
assert.ok(solveWithAllowed(fw, [...SINGLES, "x_wing"]).completed);
assert.equal(solveWithAllowed(fw, SINGLES).completed, false);
console.log("restrictability: fish fixture stuck under singles alone");

/* FR-006: honest stuck — an expert board under singles alone ends quickly */
const hard = makePuzzle(25).puz;
const rh = solveWithAllowed(hard, SINGLES);
assert.ok(!rh.timeout && rh.rounds < 200, "stuck declaration must be fast");
console.log(`stuck honesty: expert+singles rounds=${rh.rounds} completed=${rh.completed}`);

/* FR-008: guards — empty board returns immediately (no hang) */
const t0 = Date.now();
const re = solveWithAllowed(new Array(81).fill(0), SINGLES);
assert.ok(Date.now() - t0 < 100 && !re.completed);
console.log("loop guards: empty board returns fast");

console.log("training tests: all pass");
