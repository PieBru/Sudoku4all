# Feature Specification: Intermediate Lesson Page, Part 1 — Fish and Single-Digit Patterns (chapter 03)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §3 (chapter 03 row), §4 (L3, L6), §5 (row `004-intermediate-fish`), §5.1, §7; Brief §Tier 3 (fish family + single-digit patterns)

## Context (OBSERVED)

- Technique source: the Brief, section *Tier 3 — Intermediate*, first half. Fish family: X-Wing, Swordfish, Jellyfish, Finned/Sashimi fish, Franken/Mutant fish. Single-digit patterns: Skyscraper, 2-String Kite, Turbot fish, Empty rectangle. Names and one-line definitions come from the Brief; the Brief also notes SudokuWiki deprecates the empty rectangle as redundant — the page must be honest about that (proposal §6: never contradict the Brief).
- This spec delivers the page shell plus these sections; a sibling spec (`005-intermediate-wings`) completes the page with wings, uniqueness, Sue de Coq, and remote pairs. Until then the page MUST present itself as part 1 of 2 (proposal §5 split rule).
- Language tier: plain English (L3) — sentence ceiling ~25 words, terms defined at first use, names Brief-exact.
- Chapter graduation (proposal §3) spans the finished page: find an X-Wing and a UR type 1 on prepared boards. The X-Wing half becomes teachable and checkable with this spec; the UR half lands with spec 005, which owns the completed page's checkpoint.
- Framework from spec 000; prev neighbor chapter 02 (spec 003) exists by build order; next neighbor chapter 04 does not exist yet.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A medium solver meets their first fish (Priority: P1)

A player comfortable with pairs reads the X-Wing section. The idea is built before the name: one digit, two rows, the same two columns — a rectangle; wherever the digit sits, those columns' other cells lose it. A worked board shows the rectangle and the eliminations. Swordfish and Jellyfish follow as the same idea on three and four lines.

**Why this priority**: fish are the chapter's headline family and the graduation requirement's first half.

**Independent Test**: hand the reader a prepared board with an X-Wing; they trace the rectangle and name the cells that lose the digit.

**Acceptance Scenarios**:

1. **Given** the X-Wing section, **When** the reader follows its worked board, **Then** the four rectangle cells and the eliminated cells are both marked, and the name X-Wing appears only after the plain-English build-up.
2. **Given** the Swordfish section, **When** read after X-Wing, **Then** it is presented as the same pattern one line bigger, with one worked board.
3. **Given** the fish family overview, **When** the reader lists what they learned, **Then** X-Wing, Swordfish, and Jellyfish are each named with their line-count (2, 3, 4).

### User Story 2 - Skyscrapers and kites: the everyday hard-puzzle tools (Priority: P2)

The single-digit patterns are the most common finds on hard puzzles. Skyscraper and 2-String Kite each get a worked board; turbot fish is taught as the general shape both belong to; the empty rectangle is covered with the Brief's honesty note that some schools consider it redundant.

**Why this priority**: these patterns pay off immediately on the game's Hard difficulty; the honesty note keeps trust.

**Independent Test**: the reader finds the skyscraper on a prepared board and says which cells lose the digit.

**Acceptance Scenarios**:

1. **Given** the skyscraper section, **When** the reader studies the board, **Then** the two strong links and the elimination at the overlap are marked.
2. **Given** the 2-String Kite section, **When** read, **Then** the row link, box link, and joining column are each pointed out on the board.
3. **Given** the empty rectangle section, **When** read, **Then** the technique is explained and the note that one canonical school deprecates it as redundant is present.

### User Story 3 - Finned fish without fear (Priority: P3)

Finned and sashimi variants and the franken/mutant zoo are named and explained briefly as X-Wing/Swordfish with spoiler cells, sharing one worked example; the reader learns to recognize, not master, them here.

**Why this priority**: awareness prevents panic when solvers elsewhere use these names; mastery is not this page's job.

**Independent Test**: the reader can say what a fin is in one sentence after reading.

**Acceptance Scenarios**:

1. **Given** the finned fish section, **When** read, **Then** a fin is defined in one sentence and shown as marked spoiler cells on the shared example.
2. **Given** franken/mutant fish, **When** read, **Then** they are named as fish whose lines mix boxes with rows/columns, without full tutorials.

### Edge Cases

- **Page completeness**: until spec 005 lands, the page MUST carry a visible "part 1 of 2" marker and MUST NOT link to chapter 04's page as if the ladder were complete; the next-neighbor slot stays "coming soon".
- **Checkpoint scope**: with only part 1 present, the checkpoint section MUST limit itself to fish and single-digit patterns; spec 005 replaces it with the full chapter checkpoint.
- **Board data integrity**: worked boards are validated positions or clearly marked fragments; finned examples show fins unambiguously.
- **Reader arriving mid-ladder**: one opening line states the expected background (chapter 02's pairs and notes).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page shell MUST exist at the lessons location for chapter 03 with the shared template sections, a visible "part 1 of 2" marker, and an opening line stating expected background.
- **FR-002**: The page MUST contain fish-family sections teaching X-Wing, Swordfish, and Jellyfish (built plain-English first, Brief name last), each with at least one worked board (X-Wing and Swordfish) or a clear line-count statement (Jellyfish may share the Swordfish treatment's extension pattern).
- **FR-003**: The page MUST contain single-digit-pattern sections teaching Skyscraper, 2-String Kite, and Turbot fish, each with the links/eliminations marked on a worked board (turbot fish may use the skyscraper board as its generalization).
- **FR-004**: The page MUST cover the Empty Rectangle, including the Brief's note that a canonical school deprecates it as redundant.
- **FR-005**: The page MUST name finned/sashimi fish (one-sentence fin definition, one shared worked example) and franken/mutant fish (named, one-line family description) without full tutorials.
- **FR-006**: Every new term MUST be defined with an example at first use; names MUST match the Brief exactly; the page MUST pass the plain-English budget (≤ 25-word sentences).
- **FR-007**: The "Try it" section MUST link to the game and instruct: difficulty Hard, New game, then hunt one digit's rows and columns for a rectangle.
- **FR-008**: The part-1 checkpoint MUST pose 2–3 "can you…?" questions covering fish and single-digit patterns on prepared boards.
- **FR-009**: Footer navigation MUST follow the existing-neighbors-only policy (prev to chapter 02 live; next "coming soon") and the index row MUST flip to a link.

### Key Entities

- **TechniqueSection**: plain-English what/when, worked board(s), Brief-exact name and one-liner.
- **DisplayBoard**: validated position or marked fragment, with pattern cells and eliminated cells visually distinguished.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can find an X-Wing on a prepared board (checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget (readability gate exit 0 — pass/fail).
- **SC-003**: The page loads with zero page errors, template sections present, all links resolving, boards rendering (lesson gate exit 0 — pass/fail), and carries the "part 1 of 2" marker until spec 005 completes it.
- **SC-004**: The game remains untouched (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- Spec 005 completes this page (wings, uniqueness, Sue de Coq, remote pairs, full checkpoint, marker removal) — those techniques are explicitly out of scope here.
- Worked boards may come from generated hard/expert positions via the engine seam (tests/engine.test.mjs:9-12) or hand-built fragments, validated or clearly marked.
- Jellyfish and the mutant zoo are recognition-level only; deep tutorials are deferred indefinitely (they are solver territory per the Brief).
- Parked: deep-linking Hard into the game; interactive candidate toggling on display boards (boards show marks statically).
