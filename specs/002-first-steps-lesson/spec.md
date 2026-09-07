# Feature Specification: First Steps Lesson Page (chapter 00, fun-size boards)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Done

**Input**: specs/proposal.md §3 (chapter 00 row), §3.1 (fun-size ladder + mini.js UX), §4 (L1, L2, L4, L6), §5 (row `002-first-steps-lesson`), §7, Appendix D

## Context (OBSERVED)

- This chapter has no Brief section — the Brief starts at beginner techniques; the proposal (§6) makes first principles plus the app's own UI the source. It teaches what the game is and how to hold it, not any solving technique.
- Fun-size ladder fixed by proposal §3.1: fruit 4×4 → digit 4×4 → digit 6×6 → bridge to 9×9; concepts (row, column, cell, box) are named *while playing*, never in a text wall first.
- A verified real puzzle pair exists for the fruit 4×4 (proposal Appendix D, checked 2026-09-07): puzzle `1.34341..14343.1`, solution `1234341221434321` — valid grid, exactly one solution. The digit 4×4 and 6×6 pairs are authored in this spec's implementation and validated by the gate the same way.
- Playable boards are pure data: size, box dimensions, puzzle, solution, optional symbols — no solver ships (proposal Appendix D). A tiny playable-board script (the only new script besides the framework's display renderer) renders and checks them in the page.
- App terminology to mirror (L6): New game (407), Restart puzzle (408), notes (412), Undo (415), Hint (417) at sudoku.html:407-417; given cells in the app look pinned — the fun-size boards copy that look.
- Fear-killers required up front (L4, honest form sealed by proposal v3): no math is needed; the lessons are never timed and never count mistakes; Undo and Hint always exist. The real game does measure — its clock only reports how fast you were and never rushes you, and it counts mistakes without punishing one (Undo always rescues). The page says this plainly instead of promising a timer-free game the app cannot deliver.
- Framework pieces (index row for chapter 00, stylesheet, kid language budget, lesson gate) come from spec 000; this spec extends the gate with fun-size validation and playability checks.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A frightened adult wins their first game in one minute (Priority: P1)

An adult who always avoided Sudoku opens the page. Up front it says: no math needed, nothing here is timed, you cannot fail here — and the real game's clock only watches, it never rushes. They play the fruit board — four fruits, sixteen squares — tap a cell, tap a fruit. A wrong fruit wobbles and disappears; nothing is counted, nothing turns red. The board fills; a small celebration appears. Fear did not get a foothold.

**Why this priority**: the chapter exists to convert fear into fun at first contact; everything else is secondary.

**Independent Test**: hand the page to someone who has never played; they complete the fruit board unaided and smile.

**Acceptance Scenarios**:

1. **Given** the page top, **When** the visitor reads the intro, **Then** all four fear-killers are stated before any game (no math is needed; these lessons are never timed and never count mistakes; Undo and Hint always exist; when you play the real game its clock only reports — never rushes — and its mistake count never punishes, Undo always rescues).
2. **Given** the fruit board, **When** the visitor taps a cell and then a fruit button, **Then** the fruit appears in the cell (big tap targets; number keys 1–4 also work).
3. **Given** a tap that contradicts the solution, **When** it is made, **Then** the cell wobbles gently and stays empty — no mistake counter, no red, no failure state anywhere in this chapter.
4. **Given** the last empty cell is filled correctly, **When** the board completes, **Then** a small celebration appears.

### User Story 2 - A kid learns the words while playing (Priority: P1)

A 6-year-old plays the ladder. As each board appears, one sentence names what they are looking at: this line is a row; this little square is a cell; this thick-bordered chunk is a box. On the 6×6 they notice boxes are wide. By the end they can point at row, column, cell, and box on the real 9×9 picture.

**Why this priority**: the concepts are the chapter's graduation requirement, taught through play, not lecture.

**Independent Test**: after playing, the kid points correctly at a row, a column, a cell, and a box on the big board picture.

**Acceptance Scenarios**:

1. **Given** each fun-size board, **When** it is played, **Then** row, column, cell, and box are each named in kid words during that game.
2. **Given** the digit 4×4 board, **When** it opens, **Then** the text connects it to the fruit board ("the fruits become numbers; the game stays the same").
3. **Given** the bridge section, **When** the 6×6 and the real 9×9 board are shown together, **Then** the text says it is the same game with more squares, and invites playing the real one when ready.

### User Story 3 - The puzzles themselves are trustworthy (Priority: P2)

A helper (parent, teacher) wants certainty the mini games are fair: every board has exactly one solution, its givens are consistent, and its solution is valid.

**Why this priority**: a broken mini puzzle would destroy trust at the most fragile moment.

**Independent Test**: the lesson gate validates every playable board's data mathematically.

**Acceptance Scenarios**:

1. **Given** any playable board on the page, **When** the gate validates it, **Then** the solution is a valid grid (each symbol once per row, column, box), the puzzle matches the solution, and the puzzle has exactly one solution.
2. **Given** a hand-typo'd board, **When** the gate runs, **Then** it fails loudly (the page cannot ship).

### Edge Cases

- **Rapid tapping / changed mind**: re-tapping a filled cell replaces or clears the entry; no stuck states; the wobble never locks input.
- **Keyboard players**: number keys work on digit boards; symbol boards accept keys 1–4 mapped to the four fruits (symbols themselves cannot be typed).
- **Re-completing a board**: the celebration appears once per completion; clearing and re-solving shows it again, with no double-firing during the same completion.
- **Given (locked) cells**: pre-filled cells cannot be changed and look pinned, exactly like the game's givens.
- **Data typos**: impossible puzzle data fails the gate at build time (see User Story 3).
- **Scripts blocked**: the page's text and pictures remain readable; playable boards visibly degrade to their starting picture, no crash.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page MUST exist at the lessons location for chapter 00, follow the shared template, and state all four fear-killers before the first game, in kid-readable language — the fourth being the honest note about the real game (its clock only reports how fast you were, its mistake count never punishes, Undo always rescues).
- **FR-002**: The page MUST contain the three playable fun-size boards in order — fruit 4×4 (2×2 boxes, four fruit symbols), digit 4×4, digit 6×6 (2×3 boxes) — followed by a bridge section showing the 6×6 beside the real 9×9 with an invitation to play the real game.
- **FR-003**: Concepts MUST be named during play in kid words — row, column, cell, box — including that boxes are wide rectangles on the 6×6; never in a text-only preamble before the first game.
- **FR-004**: Playable input MUST be: tap a cell then tap a big symbol/digit button (number keys also accepted — 1–4 on a 4×4, 1–6 on a 6×6); entries contradicting the solution wobble gently and do not stick; there MUST be no mistake counter, timer, red failure styling, or any other failure state on this page.
- **FR-005**: Completing a playable board MUST trigger a small celebration visible to the learner.
- **FR-006**: Given cells MUST be locked and visually pinned like the game's givens.
- **FR-007**: Every playable board's data MUST be validated by the lesson gate: valid solution, puzzle consistent with it, exactly one solution (brute-force check); the fruit 4×4 MUST use the verified pair recorded in the proposal's Appendix D.
- **FR-008**: The lesson gate MUST exercise playability end to end: place an entry via the buttons, verify a contradicting entry wobbles and does not stick, and verify the celebration appears on completion.
- **FR-009**: Main text MUST pass the kid language budget (≤ 15-word sentences, average ≤ 10, no banned jargon outside asides) and use the game's own words for its controls; every section carries a "For grown-ups" aside.
- **FR-010**: The page MUST load only the framework's display renderer plus the one shared playable-board script; footer navigation follows the existing-neighbors-only policy, and the index row for chapter 00 flips from "coming soon" to a link.

### Key Entities

- **MiniPuzzle**: grid size, box dimensions, puzzle string, solution string, optional symbol list; validated as fair (unique solution) before shipping.
- **FunSizeBoard**: a MiniPuzzle in its played form — cell states, locked givens, completion state, celebration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A never-played visitor completes the fruit board and the 6×6 unaided (the chapter's graduation bar; verified by the playability gate exercising a full solve — pass/fail).
- **SC-002**: Every playable board is mathematically fair (gate validation exit 0 — pass/fail).
- **SC-003**: The page contains no failure state of any kind (no counter, timer, or red styling on wrong entries — verified by the playability check — pass/fail).
- **SC-004**: The page passes the kid language budget and loads with zero page errors, all links resolving (readability + lesson gates exit 0 — pass/fail).

## Assumptions

- Deferred (proposal §3.1 `ponytail:` note): no contradiction-hunting is taught here — chapter 01's job; a strict mode for the mini boards is added only if learners bounce at the 9×9 transition.
- The playable-board script is deliberately tiny data-driven rendering; no general Sudoku engine ships in the lessons (the full engine stays in the game).
- The 9×9 bridge uses a static picture of the real board (display renderer), not a playable 9×9.
- Parked: deep-linking into the game (Try it here is the bridge invitation, phrased for the game's New game flow), progress tracking, accounts, internationalization.
