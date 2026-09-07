# Feature Specification: Intermediate Lesson Page, Part 2 — Wings, Uniqueness, and Misc (completes chapter 03)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §3 (chapter 03 row), §4 (L3, L6), §5 (row `005-intermediate-wings`), §5.1, §7; Brief §Tier 3 (wings, uniqueness family, miscellaneous)

## Context (OBSERVED)

- Technique source: the Brief, section *Tier 3 — Intermediate*, second half. Wings: XY-Wing (Y-Wing), XYZ-Wing, W-Wing, WXYZ-Wing/Fireworks. Uniqueness family — the Brief flags the core assumption explicitly: these assume the puzzle has exactly one solution and exploit that a deadly-pattern rectangle can never be reached: Unique Rectangle types 1–6 / Hidden UR, BUG+1, Avoidable Rectangle. Miscellaneous: Sue de Coq, Remote Pairs.
- This spec completes the page started by spec `004-intermediate-fish` (fish + single-digit patterns already present): it adds these sections, removes the "part 1 of 2" marker, and installs the chapter's full checkpoint (graduation: find an X-Wing **and** a UR type 1 on prepared boards — proposal §3).
- The uniqueness assumption deserves special care: the game's own engine guarantees unique puzzles (engine gate asserts well-posedness, tests/engine.test.mjs:81-98), so the page can honestly tell learners why the trick is safe here.
- Language tier: plain English (L3), names Brief-exact, terms defined at first use.
- Prev neighbor chapter 02 exists; next neighbor chapter 04 does not exist yet — its slot stays "coming soon" until spec 006 builds that page, at which point this page's next link flips.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Wings: three cells that corner a digit (Priority: P1)

A solver who knows fish reads the XY-Wing section: a pivot cell holding two digits, two pincer cells, and one digit that both pincers can see dying everywhere they jointly look. The XYZ-Wing is the same shape with the pivot also holding the third digit; the W-Wing joins two non-seeing cells through a strong link. Worked boards mark pivot, pincers, and victims.

**Why this priority**: wings are the most-used Tier-3 technique after fish; the graduation-adjacent skill for expert-level puzzles.

**Independent Test**: the reader identifies pivot and pincers on a prepared XY-Wing board and points at the cell that loses a digit.

**Acceptance Scenarios**:

1. **Given** the XY-Wing section, **When** the reader follows the worked board, **Then** pivot, pincers, and at least one eliminated cell are each marked and named.
2. **Given** the XYZ-Wing section, **When** read after XY-Wing, **Then** it is presented as the same pattern with the pivot holding the extra digit, sharing or extending the example.
3. **Given** the W-Wing section, **When** read, **Then** the two cells and the joining strong link are shown, plus the resulting elimination.
4. **Given** the family overview, **When** WXYZ-Wing/Fireworks are named, **Then** they are presented as four-cell extensions without full tutorials.

### User Story 2 - Uniqueness tricks with the safety caveat (Priority: P1)

The reader meets the deadly rectangle idea — two digits swap-able in two boxes, which a proper puzzle can never end with — then UR type 1 as the direct use: if avoiding the rectangle forces one candidate, that candidate is right. BUG+1 follows. The page states the assumption once, clearly, and why it is safe in this game.

**Why this priority**: UR type 1 is the chapter's second graduation requirement; the caveat is what keeps the tool honest.

**Independent Test**: the reader finds the UR type 1 on a prepared board and states the assumption in their own words.

**Acceptance Scenarios**:

1. **Given** the uniqueness intro, **When** read, **Then** the deadly-rectangle picture is shown and the one-solution assumption is stated with the note that this game's puzzles are guaranteed unique.
2. **Given** the UR type 1 section, **When** the reader follows the worked board, **Then** the rectangle, the two digits, and the candidate that must be true are all marked.
3. **Given** UR types 2–6 and Hidden UR, **When** browsed, **Then** they appear as a compact table of one-liners (Brief wording) rather than full tutorials.
4. **Given** the BUG+1 section, **When** read, **Then** the grave picture and the single three-candidate cell rule are shown on one board.

### User Story 3 - The rare ones get honest billing (Priority: P3)

Sue de Coq and Remote Pairs are taught briefly with one example each, labeled as rare finds — enough to recognize them when a solver elsewhere names them.

**Why this priority**: completeness of the Brief's Tier 3 without inflating the page.

**Independent Test**: the reader can say in one sentence what each does.

**Acceptance Scenarios**:

1. **Given** the Sue de Coq section, **When** read, **Then** one worked example and a one-sentence definition are present.
2. **Given** the Remote Pairs section, **When** read, **Then** the chain of identical pairs and the parity elimination are shown on one board.

### Edge Cases

- **Page completion transition**: this spec must remove the part-1 marker and replace the part-1 checkpoint with the full chapter checkpoint; both states are gate-checkable (marker absent; checkpoint covers X-Wing and UR type 1).
- **Uniqueness misuse**: the caveat must appear before the first uniqueness technique, not as a footnote.
- **Avoidable Rectangle** (Brief list item): covered in the UR types table as "same logic on already-placed digits" — no separate tutorial.
- **Next neighbor may still not exist**: chapter 04's slot stays "coming soon" here; spec 006 flips it later.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The page MUST gain wings sections — XY-Wing, XYZ-Wing, W-Wing each with a worked board marking the pattern and the elimination; WXYZ-Wing/Fireworks named as four-cell extensions.
- **FR-002**: The page MUST gain a uniqueness section opening with the deadly-rectangle picture and the one-solution assumption (including why it is safe in this game), then teaching UR type 1 on a worked board and covering UR types 2–6, Hidden UR, and Avoidable Rectangle as a compact one-liner table.
- **FR-003**: The page MUST gain a BUG+1 section with the grave picture and the single three-candidate rule on one board.
- **FR-004**: The page MUST gain Sue de Coq and Remote Pairs sections, each with one worked example and a one-sentence definition, billed as rare finds.
- **FR-005**: On completion the page MUST drop the "part 1 of 2" marker and carry the full chapter checkpoint: 2–3 "can you…?" questions including finding an X-Wing and finding a UR type 1 on prepared boards.
- **FR-006**: Every new term MUST be defined with an example at first use; names MUST match the Brief exactly; the page MUST pass the plain-English budget (≤ 25-word sentences).
- **FR-007**: The "Try it" section MUST link to the game and instruct: difficulty Expert, New game, then hunt a wing before anything harder.
- **FR-008**: Footer navigation MUST follow the existing-neighbors-only policy; when chapter 04's page lands later, this page's next link MUST flip (that flip is specced in 006/007, not here).

### Key Entities

- **TechniqueSection**: plain-English what/when, worked board(s), Brief-exact name and one-liner.
- **UniquenessCaveat**: the one-solution assumption statement, shown once before the family.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can find an X-Wing and a UR type 1 on prepared boards (full checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget (readability gate exit 0 — pass/fail).
- **SC-003**: The completed page loads with zero page errors, all template sections, no part-1 marker, all links resolving, boards rendering (lesson gate exit 0 — pass/fail).
- **SC-004**: The game remains untouched (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- Spec 004's sections, shell, and index row already exist; this spec only completes the page and swaps the checkpoint.
- UR types 2–6, Hidden UR, Avoidable Rectangle stay table-level forever (Brief one-liners); deep tutorials are not planned in any spec.
- Worked boards may come from generated positions via the engine seam (tests/engine.test.mjs:9-12) or hand-built fragments, validated or clearly marked.
- Parked: deep-linking Expert into the game; interactive candidate toggling; progress tracking.
