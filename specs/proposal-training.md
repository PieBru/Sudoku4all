# Proposal — Training Studio: boards that train exactly the techniques you choose

Companion to `specs/proposal.md` (the learning ladder) and
`outputs/sudoku-solving-methods-brief.md` (*the Brief*, technique source of
truth). Where the ladder teaches techniques, this proposal delivers the
**practice machine**: the player picks a difficulty level, ticks the
techniques they want to train, and the app builds a Sudoku board that can be
solved using **only** those techniques — nothing harder will ever be needed.

**Status**: proposal v2 (adversarial revision of v1: two-phase carve with
clue targets and exercise bias replacing greedy-to-minimality — §5; the
uniqueness assert reframed as the detector-soundness tripwire — §5; stable
technique IDs — §7, Appendix A; deterministic sabotages — §8). §9 lists the
decisions this document seals; any of them can be vetoed before the specs
are cut, otherwise they stand.

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
   stays inside the checked set, sized like the casual difficulty it maps
   to. Play it now (solution hidden), or **print** it (optionally with the
   solution page).

The feature lives inside the single-file app (`sudoku.html`). The casual
*New game* difficulties (clue-count based) stay untouched — Training is a
separate, additive mode.

## 2. Directives encoded here (from the operator)

| Directive | Where it lands |
| --- | --- |
| Generate boards with or without solution | Output options (§6): play now (hidden) or print with optional solution page |
| Boards train the selected difficulty level: techniques up to it, never ahead | Level semantics + two-phase carve (§4, §5) |
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
- the solution is the real, unique one (completion equals the carved grid's
  own solution — see the tripwire below);
- the solver can report **which techniques the board actually used**.

One honesty note that v1 glossed over: the first two guarantees hold **only
if every detector is sound** — a detector that eliminates a candidate
present in some solution would "complete" to a wrong grid. Soundness is
therefore guarded explicitly: every generated board passes a final
`countSolutions(board, 2) == 1` check (§5), and that check failing means
*engine bug* — it aborts loudly, never retries (re-running a bug is not a
strategy).

Verification cost grows with technique power. Singles through wings are
deterministic pattern detectors — verifiable in v1. Chains (Advanced) require
search, not pattern matching: **v1 ships them visibly disabled with a stated
reason**, rather than pretending to verify them (§4). Nothing silent ships.

## 4. Training levels and the technique checklist

Levels mirror the ladder chapters; each carries a **carve target** — the
clue count generation aims for, reusing the app's own casual `CLUES` table
(`sudoku.html`, easy 40 / medium 34 / hard 29 / expert 25) so a training
board *feels* like its casual counterpart:

| Training level | Ladder chapter | ≈ casual difficulty (carve target) | Techniques (checkboxes) |
| --- | --- | --- | --- |
| **Beginner** | 01 *Your first two tricks* | Easy (40 clues) | naked single*, hidden single* (cross-hatching / full house are the by-hand ways to find a hidden single — said in the label tooltip) |
| **Basic** | 02 *Pairs that talk to each other* | Medium (34 clues) | naked pair/triple/quad, hidden pair/triple/quad, pointing, claiming (8 boxes) |
| **Intermediate** | 03 *Patterns with funny names* | Hard (29 clues) | X-Wing, Swordfish, Jellyfish, skyscraper, 2-string kite, turbot fish, XY-Wing, XYZ-Wing, W-Wing (9 boxes) |
| **Advanced** | 04 *Chains* | Expert (25 clues) | — disabled in v1: "Chain techniques cannot be verified yet — coming in a future version." (loud, never fake) |

Targets are **floors, not promises**: carving stops when the target is
reached, or earlier-still — at whatever clue count the allowed set can no
longer carve deeper (an Intermediate set often cannot reach 29 clues without
needing chains; a 31-clue board that never leaves the checked set is the
correct outcome, not a failure).

\* **Singles are locked on and cannot be unchecked.** Every logical solve —
champions included — ends every step in a placement, and a justified
placement is always a naked or hidden single; unchecking them would make
"solvable with only my selection" impossible by definition. The UI explains
this in one line at the locked checkboxes.

**Deliberately not in the v1 checklist** (so nothing is silently missing):
finned/sashimi/franken/mutant fish, empty rectangle (the Brief notes
SudokuWiki deprecates it as redundant), WXYZ-wing, the uniqueness family
(UR types, BUG+1, avoidable rectangle), Sue de Coq, remote pairs, the ALS
family, all chains. These are v2 candidates listed in every spec's
Assumptions; they join only when their detectors are verified by gates.

Semantics (sealed): **exclusive, not prescriptive.** A generated board never
needs anything outside the checked set; whether a specific checked technique
is *required* is reported (§6.2) but not guaranteed. "Guaranteed to contain
an X-Wing" is a different, much harder generator — parked for v2. What v1
*does* promise, beyond exclusivity, is the **exercise bias** of §5: when
non-single techniques are checked, the board will exercise at least one of
them, or generation fails loudly.

## 5. Algorithm — two-phase carve by allowed set

```text
full  = genFull()                          # existing, gate-verified
board = copy(full)

# Phase A — carve down to the level's clue target
for cell in shuffled(cells of full):       # each cell considered once
    if clues(board) == TARGET: break
    backup = board[cell]; board[cell] = 0
    if solveWithAllowed(board) completes:  keep the removal
    else:                                 board[cell] = backup

# Phase B — exercise bias (only if >= 1 non-single technique is checked)
if no checked non-single technique contributed to the final solve:
    keep carving past the target (same rule) until one contributes
    or no removal keeps allowed-solvability

assert countSolutions(board, 2) == 1       # detector-soundness tripwire:
                                          # failure = engine bug = loud abort,
                                          # never a retry, never a silent board
report = techniques used by that final solve
```

`solveWithAllowed` runs the cheapest-first detector ladder restricted to the
checked set and keeps its own candidate grid (the player's notes are
irrelevant to it); "completes" means the grid fills logically. Phase A sizes
the board like its casual difficulty; Phase B is what makes it *training*:
without it, a target-sized board is usually singles-only and the player who
checked "pointing" would silently practice Beginner again.

Retry triggers, enumerated: (a) Phase B cannot find exercise within its
budget → new attempt (fresh `genFull`, fresh shuffle); (b) the uniqueness
tripwire fires → loud abort, no retry (engine bug); (c) attempt/wall-clock
budget exhausted → loud failure: *"Couldn't build a board with only these
techniques. Try enabling a few more."* Never a silent fallback to an
unverified board.

**Loop guards are mandatory** (project hard rule): every generation run
carries an iteration cap and a wall-clock cap; starting values — ≤ 8 full
attempts, ≤ 5 s total, ≤ 60 solver runs per attempt — tuned by the specs.

## 6. UI and output

### 6.1 Training studio panel

A new collapsible section inside the existing settings menu, following the
app's DOM/ARIA conventions and the every-control-explains-itself rule:

- **Level selector** — three active segmented buttons + Advanced visibly
  disabled with its reason (tooltip + `aria-disabled`).
- **Checklist** — grouped by level, only levels ≤ selected are shown
  (techniques ahead of the level are never displayed, matching "not those
  ahead of it"). Switching level defaults that level's group to all-checked,
  **except where the player has saved unchecks — saved state always wins**.
- **All / None** — act on the *currently selected level's group* only. At
  Beginner both are disabled: the group is the two locked singles.
- **Generate** — builds the board (§5), shows the report, and asks for
  confirmation if a game is in progress (same convention as New game /
  Restart). The generated board becomes the active game.
- **Status line** — reuses the app's `aria-live` status div: progress,
  failure messages (why + what to do + retry), success.

Unchecking a whole level's boxes is legitimate and documented in the UI: it
trains the levels *below* at this level's carve depth.

### 6.2 After generation

A one-line **report**, honestly labeled as the solver's own path: *"Solve
path (easiest techniques first): hidden single, pointing, X-Wing."* (from
the final verification solve — free, we already ran it).

### 6.3 With or without solution

- **Play now** — the generated board is the game; solution hidden as usual.
- **Print** — `@media print` stylesheet + `window.print()`: the grid on one
  page; if *include solution* is checked, the solved grid on a second page.
  Browser-native print-to-PDF covers offline training; zero new code paths
  beyond CSS.

`ponytail: no PNG/text export, no seed sharing in v1 — add when someone asks to exchange boards.`

## 7. Persistence

`localStorage` key **`sudoku-training-v1`** (schema commented at its
definition, per project convention). Techniques are stored by **stable
snake_case ID** (Appendix A) — never by display label, so renaming a label
or fixing its capitalization cannot orphan a save:

```json
{ "level": "intermediate",
  "unchecked": { "basic": ["naked_quad"], "intermediate": ["jellyfish"] } }
```

Saved on every change; restored on open. It never touches the game key
(`sudoku-v1`) or the theme key. Unknown fields are ignored on load; corrupt
or older saves fall back to defaults loudly in the status line, never
silently.

## 8. Slim spec plan and gates

Specs continue the repo's numbering in build order; independent of the
lesson specs 000–008 (may interleave freely).

| Spec | Delivers | Size | Depends on |
| --- | --- | --- | --- |
| `009-training-solver` | pure technique-solver section inside `sudoku.html` (singles → wings, cheapest-first, headless-testable via the existing extraction seam) + `tests/training.test.mjs` | M | — |
| `010-training-generator` | two-phase carve generator + guards + used-technique report (pure section, same seam) | M | 009 |
| `011-training-ui` | studio panel, checklist, All/None, persistence, confirm-on-generate, report line, print view | M | 010 |

| Gate | Command | Asserts |
| --- | --- | --- |
| Training engine | `node tests/training.test.mjs` | solver: per-technique fixture boards complete using only their technique + singles, and completions equal the board's unique solution (via `countSolutions`); stuck ⇒ declared, never wrong. Generator: for random checked subsets (singles always on) the board completes under the subset alone (exclusivity), passes the uniqueness tripwire, respects iteration + wall-clock caps; exercise bias: with default Basic checks, ≥ 4 of 5 runs' reports include a non-single technique. Perf smoke (initial budget, spec-tunable): Basic median < 1 s, Intermediate median < 3 s |
| Training UI | `uv run python tests/browser.test.py` (new section) | panel opens; level select filters the checklist; level switch restores saved unchecks; checkboxes persist across reload; All/None toggle the current group and are disabled at Beginner; singles locked; generate → playable board + correct report; print view shows grid (+ solution page when checked); Advanced disabled with reason; confirm dialog on in-progress games; failures announced via `aria-live` |
| App unharmed | `node tests/engine.test.mjs` and `uv run python tests/browser.test.py` (existing sections) | stay green — casual game flow untouched |

Fixture boards may reuse the already-verified lesson diagram positions
(naked pair, hidden pair, pointing, X-Wing, XY-Wing from the ladder-spec
groundwork) — verified data, zero new derivation.

Sabotage culture — two deterministic bites per engine spec, budget-independent:
(a) delete the pointing detector → its fixture board is declared stuck and
the gate exits 1; (b) make the X-Wing detector unsound (eliminate one extra
candidate) → the uniqueness tripwire aborts loudly and the gate exits 1.
Gates that cannot bite are theater.

## 9. Decisions sealed by this proposal

1. Semantics are **exclusive** (never needs anything outside the checked set) plus the **exercise bias**: with non-single techniques checked, at least one is exercised or generation fails loudly. The "guaranteed to require technique X" generator stays parked for v2.
2. Naked + hidden singles are locked on, with a one-line explanation in the UI.
3. Training levels are the ladder tiers (Beginner/Basic/Intermediate, Advanced planned); casual clue-count difficulties remain untouched.
4. Carve targets reuse the app's `CLUES` table, floor semantics (stop at target; stop higher when the set cannot carve deeper) — training boards feel like their casual difficulty.
5. Advanced (chains) ships disabled with a visible reason — no fake verification.
6. Generation is two-phase carve (target then exercise bias) with mandatory iteration + wall-clock guards, enumerated retry triggers, and loud, actionable failure.
7. The final `countSolutions == 1` check is the detector-soundness tripwire: firing it aborts loudly and never retries — it is a bug alarm, not belt-and-braces.
8. The v1 checklist is exactly Appendix A's 19 boxes; absent techniques are named, not silent.
9. The solver and generator are pure sections inside the single-file app — the app stays one file, testable through the existing headless seam, with their own candidate grid independent of player notes.
10. Output is play-now (solution hidden) plus browser-native print with an optional solution page; no file/image export in v1.
11. Preferences persist under `sudoku-training-v1` keyed by stable technique IDs (never display labels), schema commented in place, isolated from the game and theme keys.
12. Every generated board keeps the app's existing invariants: unique solution, valid givens, undo/notes/hints all work.
13. Specs 009 → 010 → 011 (solver → generator → UI), independent of 000–008; technique names come from the Brief so the studio and the lessons never disagree.

---

## Appendix A — the exact v1 checklist (spec-ready, 19 boxes)

Stable IDs are the persistence and solver keys; labels are what the player
sees. Solver order = table order (cheapest first) — the same escalation
discipline the Brief's champion layer teaches.

| ID | Level | Label (player-facing) | Solver rule (one line) | Source |
| --- | --- | --- | --- | --- |
| `naked_single` | Beginner | naked single *(locked)* | cell with exactly one candidate → place it | Brief Tier 1 |
| `hidden_single` | Beginner | hidden single *(locked)* | digit with exactly one cell in a unit → place it | Brief Tier 1 |
| `naked_pair` | Basic | naked pair | 2 cells of a unit holding exactly the same 2 candidates → eliminate those candidates elsewhere in the unit | Brief Tier 2 |
| `naked_triple` | Basic | naked triple | same rule with 3 cells / 3 candidates | Brief Tier 2 |
| `naked_quad` | Basic | naked quad | same rule with 4 cells / 4 candidates | Brief Tier 2 |
| `hidden_pair` | Basic | hidden pair | 2 candidates confined to the same 2 cells of a unit → strip other candidates from those cells | Brief Tier 2 |
| `hidden_triple` | Basic | hidden triple | same rule with 3 candidates / 3 cells | Brief Tier 2 |
| `hidden_quad` | Basic | hidden quad | same rule with 4 candidates / 4 cells | Brief Tier 2 |
| `pointing` | Basic | pointing | digit's box-candidates all in one row/column → eliminate along that row/column outside the box | Brief Tier 2 |
| `claiming` | Basic | claiming | digit's row/column-candidates all in one box → eliminate in the box outside that row/column | Brief Tier 2 |
| `x_wing` | Intermediate | X-Wing | digit confined in 2 rows (or columns) to the same 2 columns (or rows) → eliminate along those lines elsewhere | Brief Tier 3 |
| `swordfish` | Intermediate | Swordfish | X-Wing's rule with 3 lines / 3 cover lines | Brief Tier 3 |
| `jellyfish` | Intermediate | Jellyfish | X-Wing's rule with 4 lines / 4 cover lines | Brief Tier 3 |
| `skyscraper` | Intermediate | skyscraper | two parallel strong links joined by a weak link → the tip-overlap cells lose the digit | Brief Tier 3 |
| `two_string_kite` | Intermediate | 2-string kite | row strong link + column strong link joined through a box → the overlap cell loses the digit | Brief Tier 3 |
| `turbot_fish` | Intermediate | turbot fish | any two strong links joined by one weak link (general family) → overlap loses the digit | Brief Tier 3 |
| `xy_wing` | Intermediate | XY-Wing | pivot {x,y} + pincers {x,z},{y,z} → z dies where both pincers see | Brief Tier 3 |
| `xyz_wing` | Intermediate | XYZ-Wing | pivot {x,y,z} + pincers {x,z},{y,z} → z dies where all three see | Brief Tier 3 |
| `w_wing` | Intermediate | W-Wing | two non-seeing {x,y} cells joined by an x strong link → y dies where both see | Brief Tier 3 |

Subsumption note for spec writers: turbot fish is the general case of
skyscraper and 2-string kite. Checking only `turbot_fish` is valid (the
generic detector fires); checking the specific ones alongside is also valid —
cheapest-first ordering reaches them first, and the report names the specific
technique when it fires.

## Appendix B — localStorage schema

```js
// sudoku-training-v1 — Training Studio preferences.
// level:     "beginner" | "basic" | "intermediate" (Advanced pending v2)
// unchecked: per level, technique IDs (Appendix A) the player unticked;
//            singles are structural and never appear here.
// IDs are stable forever; labels may be reworded without breaking saves.
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
1. Detectors for every Appendix A row, keyed by stable ID; each returns
   placements/eliminations or none — and must be SOUND: never eliminate a
   candidate present in some solution.
2. Solver completes ⇒ grid valid and equal to the board's unique solution
   (cross-checked via countSolutions in tests); stuck ⇒ declares stuck
   (no brute-force fallback inside the solver).
3. Technique set restrictable per run (checked IDs); used-technique log kept.
4. Maintains its own candidate grid — no DOM access, no dependence on player
   notes; works under the existing Node extraction seam.
5. All loop guards present (iteration + wall-clock caps).

## Acceptance (binary)
- node tests/training.test.mjs → exit 0 (fixture boards per technique,
  oracle cross-checks vs countSolutions)
- node tests/engine.test.mjs && uv run python tests/browser.test.py → exit 0
- Sabotage A: delete the pointing detector → its fixture turns stuck, gate exits 1.
- Sabotage B: unsound X-Wing (one extra elimination) → uniqueness tripwire
  fires, gate exits 1.
```
