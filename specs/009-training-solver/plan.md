# Plan — 009 Training solver

TRAIN_TECHNIQUES (19 stable snake_case IDs, cheapest-first) with one
deterministic detector each (tCombs ascending, no shuffle); SEE map
from GROUPS; solveWithAllowed(board, allowedIds) with used log (only
grid-changing firings), honest stuck (full pass, no change → stop, no
brute force), guards 81 placements / 200 elimination rounds / 500 ms.
tests/training.test.mjs: 17 machine-searched fixtures (seeded random
carve; completes under singles+T; completion equals independent
brute-force oracle), restrictability, determinism, stuck honesty,
guard test. Detector bug caught and fixed en route (xy_wing bogus
subset continue — proven against the lesson's verified XY-Wing board).
