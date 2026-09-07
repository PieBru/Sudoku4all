# Proposal — Training Studio: boards that train exactly the techniques you choose

Companion to `specs/proposal.md` (the learning ladder) and
`outputs/sudoku-solving-methods-brief.md` (*the Brief*, technique source of
truth). Where the ladder teaches techniques, this proposal delivers the
**practice machine**: the player picks a difficulty level, ticks the
techniques they want to train, and the app builds a Sudoku board that can be
solved using **only** those techniques — nothing harder will ever be needed.

**Status**: proposal v1. §9 lists the decisions this document seals; any of
them can be vetoed before the specs are cut, otherwise they stand.

---

## 1. Goal

Let a player generate training boards tailored to their current ladder rung:

1. Pick a **training level** (Beginner / Basic / Intermediate — the ladder
   tiers; Advanced is planned, see §4).
2. See every technique **up to and including** that level, pre-checked.
   Techniques **ahead** of the level are never included.
3. Uncheck techniques to narrow the training; **All / None** buttons toggle
   the whole current level's group in one click.
4. Press **Generate** → a playable, unique-solution board whose solve path
   stays inside the checked set. Play it now (solution hidden), or **print**
   it (optionally with the solution page).

The feature lives inside the single-file app (`sudoku.html`). The casual
*New game* difficulties (clue-count based) stay untouched — Training is a
separate, additive mode.

## 2. Directives encoded here (from the operator)

| Directive | Where it lands |
| --- | --- |
| Generate boards with or without solution | Output options (§6): play now (hidden) or print with optional solution page |
| Boards train the selected difficulty level: techniques up to it, never ahead | Level semantics + carve-by-solver algorithm (§4, §5) |
| Per-level, per-technique checkboxes | Checklist UI (§6.1) |
| One button enables/disables all techniques of the current level | All / None buttons (§6.1) |

## 3. Why this is buildable (the honest feasibility ladder)

The current engine is a brute-force solution counter — it cannot tell *which*
techniques a board needs. This feature therefore adds a **logical technique
solver**: a deterministic engine that tries detectors cheapest-first (singles
→ pairs → intersections → fish → turbot → wings) and either completes the
grid or gets honestly stuck. That engine makes three guarantees testable:

- a board generated for a checked set **completes** under that set alone
  (exclusivity — the core promise);
- the solution is the real, unique one (cross-checked against the existing
  `countSolutions`);
- the solver can report **which techniques the board actually used**.

Verification cost grows with technique power. Singles through wings are
deterministic pattern detectors — verifiable in v1. Chains (Advanced) require
search, not pattern matching: **v1 ships them visibly disabled with a stated
reason**, rather than pretending to verify them (§4). Nothing silent ships.

## 4. Training levels and the technique checklist

Levels mirror the ladder chapters and map onto the app's casual difficulties
for orientation only:

| Training level | Ladder chapter | ≈ casual difficulty | Techniques (checkboxes) |
| --- | --- | --- | --- |
| **Beginner** | 01 *Your first two tricks* | Easy | naked single*, hidden single* (cross-hatching / full house are the by-hand ways to find a hidden single — said in the label tooltip) |
| **Basic** | 02 *Pairs that talk to each other* | Medium | naked pair/triple/quad, hidden pair/triple/quad, pointing, claiming (8 boxes) |
| **Intermediate** | 03 *Patterns with funny names* | Hard | X-Wing, Swordfish, Jellyfish, skyscraper, 2-string kite, turbot fish, XY-Wing, XYZ-Wing, W-Wing (9 boxes) |
| **Advanced** | 04 *Chains* | Expert | — disabled in v1: "Chain techniques cannot be verified yet — coming in a future version." (loud, never fake) |

\* **Singles are locked on and cannot be unchecked.** Every logical solve —
champions included — ends every step in a placement, and a placement is
always a naked or hidden single; unchecking them would make "solvable with
only my selection" impossible by definition. The UI explains this in one
line at the locked checkboxes.

**Deliberately not in the v1 checklist** (so nothing is silently missing):
finned/sashimi/franken/mutant fish, empty rectangle (the Brief notes
SudokuWiki deprecates it as redundant), WXYZ-wing, the uniqueness family
(UR types, BUG+1, avoidable rectangle), Sue de Coq, remote pairs, the ALS
family, all chains. These are v2 candidates listed in every spec's
Assumptions; they join only when their detectors are verified by gates.

Semantics (sealed): **exclusive, not prescriptive.** A generated board never
needs anything outside the checked set; whether a specific checked technique
is *required* is reported (§6.2) but not guaranteed. "Guaranteed to contain
an X-Wing" is a different, much harder generator — parked for v2.

## 5. Algorithm — carve by allowed set

```text
full  = genFull()                          # existing, gate-verified
board = copy(full)
for cell in shuffled(cell order):          # each non-given cell once
    backup = board[cell]; board[cell] = 0
    if solveWithAllowed(board) completes:  keep the removal
    else:                                 board[cell] = backup
assert countSolutions(board, 2) == 1       # belt and braces; logical
                                          # completion already implies it
report = techniques used by that final solve
```

`solveWithAllowed` runs the cheapest-first detector ladder restricted to the
checked set; "completes" means the grid fills logically. Greedy carving to
minimality is what makes the board actually exercise the level's harder
techniques instead of stopping at an easy plateau.

**Loop guards are mandatory** (project hard rule): every generation run
carries an iteration cap and a wall-clock cap; starting values — ≤ 8 full
attempts, ≤ 5 s total — tuned by the specs. On exhaustion the studio fails
loud: *"Couldn't build a board with only these techniques. Try enabling a
few more."* Never a silent fallback to an unverified board.

## 6. UI and output

### 6.1 Training studio panel

A new collapsible section inside the existing settings menu, following the
app's DOM/ARIA conventions and the every-control-explains-itself rule:

- **Level selector** — three active segmented buttons + Advanced visibly
  disabled with its reason (tooltip + `aria-disabled`).
- **Checklist** — grouped by level, only levels ≤ selected are shown
  (techniques ahead of the level are never displayed, matching "not those
  ahead of it"). Selecting a level pre-checks everything up to and including
  it, restoring each technique's last saved state.
- **All / None** — act on the *currently selected level's group* only.
- **Generate** — builds the board (§5), shows the report, and asks for
  confirmation if a game is in progress (same convention as New game /
  Restart). The generated board becomes the active game.
- **Status line** — reuses the app's `aria-live` status div: progress,
  failure messages (why + what to do + retry), success.

### 6.2 After generation

A one-line **report**: *"This board uses: hidden single, pointing, X-Wing."*
(from the final verification solve — free, we already ran it).

### 6.3 With or without solution

- **Play now** — the generated board is the game; solution hidden as usual.
- **Print** — `@media print` stylesheet + `window.print()`: the grid on one
  page; if *include solution* is checked, the solved grid on a second page.
  Browser-native print-to-PDF covers offline training; zero new code paths
  beyond CSS.

`ponytail: no PNG/text export, no seed sharing in v1 — add when someone asks to exchange boards.`

## 7. Persistence

`localStorage` key **`sudoku-training-v1`** (schema commented at its
definition, per project convention):

```json
{ "level": "intermediate",
  "unchecked": { "basic": ["naked quad"], "intermediate": ["Jellyfish"] } }
```

Saved on every change; restored on open. It never touches the game key
(`sudoku-v1`) or the theme key.

## 8. Slim spec plan and gates

Specs continue the repo's numbering in build order; independent of the
lesson specs 000–008 (may interleave freely).

| Spec | Delivers | Size | Depends on |
| --- | --- | --- | --- |
| `009-training-solver` | pure technique-solver section inside `sudoku.html` (singles → wings, cheapest-first, headless-testable via the existing extraction seam) + `tests/training.test.mjs` | M | — |
| `010-training-generator` | carve-by-allowed-set generator + guards + used-technique report (pure section, same seam) | M | 009 |
| `011-training-ui` | studio panel, checklist, All/None, persistence, confirm-on-generate, report line, print view | M | 010 |

| Gate | Command | Asserts |
| --- | --- | --- |
| Training engine | `node tests/training.test.mjs` | solver: completes ⇒ grid valid and equals `genFull`'s solution; stuck ⇒ declared, never wrong; generator: for random checked subsets (singles always on) the board completes under the subset alone (exclusivity), `countSolutions(board,2)==1`, carve respects iteration + wall-clock caps; perf smoke: Basic median < 1 s, Intermediate median < 3 s over 5 runs |
| Training UI | `uv run python tests/browser.test.py` (new section) | panel opens; level select filters the checklist; checkboxes persist across reload; All/None toggle the current group; singles locked; generate → playable board + correct report; print view shows grid (+ solution page when checked); Advanced disabled with reason; confirm dialog on in-progress games; failures announced via `aria-live` |
| App unharmed | `node tests/engine.test.mjs` and `uv run python tests/browser.test.py` (existing sections) | stay green — casual game flow untouched |

Sabotage culture (one per engine spec): cripple the pointing detector → the
exclusivity test must fail; break the All/None handler → the browser test
must fail. Gates that cannot bite are theater.

## 9. Decisions sealed by this proposal

1. Semantics are **exclusive** (never needs anything outside the checked set); the "guaranteed to require technique X" generator is parked for v2.
2. Naked + hidden singles are locked on, with a one-line explanation in the UI.
3. Training levels are the ladder tiers (Beginner/Basic/Intermediate, Advanced planned); casual clue-count difficulties remain untouched.
4. Advanced (chains) ships disabled with a visible reason — no fake verification.
5. Generation is carve-by-allowed-set with mandatory iteration + wall-clock guards and loud, actionable failure.
6. The v1 checklist is exactly §4's list; absent techniques are named, not silent.
7. The solver and generator are pure sections inside the single-file app — the app stays one file, testable through the existing headless seam.
8. Output is play-now (solution hidden) plus browser-native print with an optional solution page; no file/image export in v1.
9. Preferences persist under `sudoku-training-v1`, schema commented in place, isolated from the game and theme keys.
10. Every generated board keeps the app's existing invariants: unique solution, valid givens, undo/notes/hints all work.
11. Specs 009 → 010 → 011 (solver → generator → UI), independent of 000–008; technique names come from the Brief so the studio and the lessons never disagree.

---

## Appendix A — the exact v1 checklist (spec-ready)

| Level | Checkbox label | Solver rule (one line) | Source |
| --- | --- | --- | --- |
| Beginner | naked single *(locked)* | cell with exactly one candidate → place it | Brief Tier 1 |
| Beginner | hidden single *(locked)* | digit with exactly one cell in a unit → place it | Brief Tier 1 |
| Basic | naked pair / triple / quad | n cells of a unit holding exactly the same n candidates → eliminate those candidates elsewhere in the unit | Brief Tier 2 |
| Basic | hidden pair / triple / quad | n candidates confined to the same n cells of a unit → strip other candidates from those cells | Brief Tier 2 |
| Basic | pointing | digit's box-candidates all in one row/column → eliminate along that row/column outside the box | Brief Tier 2 |
| Basic | claiming | digit's row/column-candidates all in one box → eliminate in the box outside that row/column | Brief Tier 2 |
| Intermediate | X-Wing / Swordfish / Jellyfish | digit confined in n rows (or columns) to the same n columns (or rows) → eliminate along those lines elsewhere | Brief Tier 3 |
| Intermediate | skyscraper | two parallel strong links joined by a weak link → the tip-overlap cells lose the digit | Brief Tier 3 |
| Intermediate | 2-string kite | row strong link + column strong link joined through a box → the overlap cell loses the digit | Brief Tier 3 |
| Intermediate | turbot fish | any two strong links joined by one weak link (general family) → overlap loses the digit | Brief Tier 3 |
| Intermediate | XY-Wing | pivot {x,y} + pincers {x,z},{y,z} → z dies where both pincers see | Brief Tier 3 |
| Intermediate | XYZ-Wing | pivot {x,y,z} + pincers {x,z},{y,z} → z dies where all three see | Brief Tier 3 |
| Intermediate | W-Wing | two non-seeing {x,y} cells joined by an x strong link → y dies where both see | Brief Tier 3 |

Solver order = table order (cheapest first) — the same escalation discipline
the Brief's champion layer teaches.

## Appendix B — localStorage schema

```js
// sudoku-training-v1 — Training Studio preferences.
// level:        "beginner" | "basic" | "intermediate" (Advanced pending v2)
// unchecked:    per level, technique labels the player unticked;
//               singles are structural and never appear here.
// Schema is additive-only; unknown fields are ignored on load (corrupt or
// older saves fall back to defaults loudly in the status line, never
// silently).
```

## Appendix C — extraction-ready skeleton: `specs/009-training-solver/spec.md`

```markdown
# Spec 009 — Training solver (pure section in sudoku.html)

**Status**: 📝 Draft  ·  Source: proposal-training.md §4–§5, Appendix A  ·  Depends: —  ·  Size: M

## Goal
A deterministic technique solver (singles → wings, cheapest-first,
candidate bitmasks) living in sudoku.html's pure-logic section, exercisable
headless by tests/training.test.mjs.

## Requirements
1. Detectors for every Appendix A row; each returns placements/eliminations
   or none — never a wrong move.
2. Solver completes ⇒ grid valid and identical to the known solution;
   stuck ⇒ declares stuck (no brute-force fallback inside the solver).
3. Technique set restrictable per run (checked set); used-technique log kept.
4. All loop guards present (iteration + wall-clock caps).
5. No DOM access; works under the existing Node extraction seam.

## Acceptance (binary)
- node tests/training.test.mjs → exit 0 (oracle cross-checks vs countSolutions)
- node tests/engine.test.mjs && uv run python tests/browser.test.py → exit 0
- Sabotage: comment out the pointing detector → training test exits 1.
```
