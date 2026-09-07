# Feature Specification: Training Technique Solver (pure section in sudoku.html)

**Feature Branch**: `specify/training-studio`

**Created**: 2026-09-07

**Status**: Done

**Input**: specs/proposal-training.md §3 (feasibility ladder + soundness honesty), §4 (levels, Appendix A checklist), §5 (`solveWithAllowed`), §8 (Training-engine gate, solver half; sabotage culture), Appendix C skeleton

## Context (OBSERVED)

- The app is the single file `sudoku.html`; its pure-logic section already holds the engine the solver builds on: `BOX/PEERS/GROUPS` unit tables (469+), `popcount` (506), `countSolutions(bd, limit)` (516), `genFull()` (584), `makePuzzle(clues)` (617), `validPuzzle(puz)` (641) — all before the `typeof document` UI guard (656), so a pure technique solver placed beside them runs headless in Node.
- The headless seam exists and is proven: `tests/engine.test.mjs:7-13` loads the whole `<script>` through a `Function` wrapper and destructures named exports — `tests/training.test.mjs` reuses exactly this seam, adding the solver's exports.
- `countSolutions` is the soundness oracle: for any well-posed fixture the completion of a sound solve must equal the grid `countSolutions` recovers; `validPuzzle` (641) shows the GROUPS-conflict pattern detectors can reuse.
- Verified fixture data already exists in the repo's spec groundwork: the ladder-spec diagram positions for naked pair, hidden pair, pointing, X-Wing, and XY-Wing (named reusable by proposal §8). The remaining 14 Appendix A techniques get fixtures authored at implementation time, validated by this spec's own gate.
- Proposal Appendix A is the authoritative detector contract: 19 stable snake_case IDs, one-line solver rules, cheapest-first order (singles → subsets → intersections → fish/turbot → wings).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Solving with only what is checked (Priority: P1)

The generator (spec 010) needs one primitive: give the solver a board and a checked technique set, and it either completes the grid using only those techniques — recording which ones it used, cheapest-first — or honestly says it is stuck. No brute force, no guessing, no wrong placements, ever.

**Why this priority**: exclusivity ("never needs anything outside the checked set") is the whole feature's core promise, and this solver is the only thing that can verify it.

**Independent Test**: run the solver headless on fixture boards through the existing extraction seam (`node tests/training.test.mjs`); no UI is needed.

**Acceptance Scenarios**:

1. **Given** a fixture board that needs singles + pointing, **When** solved with allowed = naked single, hidden single, pointing, **Then** it completes, and the used log contains `pointing` (plus singles).
2. **Given** the same board, **When** solved with allowed = singles only, **Then** the solver declares stuck after singles are exhausted, every placement made so far is still consistent with the board's unique solution, and no detector outside the allowed set was invoked.

### User Story 2 - Every detector is sound and honest (Priority: P1)

A player trains trust: whatever the solver eliminates must be true for the actual solution. One unsound detector would "complete" boards to wrong grids and silently poison every generated puzzle.

**Why this priority**: proposal §3 seals it — guarantees hold only if every detector is sound; this is guarded by oracles, not hope.

**Independent Test**: the gate cross-checks every fixture completion against `countSolutions`'s recovered solution.

**Acceptance Scenarios**:

1. **Given** a fixture for each of the 19 Appendix A techniques, **When** solved with allowed = singles + that technique, **Then** the board completes and the completed grid equals the board's unique solution (oracle cross-check).
2. **Given** a contradictory-givens board and an empty board, **When** solved, **Then** both are declared stuck (or invalid) — never "completed" — with zero placements.

### User Story 3 - Deterministic, cheapest-first discipline (Priority: P2)

The same board must always solve the same way, and cheap techniques must fire before expensive ones — this is the escalation discipline the lessons teach and the report (spec 011) displays.

**Why this priority**: determinism makes failures reproducible and reports trustworthy; ordering mirrors Appendix A.

**Independent Test**: run any fixture twice; logs are identical.

**Acceptance Scenarios**:

1. **Given** the same board and allowed set, **When** solved twice, **Then** the used log and final grid are byte-identical.
2. **Given** a board containing a skyscraper position, **When** solved with all Intermediate techniques checked, **Then** the log names `skyscraper`, not `turbot_fish` (specific detectors precede the general family, per Appendix A's subsumption note).

### Edge Cases

- **Singles-only allowed set**: the minimal legal set (singles are structurally locked, proposal §4); most boards then stick — declared, not forced.
- **Already-complete board**: completes immediately with an empty used log.
- **Empty board**: no candidate ever becomes placeable — stuck at round 0.
- **Contradictory givens**: defensively declared stuck (the generator never produces them; `validPuzzle` guards upstream).
- **`turbot_fish` checked alone**: the generic detector fires on skyscraper/kite positions — valid per Appendix A's subsumption note; the log still names the technique that fired (`turbot_fish`).
- **No-op eliminations**: a detector firing without changing the grid (nothing to eliminate) does not count as a technique use and does not loop — only grid-changing firings enter the log.
- **Elimination cascade**: eliminating a candidate may create singles; the solver loops placement→elimination until a full allowed round changes nothing (stuck) or the grid completes.
- **Loop guards (project hard rule)**: placements capped at 81; elimination-only rounds capped (initial value 200) and a per-solve wall-clock cap (initial value 500 ms) — a no-progress loop breaks as stuck, never hangs.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A pure technique-solver section MUST live in `sudoku.html`'s pure-logic area (no DOM access), exported through the existing `Function`-wrapper seam so `tests/training.test.mjs` can drive it headless.
- **FR-002**: Detectors MUST exist for exactly the 19 Appendix A technique IDs (stable snake_case keys — never display labels), each implementing its Appendix A one-line rule.
- **FR-003**: Every detector MUST be sound: it MUST never eliminate a candidate or place a digit that contradicts the board's unique solution; the gate MUST verify this by oracle cross-check on every fixture completion.
- **FR-004**: `solveWithAllowed(board, allowedIds)` MUST iterate detectors cheapest-first (Appendix A order), keep its own candidate grid independent of player notes and UI state, and return a result carrying: completed?, final grid, used-technique log (first-use order, cheapest-first), and rounds used.
- **FR-005**: A technique MUST appear in the used log only when its firing changed the grid (placement or elimination).
- **FR-006**: Stuck MUST be declared honestly: a full pass of all allowed detectors with no grid change ends the solve; the solver MUST NOT contain any brute-force or backtracking fallback.
- **FR-007**: The solver MUST be deterministic: fixed scan order, no randomness (no `shuffle` use), identical inputs → identical outputs.
- **FR-008**: Every solve MUST carry loop guards: a placements cap of 81, an elimination-only-rounds cap (initial 200), and a per-solve wall-clock cap (initial 500 ms); cap exhaustion reports stuck/timeout, never a hang.
- **FR-009**: The technique set MUST be restrictable per run; detectors whose IDs are not in the allowed set MUST never be invoked.
- **FR-010**: The existing product behavior MUST be unchanged by this addition (`tests/engine.test.mjs` and the existing `tests/browser.test.py` sections stay green).

### Key Entities

- **Detector**: stable ID, ladder level, Appendix A rule; sound by construction and by oracle-verified fixture.
- **SolveResult**: completed flag, final grid, used-technique log (ordered IDs), rounds consumed, stuck reason when incomplete.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `node tests/training.test.mjs` exits 0: per-technique fixtures (all 19) complete under singles + that technique; every completion equals the oracle-verified unique solution; stuck boards (singles-only restrictions, contradictory givens, empty board) are declared stuck.
- **SC-002**: Determinism: repeated runs of the same fixture produce byte-identical used logs (gate assertion).
- **SC-003** (sabotage A, deterministic): with the pointing detector deleted, the pointing fixture is declared stuck and the gate exits 1.
- **SC-004** (sabotage B, deterministic): with an unsound X-Wing variant (one extra elimination), a fixture completes to a grid that fails the oracle cross-check and the gate exits 1 — the solver-level soundness bite (spec 010 adds the generator's uniqueness tripwire bite on top).
- **SC-005**: `node tests/engine.test.mjs` and `uv run python tests/browser.test.py` (existing sections) exit 0 — the casual app is untouched.

## Assumptions

- Fixture data: the five verified ladder positions (naked pair, hidden pair, pointing, X-Wing, XY-Wing) are reused; the other 14 technique fixtures are authored during implementation and validated by this spec's gate (completes under singles + technique; oracle equality).
- Parked as v2 detector candidates, named not silent (proposal §4): finned/sashimi/franken/mutant fish, empty rectangle (Brief: deprecated as redundant), WXYZ-wing, the uniqueness family, Sue de Coq, remote pairs, the ALS family, all chains.
- The carve generator consuming `solveWithAllowed` is spec 010; the report line rendering and panel are spec 011.
- Generation-level performance budgets (Basic median < 1 s, Intermediate median < 3 s) belong to spec 010; this spec sets only the per-solve caps in FR-008.
- The solver never reads or writes `localStorage`; it is pure logic.
