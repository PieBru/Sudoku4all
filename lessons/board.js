/* lessons/board.js — the one shared display-board renderer (spec 000).
   Boards are pure data:
     <div class="board" data-givens="81 chars of 0-9 or ."
          data-cands="idx:123;idx:45"   optional pencil notes (digits)
          data-hl="i,j"                  optional highlighted cells
          data-hx="i,j">                 optional red ✗ overlay cells
   Renders a 9×9 grid with thick box separators (the game's bR/bB pattern).
   Also syncs the game's explicit theme choice (sudoku-theme-v1) if present. */
(() => {
  
  try {
    /* the app stores a bare string ("dark"); accept JSON too for safety */
    var raw = localStorage.getItem("sudoku-theme-v1"), t = null;
    try { t = JSON.parse(raw || "null"); } catch (e) { t = raw; }
    if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
  } catch (e) {
    /* private mode or blocked storage: system theme is fine */
  }
  function render(root) {
    root.querySelectorAll(".board[data-givens]").forEach((el) => {
      var givens = el.getAttribute("data-givens") || "";
      if (!/^[0-9.]{81}$/.test(givens)) {
        el.classList.add("bad");
        return;
      }
      var cands = {};
      (el.getAttribute("data-cands") || "")
        .split(";")
        .filter(Boolean)
        .forEach((part) => {
          var kv = part.split(":");
          cands[+kv[0]] = kv[1] || "";
        });
      var hl = (el.getAttribute("data-hl") || "")
        .split(",").filter(Boolean).map(Number);
      var hl2 = (el.getAttribute("data-hl2") || "")
        .split(",").filter(Boolean).map(Number);
      var hx = (el.getAttribute("data-hx") || "")
        .split(",").filter(Boolean).map(Number);
      el.textContent = "";
      for (var i = 0; i < 81; i++) {
        var c = document.createElement("div");
        c.className = "cell";
        var col = i % 9;
        if (col === 2 || col === 5) c.classList.add("bR");
        if ((i >= 18 && i < 27) || (i >= 45 && i < 54)) c.classList.add("bB");
        var v = +givens[i] || 0;
        if (v) {
          c.classList.add("given");
          c.textContent = v;
        }
        if (cands[i]) {
          c.classList.add("cands");
          cands[i].split("").forEach((d) => {
            var s = document.createElement("span");
            s.textContent = d;
            c.appendChild(s);
          });
        }
        if (hl.indexOf(i) >= 0) c.classList.add("hl");
        if (hl2.indexOf(i) >= 0) c.classList.add("hl2");
        if (hx.indexOf(i) >= 0) c.classList.add("xmark");
        el.appendChild(c);
      }
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", () => { render(document); });
  else render(document);
  window.LessonBoards = { render: render };
})();
