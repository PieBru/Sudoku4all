# Plan — 010 Training generator

generateTrainingBoard(allowedIds, targetClues, caps) beside the engine:
two-phase carve (Phase A to the level's CLUES target, Phase B exercise
bias past target until a checked non-single contributes), carve cursor
(never re-tries a failed cell per attempt), final verification +
countSolutions==1 tripwire aborting loudly with no retry, exercise-bias
retry across attempts, guards 8 attempts / 5 s wall / 120 runs per
attempt (spec amended from 60: Phase A alone consumes ~45-55 runs,
which starved Phase B; disclosed in commit message). Gate: SC-001 12
random dropped-subset boards exclusive + unique, SC-002 default-Basic
bias 5/5, exact budget message, deterministic in-gate tripwire
exercise via detector-map injection (place-9-at-r1c1 pointing plant)
with restore-clean assertion.
