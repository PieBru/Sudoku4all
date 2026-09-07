# Sudoku Solving Methods & Patterns: Beginner → World Champion

**A cited research brief** · Compiled 2026-09-07 · Citations `[n]` resolve in `sudoku-solving-methods-brief.provenance.md`

Two independent canonical taxonomies anchor this brief: Andrew Stuart's **SudokuWiki** solver ladder (Basic → Tough → Diabolical → Extreme, ordered by the difficulty his solver tries them in) [1], and Bernhard Hobiger's **HoDoKu** solver documentation (singles → intersections → subsets → fish → wings → chains → ALS → last resort) [2]. Every technique below appears in at least one of them unless noted.

---

## 0. The core mental model

A Sudoku is a constraint-satisfaction problem. Every human "technique" is a reusable proof pattern of the same shape: *if candidate X were true here, a contradiction (or a non-unique solution) follows — so X is eliminated.* The ladder from beginner to extreme is just increasingly large proof patterns: 1 cell → 2 cells → a box-line intersection → 4 cells in a rectangle → a whole digit's candidate "fish" across 3-4 rows → chains of arbitrary length → whole-grid structures. Wikipedia's algorithm article describes the machine equivalent (backtracking, constraint propagation, exact cover) [9]; humans replace brute search with memorized patterns.

**Pencil marks (candidate notation) are the prerequisite for everything above tier 1** — writing the remaining legal digits in each empty cell. Digital solvers do this automatically; on paper it's the skill that gates all further progress [1][2].

---

## Tier 1 — Beginner: scanning and singles

Solve entire easy newspapers with just these. Every speed record ever set uses essentially only this tier, executed fast [3][5].

| Technique | What it is |
| --- | --- |
| **Scanning / cross-hatching** | For each digit, sweep rows/columns that already contain it; the intersections eliminate cells in a box until one placement remains [12] |
| **Full house / last digit** | A unit (row/col/box) missing exactly one value — fill it [2] |
| **Hidden single** | A digit fits only one cell in some unit (even if that cell holds other candidates) [1][2] |
| **Naked single** | A cell reduced to exactly one candidate [1][2] |

Champions' version: scan for "low-hanging fruit" first — digits already placed 8 times, nearly-complete boxes — before any deep analysis [11].

## Tier 2 — Basic: subsets and intersections (medium newspaper puzzles)

| Technique | What it is |
| --- | --- |
| **Naked pair / triple / quad** | N cells of one unit share exactly N candidates → those digits are excluded everywhere else in the unit [1][2] |
| **Hidden pair / triple / quad** | N digits confined to exactly N cells of a unit → other candidates in those cells are eliminated [1][2] |
| **Locked candidates — pointing** | A digit's in-box candidates all lie on one row/col → eliminated from the rest of that row/col [1][2] |
| **Locked candidates — claiming (box/line reduction)** | A digit's row/col candidates all lie in one box → eliminated from the rest of the box [1][2] |

## Tier 3 — Intermediate: fish, wings, single-digit patterns, uniqueness ("hard" → "expert")

**Fish family** (one digit, N rows × N columns):

| Technique | What it is |
| --- | --- |
| **X-Wing** | Digit confined in 2 rows to the same 2 columns (a 2×2 rectangle) → eliminated elsewhere in those columns [1][2] |
| **Swordfish / Jellyfish** | Same logic on 3 (resp. 4) rows/columns [1][2] |
| **Finned / Sashimi fish** | X-Wing/Swordfish with one or two spoiler cells ("fins"); eliminations restricted to fin peers [2] |
| **Franken / Mutant fish** | Fish whose cover/defining sets mix boxes with rows and columns [2] |

**Single-digit patterns** (degenerate fish, very common on hard puzzles):

| Technique | What it is |
| --- | --- |
| **Skyscraper** | Two parallel strong links on one digit, offset by one row/col → eliminations at the overlap [2] |
| **2-String Kite** | Strong link in a row + strong link in a box, joined by a column [2] |
| **Turbot fish** | Any two strong links joined by one weak link (skyscraper/kite generalized) [2] |
| **Empty rectangle** | A box where a digit's candidates cluster so that row+box elimination applies [2] (deprecated as redundant in [1]) |

**Bent-set "wings"** (3-4 cells):

| Technique | What it is |
| --- | --- |
| **XY-Wing (Y-Wing)** | Pivot cell {x,y} sees two pincers {x,z} and {y,z} → z eliminated from cells seeing both pincers [1][2] |
| **XYZ-Wing** | XY-Wing where the pivot also holds z itself [1][2] |
| **W-Wing** | Two non-seeing cells {x,y} joined by a strong x-link → y elimination [1][2] |
| **WXYZ-Wing / Fireworks** | 4-cell extensions of the same idea [1] |

**Uniqueness family** — *assumes the puzzle has exactly one solution*; exploits that a deadly-pattern rectangle (two interchangeable digits in two boxes) can never be reached:

| Technique | What it is |
| --- | --- |
| **Unique Rectangle types 1-6 / Hidden UR** | A 4-cell rectangle 2 digits from a deadly pattern; the type tells you which candidate to eliminate to avoid it [1][2] |
| **BUG+1** | Bivalue Universal Grave: grid where every unsolved cell has 2 candidates except one cell with 3 → the extra candidate is the solution [1][2] |
| **Avoidable Rectangle** | Same logic on already-placed digits (avoids a swap reachable by a different solution path) [1][2] |

**Miscellaneous:** **Sue de Coq** (cell+line locked-set interaction, an "intersecting locked set" [1][2]); **Remote Pairs** (chain of identical naked pairs — parity elimination [1][2]).

## Tier 4 — Advanced: chains and coloring ("diabolical" / "evil")

The unifying concept is the **AIC — Alternating Inference Chain**: strong links ("A or B must be true") alternating with weak links ("not both true"). Any closed or contradictory AIC is a valid proof; almost every named chain technique is a special case [1][2].

| Technique | What it is |
| --- | --- |
| **Simple coloring / X-chain** | Color the two states of one digit's conjugate links; a digit seeing two opposite colors dies [1][2] |
| **X-Cycles** | Closed single-digit nice loops; odd cycles or breaks give eliminations [1] |
| **XY-Chain** | Chain through bivalue cells (each cell hands off one of its two digits) [1][2] |
| **3D Medusa** | Coloring extended to *all* digits simultaneously (candidates + placed values) [1] |
| **Grouped chains** | Chains allowed to pass through candidate *sets* (a whole box-line intersection) instead of single cells [1][2] |
| **ALS family** | Almost Locked Sets (n cells with n+1 candidates): **ALS-XZ**, **ALS-XY-Wing**, **ALS chains** — set-to-set strong links [1][2] |
| **Death Blossom** | A stem cell whose candidates each bloom into a different ALS — eliminations where all blooms agree [1][2] |
| **Aligned Pair Exclusion** | Two aligned cells: any candidate pair combination that would kill all options of another cell is impossible [1] |
| **Bowman's Bingo** | Tree of labeled contradictions from one hypothesis (interactive contradiction search) [1] |
| **Forcing chains — digit / cell / unit / Nishio** | Assume a candidate/cell/unit state, propagate; if all branches agree on an elimination, it's proven [1][2] |

## Tier 5 — Extreme: the world's-hardest-puzzle toolkit

Needed only for the famous monster puzzles (AI Escargot, Golden Nugget, Easter Monster class [7][8]). Almost no human uses these routinely; they live in solver implementations and hobbyist "hardest list" discussions [1][6].

| Technique | What it is |
| --- | --- |
| **Exocet / Double Exocet** | Two target cells in mirror positions: a 3-digit "base pattern" forcing one of two base cells to a limited digit set; base+cover-cell structure gives massive eliminations [1] |
| **SK Loop** (Steve Kurzhals) | A closed loop of paired strong links through boxes (rank-0 pattern) eliminating all non-loop occurrences in the loop's rows/columns/boxes [1][6] |
| **MSLS — Multi-Sector Locked Set** | A set of units whose combined candidates exactly cover required digits → strong eliminations; a systematic way of finding rank-0 patterns [6] |
| **Pattern Overlay Method (POM)** | Enumerate all complete-solution templates consistent with the givens; candidates appearing in no template die [1] |
| **Tridagon / trivalue oddagon** | Three digits cycling in a 3-cell × 3-box "oddagon" cannot all be those digits → one cell must take a fourth digit; added to SudokuWiki recently for the newest monster class [1][15] |
| **Oddagons / non-colourable clusters** | Odd-length single-digit loops of strong links — a contradiction pattern [6] |
| **Whips / Braids** (Berthier) | A formal resolution theory: chain patterns (whips) and their generalized nets (braids) with provable logical strength; proven to solve all known 9×9 puzzles in braids [13] |
| **Forcing nets / Templates / Kraken fish** | Solver-grade generalizations: full propagation nets, per-digit template elimination, fish whose fins sprout chains [1][2] |

**Last resort:** trial-and-error / **brute force**. Logically equivalent in outcome to a big forcing net, and Stuart's own X-Wing page concedes that when patterns run dry, a backtracking checkpoint "saves time" [1]. The purist position (all puzzles solvable by memorizable patterns) vs. the pragmatist position is the community's longest-running debate [1][9].

---

## The world-champion layer: what actually differs at the top

Records (all competition-classic 9×9): **Thomas Snyder 1:23.93** on a "very easy" grid (Guinness, 2006); **Wang Shiyao 54.44 s** on a championship-grade classic (WSPC Prague, 2018) [3]. Snyder is also a multi-time World Sudoku Champion [3][14].

What separates champions is **not** a secret tier-6 technique — it is execution of tiers 1-3 at extreme speed and accuracy:

1. **Snyder notation** — mark candidates *only in pencil, only within a box, only when a digit is limited to exactly two cells in that box*. Invented/popularized by Thomas Snyder; keeps the grid clean and surfaces pointing/hidden pairs that break easy/medium puzzles open without full notation [4][5]. Practitioners note Snyder himself switches to full marks when a puzzle genuinely needs them, and WSC classics are solvable without deep notation [5].
2. **Pattern memory over search** — champions "see the grid in loops and flows", placing digits almost automatically from repeated pattern shapes rather than cell-by-cell deduction [3][11].
3. **Technique order discipline** — cheapest first: singles → subsets/intersections → simple fish/wings; escalate only when progress stalls [1][2][3]. A learn-one-at-a-time progression (naked pair → X-Wing → skyscraper…) is the standard recommendation [3].
4. **Minimal pencil marks** — top solvers skip or limit marking on easy grids to save time [3][5].
5. **Composure and error-prevention** — Snyder's own advice: stay relaxed, treat it as fun, stay in rhythm; competition strategy centers on error recovery and checking discipline [11][14].
6. **Training apparatus** — solvers with step hints (SudokuWiki [1], HoDoKu [2]), the community technique wiki Sudopedia [10], and timed practice/tracking [3]. WSC itself mixes classics with variant rounds, so breadth (jigsaw, killer, etc.) matters beyond classic technique [11].

### Suggested learning ladder

| You can already… | Learn next |
| --- | --- |
| Solve nothing | scanning, cross-hatching, full house, hidden/naked singles [12][2] |
| Solve easy | naked/hidden pairs, pointing/claiming [1][2] |
| Solve medium | triples/quads, X-Wing, XY-Wing, skyscraper, 2-string kite, UR type 1 [1][2] |
| Solve hard | Swordfish/Jellyfish, W-Wing, XYZ-Wing, coloring, remote pairs, Sue de Coq [1][2] |
| Solve expert | X-cycles/AIC, XY-chains, 3D Medusa, ALS-XZ, Death Blossom, APE [1][2] |
| Stuck on monsters | Exocet, SK loops, MSLS, POM, tridagon, Berthier braids [1][6][13] |

---

## Key references

1. SudokuWiki (Andrew Stuart) — Strategy Families: <https://www.sudokuwiki.org/strategy_families> (fetched 2026-09-07)
2. HoDoKu (Bernhard Hobiger) — Implemented Techniques: <https://hodoku.sourceforge.net/en/techniques.php> (fetched 2026-09-07)
3. Sudoku Bliss — Fastest Sudoku Time (records table): <https://sudokubliss.com/guides/fastest-sudoku-time> (fetched 2026-09-07)
4. Sudoku247Online — Snyder Notation: <https://sudoku247online.com/snyder-notation-sudoku>
5. r/sudoku — Snyder notation discussions: threads `1iu6lqi`, `g5btzu`
6. Enjoy Sudoku forum — SK-Loops and MSLS (rank-0): <http://forum.enjoysudoku.com/sk-loops-and-msls-s-t36887.html>
7. Sudoku247Online — Hardest Sudoku Ever (AI Escargot): <https://sudoku247online.com/hardest-sudoku-ever>
8. Sudoku Paradise — Hardest Compared (Golden Nugget et al.): <https://sudokuparadise.com/guides/hardest-sudoku-compared.html>
9. Wikipedia — Sudoku solving algorithms: <https://en.wikipedia.org/wiki/Sudoku_solving_algorithms>
10. Sudopedia — Solving Technique index: <https://www.sudopedia.org/wiki/Solving_Technique>
11. SudokuPulse — World Sudoku Championship: <https://sudokupulse.com/articles/world-sudoku-championship>
12. Conceptis Puzzles — Sudoku techniques (scanning): <https://www.conceptispuzzles.com/index.aspx?uri=puzzle/sudoku/techniques>
13. Berthier — Pattern-Based Constraint Satisfaction and Logic Puzzles: <https://arxiv.org/abs/1304.1628> + CSP-Rules <https://github.com/denis-berthier/CSP-Rules-V2.1>
14. Sudoku.com — Lessons from Thomas Snyder: <https://sudoku.com/how-to-play/sudoku-lessons-from-world-champion-thomas-snyder>
15. SudokuWiki — Tridagons: <https://www.sudokuwiki.org/Tridagons>

*Provenance, verification notes, and confidence levels: see `sudoku-solving-methods-brief.provenance.md`.*
