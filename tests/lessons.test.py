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
        self.chapter_rows = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and "board" in (a.get("class") or ""):
            self.boards.append((a.get("class") or "", a))
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if "data-part" in a:
            self.parts.append(a["data-part"])
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
    for cls, a in c.boards:
        if "mini" in cls:
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
        check(
            f"board data valid [{page.name}] size={size}",
            ok and nsol == 1,
            f"consistent={ok} solutions={nsol}",
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
            check(f"board givens render [{page_path.name}]", given > 0, f"given={given}")
            br_count = pg.locator(".board .cell.bR").count()
            check(
                f"box separators render [{page_path.name}]",
                br_count >= 18,
                f"bR={br_count}",
            )
        pg.close()

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
