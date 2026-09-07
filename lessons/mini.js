/* mini.js — playable fun-size boards for chapter 00 (spec 002).
   Tap a square, then tap a big key. Wrong picks wiggle away and never stick:
   no mistake counting, no timer, no failure state. Givens are locked. */
(() => {
  let active = null; // the board whose square is selected
  document.querySelectorAll(".mini").forEach((host) => {
    const size = +(host.dataset.size || 9);
    const [br, bc] = (host.dataset.box || "3,3").split(",").map(Number);
    const syms = host.dataset.symbols ? [...host.dataset.symbols] : null;
    const disp = (d) => (syms ? syms[d - 1] : String(d));
    const sol = host.dataset.solution;
    const puz = host.dataset.puzzle;

    const wrap = document.createElement("div");
    wrap.className = "miniWrap";
    const grid = document.createElement("div");
    grid.className = "mgrid";
    grid.style.setProperty("--msize", size);
    const cells = [];
    for (let i = 0; i < size * size; i++) {
      const c = document.createElement("button");
      c.type = "button";
      c.className = "cell" + (puz[i] === "." ? "" : " given");
      if (puz[i] === ".") c.setAttribute("aria-label", "empty square"); else c.textContent = disp(+puz[i]);
      c.addEventListener("click", () => state.select(i));
      cells.push(c);
      grid.appendChild(c);
    }
    cells.forEach((c, i) => {
      const r = Math.floor(i / size),
        cc = i % size;
      if ((cc + 1) % bc === 0 && cc + 1 !== size) c.classList.add("bR");
      if ((r + 1) % br === 0 && r + 1 !== size) c.classList.add("bB");
    });
    wrap.appendChild(grid);

    const bar = document.createElement("div");
    bar.className = "mbar";
    for (let d = 1; d <= size; d++) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "mkey";
      b.dataset.k = d;
      b.textContent = disp(d);
      b.addEventListener("click", () => state.try(d));
      bar.appendChild(b);
    }
    wrap.appendChild(bar);

    const note = document.createElement("p");
    note.className = "mnote";
    note.setAttribute("aria-live", "polite");
    wrap.appendChild(note);
    host.appendChild(wrap);

    const state = {
      size,
      sel: -1,
      select(i) {
        if (cells[i].classList.contains("given")) {
          bump(cells[i]);
          return;
        }
        this.sel = i;
        active = this;
        cells.forEach((c) => c.classList.remove("sel"));
        cells[i].classList.add("sel");
      },
      try(d) {
        if (this.sel < 0) return;
        const i = this.sel;
        if (+sol[i] === d) {
          cells[i].textContent = disp(d);
          cells[i].classList.add("done");
          cells[i].classList.remove("sel");
          cells[i].removeAttribute("aria-label");
          this.sel = -1;
          active = null;
          note.textContent = "Yes!";
          if (cells.every((c) => c.textContent)) party();
        } else {
          bump(cells[i]); // gentle wiggle, nothing sticks
        }
      },
    };

    function bump(c) {
      c.classList.remove("bump");
      void c.offsetWidth; // restart the animation
      c.classList.add("bump");
    }
    function party() {
      grid.classList.add("party");
      note.textContent = "🎉 You did it!";
    }
  });

  // size-aware number keys: 1-4 on a 4x4, 1-6 on a 6x6, 1-9 on a 9x9
  document.addEventListener("keydown", (e) => {
    if (!active) return;
    const d = +e.key;
    if (Number.isInteger(d) && d >= 1 && d <= active.size) active.try(d);
  });
})();
