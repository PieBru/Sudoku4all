# Feature Specification: Advanced Lesson Page, Part 1 — AIC and Single-Digit Chains (chapter 04)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Done

**Input**: specs/proposal.md §3 (chapter 04 row), §4 (L3, L6), §5 (row `006-advanced-chains`), §5.1, §7; Brief §Tier 4 (AIC concept + single-digit chain family)

## Context (OBSERVED)

- Technique source: the Brief, section *Tier 4 — Advanced*. The unifying concept comes first in the Brief: the **AIC — Alternating Inference Chain**, strong links ("A or B must be true") alternating with weak links ("not both true"); almost every named chain technique is a special case. Techniques in this half: simple coloring / X-chain, X-Cycles, XY-Chain, 3D Medusa, grouped chains. (ALS family, Death Blossom, APE, Bowman's Bingo, forcing chains belong to spec 007, which completes the page.)
- Graduation for the finished chapter (proposal §3): follow a worked AIC chain and find an XY-Wing on a prepared board. The XY-Wing find is checkable here as a bridge from chapter 03; the full checkpoint lands with spec 007.
- Language tier: plain English (L3). Chains are the first genuinely abstract topic; the page must earn the concept with pictures before the vocabulary (strong link / weak link) sticks.
- Framework from spec 000; prev neighbor chapter 03 exists (completed by specs 004+005 before this builds); next neighbor chapter 05 does not exist yet. This spec also flips chapter 03's next link to live when it lands (its own footer prev points at chapter 03).
- The game's Expert difficulty (CLUES expert = 25, sudoku.html:681) is the practice target.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The big idea: clues that pass the baton (Priority: P1)

A solver fluent in wings reads the opening. Two kinds of connection are shown on boards before any name: "at least one of these two is true" (strong) and "both cannot be true" (weak). Then a chain is walked cell by cell on a board sequence: if the start is false, the truth flows along the chain and the end contradicts — so the start is true, and everything that sees both ends of a contradiction dies. The name AIC arrives last.

**Why this priority**: everything else in the chapter is this one idea in costume; teaching it first is the difference between understanding and memorizing names.

**Independent Test**: the reader follows a worked chain board-by-board and says which cells die and why.

**Acceptance Scenarios**:

1. **Given** the opening section, **When** strong and weak links are introduced, **Then** each is shown on its own board picture before the terms are used.
2. **Given** the worked AIC chain, **When** the reader steps through it, **Then** each step's board marks the current link and the conclusion names the eliminated candidate(s) and why.
3. **Given** the section end, **When** the reader meets "AIC", **Then** the term is defined in one sentence tying together what they just did.

### User Story 2 - Coloring: the chain you can see (Priority: P1)

Simple coloring / X-chain is taught as the same idea on one digit: two colors, alternating down the conjugate links; any cell seeing both colors dies; two same-color cells colliding kills the whole color. A worked board shows both outcomes.

**Why this priority**: coloring is the everyday expert-puzzle workhorse and the gentlest chain entry point.

**Independent Test**: the reader colors along a prepared board and marks the elimination.

**Acceptance Scenarios**:

1. **Given** the coloring section, **When** the two colors are placed on the board, **Then** the alternating rule is stated once and the picture obeys it.
2. **Given** a cell seeing both colors, **When** the reader reasons, **Then** that cell loses the digit and the board marks it.
3. **Given** X-Cycles and 3D Medusa, **When** read, **Then** X-Cycles is presented as coloring closed into a loop and 3D Medusa as coloring extended to all digits at once, each with one board.

### User Story 3 - XY-Chains and grouped links at walking pace (Priority: P2)

XY-Chain: bivalue cells handing the baton; worked board with the hand-offs marked. Grouped chains: the chain may pass through a set of cells instead of one, shown as a box-line highlight riding along the board.

**Why this priority**: these unlock the last stubborn puzzles before solver territory; grouped links prevent "that step is illegal" confusion.

**Independent Test**: the reader traces an XY-Chain's hand-offs and names the victim.

**Acceptance Scenarios**:

1. **Given** the XY-Chain section, **When** read, **Then** each hand-off between bivalue cells is marked in order on the board and the final elimination is shown.
2. **Given** the grouped chains section, **When** read, **Then** one worked example shows a highlighted cell-set link and states the rule for when it is legal.

### Edge Cases

- **Page completeness**: until spec 007 lands, the page carries a visible "part 1 of 2" marker; next-neighbor slot stays "coming soon".
- **Checkpoint scope**: part-1 checkpoint covers the AIC concept, coloring, and an XY-Wing find only; spec 007 installs the full checkpoint.
- **Cognitive load**: each chain example must be ≤ 6 steps with one board per step or a clearly stepped single board; longer chains are out of pedagogical scope.
- **Board integrity**: chain boards are hand-built fragments, clearly marked (a generated full position rarely contains a teaching-ready chain); fragment marking is mandatory.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page shell MUST exist at the lessons location for chapter 04 with the shared template sections, a visible "part 1 of 2" marker, and an opening line stating expected background (chapter 03).
- **FR-002**: The page MUST open with the chain concept — strong link and weak link each shown on a board before naming, then a worked AIC chain of at most 6 steps with the conclusion's eliminations marked.
- **FR-003**: The page MUST teach simple coloring / X-chain with a worked board showing the alternating two colors and a both-colors elimination; X-Cycles and 3D Medusa MUST each be presented as the stated extension with one board.
- **FR-004**: The page MUST teach XY-Chain with hand-offs marked in order and the final elimination shown, and grouped chains with one worked cell-set example and its legality rule.
- **FR-005**: Every new term MUST be defined with an example at first use; names MUST match the Brief exactly; the page MUST pass the plain-English budget (≤ 25-word sentences).
- **FR-006**: The "Try it" section MUST link to the game and instruct: difficulty Expert, New game, then try one digit's coloring before reaching for anything else.
- **FR-007**: The part-1 checkpoint MUST pose 2–3 "can you…?" questions covering the AIC idea, a coloring elimination, and finding an XY-Wing on a prepared board.
- **FR-008**: Footer navigation MUST follow the existing-neighbors-only policy (prev to chapter 03 live — and chapter 03's next link MUST flip to this page when it lands), next "coming soon"; index row flips to a link.

### Key Entities

- **ChainStep**: one link in a worked chain — the cells involved, the link type, the board state.
- **TechniqueSection**: plain-English what/when, worked board(s), Brief-exact name and one-liner.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can follow a worked AIC chain and find an XY-Wing on a prepared board (part-1 checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget (readability gate exit 0 — pass/fail).
- **SC-003**: The page loads with zero page errors, template sections present, "part 1 of 2" marker present, all links resolving, boards rendering (lesson gate exit 0 — pass/fail).
- **SC-004**: The game remains untouched (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- Spec 007 completes this page (ALS family, Death Blossom, APE, Bowman's Bingo, forcing chains, full checkpoint, marker removal) — those are out of scope here.
- Chain examples are hand-built, clearly marked fragments; generating teaching-ready chains from the engine is explicitly not attempted.
- A "when to stop" escalation-discipline note belongs to the completed page (spec 007 installs it with the last-resort content).
- Parked: deep-linking Expert; interactive chain-building toys; progress tracking.
