# Sudoku — project memory

Self-contained `sudoku.html` app (dependency-free) + `lessons/` tutorial site
+ training studio (solver / generator / UI). No server, no bundler.

## Architecture

- `sudoku.html` — the game itself, zero dependencies (plain HTML/CSS/JS).
- `lessons/` — tutorial site (`index.html`, lesson pages 00–05, shared
  `board.js`, `lesson.css`); lesson pages follow the app theme via board.js
  bare-string parsing.
- Training suite (specs 009–011): solver, generator, studio UI with panel,
  checklist, persistence, print.
- `specs/` 000–011 (000 lesson-framework, 001–008 lessons & techniques
  fish/wings/chains/als-nets/map, 009–011 training). `outputs/` = generated
  artifacts. `pi-resume.sh` = session-resume helper.
- `pyproject.toml` (`sudoku-tests`) is a **test-gate env only** (playwright
  dep); the app itself never gains dependencies.

## Commands & flows

- **Gates (all must pass):**
  `node tests/engine.test.mjs` · `node tests/training.test.mjs` ·
  `node tests/readability.test.mjs` · `uv run python tests/lessons.test.py` ·
  `uv run python tests/browser.test.py`
- `TESTING.md` = manual human-feel checklist mirroring the automated gates —
  run it for wording/comfort/pacing the machine can't judge.
- Branch: `main`. One logical change per commit; push for backup.

## Project-specific rules

- **Never add a dependency to the app** — `sudoku.html` stays dependency-free;
  new needs go through stdlib/native browser features.
- Browser gates drive the real DOM (navigate → interact → assert the correct
  outcome); a substring/HTTP check is not a gate.
- New lesson/technique content: spec first (`specs/`), then implement, then
  extend `tests/readability.test.mjs` / `lessons.test.py` coverage.
