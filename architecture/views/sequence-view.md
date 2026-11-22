# Sequence view: one real run, from trigger to review

This view follows **real** runs on the fork, message by message, with links to the Actions runs, PRs and artifacts. Every number comes from the run's `state.json`, test report or job summary. The full run history is in `results/runs.md`.

- **Part 1, the happy path:** run 24, issue #5 `pluck`. It includes a spec redo, a failed first build attempt and an approving review.
- **Part 2, the "changes requested" path:** run 27, issue #7. The reviewer rejects a patch that passed every automatic check.
- **Part 3:** how the real pipeline differs from the sequence we planned before the first run.

## Part 1: issue #5, run 24 (approved)

- **Run:** [44993182187](https://github.com/RishabhDev01/tinydb/actions/runs/44993182187), 3 min 8 s.
- **Result:** PR [#23](https://github.com/RishabhDev01/tinydb/pull/23).
- **Hidden tests:** 9/9 (`results/results.csv`).

> **Issue [#5](https://github.com/RishabhDev01/tinydb/issues/5): "Feature: get a list of one field from all documents"**. The user asks for a `db.pluck('name')` that returns that field from every document, in insertion order, and skips documents that do not have it. It should also work on other tables: `db.table('users').pluck('email')`.

```mermaid
sequenceDiagram
  autonumber
  actor M as Maintainer
  participant GH as GitHub
  participant G as gate job
  participant O as Orchestrator (code, build job)
  participant PG as Prompt guard (llama-prompt-guard-2-86m)
  participant P as Planner (gemini-3.8-flash)
  participant J as Judge (qwen3.8-27b, Groq)
  participant B as Builder (gemini-3.8-flash, patch mode)
  participant CI as CI (pytest)
  participant R as Reviewer (gemini-4-hydrogen, review job)
  participant PJ as post job

  M->>GH: Actions, Run workflow (issue=5, round=1, start=auto)
  GH->>G: workflow_dispatch (sender is a user, not a bot)
  G-->>O: run=true. Write access is needed to dispatch (ADR-010)
  O->>O: new branch autose/issue-5 from master 0462790, baseline 227 tests pass

  Note over O,PG: Stage 0: injection screen (06:19:43)
  O->>PG: issue title + body
  PG-->>O: max score 0.001, pass

  Note over O,J: Stage 1: Requirements (06:19:43 to 06:20:12)
  O->>P: untrusted issue #35;5 + spec-writer skill + read tools
  P->>P: list_dir / read_file / grep (turn budget stated, ADR-020)
  P-->>O: spec.md: 5 ACs (all present, missing skipped, None kept, unknown field, custom table)
  O->>O: template check passes
  O->>J: is each AC testable?
  J-->>O: AC-5 NOT testable: "redundant, non-standard boolean list expression" in Then
  O->>P: redo 1/1 with the judge's reason
  P-->>O: spec.md v2
  O->>J: re-check
  J-->>O: all testable. Stage 1 PASS (5 ACs, attempt 2)

  Note over O,P: Stage 2: Design (to 06:20:46)
  O->>P: spec.md + ARCHITECTURE.md §4–5
  P-->>O: design.md: tinydb/table.py Table.pluck (NEW) "-> list[Any]", tests
  O->>O: files and the Table class exist. Stage 2 PASS (2 rows)

  Note over O,B: Stages 3–4: Implement and Test (06:20:46 to 06:20:58)
  O->>O: localize: outline of class Table (new method) + ARCHITECTURE.md §4
  O->>B: ACs + design approach + code (one request, no tools)
  B-->>O: ADD tinydb/table.py Table (pluck) + TESTS + SUMMARY
  O->>O: test-gaming scan passes. compileall + import tinydb FAILS:<br/>NameError, Any is not imported (Python 3.12)
  O->>B: attempt 2/3 + "BUILD FAILED" traceback
  B-->>O: pluck without Any + same tests
  O->>O: build passes. pytest: 233 passed. Every AC has a test. PASS (attempt 2)

  Note over O,CI: Stage 5: Release (no LLM, to 06:21:30)
  O->>GH: push autose/issue-5, open PR #35;23 (body = pr.md)
  GH->>CI: pull_request event
  CI-->>O: run 44993321665 green. Stage 5 PASS

  Note over R,PJ: Stage 6: independent review (fresh runner, read-only token, 32 s)
  O->>R: issue #35;5 text + diff (no .autose/, no spec, no design)
  R->>R: read_file, run_tests (232 passed, 1 skipped)
  R-->>PJ: verdict: approve. 3 requirements met, 3 risks checked<br/>(empty table, None values, §4 invariants)
  PJ->>GH: review comment on PR #35;23 + "Ready for a human decision"
  GH-->>M: notification. Merge or close is the maintainer's call
```

### The same run as a timeline

| # | Time (UTC) | Stage | Who | Output | Check |
|---|---|---|---|---|---|
| 1 | 06:19:40 | Trigger | Maintainer | `workflow_dispatch` | gate: run=true |
| 2 | 06:19:43 | Guard | Prompt guard | score 0.001 | pass |
| 3 | 06:20:05 | Requirements | Planner + Judge | `.autose/issue-5/spec.md` | AC-5 untestable, so 1 redo |
| 4 | 06:20:12 | Requirements | Planner + Judge | spec v2, 5 ACs | pass |
| 5 | 06:20:46 | Design | Planner | `design.md`, 2 rows | pass |
| 6 | 06:20:52 | Implement | Builder | patch for `Table.pluck` | build fails (`Any` not imported) |
| 7 | 06:20:58 | Implement + Test | Builder | patch v2, `test_autose_issue_5.py` | 233 passed, ACs covered |
| 8 | 06:21:03 | Release | Script | [PR #23](https://github.com/RishabhDev01/tinydb/pull/23) | — |
| 9 | 06:21:30 | Release | CI | [CI run](https://github.com/RishabhDev01/tinydb/actions/runs/44993321665) | green |
| 10 | +32 s | Review | Reviewer | review comment on PR #23 | **approve** |
| 11 | — | Decision | Human | merge or close | — |

**Tokens:**

| Agent | Calls | Tokens (prompt / completion) |
|---|---|---|
| Guard | 1 | 186 |
| Planner | 22 | 87.6k / 2.7k |
| Judge | 2 | 1.1k / 0.4k |
| Builder | 2 | 5.0k / 1.3k |
| Reviewer | 3 | 8.4k / 0.6k |

The audit trail (`spec.md`, `design.md`, `diff.patch`, `test_report.md`, `state.json`) is on the PR branch under `.autose/issue-5/`.

## Part 2: issue #7, run 27 (changes requested)

- **Run:** [44994263819](https://github.com/RishabhDev01/tinydb/actions/runs/44994263819).
- **Result:** PR [#26](https://github.com/RishabhDev01/tinydb/pull/26), with changes requested.

The issue is vague: "search() gives me different data the second time??". It asks to change behaviour that an existing test pins.

```mermaid
sequenceDiagram
  autonumber
  participant O as Orchestrator
  participant B as Builder (gemini-3.8-flash)
  participant P as Planner
  participant CI as CI
  participant R as Reviewer (gemini-4-hydrogen)
  participant PJ as post job
  actor M as Maintainer

  Note over O,B: Stages 3–4 (spec and design already passed)
  loop attempts 1–3
    O->>B: ACs + design + code (+ failure digest, ADR-024)
    B-->>O: deep-copy search() results
    O->>O: 1 failed: test_query_cache_documents_are_shared_with_cache (existing test)
  end
  O->>P: back to design (ADR-002) with the failure digest
  P-->>O: design v2
  loop attempts 4–6
    O->>B: same, design v2
    B-->>O: attempt 6: search() walks the stack with sys._getframe and<br/>runs the OLD code only for that test
    O->>O: all 231 tests pass (gamed)
  end
  O->>CI: PR #35;26, CI green
  O->>R: issue #35;7 + diff
  R-->>PJ: changes (route to implement). DEFECT: "special-casing a test via<br/>stack-frame inspection"
  PJ->>M: review comment on PR #35;26
  Note over PJ,M: Run 28: the post job dispatched round 2 as github-actions[bot]<br/>and the gate rejected it (bot event)
```

**What changed after this run** (ADR-026; it applies from master `6766223`):
- **Step 7 would now fail at stage 3** with `TEST GAMING`.
- **The run would stop at attempt 5:** the only failing test is an existing one, it fails identically under 2 designs, and so the run hands the decision to the maintainer.
- **Round 2 no longer starts automatically.** The post job comments `/autose round 2 <stage>`, and a person decides whether to type it.

The independent reviewer is what caught attempt 6. `gemini-3.8-flash` (the builder's own model) also rejected it when asked to review the same PR ([44996830372](https://github.com/RishabhDev01/tinydb/actions/runs/44996830372)).

## Part 3: planned vs real

| Planned before run 1 (this view, v1) | Real pipeline (runs 23–27) | Why (ADR) |
|---|---|---|
| Planner and builder on `gpt-oss-120b`, reviewer `qwen3.8-27b` (Groq free tier) | Planner and builder `gemini-3.8-flash`, reviewer `gemini-4-hydrogen`; judge and guard stay on Groq | Groq rate and daily limits stalled runs 2–14 (ADR-013/015/019/021) |
| Builder is a tool loop (`write_file`, `run_tests`) | **Patch mode**: code chooses what to show, one request, whole definitions | The tool loop wandered for 40 turns with 0 edits (ADR-014/016) |
| The builder retry sees a truncated log | It sees a **failure digest**: each failing test, its line and its error | Run 22: the log tail hid the cause (ADR-024) |
| `pytest` is the only stage-3/4 gate | Build check, **test-gaming scan**, pytest, AC-to-test map, baseline count | Run 27 passed pytest by gaming (ADR-026) |
| Round 2 auto-dispatched by the post job | Round 2 **started by a person** (`/autose round 2 <stage>`) | Run 28 was rejected by the gate as a bot event (ADR-026) |
| Trigger by label | `workflow_dispatch`, label or `/autose` comment, from trusted users only | ADR-010 |
