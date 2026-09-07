/* Training solver gate — run: node tests/training.test.mjs
   Extracts the solver from ../sudoku.html and verifies all 19 detectors on
   fixtures: each board completes under singles + that technique alone, and the
   completion equals the board's unique solution (soundness oracle, FR-003). */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const html = readFileSync(new URL("../sudoku.html", import.meta.url), "utf8");
const js = html.match(/<script>([\s\S]*)<\/script>/)[1];
const {
  GROUPS,
  TRAIN_TECHNIQUES,
  solveWithAllowed,
  countSolutions,
  makePuzzle,
  generateTrainingBoard,
  TRAIN_BUDGET_MSG,
  trainDetectors,
} = Function(
  js +
    ";return {GROUPS,TRAIN_TECHNIQUES,solveWithAllowed,countSolutions,makePuzzle,generateTrainingBoard,TRAIN_BUDGET_MSG,trainDetectors};",
)();

/* independent brute-force solver (oracle): returns the first solution of a
   known-unique board — deliberately shares no code with the technique solver */
function bruteSolve(bd) {
  const b = bd.slice();
  const okAt = (i, v) => {
    const r = (i / 9) | 0,
      c = i % 9;
    for (let k = 0; k < 9; k++) {
      if (k !== c && b[r * 9 + k] === v) return false;
      if (k !== r && b[k * 9 + c] === v) return false;
    }
    const r0 = ((r / 3) | 0) * 3,
      c0 = ((c / 3) | 0) * 3;
    for (let dr = 0; dr < 3; dr++)
      for (let dc = 0; dc < 3; dc++) {
        const j = (r0 + dr) * 9 + c0 + dc;
        if (j !== i && b[j] === v) return false;
      }
    return true;
  };
  const rec = () => {
    let best = -1,
      bestC = 10;
    for (let i = 0; i < 81; i++) {
      if (b[i]) continue;
      const opts = [];
      for (let v = 1; v <= 9; v++) if (okAt(i, v)) opts.push(v);
      if (opts.length < bestC) {
        best = i;
        bestC = opts.length;
        bestOpts = opts;
      }
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
  "naked_single",
  "hidden_single",
  "naked_pair",
  "naked_triple",
  "naked_quad",
  "hidden_pair",
  "hidden_triple",
  "hidden_quad",
  "pointing",
  "claiming",
  "x_wing",
  "swordfish",
  "jellyfish",
  "skyscraper",
  "two_string_kite",
  "turbot_fish",
  "xy_wing",
  "xyz_wing",
  "w_wing",
]);

/* fixtures: unique-solution boards needing each technique (found via seeded
   random carve + solver search, committed as static data) */
const FIXTURES = {
  naked_pair:
    "006007090801060740497251000962008107000009020170000000650000078008000500013005060",
  naked_triple:
    "020108709073009400940237008080005602000000900052000080207400005504002000060000040",
  naked_quad:
    "605703429009000000020006000700054296090060054006900010072800640300500980000000301",
  hidden_pair:
    "000215040204860700500000000341000080028001490750000002000008070000602034060407009",
  hidden_triple:
    "019680025805000900000051806008402000006000082000508060003100600000005210007246590",
  hidden_quad:
    "000198723020006090000005000007041060600700002010063800100002000083610009006030210",
  pointing:
    "902005001430007090070000000020760004600901300010350006000090802000480100040072000",
  claiming:
    "180239604030000500700500000300060100050000000040000097410705800800041702070006340",
  x_wing:
    "060758003000032040030000105090010062100207009020060700300006524000500010645001080",
  swordfish:
    "420000700510040002000710040000003006009500300001000000300860005050097163190200004",
  jellyfish:
    "475290800920186040800075030130007280000001304600000100590000020040002000712800400",
  skyscraper:
    "080500004006290571007600800804009056005060940060010000008000210702086090000007360",
  two_string_kite:
    "040070508083100000007400003050700006000000402000690000001807060306900107000016094",
  turbot_fish:
    "028100007160000430035000002000003700957018000300000914000700341514009270000041809",
  xy_wing:
    "230040000000007000400032050700803004143000207008700301070056900904201000062070000",
  xyz_wing:
    "900000862000002014040081039360007045080300270000506000000000951607000400490003680",
  w_wing:
    "309206000500034090074009030620090040900001200030060005040610009005347008003025017",
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
  assert.deepEqual(
    r.board,
    sol,
    `${t}: completion diverges from unique solution`,
  );
  /* FR-005: technique appears in used log */
  assert.ok(
    r.used.includes(t),
    `${t}: not in used log ${JSON.stringify(r.used)}`,
  );
  /* FR-007: deterministic */
  const r2 = solveWithAllowed(puz, [...SINGLES, t]);
  assert.deepEqual(r2, r, `${t}: nondeterministic result`);
  checked++;
}
console.log(
  `fixtures: ${checked} techniques verified (completion = unique solution)`,
);

/* singles are exercised by every fixture; assert they appear in used logs */
const anyR = solveWithAllowed([...FIXTURES.x_wing].map(Number), [
  ...SINGLES,
  "x_wing",
]);
assert.ok(
  anyR.used.includes("naked_single") || anyR.used.includes("hidden_single"),
);
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
console.log(
  `stuck honesty: expert+singles rounds=${rh.rounds} completed=${rh.completed}`,
);

/* FR-008: guards — empty board returns immediately (no hang) */
const t0 = Date.now();
const re = solveWithAllowed(new Array(81).fill(0), SINGLES);
assert.ok(Date.now() - t0 < 100 && !re.completed);
console.log("loop guards: empty board returns fast");

/* ============ spec 010: generator gate ============ */
const BASIC = [
  "naked_pair",
  "naked_triple",
  "naked_quad",
  "hidden_pair",
  "hidden_triple",
  "hidden_quad",
  "pointing",
  "claiming",
];
const INTER = [
  "x_wing",
  "swordfish",
  "jellyfish",
  "skyscraper",
  "two_string_kite",
  "turbot_fish",
  "xy_wing",
  "xyz_wing",
  "w_wing",
];
let gs = 1234; /* seeded RNG: reproducible gate */
const grand = () => {
  gs = (gs * 1103515245 + 12345) & 0x7fffffff;
  return gs / 0x7fffffff;
};
const dropN = (arr, n) => {
  const a = arr.slice();
  for (let k = 0; k < n; k++) a.splice((grand() * a.length) | 0, 1);
  return a;
};
/* SC-001: random checked subsets across levels; every generated board
   completes under its subset alone, within the wall-clock guard */
let boards = 0;
for (let it = 0; it < 40 && boards < 12; it++) {
  const inter = grand() < 0.5;
  const level = inter ? INTER : BASIC;
  const drops = grand() < 0.5 ? 1 : 2;
  const checked = [...SINGLES, ...dropN(level, drops)];
  const target = inter ? 29 : 34;
  let res;
  try {
    res = generateTrainingBoard(checked, target);
  } catch {
    continue;
  } /* a starved subset may loudly exhaust its budget: redraw */
  const again = solveWithAllowed(res.board, checked);
  assert.ok(
    again.completed,
    "SC-001: board must complete under its subset alone",
  );
  assert.ok(
    again.board.every((v, i) => v === res.solution[i]),
    "SC-001: completion = solution",
  );
  assert.ok(
    res.clues <= target,
    `SC-001: clue floor violated (${res.clues} > ${target})`,
  );
  assert.equal(countSolutions(res.board, 2), 1, "SC-001: unique solution");
  assert.deepEqual(
    res.given,
    res.board.map((v) => v !== 0),
    "SC-001: given flags match board",
  );
  boards++;
}
assert.ok(boards >= 12, `SC-001: only ${boards} subsets generated`);
console.log(
  `SC-001: ${boards} random-subset boards verified exclusive + unique`,
);

/* SC-002: default Basic checks — at least 4 of 5 reports include a non-single.
   Budget exhaustion is a legal failure mode (spec 010), so collect 5
   successful builds from up to 10 attempts. */
let nonSingleReports = 0,
  reports = 0;
for (let k = 0; k < 10 && reports < 5; k++) {
  let r;
  try {
    r = generateTrainingBoard([...SINGLES, ...BASIC], 34);
  } catch {
    continue;
  } /* budget: legal, just not a report */
  reports++;
  if (r.report.some((t) => BASIC.includes(t))) nonSingleReports++;
}
assert.ok(
  reports === 5,
  `SC-002: only ${reports} successful builds in 10 attempts`,
);
assert.ok(
  nonSingleReports >= 4,
  `SC-002: only ${nonSingleReports}/5 reports with non-single`,
);
console.log(`SC-002: default Basic exercise-bias ${nonSingleReports}/5`);

/* FR-004: budget exhaustion fails loudly with the exact message, no board */
let threw = null;
try {
  generateTrainingBoard(SINGLES, 34, {
    attempts: 1,
    runsPerAttempt: 3,
    wallMs: 2000,
  });
} catch (e) {
  threw = e.message;
}
assert.ok(
  threw !== null && threw.startsWith(TRAIN_BUDGET_MSG),
  `budget message wrong: ${threw}`,
);
console.log("budget exhaustion: exact message, no board returned");

/* FR-003: tripwire — an unsound detector that completes boards wrongly must
   abort loudly with no retry (planted at test time, then restored) */
{
  const real = trainDetectors.pointing;
  /* unsound plant: find two bi-value cells in one unit and kill one digit of
     one of them — the pair then swaps values, completing to a WRONG grid */
  trainDetectors.pointing = (cand) => {
    for (let i = 0; i < 81; i++) {
      if (!cand[i]) continue;
      const ci = cand[i];
      if (ci & (ci - 1)) continue; /* not bi-value */
      for (const j of GROUPS[i]) {
        const cj = cand[j];
        if (cj === ci && j > i) return { elims: [[i, ci]] };
      }
    }
    return null;
  };
  let trips = 0,
    cleanReturns = 0,
    budgetThrows = 0;
  for (let k = 0; k < 6; k++) {
    try {
      const r = generateTrainingBoard([...SINGLES, ...BASIC], 34);
      /* any return under an unsound detector must still be a correct board */
      const cnt = countSolutions(r.board, 2);
      assert.ok(
        cnt === 1 && r.board.every((v, i) => v === r.solution[i] || r.given[i]),
        "tripwire: unsound plant returned a corrupted board",
      );
      cleanReturns++;
    } catch (e) {
      if (/tripwire/.test(e.message)) trips++;
      else if (/Try enabling/.test(e.message)) budgetThrows++;
      else throw e;
    }
  }
  trainDetectors.pointing = real;
  assert.ok(
    trips >= 1,
    `tripwire never fired (trips=${trips}, clean=${cleanReturns}, budget=${budgetThrows})`,
  );
  /* and after restore, generation works again (no retry state leaked) */
  const ok = generateTrainingBoard([...SINGLES, ...BASIC], 34);
  assert.ok(ok.clues <= 34);
  console.log(
    `tripwire: fired ${trips}/6 unsound runs, aborted loudly, restore clean`,
  );
}

console.log("training tests: all pass");
