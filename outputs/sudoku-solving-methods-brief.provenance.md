# Provenance — Sudoku Solving Methods Brief

Research brief: `sudoku-solving-methods-brief.md` · Compiled 2026-09-07 · Working dir: `/mnt/2TB/Piero/Work/Sudoku`

## Workflow log (deep-research)

| Phase | Performed | Result |
| --- | --- | --- |
| **Researcher** | 5 web searches + 3 full-page fetches across technique encyclopedias, solver docs, competitive/record sources, extreme-pattern forums, formal literature | 15 sources collected; two independent canonical taxonomies (SudokuWiki, HoDoKu) anchored the classification |
| **Verifier** | Every technique name checked against at least one fetched full taxonomy ([1] or [2]); record numbers cross-checked against the aggregator's primary-source links; snippet-only claims downgraded in confidence below | No technique fabricated; technique descriptions are paraphrases of fetched taxonomy entries, not invention |
| **Reviewer** | Checked brief for over-claiming: difficulty tier assignment is SudokuWiki/HoDoKu's ordering, stated as such; "what champions use" section distinguishes OBSERVED-from-source vs INFERRED | Two claims marked INFERRED below; all other claims trace to a listed source |

## Source table

| # | Source | Type | Accessed | Supports | Confidence |
| --- | --- | --- | --- | --- | --- |
| 1 | sudokuwiki.org/strategy_families (Andrew Stuart) | Authoritative solver taxonomy (full fetch) | 2026-09-07 | Tier assignment; complete technique lists incl. Tridagons, Exocet, SK Loops, POM, APE, deprecated list; brute-force pragmatism on X-Wing page | HIGH (fetched) |
| 2 | hodoku.sourceforge.net/en/techniques.php (Bernhard Hobiger) | Authoritative solver taxonomy (full fetch) | 2026-09-07 | Independent technique list; singles/intersections/subsets/fish/wings/UR/coloring/chains/ALS/last-resort; finned/sashimi/franken/mutant fish; skyscraper, 2-string kite, turbot, empty rectangle | HIGH (fetched) |
| 3 | sudokubliss.com/guides/fastest-sudoku-time | Aggregator w/ primary links (full fetch) | 2026-09-07 | Records: Snyder 1:23.93 "very easy" + 2:08.53 "easy" (Guinness 2006, links to guinnessworldrecords.com); Wang Shiyao 54.44 s WSPC Prague 2018 (links Xinhua); champion practice tips (one-technique-at-a-time, limited pencil marks, pattern recognition) | MEDIUM-HIGH (fetched, but records are secondhand citations of Guinness/Xinhua) |
| 4 | sudoku247online.com/snyder-notation-sudoku | Guide (snippet) | 2026-09-07 | Snyder notation definition; attribution to Thomas Snyder, WPC medallist | MEDIUM (snippet) |
| 5 | reddit.com r/sudoku threads 1iu6lqi, g5btzu | Community (snippets) | 2026-09-07 | Snyder = box-limited bivalue marking; Snyder uses full notes when needed; WSC classics don't need deep notation | LOW-MEDIUM (community consensus, snippet) |
| 6 | forum.enjoysudoku.com SK-Loops and MSLS thread | Expert community (snippet) | 2026-09-07 | SK Loop = well-defined rank-0 pattern family; MSLS = fuzzy/systematic rank-0 finder; oddagons, exocet usage ladder | MEDIUM (snippet, expert forum) |
| 7 | sudoku247online.com/hardest-sudoku-ever | Guide (snippet) | 2026-09-07 | AI Escargot by Arto Inkala (2006), "hardest" claim | MEDIUM (snippet) |
| 8 | sudokuparadise.com/guides/hardest-sudoku-compared.html | Guide (snippet) | 2026-09-07 | Golden Nugget et al. monster-puzzle class context | MEDIUM (snippet) |
| 9 | en.wikipedia.org/wiki/Sudoku_solving_algorithms | Encyclopedia (search result) | 2026-09-07 | Backtracking / constraint programming / exact cover framing; logic-vs-search framing | MEDIUM-HIGH |
| 10 | sudopedia.org/wiki/Solving_Technique | Community wiki index (snippet) | 2026-09-07 | Existence of categorized technique index (training resource) | MEDIUM (snippet) |
| 11 | sudokupulse.com/articles/world-sudoku-championship | Guide (snippet) | 2026-09-07 | WSC format; speed techniques (low-hanging fruit scanning, muscle memory); error prevention | MEDIUM (snippet) |
| 12 | conceptispuzzles.com sudoku techniques | Publisher guide (snippet) | 2026-09-07 | Scanning / cross-hatching mechanics | MEDIUM (snippet) |
| 13 | arxiv.org/abs/1304.1628 + github.com/denis-berthier/CSP-Rules-V2.1 | Formal literature + code (search results) | 2026-09-07 | Berthier's pattern-based resolution theory (whips/braids), CSP-Rules solver exists | MEDIUM-HIGH (arXiv/HAL presence verified via search results; book not fetched) |
| 14 | sudoku.com Snyder lessons | Interview/guide (snippet) | 2026-09-07 | Snyder's composure/rhythm advice; multi-champion status | MEDIUM (snippet) |
| 15 | sudokuwiki.org/Tridagons | Solver page (listed in [1], not fetched) | 2026-09-07 | Tridagon technique existence and recency | MEDIUM (taxonomy listing only) |

## Verification notes & limitations

- **Technique completeness**: cross-checked SudokuWiki's five difficulty tiers against HoDoKu's implementation list; the brief's tiers merge the two orderings. Where they disagree (e.g., SudokuWiki deprecates Empty Rectangles and Remote Pairs as redundant; HoDoKu keeps them), the brief keeps the technique and notes the deprecation.
- **Record claims** (Snyder 1:23.93; Wang Shiyao 54.44 s): taken from source [3], which itself links Guinness World Records and Xinhua as primaries. Primary pages were NOT fetched this session → secondhand, labeled as such.
- **INFERRED (2 claims)**: (a) "Every speed record uses essentially only tier 1-3 techniques" — no source states this directly; it is inferred from [3][5] (records set on very-easy/competition classics; WSC classics don't require advanced notation). (b) The learning-ladder mapping of "solve easy → learn pairs" progression synthesizes [1][2][3] orderings and difficulty tables from secondary guides.
- **Snippet-only sources** ([4]-[8], [10]-[12], [14]): retrieved via search snippets, not full fetch. Claims drawn from them are definitional/low-stakes (what a technique is, that a record exists) rather than load-bearing for the classification.
- **Difficulty tier labels** are SudokuWiki's solver-ordering + HoDoKu's grouping; the mapping to newspaper difficulty names (easy/medium/hard/expert) follows common guide convention ([3] and similar) and is approximate by the sources' own admission ("difficulty is rather subjective" — [1], fetched).
- Web content is untrusted-by-default; sources were used as data for synthesis, and no instructions from them were followed.
