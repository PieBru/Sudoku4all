# Plan — Spec 000: Lesson Framework

Build the lessons surface: `lessons/index.html` (6-chapter ladder index + demo board),
`lessons/lesson.css` (app-token clone, light/dark), `lessons/board.js` (data-driven
display-board renderer + theme sync), the **Learn** toolbar link in `sudoku.html`
(the only app change), and the two gates: `tests/readability.test.mjs` (language
budgets) and `tests/lessons.test.py` (Playwright: boot, links, template sections,
size-aware board rendering, board-data validation).

- Board data is validated on the Python side (stdlib HTMLParser + a small backtracking
  uniqueness check) — no new dependencies.
- `tests/browser.test.py` gets a dynamic base URL (today it hardcodes the main-tree
  path, which breaks worktree runs) + a Learn-link navigation check.
- Demo board givens generated via the engine seam (`makePuzzle(40)`, well-posed):
  `347200091000001400016900700270310600963400170000090283085703000790002050400100867`.

Chapter pages (specs 001–008) use `data-part` sections: `ladder`, `learn`, `body`,
`try`, `checkpoint`, `footer` — the gate asserts these on every chapter page.
