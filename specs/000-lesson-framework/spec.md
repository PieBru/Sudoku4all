# Feature Specification: Lesson Framework — index, board renderer, Learn link, gates

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §1, §5 (row `000-lesson-framework`), §5.1, §5.2, §7, Appendix C

## Context (OBSERVED)

Reuse seams verified on disk in this repo:

- The app is the single file `sudoku.html` (committed, 1304 lines). Design tokens live in `:root` with `color-scheme: light dark` (sudoku.html:8-9); a `prefers-color-scheme` dark block follows (26-27) and explicit `[data-theme="light"|"dark"]` blocks exist (45-46, 63-64). Lesson styling reuses this look.
- The toolbar carries the app's user-facing wording — "New game" (407), "Restart puzzle" (408), notes toggle (412), "Undo" (415), "Hint" (417). The Learn link lands in this toolbar area.
- The board-visual pattern to mirror: structural per-cell classes in `BOXCLS` (701-718) and `render()` rebuilding class names from them (894-903), producing 2×3 thick box separators.
- Difficulty targets `CLUES = {easy:40, medium:34, hard:29, expert:25}` (681) — used by later specs' "Try it" instructions.
- Existing gates: `tests/engine.test.mjs` extracts the app engine through a `Function` wrapper (9-12) — the same seam can generate verified puzzle positions for display boards; `tests/browser.test.py` drives pages via a `file://` URL with a `check(name, cond, evidence)` pattern (13-29). The Python gate env pins `playwright` (pyproject.toml).
- `.specify/init-options.json` sets sequential numbering; `specs/` contains only `proposal.md`, so this feature is spec 000.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reach the chapter index from the game (Priority: P1)

A player has the game open and wants to get better. A **Learn** control sits with the familiar buttons; activating it opens a chapter index that lists all six chapters of the learning ladder, each with its number, title, and one line saying who it is for. Nothing on the index dead-ends: chapters that are not built yet appear as clearly marked "coming soon" rows, never as broken links.

**Why this priority**: the index is the single entry point of the whole learning ladder; without it no lesson is discoverable from the product.

**Independent Test**: open the app, activate Learn, read the index — value is delivered even before any chapter page exists.

**Acceptance Scenarios**:

1. **Given** the app is open, **When** the learner activates Learn, **Then** the lessons index opens, listing six chapters, each with number, working title, and a one-line audience description.
2. **Given** the index, **When** the learner follows any chapter link, **Then** the destination page exists (no broken links; unbuilt chapters render as non-link "coming soon" rows).
3. **Given** a first-timer lands on the index, **When** they read the short 3-question guide, **Then** they can tell which chapter to start from, with "Start here" guidance visible for both never-played and already-playing visitors.

### User Story 2 - Meet a real board on the index page (Priority: P2)

The index shows one demonstration Sudoku board so an absolute beginner meets the 9×9 grid — with its 3×3 box structure — before opening any chapter.

**Why this priority**: orients beginners and proves the shared board renderer every chapter will rely on.

**Independent Test**: load the index alone; the demo board renders correctly.

**Acceptance Scenarios**:

1. **Given** the index page, **When** it loads, **Then** a display board renders 81 cells with the 3×3 box structure visually distinct, exactly like the game's board.
2. **Given** the demo board's data, **When** validated, **Then** it is a genuine, well-posed puzzle position (givens consistent, exactly one solution), generated from the app's own engine.

### User Story 3 - Lessons feel like the game, in any theme (Priority: P3)

A reader whose system is in dark mode gets dark lesson pages with readable contrast; a reader with scripts blocked still reads all text content.

**Why this priority**: consistency and graceful degradation matter, but only after discoverability and rendering exist.

**Independent Test**: open the index with the OS in dark mode, then with page scripts disabled.

**Acceptance Scenarios**:

1. **Given** a dark system theme, **When** the index opens, **Then** it renders in dark colors with readable text (same behavior as the app, which already declares `color-scheme`).
2. **Given** page scripts are blocked, **When** the index opens, **Then** all text content remains readable (the demo board area may be empty; no error state).

### Edge Cases

- **No chapter pages exist yet** (this spec ships before them): the index must show all six chapters with unbuilt ones as "coming soon", never as links.
- **`file://` relative navigation**: app → lessons/index.html and index → chapter pages must resolve as relative links from the project root.
- **Scripts disabled**: text content readable; no crash, no blank page.
- **Very narrow screens**: index text wraps; no horizontal scrolling needed to read a line.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The product MUST provide a lessons index page that lists all six chapters of the learning ladder (00 First Steps through 05 Extreme), each showing its number, working title, and a one-line audience description matching the proposal's curriculum map.
- **FR-002**: The index MUST include a short "which chapter is for me?" self-guide (3 questions in beginner-friendly wording) and "Start here" guidance distinguishing never-played visitors (chapter 00) from visitors who already play (chapter 01).
- **FR-003**: Chapters whose pages do not exist yet MUST appear as clearly marked non-link "coming soon" rows; every link on the page MUST resolve to an existing page.
- **FR-004**: The index MUST embed one demonstration 9×9 board whose givens come from a genuine, well-posed puzzle position; the board MUST render 81 cells with visually distinct 3×3 boxes, matching the game's board look.
- **FR-005**: A shared board renderer MUST turn a compact 81-character givens description into the rendered display board, with given cells visually locked; it MUST be the only script the lesson pages load for display boards.
- **FR-006**: Lesson pages MUST share one stylesheet that reproduces the game's visual language and supports both light and dark appearances (system preference and explicit), consistent with the app's existing theme behavior.
- **FR-007**: The game MUST offer a **Learn** control in its toolbar, operable by mouse and keyboard, that opens the lessons index; this MUST be the only change to the game made by the ladder specs (the separate Training Studio track, `specs/proposal-training.md`, reserves spec numbers 009–011 and changes the app under its own gates).
- **FR-008**: A language-budget gate MUST verify every existing lesson page against the proposal's readability rules: kid-readable budgets for chapter 00/01 pages and their index rows, plain-English budgets for chapters 02+, with a banned-jargon list enforced outside "For grown-ups" asides.
- **FR-009**: A lesson-page gate MUST verify, for every existing lessons page (the index included): zero page errors on load, required template sections present on chapter pages, all links resolving to real destinations, and every board rendering the cell count for its size — 81 cells for 9×9 display boards, 16 for size-4 and 36 for size-6 playable boards (`data-size`).
- **FR-010**: The two existing product gates (engine checks and the browser play-flow checks) MUST remain green after this feature; the only permitted difference in the game is the Learn control.

### Key Entities

- **LessonPage**: chapter number, file name, working title, audience line, built/coming-soon status.
- **DisplayBoard**: an 81-character givens string plus rendered form; given cells locked.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A learner reaches the chapter index from the game with exactly one interaction (verified by the browser gate's Learn-link check).
- **SC-002**: Zero broken links anywhere in the lessons pages (verified by the lesson gate's link-resolution check — pass/fail).
- **SC-003**: Every lessons page passes its language budget (verified by the readability gate — pass/fail, exit 0).
- **SC-004**: The game's behavior is unchanged except the Learn control (verified by the existing engine and browser gates both passing — pass/fail).

## Assumptions

- Chapter content is delivered by specs 001–008; this spec intentionally ships no chapter page.
- Banned-jargon baseline for kid-facing surfaces (chapters 00/01): candidate, eliminate(d), constraint, subset, intersection, bivalue, bilocation, chain, fish, wing, uniqueness, and "pencil mark" (kid text says *notes*, matching the game's button wording). Enforced outside "For grown-ups" asides.
- The readability gate uses a naive sentence splitter (proposal §7 `ponytail:` note) — upgrade only if it misfires.
- Parked per proposal §5.2 (not this spec's scope, not promoted): no deep-linking into the game, no progress tracking, no accounts, no internationalization.
- The playable fun-size board script (`mini.js`) belongs to spec 002, not to this framework.
- Footer-link policy used by all later specs: prev/next navigation links only to pages that exist; missing neighbors render as a "coming soon" marker that the neighbor's spec later flips to a real link.
