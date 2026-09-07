# Plan — 011 Training UI

Panel inside #menu (details#training): segmented level buttons
(Beginner/Basic/Intermediate + Advanced disabled with the sealed reason),
data-driven checklist (19 snake_case IDs, Beginner singles locked on with
explanation, groups <= level shown, saved unchecks win), All/None scoped to
current level and disabled at Beginner, Generate with the app's own
started-and-not-won confirm + adoption via full newGame-style reset
(diff="training", solution hidden, honest "Solve path (easiest techniques
first):" report through the aria-live status, "Building your board…"
announcement via one-paint setTimeout), prefs under sudoku-training-v1 with
loud corrupt-save reset, native print via @media print + #printView (active
entries only; solved second page when include-solution checked).
