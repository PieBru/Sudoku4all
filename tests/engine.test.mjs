/* Engine gate — run: node tests/engine.test.mjs  (no deps).
   Extracts the <script> from ../sudoku.html and exercises the pure game logic
   headless (the `typeof document` guard skips the DOM half). */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const html = readFileSync(new URL("../sudoku.html", import.meta.url), "utf8");
const js = html.match(/<script>([\s\S]*)<\/script>/)[1];
const { N, GROUPS, countSolutions, genFull, makePuzzle, shuffle, validPuzzle } =
  Function(
    js +
      ";return {N,GROUPS,countSolutions,genFull,makePuzzle,shuffle,validPuzzle};",
  )();

const validGrid = (bd) =>
  GROUPS.every((g) => new Set(g.map((i) => bd[i])).size === 9);

/* independent reference counter (deliberately naive) */
function naiveCount(bd, limit) {
  const b = bd.slice();
  let cnt = 0;
  const okAt = (i, v) => {
    const r = (i / 9) | 0,
      c = i % 9;
    for (let k = 0; k < 9; k++) {
      if (k !== c && b[r * 9 + k] === v) return false;
      if (k !== r && b[k * 9 + c] === v) return false;
    }
    const r0 = ((r / 3) | 0) * 3,
      c0 = ((c / 3) | 0) * 3;
    for (let rr = 0; rr < 3; rr++)
      for (let cc = 0; cc < 3; cc++) {
        const j = (r0 + rr) * 9 + c0 + cc;
        if (j !== i && b[j] === v) return false;
      }
    return true;
  };
  const rec = (i) => {
    if (cnt >= limit) return;
    while (i < N && b[i]) i++;
    if (i === N) {
      cnt++;
      return;
    }
    for (let v = 1; v <= 9 && cnt < limit; v++)
      if (okAt(i, v)) {
        b[i] = v;
        rec(i + 1);
        b[i] = 0;
      }
  };
  rec(0);
  return cnt;
}

/* generation validity */
for (let t = 0; t < 100; t++)
  assert.ok(validGrid(genFull()), "genFull invalid");

/* solver vs independent oracle on multi-solution boards */
for (let t = 0; t < 15; t++) {
  const { puz } = makePuzzle(25 + ((Math.random() * 16) | 0));
  const bd = puz.slice();
  for (const i of shuffle([...Array(N).keys()]).slice(0, 6)) bd[i] = 0;
  assert.equal(
    countSolutions(bd, 1000),
    naiveCount(bd, 1000),
    "solver disagrees with naive oracle",
  );
}

/* every difficulty hits its exact clue target, well-posed and consistent */
for (const [name, clues] of Object.entries({
  easy: 40,
  medium: 34,
  hard: 29,
  expert: 25,
})) {
  for (let t = 0; t < 10; t++) {
    const { puz, sol } = makePuzzle(clues);
    assert.equal(
      puz.filter((v) => v > 0).length,
      clues,
      name + ": clue count off",
    );
    assert.ok(validPuzzle(puz), name + ": not well-posed");
    assert.ok(
      validGrid(sol) && puz.every((v, i) => v === 0 || v === sol[i]),
      name + ": solution inconsistent",
    );
  }
}

/* corrupt-save rejection */
const dup = genFull();
dup[1] = dup[0]; /* duplicate given in row 0 */
assert.ok(!validPuzzle(dup), "conflicting givens must be rejected");
assert.ok(!validPuzzle(Array(N).fill(0)), "empty board must be rejected");

console.log("engine tests: all pass");
