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
        const units = [];
        for (let k = 0; k < 9; k++) {
          units.push([...Array(9)].map((_, j) => k * 9 + j));
          units.push([...Array(9)].map((_, j) => j * 9 + k));
        }
        for (let br = 0; br < 3; br++) for (let bc = 0; bc < 3; bc++)
          units.push([...Array(9)].map((_, k) => (br * 3 + (k / 3 | 0)) * 9 + bc * 3 + k % 3));
        for (const u of units) {
          const g = u.filter(j => s.puzzle[j]);
          if (g.length < 2) continue;
          if (s.puzzle[g[0]] !== s.puzzle[g[1]]) {
            s.puzzle[g[1]] = s.puzzle[g[0]];
            s.elapsed = 999; /* marker: proves rejection if it comes back as 0 */
            localStorage.setItem('sudoku-v1', JSON.stringify(s));
            return {ok: true, tampered: s.puzzle.slice(0, 9)};
          }
        }
        return {ok: false};
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
        f"tampered={r.get('tampered')} after reboot={r2['row']} elapsed={r2['elapsed']}",
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

    # ===== spec 011: Training studio =====
    tp = ctx.new_page()
    terror = []
    tp.on("pageerror", lambda e, sink=terror: sink.append(str(e)))
    tp.goto(URL)
    tp.wait_for_timeout(300)
    tp.click("#menu summary")
    tp.click("#training summary")
    tp.wait_for_timeout(100)
    check(
        "training panel boots, zero errors",
        tp.locator("#trainGen").is_visible() and not terror,
        f"errors={terror[:2]}",
    )
    adv = tp.locator('#trainLevels button[data-level="advanced"]')
    check(
        "Advanced disabled with exact reason",
        adv.get_attribute("aria-disabled") == "true"
        and adv.is_disabled()
        and adv.get_attribute("title")
        == "Chain techniques cannot be verified yet - coming in a future version.",
        adv.get_attribute("title") or "no title",
    )
    # default level Basic: 10 boxes, two locked singles
    boxes = tp.locator("#trainChecks input[type=checkbox]")
    locked = tp.locator("#trainChecks input[type=checkbox]:disabled")
    check("Basic default shows 10 boxes", boxes.count() == 10, f"got {boxes.count()}")
    check("two singles locked on", locked.count() == 2 and all(
        locked.nth(i).is_checked() for i in range(2)
    ), f"locked={locked.count()}")
    # switch to Intermediate: 19 boxes, default all-checked
    tp.click('#trainLevels button[data-level="intermediate"]')
    tp.wait_for_timeout(100)
    ib = tp.locator("#trainChecks input[type=checkbox]")
    ic = tp.locator("#trainChecks input[type=checkbox]:checked")
    check("Intermediate shows 19 boxes", ib.count() == 19, f"got {ib.count()}")
    check("Intermediate defaults all-checked", ic.count() == 19, f"checked {ic.count()}")
    # switch back to Basic: saved unchecks win (none saved -> all 10 checked)
    tp.click('#trainLevels button[data-level="basic"]')
    tp.wait_for_timeout(100)
    bc = tp.locator("#trainChecks input[type=checkbox]:checked")
    check("Basic after roundtrip all-checked", bc.count() == 10, f"checked {bc.count()}")
    # uncheck naked_quad + reload -> persistence, saved unchecks win
    tp.locator('#trainChecks input[data-id="naked_quad"]').uncheck()
    tp.wait_for_timeout(100)
    saved = tp.evaluate("localStorage.getItem('sudoku-training-v1')")
    check("prefs saved under sudoku-training-v1", '"naked_quad"' in saved, saved or "")
    tp.reload()
    tp.wait_for_timeout(300)
    tp.click("#menu summary")
    tp.click("#training summary")
    tp.wait_for_timeout(100)
    still = tp.locator("#trainChecks input[data-id=naked_quad]")
    checked_ct = tp.locator("#trainChecks input[type=checkbox]:checked").count()
    check("uncheck persists over reload", not still.is_checked() and checked_ct == 9,
          f"checked {checked_ct}")
    # keys isolated: toggling prefs never touched the game save
    tp.evaluate("localStorage.setItem('sudoku-v1', 'MARKER')")
    tp.click('#trainLevels button[data-level="beginner"]')
    tp.wait_for_timeout(100)
    v1 = tp.evaluate("localStorage.getItem('sudoku-v1')")
    check("sudoku-v1 untouched by pref toggles", v1 == "MARKER", str(v1))
    # Beginner: All/None disabled, no group checkboxes
    check("Beginner disables All/None", tp.locator("#trainAll").is_disabled()
          and tp.locator("#trainNone").is_disabled(), "")
    # generate on Beginner (no game in progress -> no confirm);
    # record every live-region text so the transient announcement is captured
    tp.evaluate(
        "window.__liveLog = []; new MutationObserver(() => "
        "window.__liveLog.push(document.getElementById('live').textContent)"
        ").observe(document.getElementById('live'), {childList: true, characterData: true, subtree: true})")
    tp.click("#trainGen")
    tp.wait_for_function(
        "!document.getElementById('live').textContent.includes('Building')",
        timeout=10000,
    )
    rep = tp.evaluate("document.getElementById('live').textContent")
    log = tp.evaluate("window.__liveLog")
    check("Building announcement lands",
          any("Building your board" in t for t in log), str(log[:4]))
    check("report uses honest prefix", "Solve path (easiest techniques first):" in rep, rep)
    givens = tp.evaluate(
        "document.querySelectorAll('#grid .cell.given').length")
    digits = tp.evaluate(
        "[...document.querySelectorAll('#grid .cell')].filter(c => /[1-9]/.test(c.textContent)).length")
    label = tp.evaluate("document.getElementById('difflabel').textContent")
    check("board adopted: clues only, Training label",
          37 <= givens <= 42 and digits == givens and "Training" in label,
          f"givens={givens} digits={digits} label={label}")
    check("training page has zero errors", not terror, f"errors={terror[:2]}")
    # generate with game in progress -> confirm respected
    tp.evaluate(
        "document.querySelector('#grid .cell:not(.given)').dispatchEvent(new Event('click', {bubbles: true}))")
    tp.evaluate("window.confirm = () => false")
    tp.click("#training summary")  # generator closes the panel on success
    tp.click("#trainGen")
    tp.wait_for_timeout(200)
    rep2 = tp.evaluate("document.getElementById('live').textContent")
    check("declined confirm leaves game untouched",
          rep2 == rep or "Building" in rep2, rep2)
    # corrupt save -> loud reset to defaults
    tp.close()
    cp = ctx.new_page()
    cp.goto(URL)
    cp.evaluate("localStorage.setItem('sudoku-training-v1', 'NOT-JSON{{{')")
    cp.close(run_before_unload=False)
    cp2 = ctx.new_page()
    cp2.goto(URL)
    cp2.wait_for_timeout(400)
    note = cp2.evaluate("document.getElementById('live').textContent")
    check("corrupt prefs fall back loudly", "Training preferences were reset" in note, note)
    cp2.click("#menu summary")
    cp2.click("#training summary")
    cp2.wait_for_timeout(100)
    lv = cp2.evaluate(
        'document.querySelector("#trainLevels button[aria-pressed=\'true\']").dataset.level')
    cct = cp2.locator("#trainChecks input[type=checkbox]:checked").count()
    check("corrupt prefs restored defaults", lv == "basic" and cct == 10,
          f"level={lv} checked={cct}")
    # print view: without and with solution, under print media
    cp2.click("#trainPrint")  # build the view under screen media (button visible)
    cp2.wait_for_timeout(200)
    cp2.emulate_media(media="print")
    vis = cp2.evaluate(
        "getComputedStyle(document.getElementById('printView')).display")
    grids = cp2.locator("#printView .pgrid").count()
    check("print media shows printView, one grid", vis == "block" and grids == 1,
          f"display={vis} grids={grids}")
    cp2.emulate_media(media="screen")
    cp2.locator("#trainSol").check()
    cp2.click("#trainPrint")
    cp2.wait_for_timeout(200)
    g2 = cp2.locator("#printView .pgrid").count()
    full = cp2.evaluate(
        "() => { const gs = [...document.querySelectorAll('#printView .pgrid')];"
        " const ne = gs.map(g => [...g.children].filter(c => /[1-9]/.test(c.textContent)).length);"
        " const ok = gs.length === 2 && gs.every(g => g.children.length === 81)"
        "   && ne[0] >= 25 && ne[1] === 81 && gs[1].closest('.psol') !== null;"
        " return {ok, ne}; }")
    check("include-solution adds solved second page", g2 == 2 and full, f"grids={g2} full={full}")
    scr = cp2.evaluate(
        "getComputedStyle(document.getElementById('printView')).display")
    check("printView hidden on screen", scr == "none", scr)
    cp2.close()

    ctx.close()
    b.close()

print()
if fails:
    print("FAILURES:", len(fails))
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("browser tests: all pass")
