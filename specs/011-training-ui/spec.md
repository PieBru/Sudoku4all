# Feature Specification: Training Studio Panel (UI, persistence, print)

**Feature Branch**: `specify/training-studio`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal-training.md §1 (goal), §2 (directives), §4 (levels + checklist semantics), §6 (UI and output), §7 + Appendix B (persistence schema), §8 (Training UI gate), §9 decisions 2/3/5/8/10/11/12

## Context (OBSERVED)

- The settings menu the panel joins is `<details id="menu">` (sudoku.html:391) with a `.panel` of `.row` divs (397-421) and `label.chk` checkbox styling (422); toolbar buttons follow the emoji-plus-words convention (`New game` 407, `Restart puzzle` 408, `Undo` 415, `Hint` 417). A second nested `<details id="help">` (424) shows the collapsible-section pattern to copy.
- The confirm-on-destructive convention exists: `confirm("Start a new game? …")` (1180) and `confirm("Restart this puzzle? …")` (1192) — Generate-over-an-in-progress-game reuses it verbatim in spirit (proposal §6.1).
- The status surface exists: `<div id="live" class="sr-only" aria-live="polite">` (456) is the app's announce channel; the win veil (460) demonstrates result surfacing.
- Persistence conventions: `KEY sudoku-v1` (678, commented), `STATS_KEY` (679), `THEME_KEY` (680), with `save()` (784) / `load()` (806) / `loadStats()` (850) showing the schema-commented try/catch pattern; the training key `sudoku-training-v1` follows Appendix B's commented schema and never touches the other keys.
- The generator (spec 010) returns pure data: board, solution, givens, clue count, report — the panel's whole job is presenting it; `winGame()` (975) and the game-state functions show where a generated board becomes the active game.
- The browser gate pattern is established: `tests/browser.test.py` drives the `file://` URL with a `check(name, cond, evidence)` helper and pageerror collection (12-30); this spec adds a training section to it (proposal §8).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configure and generate a training board (Priority: P1)

The player opens the settings menu, finds the Training section, picks Intermediate, sees only Beginner+Basic+Intermediate technique groups (nothing ahead of the level), unticks Jellyfish, presses Generate, confirms the overwrite of their in-progress game, and gets a playable training board with a one-line solve-path report.

**Why this priority**: this is the feature's entire user-facing contract — every directive (§2) lands here.

**Independent Test**: drive the panel in the browser gate end to end: open → filter → uncheck → generate → play one digit on the generated board.

**Acceptance Scenarios**:

1. **Given** the panel, **When** a level is selected, **Then** only groups ≤ that level are visible, all pre-checked per §4 (saved unchecks winning), and the technique checklist carries its player-facing labels with Beginner's two singles locked and explained in one line.
2. **Given** a game in progress, **When** Generate is pressed, **Then** the confirm dialog appears (same convention as New game); canceling aborts generation, confirming replaces the game with the generated board.
3. **Given** generation succeeds, **When** the board appears, **Then** it is playable with all standard game features (undo, notes, hints, mistakes count — decision 12) and the report line reads like *"Solve path (easiest techniques first): hidden single, pointing, X-Wing."*, labeled as the solver's own path.
4. **Given** generation fails (budget/tripwire), **When** the failure returns, **Then** the status line announces why + what to do + retry via `aria-live` — never silence, never a half-cleared panel.

### User Story 2 - All / None and saved state behave like a tool, not a trap (Priority: P1)

The All and None buttons toggle exactly the currently selected level's group — one click, predictable scope; at Beginner both sit disabled with the reason visible (the group is two locked singles). Preferences survive reload; switching levels restores the player's saved unchecks.

**Why this priority**: the one-button enable/disable directive (§2) and the saved-state-wins rule (§4) are exact operator requirements.

**Independent Test**: browser gate toggles groups, reloads, switches levels, and asserts persistence and scope.

**Acceptance Scenarios**:

1. **Given** the Basic group partially checked, **When** All then None are pressed, **Then** only the Basic group flips (Beginner's singles stay locked-checked; Intermediate boxes untouched if visible).
2. **Given** Beginner selected, **Then** All/None are disabled and the one-line "singles are always needed" explanation is visible at the locked checkboxes.
3. **Given** the player unchecked `naked_quad` in Basic and `jellyfish` in Intermediate, **When** the page reloads and levels are switched, **Then** saved unchecks are restored (saved state always wins over the default all-checked), stored by stable ID.
4. **Given** Advanced, **Then** it renders visibly disabled with its reason ("Chain techniques cannot be verified yet — coming in a future version."), never silently absent.

### User Story 3 - Print the board with or without the solution (Priority: P2)

The player wants paper practice: they tick *include solution*, press Print, and get the grid on one page and the solved grid on a second page; unticked, just the grid. Browser-native print-to-PDF; nothing else ships.

**Why this priority**: the with/without-solution directive (§2); after playing and persistence it completes the output options.

**Independent Test**: emulate print media in the browser gate and assert what is shown/hidden per the checkbox.

**Acceptance Scenarios**:

1. **Given** a generated board and *include solution* unchecked, **When** print media is active, **Then** the grid prints alone, one page, solution page absent.
2. **Given** *include solution* checked, **Then** the solved grid is additionally rendered as its own print page; the on-screen game is unaffected.

### Edge Cases

- **Corrupt or older `sudoku-training-v1` save**: falls back to defaults with a loud status-line note, never silently (Appendix B); unknown fields ignored.
- **localStorage unavailable (private mode)**: the app's existing guarded try/catch convention applies — training still works per session, no crash (matches the game key's behavior).
- **Level switch mid-configuration**: newly shown group defaults to all-checked except where saved unchecks exist (saved state wins); a group never re-checks boxes the player explicitly unchecked.
- **Unchecking a whole level**: legitimate and documented in the panel — it trains the levels below at that level's carve depth (proposal §6.1).
- **Generate pressed with no game in progress**: no confirm dialog; straight to generation.
- **Generation failure mid-flow**: previous game stays intact unless the player confirmed replacement first; the failure announcement carries the actionable message (spec 010's text) and a real retry path (press Generate again).
- **Print before any training generation**: the print view reflects the *active* board (training or casual); the optional solution page uses that board's solution — printing is never tied to a stale generated result.
- **Page busy during generation**: the generator may busy the page up to its wall-clock cap (≤ 5 s, spec 010 FR-004); Generate cannot re-enter while a run is in flight.
- **Advanced level press**: does nothing but explain (disabled + reason), including keyboard users (`aria-disabled`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A collapsible Training section MUST exist inside the existing settings menu (`#menu`), following the app's DOM/ARIA conventions (details pattern, `.row`/`label.chk` styling, emoji-plus-words buttons) and the every-control-explains-itself rule.
- **FR-002**: The level selector MUST offer Beginner / Basic / Intermediate as segmented buttons plus Advanced visibly disabled with its stated reason (tooltip + `aria-disabled`); selecting a level shows exactly the technique groups ≤ that level, pre-checked per §4 with saved unchecks winning.
- **FR-003**: The checklist MUST implement Appendix A exactly: 19 boxes with player-facing labels, keyed by stable snake_case IDs; the two Beginner singles MUST be locked on with a one-line explanation; techniques ahead of the level are never displayed.
- **FR-004**: All / None buttons MUST toggle only the currently selected level's group and MUST be disabled at Beginner.
- **FR-005**: Generate MUST call spec 010's generator with the current checked set, ask for confirmation under the app's own condition (started and not won — sudoku.html:1179-1180), adopt the resulting board as the active game on success by resetting the full game state exactly like `newGame()` does (sudoku.html:1110-1125: notes, selection, mistakes, hints, elapsed, pause, won) with the solution hidden and undo/notes/hints/mistakes all functional (decision 12), and show the one-line solve-path report honestly labeled as the solver's own cheapest-first path.
- **FR-006**: The run MUST be announced before it starts ("Building your board…") and its outcome on completion, both through the app's `aria-live` status div; failures MUST state why + what to do and offer retry; no silent states. (Mid-run progress updates are optional — the generator may busy the page up to its wall-clock cap, spec 010 FR-004.)
- **FR-007**: Preferences MUST persist under `sudoku-training-v1` per Appendix B's commented schema (level + per-level unchecked IDs, stable IDs only, additive-only, unknown fields ignored, corrupt/older saves fall back to defaults loudly in the status line), saved on every change, restored on open; the key MUST NOT touch `sudoku-v1`, `sudoku-stats-v1`, or `sudoku-theme-v1`.
- **FR-008**: A Print control MUST produce browser-native output via `@media print` CSS + `window.print()`: the grid on one page (the active board's current entries — givens and placed digits — never on-screen notes), the solved grid on a second page only when *include solution* is checked; no export code paths beyond CSS.
- **FR-009**: The casual game MUST remain untouched: existing `tests/engine.test.mjs` and the existing `tests/browser.test.py` sections stay green; only additive changes to the app.

### Key Entities

- **TrainingPanel**: level selector, grouped checklist, All/None, Generate, Print controls; source of the checked-set the generator consumes.
- **TrainingPrefs**: level + per-level unchecked technique IDs (stable); schema of Appendix B.
- **ReportLine**: the solver's cheapest-first technique path, honestly labeled.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The training section of `uv run python tests/browser.test.py` exits 0: panel opens; level select filters the checklist; level switch restores saved unchecks; checkboxes persist across reload; All/None toggle only the current group and are disabled at Beginner; singles locked; Advanced disabled with reason.
- **SC-002**: Generate flow verified end to end: confirm dialog on in-progress games (and none otherwise), generated board playable (a digit placed lands correctly), report line present and correctly labeled; failures announced via `aria-live`.
- **SC-003**: Persistence verified: `sudoku-training-v1` written on change, restored on open, stable-ID keyed (label rename cannot orphan it — asserted by reading the stored object), corrupt-save fallback loud.
- **SC-004**: Print view verified under emulated print media: grid visible alone without *include solution*; solved grid additionally present with it; on-screen game unaffected.
- **SC-005**: Existing app gates exit 0 (`node tests/engine.test.mjs`, existing browser sections) — the casual game flow is untouched (proposal §8 "App unharmed").

## Assumptions

- The generator and solver are specs 009/010; this spec consumes their data contract only (board, solution, givens, clue count, report, failure reason + message).
- Parked per proposal §6.3's `ponytail:` note: no PNG/text export, no seed sharing in v1.
- Parked for v2 (join only when detectors are gate-verified, per proposal §4): finned/sashimi/franken/mutant fish, empty rectangle, WXYZ-wing, uniqueness family, Sue de Coq, remote pairs, ALS, chains — and the Advanced level's activation with them.
- Report-line wording is fixed content ("Solve path (easiest techniques first): …"); exact technique labels come from Appendix A.
- No progress tracking, accounts, or i18n (project-wide fence, shared with the lesson ladder).
