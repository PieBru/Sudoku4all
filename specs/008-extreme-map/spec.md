# Feature Specification: Extreme Reference Map — Champion Territory (chapter 05)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Done

**Input**: specs/proposal.md §3 (chapter 05 row), §4 (L3), §5 (row `008-extreme-map`), §5.1, §7; Brief §Tier 5 + §world-champion layer + learning-ladder table

## Context (OBSERVED)

- Decision fixed by the proposal (§5 decision note + §8 item 3): chapter 05 is an honest map, **not tutorials** — the Brief itself says almost no human uses Tier-5 techniques routinely; they live in solver implementations and hardest-list hobbyist discussions. We do not teach exocet construction.
- Technique source: the Brief, section *Tier 5 — the world's-hardest-puzzle toolkit*: Exocet/Double Exocet, SK Loop, MSLS, Pattern Overlay Method, Tridagon/trivalue oddagon, Oddagons/non-colourable clusters, Whips/Braids (Berthier), Forcing nets/Templates/Kraken fish — plus the last-resort brute-force note. Champion layer (same Brief): what actually differs at the top is execution of tiers 1–3 at speed (Snyder notation, pattern memory, cheapest-first discipline, minimal pencil marks, composure/error-recovery, training apparatus), with the reported records (Thomas Snyder 1:23.93 very easy, 2006; Wang Shiyao 54.44 s championship-grade, WSPC Prague 2018).
- Provenance honesty (Brief sidecar): the records are secondhand (aggregator-sourced; primary Guinness/Xinhua pages not fetched). The page MUST present them as reported records, not as verified primary facts.
- This is the ladder's last page: prev neighbor chapter 04 exists (completed by specs 006+007); no next neighbor exists or is planned — the footer's next slot retires (map ends the ladder).
- External links are allowed on this page only (SudokuWiki, HoDoKu, Sudopedia — the Brief's own references); internal pages never link out elsewhere.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A curious solver reads the map without drowning (Priority: P1)

A solver who finished chapter 04 wonders what lies beyond. The page says it plainly: a territory of named monsters needed only for famous puzzles like AI Escargot; almost nobody uses them by hand; here is what each name means in one line, and where to read more if obsessed.

**Why this priority**: the page's entire job is orientation without intimidation.

**Independent Test**: after reading, the visitor can name any Tier-5 term they meet elsewhere and say where to look it up.

**Acceptance Scenarios**:

1. **Given** the page opening, **When** read, **Then** it states that these tools are for the famous monster puzzles and that almost no one uses them routinely.
2. **Given** the Tier-5 table, **When** the visitor looks up any name from the Brief's list, **Then** they find it with a one-line meaning drawn from the Brief and a where-to-read-more pointer.
3. **Given** the page, **When** the visitor wants the primary sources, **Then** external links to the technique references (SudokuWiki, HoDoKu, Sudopedia) are present and open the references, not homepages.

### User Story 2 - The champion reveal: it was tiers 1–3 all along (Priority: P1)

The page's centerpiece: world-class solving is not a secret tier-6 technique — it is tiers 1–3 executed at extreme speed and accuracy. Snyder notation is explained in kid-accessible plain English (mark a digit only when it fits exactly two cells of a box), the other champion habits are listed, and the reported records are shown as what speed looks like — labeled as reported.

**Why this priority**: it converts "I'll never get there" into "the path is the ladder I just climbed, faster" — the motivational payoff of the whole curriculum.

**Independent Test**: the reader states in one sentence what actually separates champions from them.

**Acceptance Scenarios**:

1. **Given** the champion section, **When** read, **Then** it states that champions run tiers 1–3 at extreme speed and accuracy, not secret techniques.
2. **Given** the Snyder notation explanation, **When** read, **Then** it is understandable by a chapter-01 graduate (plain words, one small example board) and notes that its inventor switches to full notes when a puzzle needs them.
3. **Given** the records display, **When** read, **Then** the times are labeled as reported records with their events (very-easy and championship-grade distinguished), matching the Brief's caveat.

### User Story 3 - The ladder ends with a next step, not a cliff (Priority: P2)

Finishing the map, the visitor gets a closing "your path from here": the Brief's learning-ladder table restated in the page's own words — timed practice, step-hint solvers, one-new-technique-at-a-time — and a link back into the game to play.

**Why this priority**: turns the reference dead-end into a practical continuation.

**Independent Test**: the visitor can name their next training action after finishing the page.

**Acceptance Scenarios**:

1. **Given** the closing section, **When** read, **Then** it lists the training apparatus habits (timed practice, step-hint solvers, learn-one-at-a-time) and links to the game.
2. **Given** the footer, **When** the visitor looks for a next chapter, **Then** the ladder-end is explicit (no dangling next link; the index link remains).

### Edge Cases

- **Over-promising**: no Tier-5 section may imply the reader will learn to apply the technique here — one-liners and pointers only (page-level honesty check).
- **Records accuracy**: times must match the Brief exactly (1:23.93 / 54.44 s) and carry the reported label; conflating the two record classes (very easy vs championship-grade) fails review.
- **External link safety**: out-links open in a new browsing context and go to the named reference pages.
- **Ladder end**: the next-neighbor slot is retired (not "coming soon") — the map is the final chapter by design.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter page MUST exist at the lessons location for chapter 05, following the shared template with its honesty opening: monster-puzzle territory, almost nobody uses these by hand.
- **FR-002**: The page MUST contain a Tier-5 reference table covering every name in the Brief's Tier 5 (Exocet/Double Exocet, SK Loop, MSLS, POM, Tridagon, Oddagons, Whips/Braids, Forcing nets/Templates/Kraken fish) — one Brief-faithful line each, no tutorials — plus pointers to the technique references (SudokuWiki, HoDoKu, Sudopedia).
- **FR-003**: The page MUST contain a champion section stating that top-level solving is tiers 1–3 at extreme speed and accuracy, explaining Snyder notation in plain words with one small example, and listing the champion habits (pattern memory, cheapest-first discipline, minimal marks, composure and error recovery).
- **FR-004**: Reported records MUST appear with the Brief's exact times (1:23.93 very easy; 54.44 s championship-grade), distinguished by class and labeled as reported.
- **FR-005**: The page MUST close with a "your path from here" section (timed practice, step-hint solvers, one-technique-at-a-time) linking back to the game.
- **FR-006**: Every term MUST match the Brief exactly; the page MUST pass the plain-English budget (≤ 25-word sentences).
- **FR-007**: External links MUST appear only on this page, open in a new browsing context, and target the named reference pages; all internal links MUST resolve.
- **FR-008**: Footer navigation MUST show prev to chapter 04 (live) and an explicit ladder-end instead of a next link; the index row flips to a link and the index's ladder display reflects completion.

### Key Entities

- **MapEntry**: a Tier-5 name with its one-line Brief-faithful meaning and where-to-read pointer.
- **ChampionHabit**: a named habit from the Brief's champion layer with a plain-English line.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The visitor can name any Brief Tier-5 term after reading and knows where to read more (checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget and loads with zero page errors, all template sections, all internal links resolving (readability + lesson gates exit 0 — pass/fail).
- **SC-003**: No Tier-5 entry promises applied mastery; records carry the reported label (content honesty checks inside the lesson gate — pass/fail).
- **SC-004**: The game remains untouched (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- This is the ladder's final chapter by design; no spec extends beyond it (the Brief's learning-ladder table is the reader's onward path, not new pages).
- Snyder notation gets a plain-English explanation but not a practice drill; drills and timed mode belong to the game someday, parked here.
- The champion-layer content summarizing tiers 1–3 belongs to this page, not retrofitted into earlier chapters (they already teach the techniques themselves).
- Parked: progress tracking, accounts, internationalization, deep-linking into the game.
