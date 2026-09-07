"""tests/lessons.test.py — the lesson-page gate (spec 000 FR-009).

Checks every lessons/*.html page: zero page errors, template data-parts on
chapter pages, every link resolving to a real file, every board rendering the
cell count for its size (81 for 9x9 display boards; 16/36 for .mini), and
board DATA validated offline (givens consistent + exactly one solution).
Also drives the app -> Learn -> index flow.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1]
LESSONS = BASE / "lessons"
REQUIRED_PARTS = ["ladder", "learn", "body", "try", "checkpoint", "footer"]
PAGE_RULES = {
    "01-beginner.html": {
        "techniques": ["crosshatching", "full_house", "hidden_single", "naked_single"],
        "full_boards_min": 2,
    },
    "02-basic.html": {
        "techniques": ["naked_pair", "hidden_pair", "pointing", "claiming"],
        "full_boards_min": 0,
    },
    "05-extreme.html": {
        "techniques": ["tier5", "champion", "path"],
        "full_boards_min": 0,
        "required": ['target="_blank"'],
    },
    "04-advanced.html": {
        "techniques": [
            "links",
            "aic",
            "simple_coloring",
            "x_cycles",
            "medusa_3d",
            "xy_chain",
            "grouped_chains",
            "als",
            "forcing_chains",
            "death_blossom",
            "ape",
            "escalation",
        ],
        "full_boards_min": 0,
        "required": ['data-hl="0,38" data-hl2="20,43"'],
        "banned": ["part 1"],
    },
    "03-intermediate.html": {
        "techniques": [
            "x_wing",
            "swordfish",
            "skyscraper",
            "two_string_kite",
            "turbot_fish",
            "finned_fish",
            "xy_wing",
            "w_wing",
            "uniqueness",
            "bug",
            "sue_de_coq",
            "remote_pairs",
        ],
        "full_boards_min": 0,
        "banned": ["part 1"],
    },
}
fails = []


def check(name, cond, evidence=""):
    print(("PASS" if cond else "FAIL"), "|", name, "|", evidence)
    if not cond:
        fails.append(name)


# ---------- offline board-data validation (stdlib only) --------------------


def units_for(size, brows, bcols):
    units = []
    for g in range(size):
        units.append([(g, c) for c in range(size)])
        units.append([(r, g) for r in range(size)])
    for br in range(size // brows):
        for bc in range(size // bcols):
            units.append(
                [
                    (br * brows + r, bc * bcols + c)
                    for r in range(brows)
                    for c in range(bcols)
                ]
            )
    return units


def count_solutions(puz, size, brows, bcols, limit=2):
    """puz: dict {(r,c): int} of filled cells. (consistent, solutions<=limit)."""
    units = units_for(size, brows, bcols)
    grid = dict(puz)
    for u in units:
        filled = [grid[c] for c in u if c in grid]
        if len(set(filled)) != len(filled):
            return (False, 0)
    all_cells = [(r, c) for r in range(size) for c in range(size)]
    cell_units = {cell: [u for u in units if cell in u] for cell in all_cells}
    digits = frozenset(range(1, size + 1))
    n = 0

    def cands(cell):
        used = set()
        for u in cell_units[cell]:
            for other in u:
                v = grid.get(other)
                if v:
                    used.add(v)
        return digits - used

    def solve():
        nonlocal n
        empties = [c for c in all_cells if c not in grid]
        if not empties:
            n += 1
            return n >= limit
        best = min(empties, key=lambda c: len(cands(c)))
        for v in sorted(cands(best)):
            grid[best] = v
            hit = solve()
            del grid[best]
            if hit:
                return True
        return False

    solve()
    return (True, n)


class Collector(HTMLParser):
    """Collects the bits the gate cares about from one page."""

    def __init__(self):
        super().__init__()
        self.boards = []  # (class string, attrs dict)
        self.hrefs = []
        self.parts = []
        self.techniques = []
        self.chapter_rows = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div":
            cls = (a.get("class") or "").split()
            if "board" in cls or "mini" in cls:
                self.boards.append((a.get("class") or "", a))
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if "data-part" in a:
            self.parts.append(a["data-part"])
        if "data-technique" in a:
            self.techniques.append(a["data-technique"])
        if tag == "li" and "data-chapter" in a:
            self.chapter_rows += 1


def parse_page(path):
    c = Collector()
    c.feed(path.read_text())
    return c


pages = sorted(LESSONS.glob("*.html"))
check("pages discovered", len(pages) >= 1, f"{[p.name for p in pages]}")
built = {p.name[:2] for p in pages if re.match(r"\d\d-", p.name)}

for page in pages:
    c = parse_page(page)
    text = page.read_text(encoding="utf-8")
    for href in c.hrefs:
        if re.match(r"^(https?:|#|mailto:)", href):
            continue
        ref = href.split("#")[0]
        if not ref:
            continue
        target = (page.parent / ref).resolve()
        check(f"link resolves [{page.name}] {href}", target.exists(), str(target))
    if re.match(r"\d\d-", page.name):
        missing = [p for p in REQUIRED_PARTS if p not in c.parts]
        check(f"template parts [{page.name}]", not missing, f"missing={missing}")
        rule = PAGE_RULES.get(page.name)
        if rule:
            tmiss = [t for t in rule["techniques"] if t not in c.techniques]
            check(
                f"technique sections [{page.name}]",
                not tmiss,
                f"missing={tmiss}",
            )
            full = sum(1 for _, a in c.boards if "data-fragment" not in a)
            check(
                f"full-position boards >= {rule['full_boards_min']} [{page.name}]",
                full >= rule["full_boards_min"],
                f"full={full}",
            )
            hits = [b for b in rule.get("banned", []) if b in text]
            check(
                f"banned strings absent [{page.name}]",
                not hits,
                f"found={hits}",
            )
            miss2 = [b for b in rule.get("required", []) if b not in text]
            check(
                f"required strings present [{page.name}]",
                not miss2,
                f"missing={miss2}",
            )
    for cls, a in c.boards:
        if "mini" in cls.split():
            size = int(a.get("data-size", "0") or "0")
            bb = str(a.get("data-box", "3,3") or "3,3").split(",")
            brows, bcols = int(bb[0]), int(bb[1])
            gv = str(a.get("data-puzzle", "") or "")
            syms = str(a.get("data-symbols", "") or "")
            if syms:
                mapping = {ch: str(i + 1) for i, ch in enumerate(syms)}
                gv = "".join(mapping.get(ch, ch) for ch in gv)
        else:
            size, brows, bcols = 9, 3, 3
            gv = str(a.get("data-givens", "") or "")
        cells = {
            (i // size, i % size): int(ch)
            for i, ch in enumerate(gv)
            if ch.isdigit() and ch != "0"
        }
        ok, nsol = count_solutions(cells, size, brows, bcols)
        if "mini" in cls.split():
            # spec 002 / Appendix D: solution valid + puzzle agrees + unique
            sols = str(a.get("data-solution", "") or "")
            scells = {
                (i // size, i % size): int(ch)
                for i, ch in enumerate(sols)
                if ch.isdigit() and ch != "0"
            }
            units = units_for(size, brows, bcols)
            sol_ok = all(
                len({v for c in u if (v := scells.get(c))})
                == sum(1 for c in u if c in scells)
                for u in units
            )
            agrees = all(scells.get(k) == v for k, v in cells.items())
            check(
                f"mini data valid [{page.name}] size={size}",
                ok and nsol == 1 and sol_ok and agrees,
                f"consistent={ok} solutions={nsol} sol_valid={sol_ok} agrees={agrees}",
            )
        elif "data-fragment" in a:
            check(
                f"fragment consistent [{page.name}]",
                ok,
                f"conflict-free (solutions={nsol})",
            )
        else:
            check(
                f"board data valid [{page.name}] size={size}",
                ok and nsol == 1,
                f"consistent={ok} solutions={nsol}",
            )
        # candidate truth: any shown notes must be legal for that cell
        # (teaching boards may filter a long list down to the focus digits)
        if size == 9:
            units9 = units_for(9, 3, 3)
            cands_attr = str(a.get("data-cands", "") or "")
            for part in filter(None, cands_attr.split(";")):
                kv = part.split(":")
                ci = int(kv[0])
                cell = (ci // 9, ci % 9)
                legal = set(range(1, 10))
                for u in units9:
                    if cell not in u:
                        continue
                    for other in u:
                        if other != cell and other in cells:
                            legal.discard(cells[other])
                shown = {int(d) for d in kv[1] if d.isdigit()}
                check(
                    f"cands legal [{page.name}] cell {ci}",
                    shown <= legal and cells.get(cell, 0) == 0,
                    f"shown={sorted(shown)} legal={sorted(legal)}",
                )

idx = LESSONS / "index.html"
if idx.exists():
    c = parse_page(idx)
    check("index lists six chapters", c.chapter_rows == 6, f"rows={c.chapter_rows}")
    soon = idx.read_text().count('class="soon"')
    check(
        "index coming-soon count matches unbuilt chapters",
        soon == 6 - len(built),
        f"soon={soon} unbuilt={6 - len(built)}",
    )

# ---------- live browser checks ---------------------------------------------
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    for page_path in pages:
        pg = ctx.new_page()
        errs: list = []
        pg.on("pageerror", lambda e, sink=errs: sink.append(str(e)))
        pg.goto(page_path.as_uri())
        pg.wait_for_timeout(200)
        check(f"no page errors [{page_path.name}]", not errs, str(errs[:2]))
        boards = pg.locator(".board, .mini")
        for bi in range(boards.count()):
            el = boards.nth(bi)
            size = int(el.get_attribute("data-size") or "9")
            cells = el.locator(".cell").count()
            check(
                f"board {bi} cell count [{page_path.name}]",
                cells == size * size,
                f"size={size} cells={cells}",
            )
        if re.match(r"\d\d-", page_path.name):
            given = pg.locator(".board .given").count()
            check(
                f"board givens render [{page_path.name}]", given > 0, f"given={given}"
            )
            br_count = pg.locator(".board .cell.bR").count()
            check(
                f"box separators render [{page_path.name}]",
                br_count >= 18,
                f"bR={br_count}",
            )
        pg.close()

    # spec 002: mini boards are really playable — drive the fruit 4x4
    f00 = LESSONS / "00-first-steps.html"
    if f00.exists():
        pg = ctx.new_page()
        errs: list = []
        pg.on("pageerror", lambda e, sink=errs: sink.append(str(e)))
        pg.goto(f00.as_uri())
        pg.wait_for_timeout(200)
        mini = pg.locator(".mini").first
        sol = mini.get_attribute("data-solution") or ""
        puz = mini.get_attribute("data-puzzle") or ""
        empties = [i for i, ch in enumerate(puz) if ch == "."]
        cells = pg.locator(".mgrid .cell")
        # wrong pick first: must wobble and never stick, with no red state
        i0 = empties[0]
        wrong = next(d for d in "1234" if d != sol[i0])
        cells.nth(i0).click()
        mini.locator(f'.mkey[data-k="{wrong}"]').click()
        pg.wait_for_timeout(120)
        cls = cells.nth(i0).get_attribute("class") or ""
        txt = cells.nth(i0).text_content()
        check(
            "mini wrong pick wobbles, never sticks",
            "bump" in cls and not txt and "wrong" not in cls,
            f"class={cls} text={txt!r}",
        )
        for i in empties:
            cells.nth(i).click()
            pg.keyboard.press(sol[i])
        note = mini.locator(".mnote").text_content()
        check("mini completion celebrates", "You did it" in (note or ""), repr(note))
        # size-aware keys: 5 must not land on a 4x4
        m2 = pg.locator(".mini").nth(1)
        puz2 = m2.get_attribute("data-puzzle") or ""
        j0 = next(i for i, ch in enumerate(puz2) if ch == ".")
        m2.locator(".cell").nth(j0).click()
        pg.keyboard.press("5")
        check(
            "mini keys size-aware (5 rejected on 4x4)",
            not m2.locator(".cell").nth(j0).text_content(),
            repr(m2.locator(".cell").nth(j0).text_content()),
        )
        check("mini page: no errors", not errs, str(errs[:2]))
        pg.close()

    # theme sync: an explicit dark choice in the app follows the reader
    # into the lesson pages (board.js reads sudoku-theme-v1)
    tp = ctx.new_page()
    tp.goto((LESSONS / "index.html").as_uri())
    tp.evaluate("localStorage.setItem('sudoku-theme-v1', 'dark')")
    tp.goto((LESSONS / "02-basic.html").as_uri())
    tp.wait_for_timeout(150)
    th = tp.evaluate("document.documentElement.dataset.theme || ''")
    bg = tp.evaluate("getComputedStyle(document.body).backgroundColor")
    check(
        "lesson pages follow the app's dark theme",
        th == "dark",
        f"theme={th!r} bg={bg}",
    )
    tp.close()

    pg = ctx.new_page()
    errs: list = []
    pg.on("pageerror", lambda e, sink=errs: sink.append(str(e)))
    pg.goto((BASE / "sudoku.html").as_uri())
    pg.wait_for_timeout(300)
    pg.click("#menu summary")  # open the collapsed settings menu first
    pg.click("#learnBtn")
    pg.wait_for_url("**/lessons/index.html", timeout=5000)
    check("Learn link reaches the index", "lessons/index.html" in pg.url, pg.url)
    check("no page errors on the way", not errs, str(errs[:2]))
    pg.close()
    b.close()

print(f"\nlessons gate: {'ALL PASS' if not fails else str(len(fails)) + ' FAIL'}")
sys.exit(1 if fails else 0)
