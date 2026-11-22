# Stage map

| # | Stage | Agent | Model (repo variable) | Artifact | Check | Who decides pass/fail | On failure |
|---|---|---|---|---|---|---|---|
| 1 | Requirements | Planner (A1 `spec-writer` skill) | `PLANNER_MODEL` | `spec.md` | (a) script: ≥1 criterion, each has ID `AC-n` and Given/When/Then; (b) LLM judge (`JUDGE_MODEL`, different model) rates each AC testable yes/no | Orchestrator: both (a) and (b) must pass | 1 redo with judge feedback, then stop and explain in `spec.md` |
| 2 | Design | Planner (reads `ARCHITECTURE.md`) | `PLANNER_MODEL` | `design.md` | script: "Files to change" table present; every named file exists (or is marked NEW); every named function found by grep | Orchestrator | 1 redo with missing names, then stop |
| 3 | Implementation | Orchestrator localizes, Builder patches (ADR-016) | `BUILDER_MODEL` | `diff.patch` | `pip install -e .` and `python -m compileall tinydb` succeed; diff non-empty; no edits outside allowed paths | Orchestrator | Feeds error back to builder (counts as an attempt) |
| 4 | Testing | Builder (same context as 3) | `BUILDER_MODEL` | `test_report.md` | full `pytest` exit 0, and every `AC-n` appears in a new test name/docstring | Orchestrator | back to 3, max 3 attempts; then back to 2 once; then stop |
| 5 | Release | Script (no LLM) | — | `pr.md` + PR link | PR open; `gh pr checks --watch` all green | Orchestrator | stop, record failing check |
| 6 | Review | Reviewer (separate job) | `REVIEWER_MODEL` (different family) | `review.md` + `verdict.json` | verdict JSON valid; approve, or `changes` with `target: design\|implement` | Post job routes it; 2 rounds max | round < 2 → re-run from target stage; else hand to human |

The human always makes the final merge decision. The workflow never merges.
