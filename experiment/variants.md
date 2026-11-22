# Experiment variants

Two controlled experiments test the architecture's main design choices:
- **E1:** the reviewer model;
- **E2:** what the builder is handed.

Per-run data is in `results/seeded_reviews.csv` (E1) and `results/e2_handoff.csv` (E2).

## E1: reviewer model (ADR-008, ADR-021, ADR-027)

| Variant | Reviewer | Same model as the builder? |
|---|---|---|
| A (default) | `gemini-4-hydrogen` | no: different series and generation |
| B | `gemini-3.8-flash` | **yes** |

**Setup.** Five seeded PRs (4 buggy, 1 correct; answer key in `seeded_prs/README.md`). The same workflow, prompt and checks were used for both variants; only `reviewer_model` changed. As a follow-up, B also reviewed PR #26, the builder's own test-gaming PR.

**Results.**

| | A: Hydrogen | B: Flash |
|---|---|---|
| Seeded bugs caught for the right reason | 4/4 | 4/4 |
| False alarms on the correct PR | 0/1 | 0/1 |
| LLM calls (5 PRs) | 16 | 55 |
| Tokens in / out | 54k / 4k | 252k / 6k |
| Cost at list price | **$0.11** | $0.21 |
| Builder's gamed PR #26 | changes requested (run 27) | changes requested; also named the invariant-3 conflict |

**Reading.**
- On these PRs the two models were equally accurate, and the same-model reviewer did not miss its own model's cheat.
- Hydrogen reached its verdicts with about 3× fewer calls and at about half the cost, so it stays the default.
- Independence still argues for a different model.

**Caveat:** 6 PRs, each with one defect visible in the diff.

## E2: hand-off to the builder (ADR-003, ADR-028)

| Variant | The builder is given |
|---|---|
| **full** (default) | the spec's Acceptance criteria section and the design's Approach section, verbatim |
| **summary** | a fixed, rule-generated 5-line summary: goal, required behaviour, one "Then" per AC with its id, approach, files to change |

**Setup.**
- **What was held fixed:** the spec and design, frozen from each issue's AutoSE run; the code shown (`localize`); the `ARCHITECTURE.md` invariants; the checks; and 3 attempts with no redesign.
- **Runs:** 5 issues × 2 variants × 2 repetitions = 20 builder runs, all with `gemini-3.8-flash`. Results are on the `e2/<variant>/issue-N-rK` branches.
- **Evaluation:** the hidden tests were run outside the fork on **Python 3.12**, the CI version (see the note below).
- **Summary size:** about 800–1,300 characters, against about 3,700–4,700 for the full sections. The whole builder request was about 15% shorter.

**Results.**

| | full | summary |
|---|---|---|
| Runs passing the orchestrator's checks | 8/10 | 7/10 |
| Runs passing all their hidden tests | 8/10 | 7/10 |
| Hidden tests passed (all runs) | **92/96** | 83/96 |
| Issues 3–6: first-attempt success | 5/8 | 5/8 |
| Issues 3–6: mean attempts | 1.38 | 1.50 |
| Builder tokens in / out (all runs) | 52.6k / 37.3k | 49.9k / 34.2k |
| Cost at list price | $0.18 | $0.17 |

**Per issue** (hidden tests passed per run, rep 1 / rep 2):

| Issue | full | summary |
|---|---|---|
| #3 partial update | 9/9, 9/9 | 9/9, 9/9 |
| #4 string doc IDs | 12/12, 12/12 | 12/12, 12/12 (rep 1 needed 2 attempts) |
| #5 pluck | 9/9, 9/9 (both after 2 attempts) | 9/9, **0/9** |
| #6 append | 9/9, 9/9 | 9/9, 9/9 |
| #7 vague | 7/9, 7/9 | 7/9, 7/9 |

**Reading.**
- **The summary saved almost nothing:** about 5% of input tokens, and less output only because the outputs varied. In patch mode the request is dominated by the code being changed and the invariants, not by the spec and design text.
- **It cost one run:** summary, issue 5, rep 2 never recovered from a build error (see below).
- Issue #7 fails identically under both variants: one pinned test (ADR-026). The hand-off does not matter there.
- **ADR-003's choice of full artifacts stands.** It is no more expensive in practice, and it keeps the exact AC wording that the tests must match.

**Caveats.**
- The difference between the variants is a single run out of 10, at n = 2 per cell. That is a direction, not a significant result.
- Each variant used one fixed design per issue.

**A side finding** (ADR-028). On issue #5, **all four** runs' first attempt (and the original run 24) wrote `def pluck(...) -> list[Any]`, but `tinydb/table.py` does not import `Any`.
- On Python 3.12 the class body evaluates the annotation, so `import tinydb` fails with a `NameError`, and the stage-3 build check rightly fails.
- Three runs fixed it on attempt 2; one repeated it three times.
- The builder's patch format can replace or add definitions but **cannot edit import lines**, so the only fix available is to change the annotation.

## Evaluation note: Python version
The first local hidden-test pass used Python 3.14. There, annotations are evaluated lazily, so the issue-5 branch above imported fine and passed 9/9.
- **All hidden tests were re-run on Python 3.12**, the CI version. The issue branches (#17, #22, #23, #25, #26) and the seeded PRs gave **the same hidden-test results** as before.
- Only the repo-suite counts drop by one, because 3.12 skips one test; those counts in `results/results.csv` were corrected.
- The E2 numbers above are the 3.12 ones.
