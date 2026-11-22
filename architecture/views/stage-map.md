# Stage map

| # | Stage | Agent | Model (repo variable) | Artifact | Check | Who decides pass/fail | On failure |
|---|---|---|---|---|---|---|---|
| 0 | Gate + injection screen | Code + prompt guard | `GUARD_MODEL` (Groq) | `state.json` | trusted trigger, not a bot (ADR-010); guard score below threshold (ADR-011) | Gate job / orchestrator | skip, or stop with reason |
| 1 | Requirements | Planner (A1 `spec-writer` skill) | `PLANNER_MODEL` | `spec.md` | (a) script: ≥1 criterion, each has ID `AC-n` and Given/When/Then; (b) LLM judge (`JUDGE_MODEL`, different model) rates each AC testable yes/no | Orchestrator: both (a) and (b) must pass | 1 redo with judge feedback, then stop and explain in `spec.md` |
| 2 | Design | Planner (reads `ARCHITECTURE.md`) | `PLANNER_MODEL` | `design.md` | script: "Files to change" table present; every named file exists (or is marked NEW); every named function found by grep | Orchestrator | 1 redo with missing names, then stop |
| 3 | Implementation | Orchestrator localizes, Builder patches (ADR-016) | `BUILDER_MODEL` | `diff.patch` | `compileall` + `import tinydb` succeed; diff non-empty; no edits outside allowed paths; **no test-gaming patterns** in added `tinydb/` lines (ADR-026) | Orchestrator | Feeds error back to builder (counts as an attempt) |
| 4 | Testing | Builder (same context as 3) | `BUILDER_MODEL` | `test_report.md` | full `pytest` exit 0, and every `AC-n` appears in a new test name/docstring | Orchestrator | back to 3 with a **failure digest** (ADR-024), max 3 attempts; then back to 2 once; then stop. Stops early if only existing tests fail identically under 2 designs (**conflict stop**, ADR-026) |
| 5 | Release | Script (no LLM) | — | `pr.md` + PR link | PR open; `gh pr checks --watch` all green | Orchestrator | stop, record failing check |
| 6 | Review | Reviewer (separate job) | `REVIEWER_MODEL` (different family) | `review.md` + `verdict.json` | verdict JSON valid; approve, or `changes` with `target: design\|implement` | Post job routes it; 2 rounds max | `changes`: comment with `/autose round 2 <stage>`, which **a person** decides to type (ADR-026); else hand to human |

The human always makes the final merge decision. The workflow never merges.


Models in the runs reported (runs 17–27): planner and builder `gemini-3.8-flash`, judge `qwen/qwen3.8-27b`, reviewer `gemini-4-hydrogen`, guard `llama-prompt-guard-2-86m` (ADR-019, ADR-021).
