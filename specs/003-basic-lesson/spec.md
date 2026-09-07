# Feature Specification: Basic Lesson Page (chapter 02)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §3 (chapter 02 row), §4 (L3, L6), §5 (row `003-basic-lesson`), §5.1, §7; Brief §Tier 2

## Context (OBSERVED)

- Technique source: the Brief, section *Tier 2 — Basic: subsets and intersections*: naked pair/triple/quad; hidden pair/triple/quad; locked candidates — pointing; locked candidates — claiming. Names and one-line definitions come from the Brief (SudokuWiki + HoDoKu); wording may be simplified, claims may not be invented (proposal §6).
- This chapter's language tier changes to plain English (L3): sentence ceiling 25 words; every new term defined with an example at first use; kid budgets no longer apply.
- Chapter graduation fixed by the proposal §3: the reader can spot a naked pair and a pointing pattern on a prepared board.
- Framework from spec 000: template sections, shared stylesheet, display-board renderer, both gates. Chapter 01's page (spec 001) is this page's prev neighbor and already exists by build order.
- The "Try it" instruction targets the game's Medium difficulty (CLUES medium = 34, sudoku.html:681) with controls named exactly as the app words them (New game etc., sudoku.html:407-417).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - An easy-level solver breaks their first wall (Priority: P1)

A player who solves easy puzzles but stalls on medium ones reads the page. Naked pairs are shown as "two cells that share the same two digits — those digits belong to them, so nobody else in the row/column/box can have them". Each idea comes with a board where the pattern is visible and the payoff (what gets eliminated, where) is marked.

**Why this priority**: subsets and intersections are exactly the medium-puzzle toolkit; this is the chapter's core value.

**Independent Test**: give the reader a prepared board containing a naked pair; they point at the two cells and say what follows.

**Acceptance Scenarios**:

1. **Given** the naked pair section, **When** the reader studies its worked board, **Then** the pair's two cells and the cells that lose the digit are both visibly marked.
2. **Given** the hidden pair section, **When** the reader compares it with the naked pair board, **Then** the difference (cells hiding two digits vs. digits confined to two cells) is stated in one sentence and shown.
3. **Given** any term first used on the page (pair, triple, quad, locked candidates, pointing, claiming), **When** it appears, **Then** a definition and example accompany the first use.

### User Story 2 - Pointing vs claiming stops being confusing (Priority: P2)

The two intersection techniques are the classic confusion pair. The page teaches them as mirror images: pointing = the box forces the row/column; claiming = the row/column forces the box. The checkpoint tests exactly this distinction.

**Why this priority**: misapplying intersections is the most common medium-level error the chapter can prevent.

**Independent Test**: the reader answers the checkpoint's pointing-vs-claiming question correctly from the page alone.

**Acceptance Scenarios**:

1. **Given** the pointing section's board, **When** the digit's in-box candidates are highlighted, **Then** the elimination outside the box on that row/column is shown and named pointing.
2. **Given** the claiming section's board, **When** the same highlight style is used, **Then** the direction of forcing is reversed and the mirror-sentence is stated.
3. **Given** the checkpoint, **When** the reader classifies two prepared positions, **Then** one is pointing and one is claiming.

### User Story 3 - Straight into a medium game (Priority: P3)

After the checkpoint the reader wants a live target; the Try it section sends them to a Medium game with one concrete first move to hunt for.

**Why this priority**: practice converts recognition into skill, but only after the concepts land.

**Independent Test**: follow Try it; the game opens at Medium with the named controls.

**Acceptance Scenarios**:

1. **Given** Try it, **When** followed, **Then** the game opens and the reader sets difficulty Medium and presses New game using only wording the page used.
2. **Given** the suggested first hunt (look for a pair), **When** the reader scans their fresh board, **Then** the page has told them exactly what to look for.

### Edge Cases

- **Terminology overload**: pair/triple/quad are counting words introduced once and reused; the page never uses subset, the Brief's umbrella term, without defining it as "the family name".
- **Neighbor availability**: chapter 01 exists (prev link live); chapter 03 may not exist yet — next renders as "coming soon"; index row flips on delivery.
- **Board data integrity**: every worked-example board is a genuine, well-posed position or a clearly marked fragment; the gate validates boards it can fully check.
- **A reader arrives from chapter 01 expecting kid wording**: the page opens by saying it talks to grown-up solvers now (one line), so the register shift is explicit, not jarring.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page MUST exist at the lessons location for chapter 02, following the shared template (learn list, technique body, try it, checkpoint).
- **FR-002**: The page MUST teach, each as its own section with the Brief's exact name: naked pair/triple/quad, hidden pair/triple/quad, pointing, claiming — with the mirror relationship between pointing and claiming stated explicitly.
- **FR-003**: Naked pair, hidden pair, pointing, and claiming MUST each have at least one worked display board marking both the pattern's cells and the cells that lose candidates; triples and quads MUST be covered as direct extensions of the pair idea with at least one shared example each.
- **FR-004**: Every new term MUST be defined with an example at first use, and technique names MUST match the Brief exactly.
- **FR-005**: The page MUST pass the plain-English language budget (sentences ≤ 25 words) with game terminology matching the app's wording.
- **FR-006**: The "Try it" section MUST link to the game and instruct: difficulty Medium, New game, then hunt for one pair before anything else.
- **FR-007**: The checkpoint MUST pose 2–3 "can you…?" questions matching the chapter's graduation criterion, at least one of which distinguishes pointing from claiming on prepared boards.
- **FR-008**: Footer navigation MUST follow the existing-neighbors-only policy (prev to chapter 01 live; next as "coming soon" until chapter 03 exists) and the index row MUST flip to a link.

### Key Entities

- **TechniqueSection**: plain-English what/when, worked example boards, Brief-exact name and one-liner.
- **DisplayBoard**: validated well-posed position or clearly marked fragment; pattern cells and affected cells marked.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can spot a naked pair and a pointing pattern on prepared boards (checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget end to end (readability gate exit 0 — pass/fail).
- **SC-003**: The page loads with zero page errors, all template sections, all links resolving, boards rendering (lesson gate exit 0 — pass/fail).
- **SC-004**: The game remains untouched by this spec (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- Framework, gates, and index come from spec 000; gate extensions assert this page's specifics (technique sections present, checkpoint content).
- Pencil-mark (notes) usage is assumed taught by the game's own help; this page may remind the reader to note digits using the game's word, notes.
- Worked boards may be positions from generated medium puzzles (engine seam, tests/engine.test.mjs:9-12) or hand-built fragments, provided each is validated or clearly marked as a fragment.
- Parked: deep-linking Medium into the game; strict quads tutorials (the pair-extension treatment covers them); progress tracking.
