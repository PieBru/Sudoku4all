# Sudoku — manual testing checklist

Open `sudoku.html` in a browser. Work top to bottom; every line says what to
do and what should happen. The automated gates cover the same ground headless
(`node tests/engine.test.mjs`, `node tests/training.test.mjs`,
`node tests/readability.test.mjs`, `uv run python tests/lessons.test.py`,
`uv run python tests/browser.test.py`) — this list is for the human feel:
comfort, wording, pacing, and anything the machine cannot judge.

## 1. The game

- [ ] **New game** — pick each of Easy / Medium / Hard / Expert; a fresh board
      appears with the right feel of difficulty (clue counts drop as level rises).
- [ ] **Confirm dialogs** — start a game, place one digit, then press
      New game / Restart puzzle: both must ask before replacing your progress.
      A won game or an untouched board must NOT ask.
- [ ] **Entering digits** — click a cell, type 1–9 (top row and numpad); the
      digit lands. Arrows move the selection. Click a given cell: nothing can
      be typed there.
- [ ] **Wrong answers** — enter a digit that contradicts a given: the cell
      flashes red, shakes, un-places itself, and the ✗ mistake counter grows.
- [ ] **Notes** — toggle Notes (button or N), type digits: small pencil marks
      appear and toggle. Shortcut without toggling: hold Shift and press a digit
      (real keyboard: Shift+2 types `@` — the note must still land).
- [ ] **Erase / Undo** — Delete, Backspace or 0 clears a cell; Undo (button,
      U, or Ctrl+Z) steps back moves including notes. After a win, Undo must
      refuse (nothing un-wins).
- [ ] **Hint** — the 💡 places one correct digit and the counter increments.
- [ ] **Pause** — Pause (P) covers the board; switching browser tabs mid-game
      auto-pauses. The timer only runs while playing.
- [ ] **Conflicts toggle** — uncheck "Highlight conflicts": contradictory
      entries stop being flagged (mistake counting at entry time is unaffected).
- [ ] **Theme** — the ☀ button cycles System → Light → Dark → System; every
      surface including the lessons follows, and the choice survives reload.
- [ ] **Win** — finish a puzzle: the veil reports your time; a personal best
      updates the 🏆 display. Win again slower: best time must NOT regress.
- [ ] **Resume** — reload the page mid-game: board, notes, timer, mistakes all
      come back. Corrupt a save by hand (devtools → change a digit inside
      `sudoku-v1` to create a row conflict) and reload: a fresh game starts.

## 2. Training studio (Settings & controls → Training studio)

- [ ] **Panel** — opens/closes smoothly inside the settings menu.
- [ ] **Levels** — Beginner / Basic / Intermediate select; Advanced is greyed
      out and its tooltip says the chain-technique reason verbatim.
- [ ] **Checklist** — Basic shows 10 techniques, Intermediate 19; techniques
      above the chosen level never appear. The two singles are locked on with
      their one-line explanation.
- [ ] **All / None** — toggle only the current level's group; both disabled at
      Beginner.
- [ ] **Persistence** — uncheck e.g. Naked quad at Basic, reload: still
      unchecked; switching away and back keeps your unchecks. None of this
      touches your in-progress game or best times (separate storage key).
- [ ] **Build board** — with a game in progress it asks; otherwise "Building
      your board…" then a one-line solve path ("Solve path (easiest techniques
      first): …") in the status area, and the board becomes the active game
      under a "Training · …" label. Play it fully: undo, notes, hints, win all
      work.
- [ ] **Budget failure** — select Basic, uncheck everything except Pointing,
      build repeatedly: eventually the exact message "Couldn't build a board
      with only these techniques. Try enabling a few more." No silent states.
- [ ] **Corrupt prefs** — set `sudoku-training-v1` to garbage in devtools and
      reload: the status line announces the reset and defaults come back.
- [ ] **Print** — play some digits, press Print: the browser print preview
      shows the grid with your entries (never pencil marks); with "include
      solution in print" checked a second solved page follows.

## 3. Lessons (Learn)

- [ ] **Index** — six chapter rows, all live; the 3-question guide points a
      first-time player to the right chapter.
- [ ] **Chapter 00** — fear-killers read honestly; the fruit 4×4 is playable
      by tapping a cell then a fruit (or keys): a wrong pick wobbles and never
      sticks, completion celebrates; on the digit 4×4, pressing 5 does nothing.
      The 6×6 plays the same. Givens are locked.
- [ ] **Chapters 01–04** — each technique has a diagram whose highlights and
      ✗ marks match its caption; checkpoints and Try-it sections read clean;
      footer links walk the ladder both directions.
- [ ] **Chapter 05** — the Tier-5 reference table, champion section, and
      external links (open in a new tab).
- [ ] **Theme** — set the app to Dark, then open any chapter: the lesson pages
      follow the app's choice.
- [ ] **Back to the game** — from any chapter you can get back to the index
      and to the game; no dead links anywhere.

## 4. Anything machine-invisible

Wording that reads wrong, timings that feel off, a celebration that
underwhelms, a diagram you have to squint at — write it down; that is exactly
what this pass is for.
