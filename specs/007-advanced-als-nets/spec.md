# Feature Specification: Advanced Lesson Page, Part 2 — ALS Family and Forcing Nets (completes chapter 04)

**Feature Branch**: `specify/lesson-ladder`

**Created**: 2026-09-07

**Status**: Draft

**Input**: specs/proposal.md §3 (chapter 04 row), §4 (L3, L6), §5 (row `007-advanced-als-nets`), §5.1, §7; Brief §Tier 4 (ALS family, Death Blossom, APE, Bowman's Bingo, forcing chains) + last-resort note

## Context (OBSERVED)

- Technique source: the Brief, section *Tier 4 — Advanced*, second half. ALS family: ALS-XZ, ALS-XY-Wing, ALS chains — Almost Locked Sets (n cells with n+1 candidates) forming set-to-set strong links. Death Blossom: a stem cell whose candidates each bloom into a different ALS. Aligned Pair Exclusion: two aligned cells where impossible pair-combinations eliminate candidates. Bowman's Bingo: a labeled tree of contradictions from one hypothesis. Forcing chains — digit / cell / unit / Nishio: assume, propagate, and whatever all branches agree on is proven.
- The Brief's **last resort** note must be honored on the completed page: trial-and-error / brute force is logically equivalent in outcome to a big forcing net; when patterns run dry, a backtracking checkpoint "saves time" — and the purist-vs-pragmatist debate is the community's longest-running one. The completed chapter ends with this honesty plus an escalation-discipline note (cheapest technique first — the champion habit from the Brief's champion layer).
- This spec completes the page started by spec `006-advanced-chains`: adds these sections, removes "part 1 of 2", installs the full chapter checkpoint (follow a worked AIC chain and find an XY-Wing on prepared boards — proposal §3).
- Prev neighbor chapter 03 exists and its next link points here once this page lands; next neighbor chapter 05 does not exist yet (spec 008 flips it later).
- Language tier: plain English (L3); ALS needs its prerequisite (locked sets, chapter 02's pairs idea) named explicitly at first use.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Almost Locked Sets: groups that behave like cells (Priority: P1)

The reader meets the ALS idea: a little group of cells whose candidates total one more than the group's size — squeeze any one digit out and the rest lock solid, like a bivalue cell made of several cells. ALS-XZ is shown as the two-group version of the X-wing idea; ALS-XY-Wing as the wing version; ALS chains as the baton-passing version.

**Why this priority**: the ALS family is the workhorse of the chapter's second half and the conceptual bridge from cells to groups.

**Independent Test**: the reader circles an ALS on a prepared board and says what happens when one of its shared digits is placed elsewhere.

**Acceptance Scenarios**:

1. **Given** the ALS intro, **When** the n-cells-n+1-candidates idea is shown, **Then** it is connected back to chapter 02's pairs (a naked pair is the degenerate case) and one board shows a group locking when squeezed.
2. **Given** the ALS-XZ section, **When** read, **Then** two groups, their shared digit, and the resulting elimination are marked on one board.
3. **Given** ALS-XY-Wing and ALS chains, **When** read, **Then** each is presented as the named wing/chain idea applied to groups, with one worked example total.

### User Story 2 - Assume and propagate: forcing chains and friends (Priority: P1)

Forcing chains are taught as honest trial: assume one candidate, let the grid push back, and if every branch ends in the same elimination, it is proven. The digit/cell/unit flavors are named; Nishio is the same logic pointed at one digit. Bowman's Bingo is shown as the organized tree version; Death Blossom and APE get one worked example each, billed as rare.

**Why this priority**: forcing logic is what solvers actually run when patterns fail, and the honesty framing (it is not cheating) is the chapter's trust moment.

**Independent Test**: the reader follows a worked forcing chain and states the proven elimination.

**Acceptance Scenarios**:

1. **Given** the forcing-chain section, **When** a two-branch assumption is walked, **Then** both branches are shown and the shared conclusion is marked as proven.
2. **Given** the Nishio paragraph, **When** read, **Then** it is defined as the digit-pointed version in one sentence.
3. **Given** Death Blossom and APE, **When** browsed, **Then** each has exactly one worked example and a rarity label.

### User Story 3 - The exit door: when to stop pattern-hunting (Priority: P2)

The completed chapter closes with the escalation discipline (cheapest technique first, always) and the last-resort honesty section: trial with a clean conscience, because it is logically equivalent to a big net — and the debate about it is old and unresolved.

**Why this priority**: prevents both failure modes — brute-forcing too early and feeling guilty when they do.

**Independent Test**: the reader can state the escalation order and the last-resort justification in two sentences.

**Acceptance Scenarios**:

1. **Given** the closing section, **When** read, **Then** the cheapest-first escalation order is restated compactly (singles → pairs/intersections → fish/wings → chains → assume-and-propagate).
2. **Given** the last-resort paragraph, **When** read, **Then** it states that trial is outcome-equivalent to a large forcing net and that the purist-vs-pragmatist debate exists.

### Edge Cases

- **Completion transition**: part-1 marker removed, full checkpoint installed — both states gate-checkable.
- **Prerequisite drift**: if the reader skipped chapter 02, the ALS intro's pairs callback names where pairs are taught (self-healing cross-reference).
- **Checkpoint scope**: full checkpoint covers the AIC chain follow and the XY-Wing find (graduation), not ALS mastery.
- **Next neighbor**: chapter 05's slot stays "coming soon"; spec 008 flips it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The page MUST gain an ALS section teaching the n-cells-with-n+1-candidates idea with its chapter-02 callback, then ALS-XZ with a fully marked worked board, and ALS-XY-Wing plus ALS chains presented as the group versions of the wing/chain ideas with at least one worked example.
- **FR-002**: The page MUST gain a forcing-chains section walking a branched assumption to a shared proven elimination, naming the digit/cell/unit flavors, defining Nishio in one sentence, and covering Bowman's Bingo as the organized tree version.
- **FR-003**: Death Blossom and Aligned Pair Exclusion MUST each appear with exactly one worked example and a rarity label.
- **FR-004**: The completed page MUST close with the cheapest-first escalation order and the last-resort honesty paragraph (trial is outcome-equivalent to a large net; the debate exists).
- **FR-005**: On completion the page MUST drop the "part 1 of 2" marker and carry the full chapter checkpoint: 2–3 "can you…?" questions including following a worked AIC chain and finding an XY-Wing on prepared boards.
- **FR-006**: Every new term MUST be defined with an example at first use; names MUST match the Brief exactly; the page MUST pass the plain-English budget (≤ 25-word sentences).
- **FR-007**: The "Try it" section MUST link to the game and instruct: difficulty Expert, New game, and if stuck twice on one technique, drop to the cheapest technique and re-scan before assuming anything.
- **FR-008**: Footer navigation MUST follow the existing-neighbors-only policy; chapter 03's next link MUST point here (flipping it if it was "coming soon"), next stays "coming soon" until chapter 05 lands.

### Key Entities

- **ALS**: a group of cells with one more candidate than cells; locks when squeezed by a shared digit.
- **ForcingBranch**: one assumption's propagation path; branches sharing a conclusion prove it.
- **TechniqueSection**: plain-English what/when, worked board(s), Brief-exact name and one-liner.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can follow a worked AIC chain and find an XY-Wing on prepared boards (full checkpoint content check — pass/fail).
- **SC-002**: The page passes the plain-English budget (readability gate exit 0 — pass/fail).
- **SC-003**: The completed page loads with zero page errors, all template sections, no part-1 marker, the escalation/last-resort closing present, all links resolving (lesson gate exit 0 — pass/fail).
- **SC-004**: The game remains untouched (existing gates exit 0 unchanged — pass/fail).

## Assumptions

- Spec 006's sections and shell exist; this spec completes the page and swaps the checkpoint.
- ALS deep-dive tutorials (ALS-XZ rule variants, doubly linked ALS) stay out of scope; the Brief's one-liners define the ceiling.
- Worked boards are hand-built, clearly marked fragments; chain and net examples obey the ≤ 6-step comprehension cap from spec 006.
- Parked: deep-linking Expert; interactive assumption toys; progress tracking.
