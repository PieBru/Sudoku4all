# Proposal — Sudoku Learning Ladder: from "what is Sudoku?" to champion tricks

Companion to `outputs/sudoku-solving-methods-brief.md` (the technique source of
truth, cited below as *the Brief*). This document does **not** teach
techniques — it is the bridge that turns the Brief into shippable lesson
pages: the curriculum map, the one-page-per-chapter rule, the language rules
(including "a 6-year-old can read the Beginner page"), and a full breakdown of
the slim specs to create next.

**Status**: proposal v2 (v2 adds the fun-size intro ladder — §3.1 and
Appendix D). §8 lists the decisions this document seals; any of
them can be vetoed before the specs are cut, otherwise they stand.

---

## 1. Goal

Anyone — a 6-year-old, an adult who always feared Sudoku's complexity, a
hobbyist stuck at medium — can open this project and climb the ladder one
rung at a time, in human-friendly language, until they reach the
champion-level layer of the Brief.

Two artifacts deliver this:

1. `lessons/` — **one standalone HTML page per chapter** (user directive:
   split content by chapter, one page each; start with Beginner).
2. A single **Learn** link in `sudoku.html` pointing to `lessons/index.html`.
   The app core stays single-file and untouched apart from that one link.

## 2. Directives encoded here (from the operator)

| Directive | Where it lands |
| --- | --- |
| Human-friendly language; Beginner readable by a 6-year-old | Language rules L1–L6 (§4), enforced by a runnable gate (§7) |
| If a page is too big, one page per chapter; begin with the Beginner page | Chapter split (§3) + build order (§5, Beginner is spec 001) |
| An introductory step for kids and Sudoku-shy adults | Chapter `00-first-steps` (§3), its own spec (002) |
| First contact must be fun, not fear: simplified smaller boards teach row / column / cell / box by playing | Fun-size ladder (§3.1), delivered by spec 002 via `lessons/mini.js` |

The Brief itself (158 lines) fits any context comfortably; the one-page rule
applies to the *user-facing lesson pages*, which is where size actually
hurts.

## 3. Curriculum map — chapters

Chapters are numbered in **curriculum order** (the order a learner reads
them). Each is one page under `lessons/`.

| Page | Working title | Audience | Source (Brief section) | You graduate when… |
| --- | --- | --- | --- | --- |
| `00-first-steps.html` | *Sudoku? Hello!* | kids 6+, first-timers, adults who fear its complexity | new content (the Brief starts one rung up) + fun-size boards (§3.1) + the app's own UI | you solved a 4×4 and a 6×6 board all by yourself, you can point at a row / column / box / cell, and starting a real 9×9 game in the app feels friendly |
| `01-beginner.html` | *Your first two tricks* | beginners | Tier 1 — scanning/cross-hatching, full house, hidden single, naked single | you can solve an easy puzzle using scanning and cross-hatching on your own |
| `02-basic.html` | *Pairs that talk to each other* | easy-level solvers | Tier 2 — naked/hidden pairs→quads, pointing, claiming | you can spot a naked pair and a pointing pair on a prepared board |
| `03-intermediate.html` | *Patterns with funny names* | medium-level solvers | Tier 3 — fish, single-digit patterns, wings, uniqueness, Sue de Coq, remote pairs | you can find an X-Wing and a UR type 1 on prepared boards |
| `04-advanced.html` | *Chains: following clues* | hard-level solvers | Tier 4 — AIC, coloring, XY-chains, 3D Medusa, ALS, forcing nets… | you can follow a worked AIC chain and find an XY-Wing on a prepared board |
| `05-extreme.html` | *Champion territory: a map, not a manual* | the curious | Tier 5 + champion layer | you know the names, why they exist, and where to read more |

Chapter 00 deliberately repeats nothing from chapter 01: it teaches **what
the game is and how to hold the pencil** (literally: how to click, type,
undo, and write notes in the app), not any solving technique.

### 3.1 Chapter 00 internals — the fun-size ladder

First contact is play, never a wall of 81 squares. Chapter 00 teaches the
main concepts — row, column, cell, box — **on boards small enough to win in
under a minute**, all playable in the page via `lessons/mini.js`:

1. **Fruit 4×4** — 2×2 boxes, four fruit symbols (🍎 🍌 🍇 🍓) instead of
   any digits. The very first win proves "this is not math".
2. **Digit 4×4** — same board, digits 1–4: "the fruits become numbers; the
   game stays exactly the same."
3. **Digit 6×6** — 2×3 boxes, digits 1–6: one size up, one new wrinkle
   (boxes are wide rectangles now).
4. **Bridge to the real board** — the 6×6 pictured next to a 9×9: "same
   game, more squares. Press *Learn → play* whenever you feel ready."

Concepts are named *while playing* ("this line is a row; this little square
is a cell; this thick-bordered chunk is a box — each fruit fits once in
each"), never in a wall of text before the first game.

mini.js UX (fear-first, hard rules for the spec):

- Tap a cell, then tap a big button holding the digit or fruit (keyboard
  1–9 also works) — big targets for small fingers.
- An entry that contradicts the solution wobbles gently and does **not**
  stick. No mistake counter, no red, no timer — chapter 00 has no failure
  state at all.
- Completing a board triggers a small celebration ("You did it! 🎉").
- Given cells are locked and look pinned, exactly like in the real app.

`ponytail: no contradiction-hunting is taught here — that is chapter 01+'s job; add a strict mode to mini.js only if learners bounce at the 9×9 transition.`

## 4. Language & tone rules (hard requirements)

- **L1 — kid-readable (chapters 00 and 01 only).**
  - Sentences: aim ≤ 10 words, hard ceiling 15 (enforced by the gate, §7).
  - Everyday words only. Every term is explained in kid words *before* its
    grown-up name appears ("Grown-ups call this trick cross-hatching").
  - One idea per sentence. Second person. Active voice.
  - Show, don't describe: every technique shown on a mini-board, not prose-only.
  - Mistakes are normal: "even champions press Undo."
  - Zero math framing in chapter 00: digits are labels; "you could play with
    9 different fruits."
- **L2 — dual audience.** Every section of chapters 00/01 carries a small
  *For grown-ups* aside (1–3 sentences, adult tone, may use the real jargon).
  Adults get the precise version without being babied by the main text.
- **L3 — plain English (chapters 02+).** Sentence ceiling ~25 words; every
  new term gets definition + example at first use; technique names match the
  Brief exactly (X-Wing, not "cross thing").
- **L4 — fear-killers required in chapter 00**, stated up front: no math is
  needed; nothing is timed unless you ask; Undo and Hint always exist; the
  game never judges you.
- **L5 — the gate makes L1/L3 testable, not vibes**: a tiny readability test
  (§7) enforces sentence budgets and a banned-jargon list per chapter.
- **L6 — terminology matches the app UI**: lesson pages use the same words
  the app shows (notes, hint, mistakes, New game, Restart), so the learner is
  never lost when they switch from lesson to game.

## 5. Slim spec plan

**Slim** = goal + ≤ 10 requirements + binary acceptance checks, implementable
and verifiable in one sitting. Specs live at `specs/NNN-name/spec.md` +
`tasks.md`, numbered in **build order** (this is the layout the
magic-spec-implement-and-test workflow consumes). Pages are content units;
specs are build units — a big chapter may be delivered by two specs, split
along the Brief's sub-family lines.

| Spec | Delivers | Source | Size | Depends on |
| --- | --- | --- | --- | --- |
| `000-lesson-framework` | `lessons/index.html`, shared `lesson.css`, tiny `board.js` mini-board renderer, page template, Learn link in the app, readability gate test | this proposal | S | — |
| `001-beginner-lesson` | `lessons/01-beginner.html` (complete) | Brief Tier 1 | M | 000 |
| `002-first-steps-lesson` | `lessons/00-first-steps.html` (complete) + `lessons/mini.js` + 3 gate-validated fun-size puzzles (fruit 4×4, digit 4×4, digit 6×6) | new + app UI | M | 000 |
| `003-basic-lesson` | `lessons/02-basic.html` (complete) | Brief Tier 2 | M | 000 |
| `004-intermediate-fish` | page shell + fish family + single-digit pattern sections of `03-intermediate.html` | Brief Tier 3 (first half) | M | 000 |
| `005-intermediate-wings` | wings + uniqueness + Sue de Coq + remote pairs sections (completes the page) | Brief Tier 3 (second half) | M | 004 |
| `006-advanced-chains` | page shell + AIC concept + coloring/X-chain/X-cycles/XY-chain/3D Medusa/grouped sections of `04-advanced.html` | Brief Tier 4 (first half) | M | 000 |
| `007-advanced-als-nets` | ALS family + Death Blossom + APE + Bowman's Bingo + forcing nets sections (completes the page) | Brief Tier 4 (second half) | M | 006 |
| `008-extreme-map` | `lessons/05-extreme.html` — reference map, not tutorials | Brief Tier 5 + champion layer | S | 000 |

**Build order** = spec number order: framework → **Beginner first (user
directive)** → First Steps → Basic → Intermediate → Advanced → Extreme.
Chapter numbering (§3) is curriculum order and intentionally differs from
spec order.

Decision note on chapter 05: we do not teach exocet construction. The extreme
page is an honest map — names, one-liners from the Brief, why they exist, and
links — because the Brief itself says almost no human uses these routinely.

### 5.1 Page template (every chapter page)

```html
<!-- lessons/NN-name.html -->
<header>            chapter number, title, one-line promise
<section data-part="learn">     "You will learn" — 3–5 bullets (kid words on 00/01)
<section data-part="body">      one <article> per technique:
                                 plain-words what it is → when to use it →
                                 worked example on a mini-board →
                                 "grown-ups call it …" (+ Brief one-liner)
<section data-part="try">       "Try it": link to ../sudoku.html + one-line instruction
<section data-part="checkpoint">  2–3 can-you questions (the exit criterion of §3)
<footer>            prev · index · next
```

- Mini-boards are rendered by one tiny shared script from compact data
  (`<div class="board" data-givens="…81 chars…"></div>` expanded by
  `lessons/board.js`, ~30 lines). Lesson pages carry no other JS.
- `lesson.css` reuses the app's look (same tokens, `prefers-color-scheme` +
  `color-scheme`), so lessons feel like the game.

### 5.2 Scope fences (YAGNI, stated so no spec drifts)

- No JS in lesson pages beyond `board.js` (static display boards, all
  chapters) and `mini.js` (playable fun-size boards, chapter 00 only).
- No app changes beyond the Learn link. "Try it" cannot deep-start a
  difficulty (the app resumes the saved game; deep-linking would fight
  localStorage) — a text instruction suffices.
  `ponytail: no deep-link; add a ?difficulty= handler in the app if learners stumble here.`
- No progress tracking, no accounts, no i18n (English only).

## 6. How each spec uses the Brief

The Brief is the technique source of truth: names, groupings, one-line
definitions, citations. Each spec's *Source* field names the Brief section;
lesson content may expand the Brief with examples and friendlier words but
must never contradict it or invent technique claims. Chapter 00 has no Brief
section (the Brief starts at beginner techniques) — its source is first
principles plus the app's UI, and its spec says so explicitly.

## 7. Gates (all binary, all runnable)

| Gate | Command | Applies to |
| --- | --- | --- |
| Readability | `node tests/readability.test.mjs` | every lesson page: chapters 00/01 → max sentence ≤ 15 words, average ≤ 10, banned-jargon list absent outside *For grown-ups* asides; chapters 02+ → max sentence ≤ 25 words |
| Lesson page boot | `uv run python tests/lessons.test.py` (Playwright) | 0 page errors, template sections present, nav links resolve, mini-boards render 81 cells; chapter 00 additionally: every `.mini` validates (Appendix D) and is playable — tap a button to place a digit, a contradicting entry wobbles and does not stick, a full solve shows the celebration |
| App untouched | `node tests/engine.test.mjs` and `uv run python tests/browser.test.py` | stay green; only the Learn link may differ in the app |

`ponytail:` the readability check uses a naive sentence splitter (split on
`.!?`); upgrade to a real readability library only if it misfires.

## 8. Decisions sealed by this proposal

1. Lessons are standalone static pages under `lessons/`; the app gains only a Learn link.
2. One spec per chapter, split in two only for Intermediate and Advanced (along Brief sub-families); spec numbers = build order, chapter numbers = curriculum order.
3. Chapter 05 (extreme) is a reference map, not tutorials.
4. Language rules L1–L6 apply, with a runnable readability gate.
5. "Try it" links with a text instruction; no deep-linking into the app.
6. The Brief is the technique source of truth; lessons never contradict it.
7. Build order: framework → Beginner → First Steps → Basic → Intermediate → Advanced → Extreme.
8. Chapter 00 teaches row / column / cell / box by playing fun-size boards (fruit 4×4 → digit 4×4 → 6×6 → 9×9 bridge) via `lessons/mini.js`; contradictions wobble and never stick — the intro has no failure state.

---

## Appendix A — kid-language sample (the bar for chapter 01)

> **Find the 7!**
> Look at the big box on the top left. Some rows already have a 7. Those rows
> say: "No 7 here!" Some columns have a 7 too. They say: "No 7 here!" Now
> count the free little squares in that box. Is there just one? That square
> gets the 7. Well done — you just did the most famous Sudoku trick!
> Grown-ups call it **cross-hatching**.

*For grown-ups:* cross-hatching sweeps the rows and columns that already
contain a digit; their intersections eliminate cells in a box until one
placement remains [SudokuWiki/HoDoKu, Brief Tier 1].

## Appendix B — extraction-ready skeleton: `specs/001-beginner-lesson/spec.md`

```markdown
# Spec 001 — Beginner lesson page (lessons/01-beginner.html)

**Status**: 📝 Draft  ·  Source: Brief §Tier 1  ·  Depends: 000  ·  Size: M

## Goal
A standalone, 6-year-old-readable page teaching scanning/cross-hatching,
full house, hidden single, naked single — each shown on a mini-board.

## Requirements
1. Page follows the §5.1 template; all data-part sections present.
2. Techniques covered, in order: cross-hatching, full house ("last empty
   square"), hidden single, naked single. Each: kid words first, grown-up
   name + Brief one-liner last, ≥ 1 mini-board worked example each
   (cross-hatching gets ≥ 2, step by step).
3. ≥ 2 mini-boards use data-givens strings that are real positions from the
   app's generator (easy puzzles, verified well-posed).
4. "For grown-ups" aside present in every section (L2).
5. "Try it" links ../sudoku.html with the instruction: pick Easy, press New
   game, find all the 7s first.
6. Checkpoint = the chapter-01 exit criterion of the curriculum map.
7. Language rules L1 + L6 pass the readability gate.
8. Footer: prev → lessons/00-first-steps.html, next → lessons/02-basic.html
   (links may point at not-yet-built pages; index handles that gracefully).

## Out of scope
Pencil-mark technique teaching (notes are only named, as the app calls them),
pairs, any Tier 2+ technique, app changes.

## Acceptance (binary)
- node tests/readability.test.mjs  → exit 0
- uv run python tests/lessons.test.py  → exit 0, 0 page errors
- node tests/engine.test.mjs && uv run python tests/browser.test.py  → exit 0
```

## Appendix C — lessons index sketch (`lessons/index.html`)

- Chapter list: number, title, one-line *who is this for*, and a 3-question
  "Which chapter is for me?" guide (kid wording: "Can you solve an easy
  puzzle all by yourself? → No: start at chapter 1. Yes: go to chapter 2.")
- "Start here" badge on chapter 00 for first-timers and on chapter 01 for
  players who already know the rules.

## Appendix D — fun-size boards: data format and gate

Puzzles are pure data — no solver ships in the lessons:

```html
<div class="mini" data-size="4" data-box="2,2"
     data-puzzle="1.34341..14343.1"
     data-solution="1234341221434321"
     data-symbols="🍎,🍌,🍇,🍓"></div>
```

- `mini.js` renders the grid, takes input, and compares against
  `data-solution`. Omit `data-symbols` for digits.
- The example pair above is real: solution verified as a valid 4×4 grid and
  the puzzle verified to have exactly one solution (checked 2026-09-07).
- The gate validates every `.mini` on the page the same way: solution is a
  valid grid (each symbol once per row, column, box), puzzle is consistent
  with the solution, and the puzzle has exactly one solution (brute force —
  trivial at 4×4/6×6). A hand-typo'd puzzle can never ship.
