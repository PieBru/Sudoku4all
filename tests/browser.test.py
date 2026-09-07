"""Browser gate — run: uv run python tests/browser.test.py

Asserts the UI-level fixes from the 2026-09-07 audit against the live page:
box separators survive render(), wrong-entry flash visible, Shift+digit notes
fire on real-layout events, ARIA rows, color-scheme, corrupt-save rejection,
undo blocked after win, stats store only consumed fields, and (spec 000) the
Learn link opens the lessons index.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "sudoku.html").as_uri()
fails = []


def check(name, cond, evidence=""):
    print(("PASS" if cond else "FAIL"), "|", name, "|", evidence)
    if not cond:
        fails.append(name)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    page.wait_for_timeout(300)

    check("boot: no page errors", not errors, "; ".join(errors[:3]))

    borders = page.evaluate(
        """() => {
        const cell = (i) => document.querySelectorAll('#grid .cell')[i];
        return {
          col5: getComputedStyle(cell(5)).borderRightWidth,
          row5: getComputedStyle(cell(45)).borderBottomWidth,
          plain: getComputedStyle(cell(4)).borderRightWidth,
          lastRow: getComputedStyle(cell(80)).borderBottomWidth,
        };
      }"""
    )
    check(
        "box separators 2px at interior boundaries, none at edges",
        borders["col5"] == "2px"
        and borders["row5"] == "2px"
        and borders["plain"] == "1px"
        and borders["lastRow"] == "0px",
        str(borders),
    )

    # wrong entry: 'wrong' class present right after the (synchronous) handler
    r = page.evaluate(
        """() => {
        const s = JSON.parse(localStorage.getItem('sudoku-v1'));
        const i = s.board.findIndex(v => !v);
        const wrong = [1,2,3,4,5,6,7,8,9].find(v => v !== s.solution[i]);
        const cells = [...document.querySelectorAll('#grid .cell')];
        cells[i].dispatchEvent(new MouseEvent('click', {bubbles: true}));
        document.dispatchEvent(new KeyboardEvent('keydown', {key: String(wrong), bubbles: true}));
        return {cls: cells[i].className};
      }"""
    )
    check("wrong-entry flash class survives render()", "wrong" in r["cls"], r["cls"])

    # real-layout Shift+digit (e.key '@', physical Digit2) writes a pencil note
    r = page.evaluate(
        """() => {
        const s0 = JSON.parse(localStorage.getItem('sudoku-v1'));
        const i = s0.board.findIndex(v => !v);
        const cells = [...document.querySelectorAll('#grid .cell')];
        cells[i].dispatchEvent(new MouseEvent('click', {bubbles: true}));
        document.dispatchEvent(new KeyboardEvent('keydown', {key: '@', code: 'Digit2', shiftKey: true, bubbles: true}));
        return {i, notes: JSON.parse(localStorage.getItem('sudoku-v1')).notes[i]};
      }"""
    )
    check(
        "Shift+digit note (real-layout e.key)",
        bool(r["notes"] & 4),
        f"notes[{r['i']}]={r['notes']}",
    )

    # ARIA: 9 rows of 9 gridcells
    r = page.evaluate(
        """() => {
        const rows = document.querySelectorAll('#grid [role="row"]').length;
        const cells = document.querySelectorAll('#grid [role="gridcell"]').length;
        const parented = [...document.querySelectorAll('#grid [role="gridcell"]')]
          .every(c => c.parentElement.getAttribute('role') === 'row');
        return {rows, cells, parented};
      }"""
    )
    check(
        "ARIA grid has 9 rows x 9 gridcells",
        r == {"rows": 9, "cells": 81, "parented": True},
        str(r),
    )

    # color-scheme follows theme
    r = page.evaluate(
        """() => {
        const cs = () => getComputedStyle(document.documentElement).colorScheme;
        const out = [cs()];
        for (const _ of [1, 2, 3]) {
          document.getElementById('themeBtn').click();
          out.push(cs());
        }
        return out;
      }"""
    )
    check(
        "color-scheme tracks theme (system/light/dark/system)",
        r == ["light dark", "light", "dark", "light dark"],
        str(r),
    )

    # corrupt save (conflicting givens) must be rejected on boot.
    # page.close(run_before_unload=False): a reload would fire pagehide and the
    # app's save() would clobber the tamper before it is ever tested.
    r = page.evaluate(
        """() => {
        const s = JSON.parse(localStorage.getItem('sudoku-v1'));
        let a = -1, c = -1;
        for (let j = 0; j < 9; j++) if (s.puzzle[j]) { if (a < 0) a = j; else if (s.puzzle[j] !== s.puzzle[a]) { c = j; break; } }
        if (c < 0) return {ok: false, why: 'no pair'};
        s.puzzle[c] = s.puzzle[a];
        s.elapsed = 999; /* marker: proves rejection if it comes back as 0 */
        localStorage.setItem('sudoku-v1', JSON.stringify(s));
        return {ok: true, tampered: s.puzzle.slice(0, 9)};
      }"""
    )
    page.close(run_before_unload=False)
    page = ctx.new_page()
    errors2 = []
    page.on("pageerror", lambda e: errors2.append(str(e)))
    page.goto(URL)
    page.wait_for_timeout(300)
    r2 = page.evaluate(
        """() => { const s = JSON.parse(localStorage.getItem('sudoku-v1'));
               return {elapsed: s.elapsed, row: s.puzzle.slice(0, 9)}; }"""
    )
    check(
        "corrupt save (conflicting givens) rejected -> fresh game",
        r["ok"] and r2["elapsed"] == 0 and r2["row"] != r["tampered"],
        f"tampered={r['tampered']} after reboot={r2['row']} elapsed={r2['elapsed']}",
    )
    check(
        "reboot after corrupt save: no page errors", not errors2, "; ".join(errors2[:3])
    )

    # win flow: fill every cell that disagrees with the solution (earlier checks
    # left a wrong digit + notes in the saved game); stats store only consumed
    # fields; undo blocked after win
    fill = page.evaluate(
        """() => {
        const s = JSON.parse(localStorage.getItem('sudoku-v1'));
        return s.board.map((v, i) => v === s.solution[i] ? 0 : {i, v: s.solution[i]}).filter(Boolean);
      }"""
    )
    for c in fill:
        page.locator("#grid .cell").nth(c["i"]).click()
        page.keyboard.press(str(c["v"]))
    page.wait_for_timeout(300)
    r = page.evaluate(
        """() => {
        const s = JSON.parse(localStorage.getItem('sudoku-v1'));
        const stats = JSON.parse(localStorage.getItem('sudoku-stats-v1'));
        const d = s.diff;
        return {won: s.won, veilHidden: document.getElementById('veil').hidden,
                statKeys: stats && stats[d] ? Object.keys(stats[d]).sort() : null};
      }"""
    )
    check(
        "win recorded; stats store only consumed fields",
        r["won"] and r["statKeys"] == ["time"],
        str(r),
    )
    page.keyboard.press("Control+z")
    page.wait_for_timeout(150)
    r = page.evaluate(
        """() => ({won: JSON.parse(localStorage.getItem('sudoku-v1')).won,
               veilHidden: document.getElementById('veil').hidden})"""
    )
    check("undo blocked after win", r["won"] and not r["veilHidden"], str(r))

    # spec 000: the Learn control opens the lessons index (one interaction)
    lp = ctx.new_page()
    lerrors = []
    lp.on("pageerror", lambda e, sink=lerrors: sink.append(str(e)))
    lp.goto(URL)
    lp.wait_for_timeout(300)
    lp.click("#menu summary")  # open the collapsed settings menu first
    lp.click("#learnBtn")
    lp.wait_for_url("**/lessons/index.html", timeout=5000)
    check(
        "Learn link opens the lessons index",
        "lessons/index.html" in lp.url and not lerrors,
        f"{lp.url} errors={lerrors[:2]}",
    )
    lp.close()

    ctx.close()
    b.close()

print()
if fails:
    print("FAILURES:", len(fails))
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("browser tests: all pass")
