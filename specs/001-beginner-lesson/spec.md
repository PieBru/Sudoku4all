# Feature Specification: Beginner Lesson Page (chapter 01)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §3 (chapter 01 row), §4 (L1, L2, L6), §5 (row `001-beginner-lesson`), §5.1, §7, Appendix A, Appendix B

## Context (OBSERVED)

- Spec 000 delivers the framework this page plugs into: lessons index, shared stylesheet, the display-board renderer, the Learn link, and both gates (readability + lesson-page boot). Built first per the proposal's build order; this is the first content chapter (user directive: begin with the Beginner page).
- Technique source: the Brief (`outputs/sudoku-solving-methods-brief.md`), section *Tier 1 — Beginner: scanning and singles*: scanning/cross-hatching, full house/last digit, hidden single, naked single. The Brief is the technique source of truth (proposal §6); wording may be simplified, claims may not be invented.
- Language bar set by proposal Appendix A (the "Find the 7!" cross-hatching sample): sentences aim ≤ 10 words, ceiling 15; every term explained in kid words before its grown-up name; "For grown-ups" asides carry the precise version.
- App terminology to mirror (L6): "New game", "Restart puzzle", notes, "Undo", "Hint" (sudoku.html:407-417). Kid text says *notes*, never "pencil marks".
- Display-board data must be genuine positions: the engine harness seam (tests/engine.test.mjs:9-12, `Function` wrapper exporting `genFull`/`makePuzzle`/`validPuzzle`) generates and verifies well-posed easy puzzles (CLUES easy = 40, sudoku.html:681).
- Readability gate budgets for this page (proposal §7): max sentence ≤ 15 words, average ≤ 10, banned jargon absent outside asides.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A kid learns the first trick and it clicks (Priority: P1)

A 6-year-old who can read simple sentences opens the Beginner page. Short sentences and everyday words walk them through finding where a digit goes. Every idea is shown on a real board, not just described. By the end they find placements themselves on the worked examples.

**Why this priority**: the chapter's whole reason to exist — a beginner who completes it can solve an easy puzzle.

**Independent Test**: a reader with no Sudoku knowledge reads the page top to bottom and answers the checkpoint questions; nothing above a 6-year-old reading level is required.

**Acceptance Scenarios**:

1. **Given** the Beginner page, **When** a young reader reads any main-text sentence aloud, **Then** it is at most 15 words long and uses everyday words (language-budget gate passes).
2. **Given** the cross-hatching lesson, **When** the reader follows it board by board, **Then** at least two step-by-step boards show the same digit hunt progressing from blocked cells to the single place it fits.
3. **Given** any technique section, **When** the grown-up name first appears, **Then** the kid-words explanation has already been given ("Grown-ups call this …").

### User Story 2 - A grown-up gets the precise version (Priority: P2)

An adult reading the same page wants the proper terms without wading through childish prose. Each section carries a short "For grown-ups" aside with the technique's real name and its exact definition from the Brief.

**Why this priority**: dual audience is a proposal hard rule (L2); adults must never feel babied.

**Independent Test**: read only the asides; they alone give a complete, correct Tier-1 vocabulary.

**Acceptance Scenarios**:

1. **Given** any technique section, **When** the reader opens its "For grown-ups" aside, **Then** it names the technique exactly as the Brief does and states its definition without contradiction.
2. **Given** the full page, **When** the four Tier-1 techniques are tallied, **Then** cross-hatching, full house, hidden single, and naked single are each present with an aside.

### User Story 3 - From lesson to game in one hop (Priority: P2)

A reader who finishes the page wants to try it immediately. The "Try it" section links straight to the game with one concrete instruction.

**Why this priority**: converts reading into playing while the trick is fresh.

**Independent Test**: follow the Try it link and its instruction; the game opens and the instruction is followable verbatim.

**Acceptance Scenarios**:

1. **Given** the Try it section, **When** the reader follows the link, **Then** the game opens.
2. **Given** the instruction ("pick Easy, press New game, find all the 7s first" in kid wording), **When** the reader does it in the game, **Then** every named control exists with that exact wording (Easy, New game).

### Edge Cases

- **Neighbor pages may not exist yet**: footer prev/next shows "coming soon" markers instead of links for missing neighbors; every link that does render must resolve.
- **A reader taps Try it while a saved game is open**: the game resumes the saved game by design — the instruction explicitly starts with pressing New game, so no confusion.
- **Board data typos**: worked-example boards are validated positions; a board whose data is not a well-posed position fails the lesson gate, not the reader.
- **Notes vocabulary**: pencil-mark technique is not taught here; the word used is the game's word, *notes*, and only to name the feature.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page MUST exist at the lessons location named by the curriculum map for chapter 01, following the shared page template: a "you will learn" list, a technique body, a "try it" section, and a checkpoint section.
- **FR-002**: The page MUST teach, in order: cross-hatching (framed as scanning for a digit's only home), full house ("the last empty square"), hidden single, naked single — each section explaining what it is in kid words first and giving the grown-up name last.
- **FR-003**: Every technique section MUST include at least one worked example on a display board; cross-hatching MUST include at least two boards showing the hunt step by step.
- **FR-004**: At least two display boards MUST use genuine positions from the game's own generator (well-posed easy puzzles, givens consistent with a unique solution).
- **FR-005**: Every technique section MUST carry a "For grown-ups" aside of 1–3 adult-tone sentences naming the Brief's term and definition.
- **FR-006**: Main text MUST pass the kid language budget: sentences ≤ 15 words (average ≤ 10), everyday words, banned jargon absent outside asides, and game terminology matching the app's wording.
- **FR-007**: The "Try it" section MUST link to the game and instruct: choose Easy, press New game, then hunt one digit at a time as practiced.
- **FR-008**: The checkpoint MUST pose 2–3 "can you…?" questions matching the chapter's graduation criterion (solve an easy puzzle using scanning and cross-hatching on your own).
- **FR-009**: Footer navigation MUST link only to existing neighbor pages, showing "coming soon" markers otherwise, and the index row for this chapter MUST change from "coming soon" to a link.

### Key Entities

- **TechniqueSection**: kid-words explanation, when-to-use line, worked example boards, grown-up aside (Brief term + one-liner).
- **DisplayBoard**: 81-character givens string from a verified well-posed position; given cells locked.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The page passes the kid language budget end to end (readability gate exit 0 — pass/fail).
- **SC-002**: The page loads with zero page errors, all template sections present, all links resolving, and every display board rendering 81 cells (lesson gate exit 0 — pass/fail).
- **SC-003**: All four Tier-1 techniques are present with worked boards and grown-up asides (content check inside the lesson gate — pass/fail).
- **SC-004**: The game remains untouched by this spec (existing engine and browser gates exit 0 unchanged — pass/fail).

## Assumptions

- Framework pieces (stylesheet, board renderer, gates, index) come from spec 000; this spec adds content plus the small gate extensions that assert this page's specifics.
- Pencil-mark technique teaching is out of scope (notes are only named) — pairs and every Tier 2+ technique belong to later chapters/specs.
- The worked-example boards may mix generated positions and hand-finished fragments, provided every board's data is validated; fragments clearly mark the cells under discussion.
- Parked (proposal §5.2): deep-linking a difficulty into the game; a strict mistakes mode; progress tracking.
