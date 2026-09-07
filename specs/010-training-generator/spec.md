# Feature Specification: Training Board Generator (two-phase carve)

**Feature Branch**: `specify/training-studio`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal-training.md §1 (goal), §4 (levels + carve targets + floor semantics), §5 (two-phase carve algorithm, retry triggers, guards), §6.2 (report), §8 (Training-engine gate, generator half), §9 decisions 1/4/6/7

## Context (OBSERVED)

- Everything the generator drives is already in `sudoku.html`'s pure-logic section: `shuffle` (497), `countSolutions` (516), `genFull()` (584), and the casual `makePuzzle` (617) whose retry-loop pattern (bounded attempts, fresh shuffle per attempt) this spec's guard structure mirrors; `CLUES = {easy:40, medium:34, hard:29, expert:25}` (681) supplies the per-level carve targets.
- The technique solver (`solveWithAllowed`, used-technique log, stuck declaration) is delivered by spec 009 through the same pure section and the same `Function`-wrapper headless seam (`tests/engine.test.mjs:7-13` pattern); `tests/training.test.mjs` exists from 009 and this spec extends it with the generator checks.
- `countSolutions(board, 2)` (516) is the detector-soundness tripwire's oracle: a generated board that does not have exactly one solution after an allowed-set completion means an engine bug (proposal §5, decision 7).
- The training levels map to carve targets per proposal §4: Beginner→40 (easy), Basic→34 (medium), Intermediate→29 (hard); Advanced (25/expert) is disabled until chains are verifiable (spec 011 renders that honestly; this spec simply has no Advanced generator).
- The lesson-spec groundwork fixtures (naked pair, hidden pair, pointing, X-Wing, XY-Wing — verified positions) remain available to the shared gate (proposal §8).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A board that never needs more than I checked (Priority: P1)

The player checks, say, singles + pointing + naked pair and presses Generate. The returned board is playable (solution hidden inside the result), has a unique solution, and — the core promise — completes logically using only the checked techniques. However far the carve got, exclusivity is non-negotiable.

**Why this priority**: exclusivity is the feature's contract; everything else (size, bias, speed) is quality, not truth.

**Independent Test**: headless — generate for random checked subsets (singles always on) and re-solve each board under its subset alone; assert completion + uniqueness.

**Acceptance Scenarios**:

1. **Given** any generated board and the checked set it was generated for, **When** `solveWithAllowed` re-runs on the pristine board, **Then** it completes, and the completed grid equals the board's unique solution (oracle cross-check).
2. **Given** the Intermediate level's 29-clue target and a checked set that cannot carve that deep without chains, **When** carving stalls at, say, 31 clues, **Then** generation succeeds — floor semantics: stopping higher is the correct outcome, not a failure (proposal §4).

### User Story 2 - The board actually exercises what I want to train (Priority: P1)

A player who checked "pointing" must not silently receive a singles-only board. After reaching the clue target, carving continues until at least one checked non-single technique genuinely contributes to the solve — or generation fails loudly with something to do about it.

**Why this priority**: without exercise bias, target-sized boards are usually singles-only and the whole training purpose silently degrades into Beginner practice (proposal §5, Phase B rationale).

**Independent Test**: default Basic checks (all 8 Basic boxes on), 5 runs — at least 4 reports include a non-single technique.

**Acceptance Scenarios**:

1. **Given** ≥ 1 checked non-single technique and a Phase-A carve whose solve was singles-only, **When** Phase B runs, **Then** carving continues past the target until a checked non-single technique contributes (verified solve's log), or no removal preserves allowed-solvability.
2. **Given** only singles checked (Beginner), **When** generation runs, **Then** Phase B is skipped entirely — a singles-only board is the requested outcome, not a bias failure.

### User Story 3 - Failure is loud, bounded, and actionable (Priority: P2)

Generation is search under guards. When it cannot deliver, the player hears why and what to do — never a silent fallback to an unverified board, never a hang.

**Why this priority**: project hard rules (unguarded loops, silent failures) plus proposal decision 6; trust is the product.

**Independent Test**: exhaust the budget deliberately in the gate (adversarially tiny budget) and observe the loud failure path.

**Acceptance Scenarios**:

1. **Given** Phase B cannot find exercise within its per-attempt budget, **When** attempts remain, **Then** a fresh attempt starts (fresh `genFull`, fresh shuffle) — retry trigger (a).
2. **Given** all attempts/budgets are exhausted, **When** the run ends, **Then** the result is an explicit failure carrying the message *"Couldn't build a board with only these techniques. Try enabling a few more."* — no board is returned.
3. **Given** the final `countSolutions(board, 2) == 1` tripwire fires, **When** it does, **Then** the run aborts loudly with no retry — firing it is an engine bug alarm, not belt-and-braces (proposal decision 7).

### Edge Cases

- **Target unreachable for the set** (deep Intermediate sets): floor semantics — stop at the deepest reachable clue count ≥ target; success.
- **Phase B would carve below the target into absurdity**: Phase B's rule is still allowed-solvability; it never breaks exclusivity regardless of depth.
- **Tripwire vs. budget**: tripwire aborts immediately even with attempts remaining; budget exhaustion fails loudly with the actionable message — the two paths are distinct and both observable.
- **Zero non-single checked** (Beginner): Phase B skipped; Phase A alone with the singles-only solver.
- **Solver runs per attempt** are capped (initial 60) so Phase B cannot spiral into solver-thrash near the carve floor; the cap is a guard, not a tuning knob for correctness.
- **Determinism of report**: the report always comes from one final verification solve of the pristine generated board (cheapest-first, proposal §6.2's honest labeling) — not from carve-time solver chatter.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A pure generator section MUST live beside the engine in `sudoku.html`'s headless area, exported through the existing seam, consuming spec 009's `solveWithAllowed`; it MUST NOT touch the DOM or the casual `makePuzzle` path.
- **FR-002**: Generation MUST follow the two-phase carve (proposal §5): Phase A removes shuffled cells while the allowed-set solve still completes, stopping at the level's `CLUES` target (Beginner 40, Basic 34, Intermediate 29); Phase B continues the same rule past the target, only when ≥ 1 non-single technique is checked, until one contributes or no removal preserves allowed-solvability.
- **FR-003**: Every generation run MUST end with a final verification solve of the pristine board plus the `countSolutions(board, 2) == 1` tripwire; a tripwire failure MUST abort loudly with no retry (engine bug path), and the gate MUST exercise it via the unsound-X-Wing sabotage.
- **FR-004**: Every run MUST carry loop guards with spec-tunable initial values: ≤ 8 full attempts, ≤ 5 s total wall clock, ≤ 60 solver runs per attempt; budget exhaustion MUST fail loudly with the proposal's message text, never return a board.
- **FR-005**: A successful result MUST carry the generated board, its full solution, the given-cell flags, the final clue count, and the report (technique IDs from the final verification solve, cheapest-first).
- **FR-006**: The result data MUST be shaped so the game can adopt it as an active game directly (spec 011) while preserving the app's invariants: unique solution, valid givens, standard game features work (proposal decision 12).
- **FR-007**: Exclusivity MUST hold for every emitted board: re-solving the pristine board under the checked set alone completes it (gate asserts this on every generated board, not by construction trust).
- **FR-008**: The used-technique report MUST be labeled as the solver's own cheapest-first path on the pristine board (honest labeling, proposal §6.2); no "required techniques" claim is made (exclusive, not prescriptive — decision 1).
- **FR-009**: The casual game paths MUST remain untouched: `tests/engine.test.mjs` and the existing `tests/browser.test.py` sections stay green.

### Key Entities

- **TrainingLevel**: Beginner/Basic/Intermediate; carries its carve target and its technique group.
- **GenerationResult**: success (board, solution, givens, clue count, report) or failure (reason: budget|tripwire; human message).
- **Budget**: attempts, wall-clock ms, solver-runs — constants with documented initial values.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `node tests/training.test.mjs` exits 0 including generator checks: for random checked subsets (singles always on, ≥ 10 draws across levels) every board completes under its subset alone and passes the tripwire; guards are respected (run wall clock ≤ 5 s asserted by the gate).
- **SC-002**: Exercise bias: with default Basic checks, ≥ 4 of 5 runs' reports include a non-single technique (gate assertion, exit 0/1).
- **SC-003** (sabotage, deterministic): with the pointing detector deleted (spec 009's sabotage A), any generation needing intersections fails loudly within budget — gate exits 1; and its pointing fixture stays stuck.
- **SC-004** (sabotage, deterministic): with an unsound X-Wing (one extra elimination), the uniqueness tripwire fires during generation and aborts loudly — gate exits 1.
- **SC-005**: Performance smoke (initial budgets, spec-tunable): Basic generation median < 1 s, Intermediate median < 3 s over 5 runs each (gate reports medians, exit 0/1).
- **SC-006**: `node tests/engine.test.mjs` and `uv run python tests/browser.test.py` (existing sections) exit 0.

## Assumptions

- "Guaranteed to require technique X" generation stays parked for v2 (decision 1); v1 promises exclusivity + exercise bias only.
- Advanced-level (chains) generation does not exist in this spec by design — spec 011 renders the level disabled with its reason; a future spec adds chain detectors first (009's parked list).
- Initial guard values (8 attempts / 5 s / 60 solver runs) are ceilings chosen for a 2026 laptop; the generator may internally use smaller step budgets — it MUST never exceed them.
- The UI (panel, persistence, print) is spec 011; this spec returns pure data only.
- Print/solution export beyond the returned data (no PNG/text/seed sharing) is parked per proposal §6.3's `ponytail:` note.
