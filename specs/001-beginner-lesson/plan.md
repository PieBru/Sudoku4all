# Plan — 001 Beginner lesson

Single page lessons/01-beginner.html on the spec-000 framework (board.js, lesson.css).
Gates: readability (kid rules), lessons (template parts, technique sections,
2 full-position boards, fragment consistency, links, live render, index row flip).

## Steps
1. Generate two genuine easy positions from the engine (makePuzzle 40, validPuzzle).
2. Author page: cross-hatching (2 step boards), full house, hidden single, naked single
   (fragments marked data-fragment), practice boards, Try it (Easy + New game, hunt 7s),
   checkpoint, footer, kid-safe ladder labels.
3. Flip index row 01 to a live link (soon-count stays consistent).
4. Extend tests/lessons.test.py: fragment = consistency-only; PAGE_RULES for 01.
5. Run gates; sabotage one technique section out; Status Done.
